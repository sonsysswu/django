from django.contrib import admin
from django.urls import path,include
from signup.views import main


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('signup/', include('signup.urls')),
]