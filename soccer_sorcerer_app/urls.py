from django.contrib import admin
from django.urls import path
from .views import home, predict

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict', predict),
    path('', home)
    
]
