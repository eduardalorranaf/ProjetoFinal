from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Categorias para as peças de roupa
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

# 2. Produto 
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)  
    estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='produtos')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, default='default.png')  
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# 3. Variação de Produto (Tamanho, Estoque e Preço)
class VariacaoProduto(models.Model):
    TAMANHOS = [
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    tamanho = models.CharField(max_length=2, choices=TAMANHOS)
    estoque = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Caso queira preços diferentes por tamanho


# 3. Cliente
class Cliente(AbstractUser):
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo

# 4. Carrinho de Compras
class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrinho de {self.cliente.nome_completo}'

# 4. Itens do Carrinho 
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    variacao = models.ForeignKey(VariacaoProduto, on_delete=models.CASCADE) 
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade} x {self.variacao.produto.nome} - Tamanho: {self.variacao.tamanho}'

    def total_item(self):
        return self.quantidade * self.variacao.preco  

# 5. Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.SET_NULL, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Enviado', 'Enviado'),
        ('Entregue', 'Entregue'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome_completo}'

# 6. Endereço de Entrega
class EnderecoEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f'Endereço de {self.cliente.nome_completo}'

