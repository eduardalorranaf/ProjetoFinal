from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto

# Create your views here.
def home(request):
    produtos = Produto.objects.all()

    context = {
        'produtos':produtos
    }


    return render (
        request,
        'ecommerce/index.html',
        context
    )

def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    variacoes = produto.variacoes.all() 
    produtos_recomendados = Produto.objects.filter(categoria=produto.categoria).exclude(id=produto.id)[:4]


    context = {
        'produto': produto,
        'variacoes': variacoes,
        'produtos_recomendados': produtos_recomendados,
    }

    return render(request, 'ecommerce/detalhe.html', context)
    
def produtos(request):
    produtos = Produto.objects.all()

    # Filtragem de faixa de preço
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    # Filtragem por categorias
    categorias = request.GET.getlist('categoria')
    if categorias:
        produtos = produtos.filter(categoria__nome__in=categorias)


    # Filtragem por tamanhos
    tamanho = request.GET.get('tamanho')
    if tamanho:
        produtos = produtos.filter(variacoes__tamanho=tamanho)

    # Ordenação dos produtos
    ordenar = request.GET.get('ordenar')
    if ordenar == 'price_asc':
        produtos = produtos.order_by('preco')
    elif ordenar == 'price_desc':
        produtos = produtos.order_by('-preco')
    elif ordenar == 'newest':
        produtos = produtos.order_by('-data_adicionado') 

    context = {
        'produtos':produtos
    }

    return render (
        request,
        'ecommerce/produtos.html',
        context
    )

def carrinho(request):
    
    return render (
        request,
        'ecommerce/carrinho.html'
    )

def login(request):
    
    return render (
        request,
        'ecommerce/login.html'
    )

def experimento(request):
    
    return render (
        request,
        'ecommerce/experimento.html'
    )