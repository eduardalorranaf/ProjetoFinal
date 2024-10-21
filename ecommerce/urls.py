from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalhe/<int:produto_id>', views.detalhe_produto, name='detalhes'),
    path('produtos/', views.produtos, name='produtos'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('login/', views.login, name='login'),
    path('experimento/', views.experimento, name='experimento'),
]
