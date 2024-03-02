from django.contrib import admin
from django.urls import path, include

from neekea.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('main.urls', namespace='main')),
]

if DEBUG:
    urlpatterns += [
            path('catalog/', include('goods.urls', namespace='goods')),
    ]