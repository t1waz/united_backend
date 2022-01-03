from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views


app_prefix = 'users'

urlpatterns = [
    path(f'{app_prefix}/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        f'{app_prefix}/obtain_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        f'{app_prefix}/robot_counter/', views.RobotCounterView.as_view(), name='robot_counter'
    ),
]
