from django.contrib import admin
from .models import Produto, Cliente, Categoria, Carrinho, ItemCarrinho, Pedido, EnderecoEntrega, VariacaoProduto
# Register your models here.

admin.site.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','preco','estoque','categoria','imagem','data_adicionado')

admin.site.register(VariacaoProduto)
class VariacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto','tamanho','estoque','preco')  

admin.site.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','email','telefone','data_criacao')

admin.site.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')

admin.site.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('cliente','data_criacao')

admin.site.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('carrinho','produto','quantidade')

admin.site.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente','carrinho','data_pedido','total','status')

admin.site.register(EnderecoEntrega)
class EnderecoEntregaAdmin(admin.ModelAdmin):
    list_display = ('cliente','pedido','endereco','cidade','estado','cep')
