from django.shortcuts import render, redirect
from .forms import SignUpForm,UserProfileUpdateForm
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from .models import CustomUser, UserProFile


# Create your views here.
def signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #성공하면 home으로 바로 보냄
            return render(request, 'main.html')
        return render(request, 'signup.html', {'form': form })
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form } )

def login(request):
    if request.method=='POST':
        id=request.POST.get('id')
        password=request.POST.get('password')
        user=auth.authenticate(request, id = id, password = password)
        #print(user)
        #기본은 id가 아니고 username인데 CustomUser에서 USERNAME_FIELD='id'로 설정해서 일케 해야해여 backends.py에서 약간 바꿨어여
        if user is not None:
            auth.login(request, user)
            return render(request,'home.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main')

def main(request):
    return render(request,'main.html')

def mypage(request):
    return render(request, 'mypage.html')

def home(request):
    return render(request,'home.html')

def edit(request):
    return render(request,'mypage_edit.html')

def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        try:
            form.image=request.FILES['image']
        except: #이미지가 없어도 그냥 지나가도록-!
            pass
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return redirect('/signup/mypage')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'mypage_edit.html', {'form': form})


# Create your views here.
