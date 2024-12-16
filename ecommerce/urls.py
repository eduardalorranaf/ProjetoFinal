from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalhe/<int:produto_id>', views.detalhe_produto, name='detalhes'),
    path('produtos/', views.produtos, name='produtos'),
    path('sobre/', views.sobre, name='sobre'),

    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_carrinho/<int:variacao_id>', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('remover_carrinho/<int:item_id>', views.remover_carrinho, name='remover_carrinho'),

    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('cadastrar_endereco/', views.criar_endereco, name='criar_endereco'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastro'),
    path('editar_produto/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('remover_produto/<int:produto_id>', views.remover_produto, name='remover_produto'),
    path('experimento/', views.experimento, name='experimento'),
   
]



