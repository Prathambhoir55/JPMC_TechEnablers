from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,permissions
from django.http import JsonResponse
from .utils import *


class TripAPI(GenericAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = User.objects.get(id = self.request.user.id)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            validated_data = serializer.create(serializer.validated_data, user)
        return JsonResponse(validated_data, status=status.HTTP_201_CREATED)


class TripListAPI(ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = User.objects.get(id = self.request.user.id)
        queryset = Trip.objects.filter(user=user)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)