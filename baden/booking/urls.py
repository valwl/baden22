from django.urls import path
from . import views


urlpatterns = [
    path('create_booking/', views.BookingCreateView.as_view(), name='create_booking'),
    path('booking_detail/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('booking_list/', views.BookingListView.as_view(), name='booking_list'),
]