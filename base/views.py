from django.shortcuts import render, redirect, reverse
# from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
# для кастомной модели пользователя вместо встроенной формы регистрации будем использовать кастомную
# from django.contrib.auth.forms import UserCreationForm
from base.forms import CustomUserCreationForm
from .models import User, Room, Topic, Message
from .forms import RoomForm, UserForm


# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Backend developers'},
# ]

# def redirect_to_previous(request, times=1):
#     previous_url = request.META.get('HTTP_REFERER')
#     for i in range(times):
#         previous_url = request.META.get('HTTP_REFERER', previous_url)
#
#     return redirect(previous_url)

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # используютс имена полей в форме логина
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    # используется значение переменной q в GET запросе

    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    # print(f'q not unquoted=[{q}]')
    # q = quote(q)
    # print(f'q unquoted=[{q}]')

    rooms = Room.objects.filter(
        Q(topics__name__icontains=q)
        |
        Q(name__icontains=q)
        |
        Q(description__icontains=q)
        |
        Q(host__username__icontains=q)
        |
        Q(host__name__icontains=q)
    ).distinct()

    topics_count = Topic.objects.all().count()
    topics = Topic.objects.annotate(Count('rooms')).order_by('-rooms__count')[0:5]
    room_count = rooms.count()
    # добавляем функционал поиска по ленте недавнего
    rooms_messages = Message.objects.filter(
        Q(room__topics__name__icontains=q)
    )

    context = {'rooms': rooms, 'topics': topics, 'topics_count': topics_count, 'room_count': room_count,
               'rooms_messages': rooms_messages}
    return render(request, 'base/home.html', context)


# pk - аргумент строки
def room(request, pk):
    room = Room.objects.get(id=pk)
    rooms_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            # body - имя поля в форме с POST запросом
            body=request.POST.get('body')
        )
        # добавляем пользователя в комнату после его сообщения
        room.participants.add(request.user)
        return redirect(request.META['HTTP_REFERER'])

    context = {'room': room, 'rooms_messages': rooms_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    rooms_messages = user.message_set.all()
    # topics = Topic.objects.all()
    topics = Topic.objects.filter(rooms__in=rooms).distinct().annotate(Count('rooms')).order_by('-rooms__count')
    # topics_count = Topic.objects.all().count()
    topics_count = topics.count()
    context = {'user': user, 'rooms': rooms, 'topics_count': topics_count, 'rooms_messages': rooms_messages,
               'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics_available = Topic.objects.all()

    if request.method == 'POST':
        topics_ids = request.POST.getlist('topics')

        # максимальное количество тем: 5
        # if len(topics_ids)>5:
        #     return

        topics = []

        for topic_id in topics_ids:
            try:
                topics.append(Topic.objects.get(pk=topic_id))
            except Topic.DoesNotExist:
                pass

        room = Room(
            host=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        room.save()

        room.participants.add(request.user)
        room.topics.add(*topics)

        return redirect('home')

    context = {'form': form, 'topics_available': topics_available, 'create': True}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics_available = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topics_names = request.POST.get('topics')
        topics = []
        for topic_name in topics_names:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            topics.append(topic)

        # Check if the data has changed
        if (
                room.name != request.POST.get('name') or
                room.topics != topics or
                room.description != request.POST.get('description')
        ):
            room.name = request.POST.get('name')
            room.topics = topics
            room.description = request.POST.get('description')
            room.save()
        # else:
        #     print('Saving the same data dismissed.')

        return redirect(reverse('room', args=[room.id]))

    context = {'form': form, 'topics_available': topics_available, 'room': room, 'create': False}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    current_room = message.room

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        # print(f'message [{message}] deleted!')
        return redirect(reverse('room', args=[message.room.id]))
        # return redirect_to_previous(request, times=2)
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='/login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    topics = Topic.objects.filter(
        Q(name__icontains=q)
    ).annotate(Count('rooms')).order_by('-rooms__count')
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activities_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms_messages = rooms_messages = Message.objects.all()

    context = {'rooms_messages': rooms_messages}
    return render(request, 'base/activity.html', context)
