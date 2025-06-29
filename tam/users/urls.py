from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('profiles/', views.get_profiles),
    path('initialize/', views.profile),
    path('update-profile/', views.update_profile),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("change-password/",views.change_password),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
