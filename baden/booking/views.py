from django.shortcuts import render
from . serializers import BookingSerializer
from . models import Booking
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . permisions import IsHostOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = serializer.seve(user=request.user)
        checkout_session = booking.create_checkout_session()

        return Response({'checkout_session_id': checkout_session.id}, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']

    def get_queryset(self):
        get_queryset = super().get_queryset()
        bookings = Booking.objects.filter(user=Booking.user)
        return bookings













