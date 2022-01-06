from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)


app_prefix = 'users'

urlpatterns = [
    path(f'{app_prefix}/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        f'{app_prefix}/obtain_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
]
