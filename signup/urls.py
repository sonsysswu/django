from django.urls import path
from .views import signup,login,logout,mypage,home,edit_profile,delete_Guestbook,todolist,delete_Todolist, toggle_todo,post_write,post_list,post, post_edit, delete_post


app_name='signup'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('home/', home, name='home'),
    path('mypage/edit/', edit_profile, name='edit'),
    path('delete_Guestbook/<int:entry_id>/', delete_Guestbook, name='delete_Guestbook'),
    path('todolist/',todolist, name='todolist'),
    path('delete_Todolist/<int:todo_id>/',delete_Todolist,name='delete_Todolist'),
    path('toggle_todo/<int:todo_id>/', toggle_todo, name='toggle_todo'),
    path('post_write/', post_write, name='post_write'),
    path('post_list/',post_list,name='post_list'),
    path('post/<int:post_id>/', post, name = 'post'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('delete_post/<int:post_id>/', delete_post,name='delete_post'),
]
