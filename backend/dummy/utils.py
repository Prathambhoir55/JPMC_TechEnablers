import requests
from backend.settings import *

def give_geoid(city):
	headers = {
	"X-RapidAPI-Key": env("X-RapidAPI-Key"),
	"X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
	}
	main_url = "https://tripadvisor16.p.rapidapi.com/api/v1"
	location_url = main_url+"/hotels/searchLocation"
	querystring = {"query":city}
	response = requests.request("GET", location_url, headers=headers, params=querystring)
	return response.json()['data'][0]['geoId']

def give_hotels(geoId, checkIn, checkOut):
	headers = {
	"X-RapidAPI-Key": env("X-RapidAPI-Key"),
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
	"X-RapidAPI-Key": env("X-RapidAPI-Key"),
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
