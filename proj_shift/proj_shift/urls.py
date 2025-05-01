"""
URL configuration for proj_shift project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from shift_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('registar_cliente', views.registar_cliente, name='registar_cliente'),
    path('remover_cliente/<int:id>', views.remover_cliente, name='remover_cliente'),
    path('atualizar_cliente/<int:id>', views.atualizar_cliente, name='atualizar_cliente'),
    path('login_cliente', views.login_cliente, name='login_cliente'),

]
