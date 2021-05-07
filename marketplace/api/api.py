from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from main.models import Good

from .serializers import GoodListSerializer, GoodDetailSerializer, GoodChangeSerializer


class GoodViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        query_set = Good.objects.all()
        serializer = GoodListSerializer(query_set, many=True)
        return Response(serializer.data)

    def retrive(self, request, pk=None):
        query_set = Good.objects.all()
        good = get_object_or_404(query_set, pk=pk)
        serializer = GoodDetailSerializer(good)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        query_set = Good.objects.all()
        good = get_object_or_404(query_set, pk=pk)
        good.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        query_set = Good.objects.all()
        good = get_object_or_404(query_set, pk=pk)
        serializer = GoodChangeSerializer(data=request.data)
        if serializer.is_valid():
            good.save()
            return Response(serializer.data)

        return Response({
            'status': 'Bad request',
            'message': 'Good could not be svaed with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = GoodChangeSerializer(data=request.data)
        if serializer.is_valid():
            Good.objects.create(**serializer.validated_data)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Good could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)