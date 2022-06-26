import re
from urllib.request import urlopen
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Items.models import Item, ItemType, resevedTable
from .ItemSerializer import ItemSerializer, TypeSerializer, ReservedSerializer



@api_view(['GET'])
def all_item_capisty(request):
    type = request.query_params.get('type', None).split(',')

    location = request.GET.getlist('location')
    size = request.GET.get('size')
    print(type)
    print(location)

    items = Item.objects.all().filter(location__in=location, types__in=type, size__gte=size).distinct().order_by(
        '-size')
    serializer = ItemSerializer(items, many=True)

    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_item_Most_rated(request):
    type = request.query_params.get('type', None).split(',')
    location = request.GET.getlist('location')
    print(type)
    print(location)

    items = Item.objects.all().filter(location__in=location, types__in=type).distinct().order_by('-rate')
    serializer = ItemSerializer(items, many=True)

    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_item_by_price_DESC(request):
    type = request.query_params.get('type', None).split(',')
    location = request.GET.getlist('location')
    print(type)
    print(location)

    items = Item.objects.all().filter(location__in=location, types__in=type).distinct().order_by('-price')
    serializer = ItemSerializer(items, many=True)

    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_item_by_price_ASC(request):
    type_ids = request.query_params.get('type', None).split(',')
    location = request.GET.getlist('location')
    print(type)
    print(location)
    items = Item.objects.all().filter(location__in=location, types__in=type_ids).distinct().order_by('price')
    serializer = ItemSerializer(items, many=True)

    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def returnAvalibleTime(request, pk):
    date = request.GET.get('date')
    reserved = resevedTable.objects.all().filter(item=pk, reserved_date=date).distinct()
    serializer = ReservedSerializer(reserved, many=True)
    
    if reserved:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_item_has_type(request):
    type_ids = request.query_params.get('id', None).split(',')
    location = request.GET.getlist('location')
    items = Item.objects.all().filter(types__in=type_ids, location__in=location).distinct()
    serializer = ItemSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(serializer.error_messages)


@api_view(['GET'])
def all_item_by_name(request):
    name = request.GET.get('name')
    items = Item.objects.all().filter(name=name).distinct()
    serializer = ItemSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_item_by_location_and_type(request):
    type = request.GET.getlist('type')
    location = request.GET.getlist('location')
    print(type)
    print(location)

    items = Item.objects.all().filter(location__in=location, types__in=type).distinct()
    serializer = ItemSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_type(request):
    types = ItemType.objects.all()
    serializer = TypeSerializer(types, many=True)
    if types:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_items(request):
    # checking for the parameters from the URL
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        items = Item.objects.all()
        return items

#     def create(self, request, *args, **kwargs):
#         data = request.data
#
#         new_item = Item.objects.create(
#             name=data["name"], address=data['address'], location=data["location"], phone=data["phone"],
#             link=data["link"], about=data["about"], price=data["price"], vendor_id=data["vendor_id"]
#             , reserved=data["reserved"])
#
#         new_item.save()
#
#         for type in data["types"]:
#             types = ItemType.objects.get(type_name=type["type_name"])
#             new_item.types.add(types)
#
#         for amenities in data["types"]:
#             aamenities = ItemType.objects.get(module_name=amenities["amenities_name"])
#             new_item.amenities.add(aamenities)
#
#         for date in data["availability_date"]:
#             dates = ItemType.objects.get(availability_date=date["availability_date"],
#                                          availability_time=date["availability_time"],
#                                          status=date["status"])
#             new_item.availability_date.add(dates)
#
#         for images in data["images"]:
#             imagess = ItemType.objects.get(item_image=images["item_image"])
#             new_item.images.add(imagess)
#
#         serializer = ItemSerializer(new_item)
#
#         return Response(serializer.data)


def important_features(datasets):
    data = datasets.copy()
    for i in range(0, datasets.shape[0]):
        data["imp"] = data["name"].apply(str) + " " + data["location"].apply(str) + " " + data["price"].apply(
            str) + " " + data["rate"].apply(str) + " " + data["types"].apply(str)
    return data






@api_view(['GET'])
def all_Recommended_Item(request):

    itemstr = request.GET.get('itemstr')
    print(itemstr)

    data = Item.objects.all()
    ser = ItemSerializer(data, many=True)
    data = ser.data
    pd.options.display.width = 0
    dataf = pd.json_normalize(data, record_prefix='_')
    dataf["types"] = [re.sub(r"[\([{})\]]", '', str(types)) for types in dataf.types]
    dataf["types"] = [re.sub(r"""['"]+""", '', str(types)) for types in dataf.types]
    dataf.drop("images", axis=1, inplace=True)
    dataf.drop("amenities", axis=1, inplace=True)
    dataf.drop("vendor_id", axis=1, inplace=True)
    dataf.drop("about", axis=1, inplace=True)
    dataf.drop("link", axis=1, inplace=True)

    dataf.drop("phone", axis=1, inplace=True)
    dataf.drop("address", axis=1, inplace=True)
    dataf.drop("availability_date", axis=1, inplace=True)

    dataf.shape

    dataf.info()


    data = important_features(dataf)
    data["ids"] = [i for i in range(0, data.shape[0])]
    vec = TfidfVectorizer()

    vecs = vec.fit_transform(data["imp"].apply(lambda x: np.str_(x)))

    vecs.shape

    sim = cosine_similarity(vecs)

    sim.shape

    def recommend(imp):
        venue_id = data[data.imp == imp]["ids"].values[0]
        scores = list(enumerate(sim[venue_id]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores[0:]
        venues = [data[venues[0] == data["ids"]]["id"].values[0] for venues in sorted_scores]
        return venues




    lst = recommend(str)

    return Response(lst)



