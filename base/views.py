from django.shortcuts import render, redirect, reverse

# from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from base.admin import admin
from django.views.generic import ListView
from django.core.paginator import Paginator

# from base.permissions import add_default_permissions

# для кастомной модели пользователя вместо встроенной формы регистрации будем использовать кастомную
# from django.contrib.auth.forms import UserCreationForm
from base.forms import CustomUserCreationForm
from .models import User, Room, Topic, Message
from .forms import RoomForm, UserForm


def is_ajax(request):
    """
    This utility function is used, as `request.is_ajax()` is deprecated.

    This implements the previous functionality. Note that you need to
    attach this header manually if using fetch.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # используютс имена полей в форме логина
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_page(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            # add_default_permissions(user)

            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    context = {"form": form}
    return render(request, "base/login_register.html", context)


# def feed(request):
#     """
#     List view for posts.
#     """
#     rooms = (
#         Room.objects.filter(
#             Q(topics__name__icontains=q)
#             | Q(name__icontains=q)
#             | Q(description__icontains=q)
#             | Q(host__username__icontains=q)
#             | Q(host__name__icontains=q)
#         )
#         .distinct()
#         .annotate(votes=Count("upvotes") - Count("downvotes"))
#         .order_by("-votes")
#     )

#     # Pagination

#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     paginator = Paginator(rooms, per_page=3)
#     page_num = int(request.GET.get("page", 1))
#     if page_num > paginator.num_pages:
#         raise Http404
#     posts = paginator.page(page_num)
#     if is_ajax(request):
#         return render(
#             request, "feed_component.html", {"rooms": posts, "page_obj": page_obj}
#         )
#     return render(request, "post_list.html", {"posts": posts, "page_obj": page_obj})


def home(request):
    # используется значение переменной q в GET запросе

    if request.user.is_authenticated:
        print(f'can add? {request.user.has_perm("base.add_topic")}')

    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    # print(f'q not unquoted=[{q}]')
    # q = quote(q)
    # print(f'q unquoted=[{q}]')

    # feed = FeedListView.as_view()(request)
    # feed_objects_context = feed_objects.get_context_data()

    # Topics
    topics_count = Topic.objects.all().count()
    topics = Topic.objects.annotate(Count("rooms")).order_by("-rooms__count")[0:5]

    # добавляем функционал поиска по ленте недавнего
    # лента недавнего показывает недавние сообщения, связанные с текущем юзером, если выполнен вход
    recent_activities = Message.objects.filter(
        (
            Q(room__topics__name__icontains=q)
            | Q(room__name__icontains=q)
            | Q(room__description__icontains=q)
            | Q(room__host__name__icontains=q)
        )
    )

    if request.user.is_authenticated:
        user_room_ids = request.user.rooms.values_list("id", flat=True)
        recent_activities = recent_activities.filter(Q(room__in=user_room_ids))

    rooms = (
        Room.objects.filter(
            Q(topics__name__icontains=q)
            | Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(host__username__icontains=q)
            | Q(host__name__icontains=q)
        )
        .distinct()
        .annotate(votes=Count("upvotes") - Count("downvotes"))
        .order_by("-votes")
    )

    # Pagination

    to_paginate = [(rooms, 'page', 4, "posts"), (recent_activities, 'activitiesPage', 5, "activities")]

    paginated = {"posts": None, "activities": None}

    for current_pagination in to_paginate:
        page_num = int(request.GET.get(current_pagination[1], 1))
        paginator = Paginator(current_pagination[0], per_page=current_pagination[2])

        # page_num = int(request.GET.get("page", 1))
        # paginator = Paginator(rooms, per_page=2)

        if page_num > paginator.num_pages:
            raise Http404
        paginated[current_pagination[3]] = paginator.page(page_num)

    context = {
        # "feed_objects": rooms,
        "posts": paginated["posts"],
        "topics": topics,
        "feed_objects_count": rooms.count(),
        "topics_count": topics_count,
        "recent_activities": paginated["activities"],
    }

    # render only changing from ajax
    if is_ajax(request):
        
        # for pagination
        
        
        
        
        return render(request, "base/feed_posts.html", {"posts": paginated["posts"]})

    return render(request, "base/home.html", context)


