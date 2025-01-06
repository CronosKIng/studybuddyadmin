from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q

# Login page
def loginPage(request):
    page = 'login'
    
    # Angalia kama mtumiaji tayari ameingia, kisha rudisha kwenye home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            email = email.lower()
        
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'login_register.html', context)

# Logout function
def logoutUser(request):
    logout(request)
    return redirect('home')

# User registration
def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # Tumia herufi ndogo kwa username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register.html', {'form': form})

# Home page
def home(request):
    query = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ) if query else Room.objects.all()

    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))

    context = {
        'rooms': rooms,
        'topics': topics,
        'query': query,
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'home.html', context)

# Room details page
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'room.html', context)

# Send message in room (with image and video)
@login_required(login_url='login')
def send_message(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        message_body = request.POST.get('message_body')
        image = request.FILES.get('image')  # Picha
        video = request.FILES.get('video')  # Video

        if message_body.strip() or image or video:
            Message.objects.create(
                user=request.user,
                room=room,
                body=message_body,
                image=image,  # Hifadhi picha
                video=video   # Hifadhi video
            )
            room.participants.add(request.user)  # Ongeza mtumiaji kama mshiriki
            messages.success(request, 'Message sent successfully!')
        else:
            messages.error(request, 'Please provide a message or upload a file.')

    return redirect('room', pk=room_id)

# Create room
@login_required(login_url='login')
def createroom(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    else:
        form = RoomForm()

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)

# Update room
@login_required(login_url='login')
def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if room.host != request.user:
        return HttpResponse('You are not allowed here!')

    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)

# Delete room
@login_required(login_url='login')
def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if room.host != request.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})

# Delete message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)
    if message.user != request.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': message})

# User profile page
def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)


# Update user details
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('user-profile', pk=user.id)

    return render(request, 'update-user.html', {'form':form})

# Topics page
def topicsPage(request):
    topics = Topic.objects.all()

    query = request.GET.get('query')
    if query:
        topics = topics.filter(name__icontains=query)

    return render(request, 'topics.html', {'topics': topics})

# Activity page
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'activity.html', {'room_messages': room_messages})

# Password reset views from Django
from django.contrib.auth import views as auth_views

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})
