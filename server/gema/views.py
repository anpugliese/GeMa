from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from django.template import loader
from django.http import HttpResponse
from .models import Choice, Question
import json
from .utils.modules.isg_utils import available_geoids, calculate_orthometric_height

@csrf_exempt
def geoids(request):
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        lat = float(body["latitude"])
        lng = float(body['longitude'])
        h = float(body['h'])
        geoid_list = available_geoids((lat, lng, h))
        #lat = request.POST['latitude']
        #lng = request.POST['longitude'] 
        #h = request.POST['h']
        
        res = json.dumps({"geoid-list": geoid_list})
    return HttpResponse(res, status=200)

@csrf_exempt
def get_orthometric_height(request):
    if request.method == "POST":
        body = json.loads(request.body)
        lat = body["latitude"]
        lng = body['longitude']
        h = body['h']
        geoid_name = body["geoid-name"]
        p = (float(lat), float(lng), float(h))
        o_h = calculate_orthometric_height(p, geoid_name)
        if o_h is not None:
            res = json.dumps({"h": o_h})
        else:
            return HttpResponse("Error calculating", status=401)        
    return HttpResponse(res, status=200)