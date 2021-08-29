from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden

import json
import requests

RUN_URL = "https://api.hackerearth.com/code/run/"
CLIENT_SECRET = '1d96816dd358e560239c975798991d3ea432ee02'

def home(request):
    return render(request, 'editor/playground.html')

def compiler(request):
    return render(request, 'editor/compiler.html')

def web_compiler(request):
    return render(request, 'editor/web_compiler.html')


#From HackerEarth API
def run_code(request):
	if request.is_ajax():
		source = request.POST['source']
		lang = request.POST['lang']
		data = {
			'client_secret': CLIENT_SECRET ,
			'async': 0,
			'source': source,
			'lang': lang,
			'time_limit': 5,
			'memory_limit': 262144,
		}
		if 'input' in request.POST:
			data['input'] = request.POST['input']

		r = requests.post(RUN_URL, data=data)
		return JsonResponse(r.json(), safe=False)

	else:
		return HttpResponseForbidden()
