from rest_framework import permissions
from booking.models import Booking
from . models import Apartment


class IsHostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host == request.user
# есть ли смысл во втором классе


class CanLiveReview(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticate:
            return False

        apartment_id = view.kwargs.get('apartment.id')
        booking_status_condition = ['complete']

        user_bookings = Booking.objects.filter(user=request.user, apartment=apartment_id, status=booking_status_condition)
        return user_bookings.exusts()

    def has_object_permission(self, request, view, obj):

        user_booking = Booking.objects.filter(user=request.user, apartment=obj, status='complete')
        return user_booking.exists()
