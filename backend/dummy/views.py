from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,permissions
from django.http import JsonResponse

class HotelAPI(GenericAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            queryset = serializer.create(serializer.validated_data)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)