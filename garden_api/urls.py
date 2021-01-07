from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
# from .api import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token-auth/', obtain_jwt_token),
    path('gardens/', include('gardens.urls')),
    # path('api/', include(router.urls))

]
    