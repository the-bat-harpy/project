import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .models import Produto, Cliente, Tamanho, Cor, ProdutoNoCesto, Cesto, Tipo, Encomenda, Imagens


def get_products_by_tipo(request, tipo_id):
    produtos = Produto.objects.filter(tipo_id=tipo_id)

    produtos_data = []
    for produto in produtos:
        front_image_url = produto.imagens.frontImg_url if produto.imagens else None

        produtos_data.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.price),
            'tipo': produto.tipo.description if produto.tipo else None,
            'imagens': {
                'frontImg_url': front_image_url
            }
        })
    return JsonResponse(produtos_data, safe=False)


def tipo_produto_descricao(request, tipo_id):
    try:
        tipo = Tipo.objects.get(id=tipo_id)
        return JsonResponse({'description': tipo.description})
    except Tipo.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)


def produtos_no_cesto(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

    try:
        cliente = Cliente.objects.get(user=user)
        cesto = cliente.cesto
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    except AttributeError:
        return JsonResponse({'error': 'Cesto não encontrado'}, status=404)

    produtos_data = []

    for item in cesto.itens.all():
        produto = item.produto
        imagem_url = produto.imagens.frontImg_url if produto.imagens else None

        produtos_data.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.price),
            'quantidade': item.quantidade,
            'tamanho': item.tamanho.description if item.tamanho else None,
            'cor': item.cor.description if item.cor else None,
            'imagem': imagem_url,
        })

    return JsonResponse(produtos_data, safe=False)


def wishlist_view(request):
    try:
        user = request.user
        cliente = Cliente.objects.get(user=user)
        wishlist = cliente.wl

        if not wishlist:
            return JsonResponse([], safe=False)

        produtos = wishlist.produtos.all()

        produtos_data = []
        for produto in produtos:
            front_image_url = produto.imagens.frontImg_url if produto.imagens else None

            produtos_data.append({
                'id': produto.id,
                'nome': produto.nome,
                'preco': str(produto.price),
                'imagens': {
                    'frontImg_url': front_image_url
                }
            })

        return JsonResponse(produtos_data, safe=False)

    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)


def produto_detalhes_view(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)

        front_image_url = produto.imagens.frontImg_url if produto.imagens else None
        back_image_url = produto.imagens.backImg_url if produto.imagens else None

        tamanhos_qs = produto.tamanhos.all()
        tamanhos = [t.description for t in tamanhos_qs] if tamanhos_qs.exists() else ["sem tamanhos disponíveis"]

        cores_qs = produto.cores.all()
        cores = [{'description': c.description, 'code': c.code} for c in cores_qs]

        produto_data = {
            'id': produto.id,
            'nome': produto.nome,
            'price': str(produto.price),
            'description': produto.description if produto.description else 'Sem descrição disponível',
            'frontImageUrl': front_image_url,
            'backImageUrl': back_image_url,
            'tamanhos': tamanhos,
            'cores': cores,
            'ref': produto.id,
        }
        return JsonResponse(produto_data)

    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)


