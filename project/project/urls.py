"""
URL configuration for project project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from . import view
from basededados import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/signup/", view.signup),
    path("api/login/", view.login_view),
    path("api/logout/", view.logout_view),
    path("api/user/", view.user_view),
    path('api/produtos/<int:tipo_id>/', views.get_products_by_tipo),
    path('api/tipo-descricao/<int:tipo_id>/', views.tipo_produto_descricao),
    path('api/cesto/', views.produtos_no_cesto),
    path('api/wishlist/',views.wishlist_view),
    path('api/produto/<int:produto_id>/', views.produto_detalhes_view),
    path('api/cesto/adicionar/', views.adicionar_ao_cesto),
    path('api/csrf-cookie/', view.csrf_token),
    path('api/update-profile/', views.update_profile_view),
    path('api/encomendas/', views.encomendas_view),
    path('api/finalizar-compra/', views.finalizar_compra_view),
    path('api/encomendas/<int:encomenda_id>/editar/', views.editar_encomenda_view),
    path('api/produtos/pesquisar', views.pesquisar_produtos),
    path('api/tipos/', views.listar_tipos),
    path('api/produtos/', views.adicionar_produto),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)