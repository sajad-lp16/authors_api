from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Rating(TimeStampedModel):
    class RatingChoices(models.IntegerChoices):
        POOR = 1, "Poor"
        FAIR = 2, "Fair"
        GOOD = 3, "Good"
        VERY_GOOD = 4, "Very Good"
        EXCELLENT = 5, "Excellent"

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_("Article"), related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="ratings")
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices)
    review = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ("article", "user")

    def __str__(self):
        return f"{self.user.first_name} rated {self.article.title} as {self.get_rating_display()}"
