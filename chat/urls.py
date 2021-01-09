from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/join/<str:room>/',views.joinRoom,name="join-room"),
    path('room/<str:room>/',views.room.as_view(),name="room"),
    path('create/',views.Create.as_view(),name='create'),
]