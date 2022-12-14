""" Generic Functions """


def calculate_average_movie_series(queryset, initial_score):
    total_sum = 0
    for query in queryset:
        total_sum += query.score
    return (total_sum + initial_score) / (queryset.count() + (1 if initial_score > 0 else 0))