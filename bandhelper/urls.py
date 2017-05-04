from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/users/', include('accounts.urls')),
    url(r'^api/', include('boards.urls')),
]
