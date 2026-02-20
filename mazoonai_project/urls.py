from django.urls import path

from chatapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health', views.health, name='health'),
    path('chat', views.chat, name='chat'),
]
