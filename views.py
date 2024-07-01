from django.shortcuts import render, redirect
from . models import UserPredictModel
from . forms import UserPredictForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np
import pandas as pd

#from tensorflow import keras
from PIL import Image, ImageOps
from . import forms
from .models import predict
import pickle

def Landing_0(request):
    return render(request, 'welcome.html')
def aLanding(request):
    return render(request, 'welcome.html')


def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('input1')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)


def input1(request):
    return render(request,'input1.html')
#class_names=np.array(['ENFJ', 'ENFP', 'ENTJ', 'ENTP', 'ESFJ', 'ESFP', 'ESTJ', 'ESTP','INFJ', 'INFP', 'INTJ', 'INTP', 'ISFJ', 'ISFP', 'ISTJ', 'ISTP'])
def output(request):
	algo=request.POST.get('algo')
	url=request.POST.get('url')
	#print(row)
	out=predict(algo,url)
	#classes = class_names[int(out)]
	print(out[1])
	if out[1] >= 0.5:
		class_name = 'Yes, The URL is Good'
	else:
		class_name = 'No, The URL is Bad'
	print(class_name)
	return render(request,'output.html',{'out':class_name})

def Logout(request):
    logout(request)
    return redirect('Login_3')

