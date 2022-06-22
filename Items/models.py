from django.db import models


class ItemType(models.Model):
    type_name = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.type_name


class Amenities(models.Model):
    amenities_name = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.amenities_name


class availability_date(models.Model):
    availability_time = models.DateTimeField(null=False, blank=False)
    availability_date = models.DateTimeField(null=False, blank=False)
    status = models.BooleanField(default=False)


class images(models.Model):
    item_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.item_image


class Item(models.Model):
    name = models.CharField(max_length=300, blank=False)
    address = models.CharField(max_length=300, blank=False)
    location = models.CharField(max_length=300, blank=False)
    phone = models.TextField(blank=False)
    link = models.CharField(max_length=600, blank=False)
    about = models.CharField(max_length=1000, blank=False)
    price = models.TextField(blank=False)
    vendor_id = models.CharField(max_length=10, blank=False)
    reserved = models.BooleanField(default=False)
    rate = models.TextField(max_length=10)
    size = models.IntegerField(max_length=10,default=100)
    types = models.ManyToManyField(ItemType)
    images = models.ManyToManyField(images)
    amenities = models.ManyToManyField(Amenities)
    availability_date = models.ManyToManyField(availability_date)

    def __str__(self):
        return self.name
