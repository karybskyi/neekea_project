from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from neekea import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('main.urls', namespace='main')),
    path('user/', include('users.urls', namespace='users')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('order/', include('orders.urls', namespace='orders'))

]

if settings.DEBUG:
    urlpatterns += [
            path('catalog/', include('goods.urls', namespace='goods')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
