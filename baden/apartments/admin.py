from django.contrib import admin
from . models import Apartment, ApartmentImg, LocationImg, Location, Review


class AdminInlineApartmentImage(admin.TabularInline):
    model = ApartmentImg
    extra = 1


class AdminApartment(admin.ModelAdmin):
    fields = ['title', 'category', 'address', 'description', 'guests', 'base_price', 'weekend_price']
    inlines = [AdminInlineApartmentImage]


class AdminInlineLocationImg(admin.TabularInline):
    mmodel = Location
    extra = 1


class AdminLocation(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [AdminInlineLocationImg]


admin.site.register(Apartment, AdminApartment)
admin.site.register(Location, AdminLocation)
admin.site.register(Review)





