# Django Rest F.
from rest_framework import serializers

# Models
from apps.movies.models import (
    GenderMovieSeries,
    MovieSeries,
    ScoreMovieSeries,
    ViewsMoviesSeries
)


class GenderMoviesSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderMovieSeries
        fields = ['code', 'name']

class ViewsMovieSeriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ViewsMoviesSeries
        exclude = ['is_active']
    
    def validate(self, attrs):
        exist_score = ViewsMoviesSeries.objects.filter(
            user = attrs.get('user', None),
            movie_serie = attrs.get('movie_serie', None)
        )

        if exist_score.exists():
            raise serializers.ValidationError({'error': f'Ya marcaste como vista esta serie/pelicula'})
        
        return attrs

class ScoreMovieSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreMovieSeries
        exclude = ['is_active']
    
    def validate(self, attrs):
        exist_score = ScoreMovieSeries.objects.filter(
            user = attrs.get('user', None),
            movie_serie = attrs.get('movie_serie', None)
        )

        if exist_score.exists():
            raise serializers.ValidationError({'error': f'Ya puntuaste esta serie/pelicula'})
        
        return attrs

class MovieSeriesSerializer(serializers.ModelSerializer):
    gender = GenderMoviesSeriesSerializer()
    scores = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    class Meta:
        model = MovieSeries
        exclude = ['is_active', 'modified']

    def get_scores(self, instance):
        scores = ScoreMovieSeries.objects.filter(is_active = True, movie_serie = instance.id)
        ser = ScoreMovieSeriesSerializer(scores, many=True)
        return ser.data
    
    def get_views(self, instance):
        views = ViewsMoviesSeries.objects.filter(movie_serie = instance.id)
        return views.count()


    