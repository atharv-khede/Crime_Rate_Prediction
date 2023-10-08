from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import joblib
model = joblib.load('./static/KMeans_Clustering')
# Create your views here.
@login_required(login_url='login')
def prediction(request):
    if request.method=='POST':
        print("start post")
        state = request.POST.get('state')
        district = request.POST.get('district')
        year = request.POST.get('year')
        murder = int(request.POST.get('murder'))
        rape = int(request.POST.get('rape'))
        Kidnapping_and_Abdustion = int(request.POST.get('k and a'))
        decoity = int(request.POST.get('decoity'))
        # print(decoity)
        robbary = int(request.POST.get('robbary'))
        burglary = int(request.POST.get('burglary'))
        theft = int(request.POST.get('theft'))
        Dowry_Deaths = int(request.POST.get('DD'))
       
        list  = [murder, rape, Kidnapping_and_Abdustion,decoity,robbary,burglary,theft,Dowry_Deaths]

        pred = model.predict([[murder, 
        rape,
        Kidnapping_and_Abdustion,
        decoity,
        robbary,
        burglary,
        theft,
        Dowry_Deaths]])

        if all(x == 0 for x in list):
            pred[0]=1
        print(pred)

        if pred[0]==3:
         output = {'output': 80, 'range': 'Very High-crime'}
        
        elif pred[0]==0:
         output = {'output': 62, 'range': 'High-crime'}
        
        elif pred[0]==2:
         output = {'output': 41, 'range': 'Moderate-crime'}
         
        elif (pred[0]==1):
         output = {'output': 22, 'range': 'Low-crime'}
         
        print(output)
        return render (request,'result.html', output)
    else:
       return render (request,'prediction.html')
       
def home(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def result(request):
     return render(request, 'result.html')

def Dataset(request):
    return render(request,"dataset.html")

def Analysis(request):
    return render(request,"Analysis.html")

