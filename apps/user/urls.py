from django.urls import path, include

# Django REST F
from rest_framework.routers import DefaultRouter

# Views 
from .views import UserView

router = DefaultRouter()

router.register(r'user', UserView, basename='user')


urlpatterns = [
    path('', include(router.urls))
]