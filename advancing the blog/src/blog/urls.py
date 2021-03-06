from django.conf import settings
from django.conf.urls import url , include
from django.conf.urls.static import static
from django.contrib import admin
from posts import views 

from accounts.views import (
    login_view,
    register_view,
    logout_view,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^login/' , login_view, name='login'),
    url(r'^logout/' , logout_view, name='logout'),
    url(r'^register/' , register_view, name='register'),
    url(r'^', include("posts.urls" , namespace='posts')),
]


if settings.DEBUG:
	urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    