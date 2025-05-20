import json

import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

from .models import Produto, Cliente, Tamanho, Cor, ProdutoNoCesto, Cesto, Tipo, Encomenda, Imagens, Wishlist, Estado, ProdutoEncomenda

@api_view(['GET'])
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
            'quantidade': produto.quantidade,
            'imagens': {
                'frontImg_url': front_image_url
            }
        })
    return JsonResponse(produtos_data, safe=False)

@api_view(['GET'])
def tipo_produto_descricao(request, tipo_id):
    try:
        tipo = Tipo.objects.get(id=tipo_id)
        return JsonResponse({'description': tipo.description})
    except Tipo.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def produtos_no_cesto(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Utilizador não autenticado'}, status=401)

    try:
        cliente = Cliente.objects.get(user=user)
        if not cliente.cesto:
            cliente.cesto = Cesto.objects.create()
            cliente.save()
        cesto = cliente.cesto
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

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
            'imagens': {
                'frontImg_url': imagem_url
            }
        })

    return JsonResponse(produtos_data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def adicionar_ao_cesto(request):
    try:
        data = request.data
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
        tamanhos = Tamanho.objects.filter(description=tamanho_desc)
        if not tamanhos.exists():
            return JsonResponse({'error': 'Tamanho inválido'}, status=404)

        tamanho = tamanhos.first()

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
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Utilizador não autenticado'}, status=401)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def encomendas_view(request):
    user = request.user

    if user.is_superuser:
        encomendas = Encomenda.objects.all().select_related('estado').prefetch_related(
            'produtoencomenda_set__produto__imagens'
        )
    else:
        try:
            cliente = Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

        encomendas = Encomenda.objects.filter(cliente=cliente).select_related('estado').prefetch_related(
            'produtoencomenda_set__produto__imagens'
        )

    data = []
    for encomenda in encomendas:
        produtos = []
        for item in encomenda.produtoencomenda_set.all():
            produto = item.produto
            imagem_url = produto.imagens.frontImg_url if produto.imagens else None
            produtos.append({
                'id': produto.id,
                'nome': produto.nome,
                'preco_unitario': float(item.preco_unitario),
                'quantidade': item.quantidade,
                'tamanho': item.tamanho.description if item.tamanho else None,
                'cor': item.cor.description if item.cor else None,
                'imagem': imagem_url,
            })

        data.append({
            'id': encomenda.id,
            'estado': encomenda.estado.description,
            'total': float(encomenda.valor),
            'produtos': produtos
        })

    return JsonResponse({
        'username': user.username,
        'is_superuser': user.is_superuser,
        'encomendas': data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def finalizar_compra_view(request):
    user = request.user

    try:
        cliente = Cliente.objects.get(user=user)
        cesto = cliente.cesto
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)
    except AttributeError:
        return JsonResponse({'error': 'Cesto não encontrado'}, status=404)

    if not cesto.itens.exists():
        return JsonResponse({'error': 'Cesto vazio'}, status=400)

    encomenda = Encomenda.objects.filter(cliente=cliente, estado_id=1).first()

    if not encomenda:
        encomenda = Encomenda.objects.create(
            cliente=cliente,
            estado_id=1,
            valor=0,
            morada_entrega="",
            cartao_numero=None,
        )

        valor = 0.0
        for item in cesto.itens.all():
            produto = item.produto
            preco = float(produto.price)
            subtotal = preco * item.quantidade
            valor += subtotal

            produto.stock -= item.quantidade
            if produto.stock < 0:
                produto.stock = 0
            produto.save()

            ProdutoEncomenda.objects.create(
                encomenda=encomenda,
                produto=produto,
                quantidade=item.quantidade,
                tamanho=item.tamanho,
                cor=item.cor,
                preco_unitario=preco
            )

        encomenda.valor = valor
        encomenda.save()

        cesto.itens.all().delete()

    cliente_data = {
        'nome': user.username or '',
        'telefone': cliente.num_tel or '',
        'morada': cliente.morada or '',
        'cartao': cliente.cartao or '',
    }

    produtos = []
    for pe in encomenda.produtoencomenda_set.all():
        imagem_url = getattr(pe.produto.imagens, 'frontImg_url', None)
        produtos.append({
            'id': pe.produto.id,
            'nome': pe.produto.nome,
            'preco': f"{pe.preco_unitario:.2f}",
            'quantidade': pe.quantidade,
            'tamanho': pe.tamanho.description if pe.tamanho else None,
            'cor': pe.cor.description if pe.cor else None,
            'imagem': imagem_url,
        })

    return JsonResponse({
        'cliente': cliente_data,
        'produtos': produtos,
        'valor': round(encomenda.valor, 2),
        'encomenda_id': encomenda.id,
    })

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def criar_ou_editar_encomenda_view(request):
    user = request.user

    try:
        cliente = Cliente.objects.get(user=user)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    encomenda_id = data.get('encomenda_id')
    morada_entrega = data.get('morada_entrega')
    cartao_numero = data.get('cartao_numero')

    encomenda = None
    if encomenda_id:
        encomenda = Encomenda.objects.filter(id=encomenda_id, cliente=cliente).first()

    if not encomenda:
        encomenda = Encomenda(cliente=cliente)

    if morada_entrega is not None:
        encomenda.morada_entrega = morada_entrega

    if cartao_numero is not None:
        encomenda.cartao_numero = cartao_numero

    encomenda.save()

    return JsonResponse({
        'success': 'Encomenda criada/atualizada com sucesso',
        'encomenda_id': encomenda.id
    })

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def editar_encomenda_por_id_view(request, encomenda_id):

    user = request.user

    try:
        cliente = Cliente.objects.get(user=user)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

    try:
        encomenda = Encomenda.objects.get(id=encomenda_id, cliente=cliente)
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

    return JsonResponse({
        'success': 'Encomenda atualizada com sucesso',
        'encomenda_id': encomenda.id
    })

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

@api_view(['GET'])
def listar_tipos(request):
    tipos = Tipo.objects.all().values('id', 'description')
    tipos_list = list(tipos)
    return JsonResponse(tipos_list, safe=False)

@api_view(['POST'])
def adicionar_produto(request):

    nome = request.POST.get('nome')
    preco = request.POST.get('price')
    descricao = request.POST.get('description')
    tipo_id = request.POST.get('tipo')

    frontImg = request.FILES.get('frontImg')
    backImg = request.FILES.get('backImg')

    campos_faltando = []
    if not nome:
        campos_faltando.append('nome')
    if not preco:
        campos_faltando.append('preco')
    if not descricao:
        campos_faltando.append('descricao')
    if not tipo_id:
        campos_faltando.append('tipo')
    if not frontImg:
        campos_faltando.append('frontImg')
    if not backImg:
        campos_faltando.append('backImg')

    if campos_faltando:
        return JsonResponse({'error': f'Campos obrigatórios em falta: {", ".join(campos_faltando)}'}, status=400)

    tipo = get_object_or_404(Tipo, id=tipo_id)

    imagens = Imagens.objects.create(
        frontImg_url=frontImg,
        backImg_url=backImg,
    )

    produto = Produto.objects.create(
        nome=nome,
        price=preco,
        description=descricao,
        quantidade=0,
        tipo=tipo,
        imagens=imagens,
    )

    return JsonResponse({'status': 'Produto criado com sucesso', 'produto_id': produto.id})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remover_produto_cesto(request, produto_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
        cesto = cliente.cesto
        if not cesto:
            return Response({'error': 'Cesto não encontrado'}, status=404)

        item = cesto.itens.filter(produto__id=produto_id).first()
        if not item:
            return Response({'error': 'Produto não encontrado no cesto'}, status=404)

        cesto.itens.remove(item)


        return Response({'success': 'Produto removido do cesto'})

    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adicionar_wishlist(request):
    try:
        produto_id = request.data.get('produto_id')
        if not produto_id:
            return Response({"error": "Produto_id não fornecido"}, status=400)

        produto = Produto.objects.get(id=produto_id)
        cliente = Cliente.objects.get(user=request.user)

        if not cliente.wl:

            nova_wishlist = Wishlist.objects.create()
            cliente.wl = nova_wishlist
            cliente.save()

        cliente.wl.produtos.add(produto)
        cliente.wl.save()

        return Response({"success": "Produto adicionado à wishlist!"})

    except Produto.DoesNotExist:
        return Response({"error": "Produto não encontrado"}, status=404)

    except Cliente.DoesNotExist:
        return Response({"error": "Cliente não encontrado"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remover_da_wishlist(request):
    try:
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        produto = Produto.objects.get(id=produto_id)

        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.produtos.remove(produto)

        return JsonResponse({'mensagem': 'Produto removido da wishlist com sucesso!'})
    except Produto.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado.'}, status=404)
    except Wishlist.DoesNotExist:
        return JsonResponse({'erro': 'Wishlist não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def alterar_quantidade_produto(request):
    produto_id = request.data.get('produto_id')
    quantidade = request.data.get('quantidade')

    if produto_id is None or quantidade is None:
        return Response(
            {"error": "Os campos 'produto_id' e 'quantidade' são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quantidade_int = int(quantidade)
        if quantidade_int < 0:
            return Response(
                {"error": "A quantidade deve ser maior ou igual a zero."},
                status=status.HTTP_400_BAD_REQUEST
            )
    except ValueError:
        return Response(
            {"error": "A quantidade deve ser um número inteiro."},
            status=status.HTTP_400_BAD_REQUEST
        )

    produto = get_object_or_404(Produto, id=produto_id)
    produto.quantidade = quantidade_int
    produto.save()

    return Response({
        "success": True,
        "produto_id": produto_id,
        "quantidade": quantidade_int
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def alterar_estado_encomenda(request, encomenda_id):
    user = request.user

    if not user.is_superuser:
        return JsonResponse({'error': 'Acesso negado'}, status=403)

    encomenda = get_object_or_404(Encomenda, id=encomenda_id)

    estado_atual = encomenda.estado
    proximo_estado_id = estado_atual.id + 1

    try:
        if proximo_estado_id <= 4:
            novo_estado = Estado.objects.get(id=proximo_estado_id)
            encomenda.estado = novo_estado
            encomenda.save()
            return JsonResponse({'success': True, 'novo_estado': novo_estado.description})
        else:
            return JsonResponse({'success': False, 'message': 'Estado já está no máximo'})
    except Estado.DoesNotExist:
        return JsonResponse({'error': 'Estado inválido'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def sincronizar_encomenda(request):
    user = request.user

    try:
        cliente = Cliente.objects.get(user=user)
    except Cliente.DoesNotExist:
        return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)

    if not cliente.cesto:
        return JsonResponse({'erro': 'Cesto não encontrado'}, status=404)

    cesto_itens = ProdutoNoCesto.objects.filter(cesto=cliente.cesto)

    if not cesto_itens.exists():
        return JsonResponse({'erro': 'Cesto vazio'}, status=400)

    estado_default = Estado.objects.first()
    encomenda, _ = Encomenda.objects.get_or_create(
        cliente=cliente,
        estado=estado_default,
    )

    ProdutoEncomenda.objects.filter(encomenda=encomenda).delete()

    total = 0
    produtos_response = []

    for item in cesto_itens:
        produto = item.produto

        if produto.quantidade < item.quantidade:
            return JsonResponse({
                'erro': f'Sem stock suficiente para o produto {produto.nome}'
            }, status=400)

        produto.quantidade -= item.quantidade
        produto.save()

        ProdutoEncomenda.objects.create(
            encomenda=encomenda,
            produto=produto,
            quantidade=item.quantidade,
            tamanho=item.tamanho,
            cor=item.cor,
            preco_unitario=produto.price
        )

        subtotal = float(produto.price) * item.quantidade
        total += subtotal

        produtos_response.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': float(produto.price),
            'quantidade': item.quantidade,
            'tamanho': item.tamanho.description if item.tamanho else None,
            'cor': item.cor.description if item.cor else None,
            'imagem': produto.imagens.frontImg_url if produto.imagens else "",
        })

    encomenda.valor = total
    encomenda.morada_entrega = cliente.morada or ''
    encomenda.cartao_numero = cliente.cartao or ''
    encomenda.save()

    cesto_itens.delete()

    return JsonResponse({
        'encomenda_id': encomenda.id,
        'valor': total,
        'produtos': produtos_response,
        'cliente': {
            'nome': cliente.user.first_name,
            'morada': cliente.morada,
            'telefone': cliente.num_tel,
            'cartao': cliente.cartao,
        }
    })