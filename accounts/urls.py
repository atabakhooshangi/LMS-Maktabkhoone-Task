from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),

    # These Endpoints are related with jwt auth , navigate to /api/accounts/token to create a jwt token for Auth
    # or simply remove it
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
