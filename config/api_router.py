from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from authentication.views.user_viewset import UserViewSet
from authentication.views.admin_viewset import AdminViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("admin", AdminViewSet)


app_name = "api"
urlpatterns = router.urls
