from django.shortcuts import render
from django.http import HttpResponse
from app.tasks import add


def new_add(request):
    a = add.delay(4, 5)
    return HttpResponse(str(a))



