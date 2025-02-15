from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import string ,random,json
from django.contrib.auth.hashers import make_password
from . models import *
from django.contrib.auth import authenticate
import base64
from django.core.files.base import ContentFile

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=data['password']
        country=data['country']
        gender=data['gender']
        birth=data['birth']
        roll=None
        try:
            roll=data['type']
            if roll:
                if roll=="doctor":
                    d=Doctor.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                    send_mail(email,"Welcome..","You have a new registration in the Selene Mental Health App")
                    return JsonResponse({'state':'success'}, status=200)
                else:
                    roll="patient"
                    p=Patient.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
                    send_mail(email,"Welcome..","You have a new registration in the Selene Mental Health App")
                    return JsonResponse({'state':'success'}, status=200)      
        except Exception as e:
            print(e)
        if roll==None:
            roll="patient"
            p=Patient.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,country=country,gender=gender,birth=birth,type=roll)
            send_mail(email,"Welcome..","You have a new registration in the Selene Mental Health App")
            return JsonResponse({'state':'success'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        password=data['password']
        if authenticate(request, email=email,password=password): 
            user=User.objects.get(email=email)
            if user.type=="patient":
                Json_res=Patient.objects.get(email=email)
                Json_res.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                Json_res.save()
                res=Patient.objects.filter(email=email).values()[0]
                return JsonResponse({'state':{"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type']}}, status=200)
            else:
                Json_res=Doctor.objects.get(email=email)
                Json_res.token= ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                Json_res.save()
                res=Doctor.objects.filter(email=email).values()[0]
                return JsonResponse({'state':{"first_name":res['first_name'],"last_name":res['last_name'],"email":res['email'],"country":res['country'],"gender":res['gender'],"birth":res['birth'],"photo":res['photo'],"language":res['language'],"password":"","token":res['token'],"type":res['type']}}, status=200)

        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        token= data['token']
        obj_res=None
        try:
            obj_res=User.objects.get(email=email,token=token)
        except:
            pass
        if obj_res!=None:
            obj_res.token= None
            obj_res.save()
            return JsonResponse({'user':'logout'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def exp_logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        obj_res=None
        try:
            obj_res=User.objects.get(email=email)
        except:
            pass
        if obj_res:
            obj_res.token= None
            obj_res.save()
            return JsonResponse({'user':'logout'}, status=200)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email= data['email']
        token=data['token']
        params=data['params']
        new_values=data['new_values']
        user=User.objects.get(email=email,token=token)
        if user:
            if user.type=="patient":
                for i ,j in zip(params,new_values):
                    if hasattr(Patient, i):
                        try:
                            obj_res=Patient.objects.get(email=email)
                            if obj_res:
                                setattr(obj_res, i, j)
                                obj_res.save()
                                return JsonResponse({'state':"success"}, status=200)
                        except: 
                            return JsonResponse({'state':'form is not valid'}, status=201)       
            else:
                for i ,j in zip(params,new_values):
                    if hasattr(Doctor, i):
                        try:
                            obj_res=Doctor.objects.get(email=email)
                            if obj_res:
                                setattr(obj_res, i, j)
                                obj_res.save()
                                return JsonResponse({'state':"success"}, status=200)
                        except: 
                            return JsonResponse({'state':'form is not valid'}, status=201)
        return JsonResponse({'state':'form is not valid'}, status=201)
    return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt 
def photo(request,email):
    try:
        person=User.objects.get(email=email)
        img = open(str(person.photo), 'rb')
        response = FileResponse(img)
        return response
    except:
        return JsonResponse({"res":None})
    
@csrf_exempt 
def upload_photo(request,email):
    try:
        # data:image/jpeg;base64,
        data = json.loads(request.body)
        user= User.objects.get(email=email)
        format, imgstr = data["photo"].split(';base64,') 
        ext = format.split('/')[-1] 
        user.photo = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        user.save()
        return JsonResponse({'state':"success"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'state':e}, status=201)

@csrf_exempt 
def get_profile(request,email):
    try:
        user=User.objects.get(email=email)
        if user.type=="patient":
            user=Patient.objects.get(email=email)
            return JsonResponse({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender})
        else:
            user=Doctor.objects.get(email=email)
            return JsonResponse({"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"birth":user.birth,"gender":user.gender,"clinic_address":user.clinic_address,"rate":user.rate})
    except Exception as e:
        print(e)
        return JsonResponse({"user":None})
    
@csrf_exempt 
def check_token(request):
    data = json.loads(request.body)
    email= data['email']
    token= data['token']
    obj_res = User.objects.filter(email=email,token=token)
    if obj_res:
        return obj_res[0]
    else:
        return None
    
@csrf_exempt 
def get_doctor_list(request):
    res=[]
    users=Doctor.objects.filter(type='doctor')
    def myFunc(e):
        return e['rate']
    users.sort(reverse=True,key=myFunc)
    for i in users:
        res.append({"email":i.email,"first_name":i.first_name,"last_name":i.last_name,"rate":i.rate})
    return JsonResponse({"doctors":res})

@csrf_exempt 
def reating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_resul=check_token(request)
        if check_token(request):
            r=data['rate']
            doctor=data['doctor']
            doctor=Doctor.objects.get(email=doctor)
            old_r=doctor.rate
            old_num_rating=doctor.num_of_rate
            new_rate=(old_r+r)/(old_num_rating+1)
            new_num_rating=old_num_rating+1
            doctor.rate=new_rate
            doctor.num_of_rate=new_num_rating
            doctor.save()
            return JsonResponse({'new_rate':new_rate}, status=200)
        else:
            return exp_logout(request)
    return JsonResponse({'state':'error request method'}, status=201)

import requests
@csrf_exempt 
def send_mail(sendto,title,body):
    url = "https://mail-sender-api1.p.rapidapi.com/"
    payload = {
        "sendto": sendto,
        "name": "Selene",
        "replyTo": "",
        "ishtml": "false",
        "title": title,
        "body": body
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "mail-sender-api1.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    if(response.status_code!=200):
        url = "https://rapidmail.p.rapidapi.com/"
        response = requests.post(url, json=payload, headers=headers)

    print(response.json())