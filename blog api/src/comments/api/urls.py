from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentListAPTView,
    CommentDetailAPIView
)


urlpatterns = [
    url(r'^$', CommentListAPTView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$' , CommentDetailAPIView.as_view() , name='thread')
]








