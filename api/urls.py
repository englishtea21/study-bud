from django.urls import path
from . import views

from api.views import (
    toggle_upvote_room,
    toggle_downvote_room,
    room_votes_count
)

urlpatterns = [
    # public API
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('rooms/<str:pk>/', views.get_room),
    
    # API for ajax
    path("rooms/<int:pk>/upvote_room/", toggle_upvote_room, name="upvote_room"),
    path("rooms/<int:pk>/downvote_room/", toggle_downvote_room, name="downvote_room"),
    
    path("rooms/<int:pk>/votes_count/", room_votes_count, name="room_votes_count"),
]
