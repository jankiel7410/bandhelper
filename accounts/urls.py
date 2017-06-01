from rest_framework import routers

from accounts import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('sessions', views.SessionViewSet)
router.register('votes', views.VoteViewSet)

urlpatterns = []

urlpatterns += router.urls


# urlpatterns += [
#     url(r'^login/', obtain_jwt_token),  # zaloguj
#     url(r'^api-token-refresh/', refresh_jwt_token),
# ]
