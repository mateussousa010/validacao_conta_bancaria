"""test_documentation URL Configuration

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
from conta_bancaria.views import cadastroBancoView, contaBancariaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/conta-bancaria',
         cadastroBancoView.as_view(), name='cadastro_banco'),
    path('conta-bancaria/<int:pk>/',
         contaBancariaView.as_view(), name='conta_bancaria')
]