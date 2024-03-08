from django.shortcuts import render
from .srializers import ApartmentSerializer, LocationSerializer, ReviewSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from . models import Apartment, Location, Review
from . permisions import IsHostOrReadOnly, IsOwnerOrReadOnly, CanLiveReview
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationRetrieveView(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ApartmentCreateView(generics.CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]


class ApartmentListView(generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset


class ApartmentUpdateView(generics.UpdateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]


class ApartmentDetailView(generics.RetrieveAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def get(self, request, *args, **kwargs):

        apartment = self.get_object()

        reviews = Review.objects.filter(apartment=apartment)
        review_serializer = ReviewSerializer(reviews, many=True)

        apartment_serializer = self.get_serializer(apartment)
        data = {
            'apartment': apartment_serializer.data,
            'reviews': review_serializer.data,
        }

        return Response(data)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, CanLiveReview]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
