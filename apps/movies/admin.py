from django.contrib import admin

# Models
from apps.movies.models import (
    GenderMovieSeries,
    MovieSeries,
    ScoreMovieSeries
)

# Register your models here.
admin.site.register(GenderMovieSeries)
admin.site.register(MovieSeries)
admin.site.register(ScoreMovieSeries)
