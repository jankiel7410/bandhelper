from rest_framework import routers

from boards import views


router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'boards', views.BoardViewSet)

urlpatterns = router.urls
