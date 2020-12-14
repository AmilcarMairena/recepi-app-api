from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recepi import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recepi'

urlpatterns = [
    path('', include(router.urls))
]
