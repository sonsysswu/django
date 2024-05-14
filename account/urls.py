from django.contrib import admin
from django.urls import path,include
from signup.views import main
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('signup/', include('signup.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)