from django.urls import path

from .views import ObtainAuthTokenView, UserView

urlpatterns = [
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('register/', UserView.as_view(), name='register'),
]

