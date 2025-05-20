from django.contrib import admin
from django.urls import path
from . import view
from basededados import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth e user
    path("api/signup/", view.signup),
    path("api/login/", view.login_view),
    path("api/logout/", view.logout_view),
    path("api/user/", view.user_view),
    path("api/update-profile/", views.update_profile_view),
    # produtos
    path('api/produtos/<int:tipo_id>/', views.get_products_by_tipo),
    path('api/tipo-descricao/<int:tipo_id>/', views.tipo_produto_descricao),
    path('api/produtos/pesquisar', views.pesquisar_produtos),
    path('api/tipos/', views.listar_tipos),
    path('api/produtos/', views.adicionar_produto),
    path('api/produto/<int:produto_id>/', views.produto_detalhes_view),
    path('api/produtos/alterar-quantidade/', views.alterar_quantidade_produto, name='alterar_quantidade_produto'),
    # cesto
    path('api/cesto/', views.produtos_no_cesto),
    path('api/cesto/adicionar/', views.adicionar_ao_cesto, name='adicionar_ao_cesto'),
    path('cesto/<int:produto_id>/', views.remover_produto_cesto, name='remover-produto-cesto'),
    # wishlist
    path('api/wishlist/', views.wishlist_view),
    path('api/wishlist/add/', views.adicionar_wishlist, name='adicionar_w'
                                                             'ishlist'),
    path('api/wishlist/remove/', views.remover_da_wishlist, name='remover_da_wishlist'),
    # encomendas
    path('api/encomendas/', views.encomendas_view),
    path('api/sincronizar-encomenda/', views.sincronizar_encomenda, name='sincronizar_encomenda'),
    path('api/finalizar-compra/', views.finalizar_compra_view),
    path('api/encomenda/', views.criar_ou_editar_encomenda_view, name='criar_ou_editar_encomenda'),
    path('api/encomendas/<int:encomenda_id>/', views.editar_encomenda_por_id_view, name='editar_encomenda_por_id'),
    path('api/encomendas/<int:encomenda_id>/alterar_estado/', views.alterar_estado_encomenda,name='alterar_estado_encomenda'),

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
