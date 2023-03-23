from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chats', views.ChatViewSet, basename='chat')
router.register('messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls))
]
