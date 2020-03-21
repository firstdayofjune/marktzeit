<<<<<<< HEAD
import json
from django.shortcuts import render
from django.http import HttpResponse


def search(request):
    # TODO: search
    print(request.GET.get('query'))
    results = {'result': [
        {'name': 'Mark1', 'url': '/markt1'},
        {'name': 'Mark2', 'url': '/markt2'}
    ]}
    results = json.dumps(results)
    return HttpResponse(results)
