from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Cliente, EnderecoEntrega, ItemCarrinho, Carrinho, VariacaoProduto
from .forms import ClienteCreationForm, ClienteChangeForm, EnderecoForm, ProdutoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def home(request):
    produtos = Produto.objects.all()
    pesquisa = request.GET.get('search')  
    if pesquisa:
        produtos = Produto.objects.filter(nome__icontains=pesquisa).order_by('nome')  
    else:
        produtos = Produto.objects.all().order_by('nome') 

    context = {
        'produtos':produtos,
        'user': request.user,
        'search_query': pesquisa
    }

    return render (request,'ecommerce/index.html',context)

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

    return render (request,'ecommerce/produtos.html',context)

def sobre(request):
    
    return render(request,'ecommerce/sobre.html')

@login_required
def carrinho(request):
    carrinho = Carrinho.objects.filter(cliente=request.user).first()
    itens = carrinho.itens.all() if carrinho else []
    subtotal = 0
    taxa = 0  
    frete = 0

    for item in itens:
        item.quantidade_opcoes = range(1, item.variacao.estoque + 1)
        item.preco = item.variacao.preco 
        item_total = item.preco * item.quantidade 
        subtotal += item_total  
    
    total = subtotal + taxa + frete  

    context = {
        'itens': itens,
        'subtotal': subtotal,
        'taxa': taxa,
        'frete': frete,
        'total': total
    }

    return render(request, 'ecommerce/carrinho.html', context)

   
@login_required
def adicionar_carrinho(request, variacao_id):
    if request.method == "POST":
        variacao_id = request.POST.get('variacao_id')
        variacao = get_object_or_404(VariacaoProduto, id=variacao_id)
        carrinho, created = Carrinho.objects.get_or_create(cliente=request.user)

        item_carrinho, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            variacao=variacao,
            defaults={'quantidade': 1}
        )

        if not created:
            item_carrinho.quantidade += 1
            item_carrinho.save()

    return redirect('carrinho')

@login_required
def remover_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__cliente=request.user)
    item.delete()

    return redirect('carrinho')


def experimento(request):
    
    return render (
        request,
        'ecommerce/experimento.html'
    )


def registro(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = ClienteCreationForm()
    
    return render(request,'ecommerce/registro.html',{'form':form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'ecommerce/login.html', {'error':'Usuário ou senha inválidos.'})

    return render (
        request,
        'ecommerce/login.html'
    )

def logout_usuario(request):
    logout(request)
    return redirect('home')


@login_required
def perfil_usuario(request):
    user = request.user
    endereco = EnderecoEntrega.objects.filter(cliente=user).first()

    if request.method == "POST":
        perfil_form = ClienteChangeForm(request.POST, instance=user)
        endereco_form = EnderecoForm(request.POST, instance=endereco)

        if perfil_form.is_valid() and endereco_form.is_valid():
            perfil_form.save()
            endereco = endereco_form.save(commit=False) 
            endereco.cliente = user  
            endereco.save()  
            return redirect("perfil_usuario")

    else:
        perfil_form = ClienteChangeForm(instance=user)
        endereco_form = EnderecoForm(instance=endereco)
        

    return render(request,'ecommerce/perfil.html',{'form':perfil_form,'endereco_form':endereco_form})

@login_required
def criar_endereco(request):
    if request.method == "POST":
        endereco_form = EnderecoForm(request.POST)
        if endereco_form.is_valid():
            endereco = endereco_form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            return redirect("perfil")
    else:
        endereco_form = EnderecoForm()

    return render(request, "cadastro_endereco.html", {"endereco_form": endereco_form})


def admin_checado(user):
    return user.is_staff

@user_passes_test(admin_checado)
def dashboard(request):
    produtos_lista = Produto.objects.all().order_by('nome')
    clientes_lista = Cliente.objects.all().order_by('nome_completo')

    paginator_produtos = Paginator(produtos_lista, 4)
    page_produtos = request.GET.get('page_produtos', 1)
    try :
        produtos = paginator_produtos.page(page_produtos)
    except :
        produtos = paginator_produtos.page(1)

    paginator_clientes = Paginator(clientes_lista, 4)
    page_clientes = request.GET.get('page_clientes',1)
    try :
        clientes = paginator_clientes.page(page_clientes)
    except :
        clientes = paginator_clientes.page(1)

    if request.method == "POST" and "delete_cliente" in request.POST:
        cliente_id = request.POST.get("delete_cliente")
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()
        messages.success(request, f"Usuário '{cliente.nome_completo}' foi excluído com sucesso.")
        return redirect("dashboard")

    context = {
        'produtos':produtos,
        'clientes':clientes,
        
    }

    return render(request, 'ecommerce/dashboard.html', context)

@user_passes_test(admin_checado)
def cadastrar_produto(request):
    if request.method == 'POST':
        print(request.FILES)
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors)
        
    else:
        form = ProdutoForm()
    
    return render(request,'ecommerce/cadastro_produto.html',{'form':form})

@user_passes_test(admin_checado)
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'ecommerce/edicao_produto.html',{'form':form,'produto':produto})

@user_passes_test(admin_checado)
def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        return redirect('dashboard')
    
    return render (request,'ecommerce/dashboard.html',{'produto':produto})

