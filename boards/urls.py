from rest_framework import routers

from boards import views


router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)

urlpatterns = router.urls
