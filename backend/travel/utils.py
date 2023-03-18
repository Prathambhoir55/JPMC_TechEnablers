from geopy.geocoders import Nominatim
import requests
from backend.settings import *
from scipy.spatial.distance import cdist
import pandas as pd
from datetime import timedelta
import random


def geo_locate(latitude, longitude):

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(latitude+","+longitude)
    address = location.raw['address']

    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    dict1 = dict()
    dict1['city'] = city
    dict1['state'] = state
    dict1['country'] = country
    return dict1

def give_geoid(city):
    headers = {
    "X-RapidAPI-Key": env("X_RapidAPI_Key"),
    "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    main_url = "https://tripadvisor16.p.rapidapi.com/api/v1"
    location_url = main_url+"/hotels/searchLocation"
    querystring = {"query":city}
    response = requests.request("GET", location_url, headers=headers, params=querystring)
    print(response.json())
    return response.json()['data'][0]['geoId']

def give_hotels(geoId, checkIn, checkOut):
	headers = {
	"X-RapidAPI-Key": env("X_RapidAPI_Key"),
	"X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
	}
	main_url = "https://tripadvisor16.p.rapidapi.com/api/v1"
	hotel_url = main_url+'/hotels/searchHotels'
	querystring = {"geoId":geoId,"checkIn":checkIn,"checkOut":checkOut,"pageNumber":"1","currencyCode":"INR"}
	response = requests.request("GET", hotel_url, headers=headers, params=querystring)
	return response.json()['data']['data']

def give_restaurants(location_id):
	headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": env("X_RapidAPI_Key"),
	"X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
	}
	url = "https://worldwide-restaurants.p.rapidapi.com/search"
	payload = {
    "language":"en_US",
    "limit":"30",
    "location_id":location_id,
    "currency":"INR"
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response.json()['results']['data']


def optimal_path(queryset):
    latitudes = []
    longitudes = []
    city_names = []

    for obj in queryset:
        latitudes.append(float(obj.latitude)) 
        longitudes.append(float(obj.longitude))
        city_names.append(obj.city)
        if obj.is_start == True:
            starting_point = len(city_names)-1

    lat_long = list(zip(latitudes, longitudes))
    distance_matrix = cdist(
        lat_long, 
        lat_long
    )

    df_distance_matrix = pd.DataFrame(distance_matrix)
    cur_index = starting_point

    seq = [cur_index]
    while len(seq) < len(list(df_distance_matrix.keys())):
        nearest_clusters = list(df_distance_matrix[cur_index].sort_values().index)
        for cluster_id in nearest_clusters:
            if cluster_id != cur_index and cluster_id not in seq:
                seq.append(cluster_id)
                cur_index = cluster_id
                break

    city_sequence = []
    for i in seq:
        city_sequence.append(city_names[i])

    return city_sequence


def take_score(elem):
    return elem['rating_score']

def take_price(elem):
    return elem['price1']

def give_itinerary(data, trip):
    itinerary = {}
    start_date = trip.start_date
    end_date = trip.end_date
    total_nights = int(((end_date - start_date).total_seconds())/86400)
    total_days = total_nights+1
    avg_nights = total_nights//len(data['path'])
    remainder_nights = total_nights//len(data['path'])
    city_details = []
    estimated_budget = float(trip.budget)
    itinerary_budget = 0
    accomodation_budget = 0.3 * estimated_budget
    food_budget = 0.25 * estimated_budget
    budget_per_night = accomodation_budget/total_nights
    food_budget_per_meal = food_budget/(total_days*3)
    date_now = start_date
    for city in data['path']:
        dict1 = {}
        dict1['city'] = city
        if remainder_nights !=0:
            dict1['nights'] = avg_nights +1
            remainder_nights -=1
        else:
            dict1['nights'] = avg_nights
        dict1['days'] = dict1['nights']+1
        geoId = give_geoid(city)
        dict1['geoId'] = geoId
        checkIn = date_now.strftime("%Y-%m-%d")
        date_now = date_now + timedelta(days=dict1['nights'])
        checkOut = date_now.strftime("%Y-%m-%d")
        hotels = give_hotels(geoId, checkIn, checkOut)
        for hotel in hotels:
            hotel['price'] = int(hotel['priceForDisplay'][1:].replace(",", ""))
            hotel['rating_score'] = hotel['bubbleRating']['rating']/hotel['price']
        hotels_sorted = sorted(hotels, key=take_score, reverse=True)
        hotel_main = hotels_sorted[0]
        itinerary_budget += hotel_main['price']*dict1['nights']
        hotel = {}
        hotel['name'] = hotel_main['title']
        hotel['price'] = hotel_main['price']
        dict1['hotel'] = hotel
        city_details.append(dict1)

    for i in range(1,total_days+1):
        dict2 = {}
        dict2['date'] = start_date.strftime("%Y-%m-%d")
        for city_det in city_details:
            if city_det['days'] !=0:
                dict2['city'] = city_det
                restaurants = give_restaurants(city_det['geoId'])
                for restaurant in restaurants:
                    try:
                        price1, price2 = restaurant['price'].split(' - ')
                        price = (int(price1[1:].replace(",", "")) + int(price2[1:].replace(",", "")))/2    
                        restaurant['price1'] = price
                    except:
                        continue
                try:
                    restaurants = sorted(restaurants, key=take_price)
                    dict2['price'] = restaurants[i]['price1']
                    dict2['restaurant'] = restaurants[i]['name']
                    itinerary_budget += dict2['price']*3
                except:
                    pass

                city_det['days'] -=1
                break

        
        itinerary[f'day{i}'] = dict2
        itinerary['total_budget'] = itinerary_budget
        start_date = start_date + timedelta(days=1)

    return itinerary
        
        


        
    
