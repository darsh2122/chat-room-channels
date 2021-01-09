from chat.models import Message
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.models import Group

def index(request):
    rooms = Group.objects.all()

    context = {  
        'rooms':rooms,
    }
    return render(request, 'index.html',context)   

def joinRoom(request, room):

    user = request.user
    rooms = Group.objects.all()
    curr_room = Group.objects.get(name=room)
    user.groups.add(curr_room)
    user.save()
    context = {
        'room_name': room,
        'rooms':rooms,
    }
    redirectLink = '/room/' + room + '/'
    return redirect(redirectLink,context)

class room(View):
    def get(self,request,room):
        rooms = Group.objects.all()
        context = {
            'rooms':rooms,
            'room_name':room
        }
        return render(request, 'room.html',context)    

class Create(View):
    def get(self,request,format=None):
        return render(request,'createRoom.html')

    def post(self,request,format=None):
        name = self.request.POST.get('room')
        queryset = Group.objects.filter(name=name)
        
        if queryset.exists():
            context = {
                'error':'Room name already exists, name something else'
            }
            return render(request,'error.html',context)
        room = Group.objects.create(
            name=name,
        )
        room.save()
        redirectLink = '/room/' + room.name + '/'
        return redirect(redirectLink)

def get_last_10_messages(room_name):
    messages = Message.objects.filter(room__name=room_name)
    return messages[:10]