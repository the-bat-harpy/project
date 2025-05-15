import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

from .models import Produto, Cliente, Tamanho, Cor, ProdutoNoCesto, Cesto, Tipo


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
