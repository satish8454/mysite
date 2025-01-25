from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def index(request):
    return render(request,"index.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("chats")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chats')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat.html', {'users': users,'user':request.user})

@login_required
def fetch_messages(request, user_id):
    receiver = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver], receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    data = [
        {"sender": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M")}
        for msg in messages
    ]
    return JsonResponse(data, safe=False)

@login_required
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            receiver_id = data.get("receiver_id")
            content = data.get("content")

            if not receiver_id or not content:
                return JsonResponse({"success": False, "error": "reciever ID and content are required."}, status=400)

            receiver = User.objects.get(id=receiver_id)
            message = Message.objects.create(
                sender=request.user,
                receiver = receiver,
                content=content
            )
            print("hi")
            return JsonResponse({"success": True, "message_id": message.id})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "reciever does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)