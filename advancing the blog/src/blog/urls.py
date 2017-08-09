from django.conf import settings
from django.conf.urls import url , include
from django.conf.urls.static import static
from django.contrib import admin
from posts import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^posts/', include("posts.urls" , namespace='posts')),
]


if settings.DEBUG:
	urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)