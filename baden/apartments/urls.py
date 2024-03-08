from django.urls import path
from . import views


urlpatterns = [
    path('location_list/', views.LocationListView.as_view(), name='location_list'),
    path('location_detail/<int:pk>/', views.LocationRetrieveView.as_view(), name='location_detail'),

    path('apartment_create/', views.ApartmentCreateView.as_view(), name='apartment_create'),
    path('apartment_update/<int:pk>/', views.ApartmentUpdateView.as_view(), name='apartment_update'),

    path('review_update/<int:pk>/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review_delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review_create/', views.ReviewCreateView.as_view(), name='review_create'),

]