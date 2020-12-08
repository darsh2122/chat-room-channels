from django.shortcuts import redirect, render
from django.views.generic import View

from .models import Room

def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })    

class Create(View):
    def get(self,request,format=None):
        return render(request,'createRoom.html')

    def post(self,request,format=None):
        name = self.request.POST.get('room')
        room = Room()
        room.name = name
        room.group = name
        room.save()
        redirectLink = '/room/' + room.name + '/'
        return redirect(redirectLink)

