from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Travel Itinerary API",
      default_version='v1',
      description='''An API built for TechEnablers program of JPMC. This API will generate an travel itinerary querying the data from TripAdvisor. -Register and Login on our API platform
      -User will mark locations on a map on the frontend and the coordinates will be sent in the body of the API
      -The coordinates will be queried to Nominatim API of  geopy library which will return the city name and store it in the database.
      -The coordinates then will get sorted according to the shortest path algorithm to travelling salesman problem.
      -The data is passed on to the itinerary function which divides the budget and number of days equally for each location.
      -Based on budget per day the restaurants and hostels are chosen.
      -The restaurants and hostels are displayed further day wise''',
      terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('travel/', include('travel.urls')),
   path('accounts/', include('accounts.urls')),
   path('dummy/', include('dummy.urls')),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)