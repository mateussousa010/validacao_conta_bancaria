
from django.views.generic import CreateView, DetailView
from .forms import cadastroBanco
from .models import contaBancaria


class cadastroBancoView(CreateView):
    model = contaBancaria
    form_class = cadastroBanco
    template_name = 'conta_bancaria/cadastro_banco.html'


class contaBancariaView(DetailView):
    model = contaBancaria