# pk - аргумент строки
def room(request, pk):
    room = Room.objects.get(id=pk)
    rooms_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":

        def get_id(id_name):
            obj_id = request.POST.get(id_name)
            try:
                obj_id = int(obj_id)
            except ValueError:
                obj_id = None
            return obj_id

        # message_id = request.POST.get('message_reply_id')
        # try:
        #     reply_to_id = int(message_id)
        # except ValueError:
        #     reply_to_id = None

        reply_to_id = get_id("message_reply_id")

        edit_id = get_id("message_edit_id")

        # Если это не запрос на редактирование - сохраняем новое сообщение
        if edit_id is None:
            message = Message.objects.create(
                user=request.user,
                room=room,
                # body - имя поля в форме с POST запросом
                body=request.POST.get("body"),
                # ответить можно только на то же сообщение в комнате
                replyto=rooms_messages.filter(id=reply_to_id).first(),
            )
        elif edit_id is not None and reply_to_id is None:
            stored_message = rooms_messages.filter(id=edit_id).first()

            if stored_message is None or stored_message.user != request.user:
                return HttpResponse("You are not allowed here!")

            body = request.POST.get("body")

            if body != stored_message.body:
                stored_message.body = body
                stored_message.save()
        else:
            return HttpResponse("You are not allowed here!")

        # добавляем пользователя в комнату после его сообщения если его ещё не было
        room.participants.add(request.user)
        return redirect(request.META["HTTP_REFERER"])

    context = {
        "room": room,
        "rooms_messages": rooms_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    rooms_messages = user.message_set.all()
    # topics = Topic.objects.all()
    topics = (
        Topic.objects.filter(rooms__in=rooms)
        .distinct()
        .annotate(Count("rooms"))
        .order_by("-rooms__count")
    )
    # topics_count = Topic.objects.all().count()
    topics_count = topics.count()
    context = {
        "user": user,
        "rooms": rooms,
        "topics_count": topics_count,
        "rooms_messages": rooms_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    topics_available = Topic.objects.all()

    if request.method == "POST":
        topics_ids = request.POST.getlist("topics")

        topics = []

        for topic_id in topics_ids:
            try:
                topics.append(Topic.objects.get(pk=topic_id))
            except Topic.DoesNotExist:
                pass

        room = Room(
            host=request.user,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        room.save()

        room.participants.add(request.user)
        room.topics.add(*topics)

        return redirect("home")

    context = {"form": form, "topics_available": topics_available, "create": True}
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics_available = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        topics_names = request.POST.get("topics")
        topics = []
        for topic_name in topics_names:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            topics.append(topic)

        # Check if the data has changed
        if (
            room.name != request.POST.get("name")
            or room.topics != topics
            or room.description != request.POST.get("description")
        ):
            room.name = request.POST.get("name")
            room.topics = topics
            room.description = request.POST.get("description")
            room.save()
        # else:
        #     print('Saving the same data dismissed.')

        return redirect(reverse("room", args=[room.id]))

    context = {
        "form": form,
        "topics_available": topics_available,
        "room": room,
        "create": False,
    }
    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="/login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    current_room = message.room

    if request.user != message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        message.delete()
        # print(f'message [{message}] deleted!')
        return redirect(reverse("room", args=[message.room.id]))
        # return redirect_to_previous(request, times=2)
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="/login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)

    return render(request, "base/update-user.html", {"form": form})


def topics_page(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""

    topics = (
        Topic.objects.filter(Q(name__icontains=q))
        .annotate(Count("rooms"))
        .order_by("-rooms__count")
    )
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activities_page(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""

    rooms_messages = rooms_messages = Message.objects.all()

    context = {"rooms_messages": rooms_messages}
    return render(request, "base/activity.html", context)
