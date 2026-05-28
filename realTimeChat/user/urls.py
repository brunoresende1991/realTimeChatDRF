from user.views import UserViewSet

from rest_framework.routers import DefaultRouter

from django.contrib.auth.views import LoginView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]

router = DefaultRouter()
router.register('', UserViewSet, basename='user')
urlpatterns += router.urls
