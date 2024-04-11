from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from autoslug.fields import AutoSlugField

from core_apps.common.models import TimeStampedModel
from core_apps.articles.read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Article(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.CharField(verbose_name=_("Description"), max_length=255)
    body = models.TextField(verbose_name=_("Article content"))
    banner_image = models.ImageField(verbose_name=_("Banner image"), default="/profile_default.jpg")
    tags = TaggableManager()

    def __str__(self):
        return f"{self.author.first_name}s article"

    @property
    def estimated_reading(self):
        return ArticleReadTimeEngine.estimate_reading_time(self)

    @property
    def view_count(self):
        return self.article_views.count()

    @property
    def bookmark_count(self):
        return self.bookmarks.count()

    @property
    def average_rating(self):
        ratings = self.ratings.all()

        if ratings.count() > 0:
            average_rating = ratings.aggregate(average_rating=Avg("rating"))["average_rating"]
            return round(average_rating, 2)


class ArticleView(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_views")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_views")
    viewer_ip = models.GenericIPAddressField(verbose_name=_("viewer ip"), null=True, blank=True)

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        unique_together = ("article", "user", "viewer_ip")

    def __str__(self):
        return f"{self.article.title} viewed by {self.user.get_full_name if self.user else 'Anonymous'}"

    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view, _ = cls.objects.get_or_create(article=article, user=user, viewer_ip=viewer_ip)
