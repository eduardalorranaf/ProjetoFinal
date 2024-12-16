from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Cliente, Produto, EnderecoEntrega

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['nome_completo', 'username', 'email', 'telefone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
        self.fields['nome_completo'].widget.attrs.update({'placeholder': 'Nome Completo'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail'})
        self.fields['telefone'].widget.attrs.update({'placeholder': 'Telefone'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme sua senha'})

class ClienteChangeForm(UserChangeForm):
    class Meta:
        model = Cliente
        fields = ['nome_completo', 'username', 'email', 'telefone']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = EnderecoEntrega
        fields = ['endereco', 'cidade', 'estado', 'cep']


class ClienteLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'imagem']
