from django.shortcuts import render, redirect
from .forms import SignUpForm,UserProfileUpdateForm,GuestbookForm
from django.contrib import auth, messages
from .models import CustomUser,GuestbookEntry
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
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
        if user is not None:
            auth.login(request, user)
            return redirect('signup:home')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main')

# def main(request):
#     return render(request,'main.html')

def mypage(request):
    return render(request, 'mypage.html')

@login_required
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

def main(request):
    if request.method=='POST':
        form=GuestbookForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            message= request.POST['message']
            password= form.cleaned_data['password']
            entry= GuestbookEntry(name= name,message=message,guest_password= password)
            entry.save()
            return redirect('main')
    else:
        form =GuestbookForm()

    entries= GuestbookEntry.objects.all()
    return render(request,'main.html', {'form':form,'entries':entries})

@csrf_exempt
def delete_Guestbook(request, entry_id):
    if request.method=='POST':
        entry = GuestbookEntry.objects.get(pk=entry_id)
        password= request.POST.get('password', '')
        if password == entry.guest_password:
            entry.delete()
            messages.success(request,'방명록이 삭제되었습니다.')
        else:
            messages.error(request,'비밀번호가 올바르지 않습니다.')
    return redirect('main')
# Create your views here.
