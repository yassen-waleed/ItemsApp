from rest_framework import serializers

from Items.models import Item, images, availability_date, Amenities, ItemType


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields = ['item_image']


class Availability_date_Serializer(serializers.ModelSerializer):
    class Meta:
        model = availability_date
        fields = ['availability_time', 'availability_date', 'status']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'type_name']


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['amenities_name']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'size', 'name', 'address', 'location', 'phone', 'link', 'about', 'price',
                  'vendor_id', 'reserved', 'rate', 'types', 'images', 'amenities', 'availability_date']
        depth = 1
