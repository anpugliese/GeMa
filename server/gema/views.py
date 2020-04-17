from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from django.template import loader
from django.http import HttpResponse
from .models import Choice, Question
import json, csv
from .utils.modules.isg_utils import available_geoids, calculate_orthometric_height, available_geoids_list, calculate_orthometric_height_list

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
@api_view(['POST'])
def geoids_list(request):
    if request.method == "POST":
        print(request.data.get("file"))
        point_file = request.data.get("file")
        point_list = read_point_file(point_file)
        geoid_list = available_geoids_list(point_list)
     
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
            res = json.dumps({"h": "Undefined in geoid"})      
    return HttpResponse(res, status=200)

@csrf_exempt
@api_view(['POST'])
def get_orthometric_height_list(request):
    if request.method == "POST":
        print(request.data.get("file"))
        point_file = request.data.get("file")
        geoid_name = request.data.get("geoid-name")
        point_list = read_point_file(point_file)
        o_h = calculate_orthometric_height_list(point_list, geoid_name)
        if o_h is not None:
            res = json.dumps({"point_list": o_h})
        else:
            return HttpResponse("Error calculating", status=401)        
    return HttpResponse(res, status=200)


def read_point_file(file):    
    point_list = []
    f = file
    
  
    while True: 
     
        line = f.readline()
        #print(line)
        if not line: 
            break
        line = str(line).strip("\\rn'b")
        line_split = line.split(",")
        point_list.append([float(line_split[0]), float(line_split[1]), float(line_split[2])])
    
    f.close() 
    print(point_list)
    return point_list