from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(upload_to='media/img/baden_samer.jpeg')

    def __str__(self):
        return f'{self.name}, {self.pk}'


class LocationImg(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/apartment', default='img/apartment/bali_hotel_livingroom.jpeg')


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}, {self.pk}'


class Apartment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    location_name = models.CharField(max_length=255)
    guest = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    # host = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}, {self.pk}'


class ApartmentImg(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/apartment', default='img/apartment/vogue11jpeg')


class Review(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
