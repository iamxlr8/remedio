from django.contrib.syndication.views import Feed
from remedio.models import Rating
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

class DreamrealCommentsFeed(Feed):
    title = "Remedio User Ratings"
    link = "/drcomments/"
    description = "updates on new user ratings."

    def items(self):
        return Rating.objects.all().order_by("-time")[:5]

    def item_title(self, item):
        return item.user

    def item_description(self, item):
        return item.rating

    def item_link(self, item):
        return reverse('remedio:rate')