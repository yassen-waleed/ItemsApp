from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Items.models import Item
from .ItemSerializer import ItemSerializer


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



