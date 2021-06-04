from rest_framework.routers import SimpleRouter

from .views import CustomUserViewset

router = SimpleRouter()
router.register('', CustomUserViewset, basename='users')

urlpatterns = router.urls
