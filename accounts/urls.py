from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('sessions', views.SessionViewSet)

urlpatterns = []

urlpatterns += router.urls


# urlpatterns += [
#     url(r'^login/', obtain_jwt_token),  # zaloguj
#     url(r'^api-token-refresh/', refresh_jwt_token),
# ]
