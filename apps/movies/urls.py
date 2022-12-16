from django.urls import path, include

# Django REST F
from rest_framework.routers import DefaultRouter

# Views 
from .views import MoviesSeriesView, ScoreMovieSeriesView, ViewsMovieSerieView, TypeGenderView

router = DefaultRouter()


router.register(r'moviesseries', MoviesSeriesView, basename='moviesseries')
router.register(r'gender', TypeGenderView, basename='gender')
router.register(r'score', ScoreMovieSeriesView, basename='score')
router.register(r'views', ViewsMovieSerieView, basename='views')

urlpatterns = [
    path('', include(router.urls))
]