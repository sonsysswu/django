from django.urls import path
from .views import signup, login,logout,mypage,home,edit_profile,delete_Guestbook,todolist,delete_Todolist
from django.conf import settings
from django.conf.urls.static import static

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
    path('delete_Todolist/<int:todo_id>/',delete_Todolist,name='delete_Todolist')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
