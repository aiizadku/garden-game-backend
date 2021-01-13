from rest_framework.routers import DefaultRouter
from gardens.views import ProfileViewSet

router = DefaultRouter()

router.register('profile', ProfileViewSet)