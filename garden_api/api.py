from rest_framework.routers import DefaultRouter
from gardens.views import ProfileViewSet, StatsList

router = DefaultRouter()

router.register('profile', ProfileViewSet)
router.register('stats', StatsList)