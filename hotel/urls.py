"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from buscadorReservas import views
from django.urls import path
from buscadorReservas.views import main, select_date_room, create_reservation, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main, name="main"),
    path('select_date_room/', views.select_date_room, name="select_date_room"),
    path('create_reservation/<int:id>/<str:entry_date>/<str:departure_date>/', views.create_reservation, name="create_reservation"),
    path('contact/', views.contact, name="contact"),
]
