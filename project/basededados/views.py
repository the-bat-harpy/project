from django.http import JsonResponse
from .models import Produto

from django.http import JsonResponse
from .models import Produto, Tipo

def get_products_by_tipo(request, tipo_id):
    # Filtra os produtos pelo tipo_id passado como argumento
    produtos = Produto.objects.filter(tipo_id=tipo_id)

    # Serializa os produtos para uma lista de dicionários
    produtos_data = []
    for produto in produtos:
        # Acessa a imagem frontal (frontImg_url)
        front_image_url = produto.imagens.frontImg_url if produto.imagens else None

        produtos_data.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.price),  # Converte o preço para string
            'tipo': produto.tipo.description if produto.tipo else None,  # Tipo do produto
            'imagens': {
                'frontImg_url': front_image_url  # A URL da imagem frontal
            }
        })

    # Retorna os dados no formato JSON
    return JsonResponse(produtos_data, safe=False)

def tipo_produto_descricao(request, tipo_id):
    try:
        tipo = Tipo.objects.get(id=tipo_id)
        return JsonResponse({'description': tipo.description})
    except Tipo.DoesNotExist:
        return JsonResponse({'error': 'Tipo não encontrado'}, status=404)