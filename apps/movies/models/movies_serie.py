# Django 
from django.db import models

# Utils
from core.base_model import AlternovaModel
from core.functions import calculate_average_movie_series

# Models
from apps.user.models import User


TYPE_STREAMING = (
    ("Serie", "Serie"),
    ("Pelicula", "Pelicula"),
)

class GenderMovieSeries(AlternovaModel):
    code = models.CharField(max_length = 100, unique=True)
    name = models.CharField(max_length = 100)

    class Meta:
        db_table = "gender_movie_serie"
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
    

class MovieSeries(AlternovaModel):
    name = models.CharField(max_length = 150)
    
    gender = models.ForeignKey(
        GenderMovieSeries, 
        on_delete=models.CASCADE,
        related_name='gender_type_gender'
    )

    type_streaming = models.CharField(
        max_length = 150,
        choices=TYPE_STREAMING
    )

    image = models.ImageField(
        upload_to='media/movie-series/',
        max_length=255, 
        null=True,
        blank=True
    )
    
    average = models.FloatField(default=0)

    class Meta:
        db_table ='movie_series'
        verbose_name = "Peliculas y Series"
        verbose_name_plural = "Peliculas y Series"

    def __str__(self) -> str:
        return f"{self.name} - {self.type_streaming} - {self.gender.name}"

class ViewsMoviesSeries(AlternovaModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='views_movie_series_user'
    )

    movie_serie = models.ForeignKey(
        MovieSeries, 
        related_name='views_movie_serie', 
        on_delete=models.CASCADE
    )


    class Meta:
        db_table = "view_movie_serie"

class ScoreMovieSeries(AlternovaModel):
    score = models.IntegerField()
    comment = models.CharField(max_length = 100)
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='score_movie_series_user'
    )

    movie_serie = models.ForeignKey(
        MovieSeries, 
        related_name='score_movie_serie', 
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "score_movie_serie"
    
    def __str__(self) -> str:
        return f"{self.movie_serie.name} - Score: {self.score}"

    def save(self, *args, **kwargs):
        print("ID", self.id)
        scores_movies_series = ScoreMovieSeries.objects.filter(movie_serie = self.movie_serie.id)
        self.movie_serie.average = calculate_average_movie_series(scores_movies_series, 0 if self.id else self.score)
        self.movie_serie.save()
        super(ScoreMovieSeries, self).save(*args, **kwargs)
    

    