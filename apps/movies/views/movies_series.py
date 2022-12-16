# Django
from django.db.models import Q

# Django Rest F
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

# Models
from apps.movies.models import (
    MovieSeries,
    ScoreMovieSeries,
    ViewsMoviesSeries,
    GenderMovieSeries
)

# Serializers
from apps.movies.serializers import (
    MovieSeriesSerializer, 
    ScoreMovieSeriesSerializer,
    ViewsMovieSeriesSerializers,
    GenderMoviesSeriesSerializer
)

# Filters
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters

class MoviesSeriesFilter(django_filters.FilterSet):
    gender = django_filters.CharFilter(
        lookup_expr="exact",
        field_name="gender__code"
    )

    type_streaming = django_filters.CharFilter(
        lookup_expr="exact",
        field_name="type_streaming"
    )

    average = django_filters.NumberFilter(
        field_name='average',
        method='get_average'
    )

    class Meta:
        model = MovieSeries
        fields = ['gender', 'type_streaming', ]
    
    def get_average(self, queryset, name, value):
        return queryset.filter(
            Q(average__gte=value) &
            Q(average__lt=value+1)
        )


class TypeGenderView(viewsets.ModelViewSet):
    queryset = GenderMovieSeries.objects.all()
    serializer_class = GenderMoviesSeriesSerializer
    permission_classes = [IsAuthenticated]

class MoviesSeriesView(viewsets.ModelViewSet):
    queryset = MovieSeries.objects.filter(is_active = True)
    serializer_class = MovieSeriesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MoviesSeriesFilter
    search_fields = [
        'name'
    ]

    def isview(self, user_id, content_id):
        return ViewsMoviesSeries.objects.filter(
            movie_serie = content_id,
            user = user_id
        ).exists()
    
    def isscore(self, user_id, content_id):
        return ScoreMovieSeries.objects.filter(
            movie_serie = content_id,
            user = user_id 
        ).exists()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = {
            'data': serializer.data,
            'is_view': self.isview(request.user.id, instance.id),
            'is_score': self.isscore(request.user.id, instance.id)
        }
        return Response(res)


    @action(detail=False, methods=['GET'])
    def random(self, request, *args, **kwargs):
        queryset = MovieSeries.objects.filter(is_active = True).order_by('?').first()
        ser = self.serializer_class(queryset)
        
        res = {
            'data': ser.data,
            'is_view': self.isview(request.user.id, queryset.id),
            'is_score': self.isscore(request.user.id, queryset.id)
        }

        return Response(res)
    



class ScoreMovieSeriesView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ScoreMovieSeries.objects.filter(is_active=True)
    serializer_class = ScoreMovieSeriesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id 
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewsMovieSerieView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ViewsMoviesSeries.objects.all()
    serializer_class = ViewsMovieSeriesSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id 
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
