from django.urls import path
from .views import signup, login,logout,mypage,home


app_name='signup'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('home/', home, name='home')
]