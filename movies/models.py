from django.db import models


class RatingOptions(models.TextChoices):
    g_rate = "G"
    pg_rate = "PG"
    pg13_rate = "PG-13"
    r_rate = "R"
    nc17_rate = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        choices=RatingOptions.choices,
        max_length=20,
        null=True,
        default=RatingOptions.g_rate,
    )
    synopsis = models.TextField(null=True, default=None)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies", null=False
    )

    def __str__(self) -> str:
        return f"<Movie [{self.id}] - [{self.title}]"
