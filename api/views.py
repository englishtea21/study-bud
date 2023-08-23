from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from base.models import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from api.serializers import RoomSerializer


@api_view(["GET"])
def get_routes(request):
    routes = ["GET /api", "GET /api/rooms", "GET /api/rooms/:id"]

    return Response(routes)


@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_room(request, pk):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)


@login_required(login_url="/login")
@permission_required('vote_room')
def toggle_upvote_room(request, *args, **kwargs):
    room = get_object_or_404(Room, pk=kwargs.get("pk"))
    user = request.user
    room.downvotes.remove(user)
    if room.upvotes.contains(user):
        room.upvotes.remove(user)
    else:
        room.upvotes.add(user)
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)


@login_required(login_url="/login")
@permission_required('vote_room')
def toggle_downvote_room(request, *args, **kwargs):
    room = get_object_or_404(Room, pk=kwargs.get("pk"))
    user = request.user
    room.upvotes.remove(user)
    if room.downvotes.contains(user):
        room.downvotes.remove(user)
    else:
        room.downvotes.add(user)
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)


def room_votes_count(request, *args, **kwargs):
    room = get_object_or_404(Room, pk=kwargs.get("pk"))
    votes_count = room.upvotes.count() - room.downvotes.count()
    return JsonResponse({"votes_count": votes_count})
