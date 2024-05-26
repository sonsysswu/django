from django.shortcuts import render, redirect
from .forms import SignUpForm,UserProfileUpdateForm,GuestbookForm,TodoForm,PostForm,Post
from django.contrib import auth, messages
from .models import CustomUser,GuestbookEntry,Todo
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden
from django.contrib.auth.hashers import check_password



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

@login_required
def todolist(request):
    if request.method=='POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # text= request.POST['text']
            # completed = request.POST['completed']
            # entry= Todo(text='text', completed='completed')
            # entry.save()
            form.save()
            return redirect('signup:todolist')
    else:
        form= TodoForm()
    todo_list = Todo.objects.all()
    return render(request,'todolist.html', {'form':form, 'todo_list':todo_list})

def delete_Todolist(request,todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method=='POST':
        todo.delete()
        return redirect('signup:todolist')
    return render(request, 'todolist.html',{'todolist':todolist})

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.completed = not todo.completed  # Toggle the completed status
    todo.save()
    return redirect('signup:todolist')

@login_required
def post_write(request):
    if request.method=='POST':
        form = PostForm(request.POST,user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('signup:post', post_id=post.id)
    else:
        form = PostForm(user=request.user)
    posts=Post.objects.all()
    return render(request,'post_write.html', {'form':form,'posts':posts})

@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post(request,post_id):
    post = get_object_or_404(Post, pk=post_id)  # 해당 post_id에 해당하는 Post 객체를 가져옴
    # if post.secret:
    #     if request.method == 'POST':
    #         password = request.POST.get('password')
    #         if password == post.password:
    #             return render(request, 'post.html', {'post': post})       
    # else:
    return render(request, 'post.html', {'post': post})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('signup:post', post_id=post_id)
    else:
        form = PostForm(instance=post, user=request.user)
    return render(request, 'post_edit.html', {'form': form, 'post':post})

def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method=='POST':
        post.delete()
        return redirect('signup:post_list')
    return render(request, 'post_list.html',{'post_list':post_list})
