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
    path('api/tipo-descricao/<int:tipo_id>/', views.tipo_produto_descricao, name='tipo_produto_descricao'),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)