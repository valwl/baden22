from rest_framework import serializers
from . models import Apartment, ApartmentImg, Location, Review


class ApartmentImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImg
        fields = ['img']


class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImgSerializer(many=True, required=False)

    class Meta:
        model = Apartment
        fields = ['title', 'description', 'location', 'category', 'category']

    def create(self, validated_data):
        images_data = validated_data.pop('img', [])
        apartment = Apartment.objects.create(**validated_data)

        for image in images_data:
            ApartmentImg.objects.create(apartment=apartment, **image)

        return apartment


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

