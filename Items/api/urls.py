from django.urls import path, include
from .views import ItemViewSet, all_type
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("items", ItemViewSet, basename="Items")

urlpatterns = [
    path('', include(router.urls)),
    path('types', views.all_type, name='view-types'),
    path('types_filter', views.all_item_has_type, name='view-types'),
    path('customerItems', views.all_item_by_location_and_type, name='view-types')
]
