from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)


from users.apps import UsersConfig
from users import views


app_name = UsersConfig.name

urlpatterns = [
    # USER PROFILE GENERIC APIVIEW URLS
    path('profile/', views.UserProfileListView.as_view(), name='user-list'),
    path('profile/<int:pk>/', views.UserProfileRetrieveView.as_view(), name='user-profile'),
    path('profile/<int:pk>/update/', views.UserProfileUpdateView.as_view(), name='user-update'),
    path('profile/<int:pk>/delete/', views.UserProfileDestroy.as_view(), name='user-delete'),

    # PATH TO GET API TOKENS FOR ACCESS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
