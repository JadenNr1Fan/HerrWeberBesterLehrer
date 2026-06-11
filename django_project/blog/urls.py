from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]

path('gallery/', include('gallery.urls')),