from django.shortcuts import render

from django.http import JsonResponse
import threading

from .ai import startt

def classify(request,name):
    link=request.GET.get('url')
    threading.Thread(target=startt,args=(link,name)).start()
    return JsonResponse({'foo': link})