@require_http_methods(["POST"])
def adicionar_ao_cesto(request):
    try:
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        tamanho_desc = data.get('tamanho')
        cor_desc = data.get('cor')

        cliente = Cliente.objects.get(user=request.user)

        cesto = getattr(cliente, 'cesto', None)
        if not cesto:
            cesto = Cesto.objects.create()
            cliente.cesto = cesto
            cliente.save()

        produto = Produto.objects.get(id=produto_id)
        tamanho = Tamanho.objects.get(description=tamanho_desc)
        cor = Cor.objects.get(description=cor_desc)

        item, criado = ProdutoNoCesto.objects.get_or_create(
            cesto=cesto,
            produto=produto,
            tamanho=tamanho,
            cor=cor,
            defaults={'quantidade': 1}
        )
        if not criado:
            item.quantidade += 1
            item.save()

        return JsonResponse({'success': 'Produto adicionado ao cesto'})

    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    except Tamanho.DoesNotExist:
        return JsonResponse({'error': 'Tamanho inválido'}, status=404)
    except Cor.DoesNotExist:
        return JsonResponse({'error': 'Cor inválida'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["PUT"])
def update_profile_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

    user = request.user

    try:
        cliente = Cliente.objects.get(user=user)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    allowed_fields = ['username', 'telemovel', 'email', 'password', 'dataNascimento', 'cartao', 'morada']

    for field in allowed_fields:
        if field in data:
            if field == 'password':
                user.set_password(data[field])
                user.save()
            elif field == 'username':
                user.username = data[field]
                user.save()
            else:
                setattr(cliente, field, data[field])

    cliente.save()

    return JsonResponse({'success': 'Perfil atualizado com sucesso'})

def encomendas_view(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

    encomendas = Encomenda.objects.filter(cliente=cliente).select_related('estado').prefetch_related('produtos__imagens')

    data = []
    for encomenda in encomendas:
        produtos = []
        for produto in encomenda.produtos.all():
            imagem_url = produto.imagens.frontImg_url if produto.imagens else None
            produtos.append(imagem_url)

        data.append({
            'id': encomenda.id,
            'estado': encomenda.estado.description,
            'total': f"{encomenda.valor:.2f}€",
            'produtos': produtos
        })

    return JsonResponse({
        'username': request.user.username,
        'encomendas': data
    })

def finalizar_compra_view(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

    try:
        cliente = Cliente.objects.get(user=user)
        cesto = cliente.cesto
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    except AttributeError:
        return JsonResponse({'error': 'Cesto não encontrado'}, status=404)

    cliente_data = {
        'nome': user.username,
        'telefone': cliente.telemovel,
        'morada': cliente.morada,
    }

    produtos = []
    for item in cesto.itens.all():
        produto = item.produto
        imagem_url = produto.imagens.frontImg_url if produto.imagens else None
        produtos.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.price),
            'quantidade': item.quantidade,
            'tamanho': item.tamanho.description if item.tamanho else None,
            'cor': item.cor.description if item.cor else None,
            'imagem': imagem_url,
        })

    return JsonResponse({
        'cliente': cliente_data,
        'produtos': produtos,
    })

@require_http_methods(["PUT"])
def editar_encomenda_view(request, encomenda_id):
    user = request.user

    try:
        encomenda = Encomenda.objects.get(id=encomenda_id, cliente__user=user)
    except Encomenda.DoesNotExist:
        return JsonResponse({'error': 'Encomenda não encontrada'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    morada_entrega = data.get('morada_entrega')
    cartao_numero = data.get('cartao_numero')

    if morada_entrega is not None:
        encomenda.morada_entrega = morada_entrega
    if cartao_numero is not None:
        encomenda.cartao_numero = cartao_numero

    encomenda.save()

    return JsonResponse({'success': 'Encomenda atualizada com sucesso'})

@api_view(['GET'])
def pesquisar_produtos(request):
    termo = request.GET.get('termo', '')
    produtos = Produto.objects.filter(nome__icontains=termo)

    produtos_data = []
    for produto in produtos:
        front_image_url = produto.imagens.frontImg_url if produto.imagens else None

        produtos_data.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.price),
            'tipo': produto.tipo.description if produto.tipo else None,
            'imagens': {
                'frontImg_url': front_image_url
            }
        })

    return JsonResponse(produtos_data, safe=False)


def listar_tipos(request):
    tipos = Tipo.objects.all().values('id', 'description')
    tipos_list = list(tipos)
    return JsonResponse(tipos_list, safe=False)

@csrf_exempt
def adicionar_produto(request):
    print(request.data)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('price')
        descricao = request.POST.get('description')
        quantidade = request.POST.get('quantidade', 0)
        tipo_id = request.POST.get('categoria')

        frontImg = request.FILES.get('frontImg')
        backImg = request.FILES.get('backImg')

        if not all([nome, preco, descricao, tipo_id, frontImg, backImg]):
            return JsonResponse({'error': 'Faltam campos obrigatórios'}, status=400)

        tipo = get_object_or_404(Tipo, id=tipo_id)

        imagens = Imagens.objects.create(frontImg=frontImg, backImg=backImg)

        produto = Produto.objects.create(
            nome=nome,
            price=preco,
            description=descricao,
            quantidade=quantidade,
            tipo=tipo,
            imagens=imagens,
        )

        return JsonResponse({'status': 'Produto criado com sucesso', 'produto_id': produto.id})

    return JsonResponse({'error': 'Método não permitido'}, status=405)