from django.urls import path
from .views import signup, login,logout,mypage,home,edit_profile,delete_Guestbook
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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
