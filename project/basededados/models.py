from django.db import models
from django.contrib.auth.models import User


class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_tel = models.CharField(max_length=12)

class Imagens(models.Model):
    frontImg_url = models.CharField(max_length=200)
    backImg_url = models.CharField(max_length=200)

class Tamanho(models.Model):
    description = models.CharField(max_length=200)

class Cor(models.Model):
    description = models.CharField(max_length=200)
    code=models.CharField(max_length=200,null=True, blank=True)

class Tipo(models.Model):
    description = models.CharField(max_length=200)

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    quantidade = models.IntegerField()
    imagens = models.OneToOneField(Imagens, on_delete=models.SET_NULL, null=True)
    tamanhos = models.ManyToManyField(Tamanho)
    cores = models.ManyToManyField(Cor)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True)


class Estado(models.Model):
    description = models.CharField(max_length=200)

class Wishlist(models.Model):
    produtos = models.ManyToManyField(Produto)

class Cesto(models.Model):
    produtos = models.ManyToManyField(Produto)

class ProdutoNoCesto(models.Model):
    cesto = models.ForeignKey('Cesto', on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.SET_NULL, null=True, blank=True)
    cor = models.ForeignKey(Cor, on_delete=models.SET_NULL, null=True, blank=True)

    def subtotal(self):
        return self.quantidade * self.produto.price


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    morada = models.CharField(max_length=200, null=True, blank=True)
    num_tel = models.CharField(max_length=12, null=True, blank=True)
    cartao = models.CharField(max_length=16, null=True, blank=True)
    data_nasc = models.DateField(null=True, blank=True)
    wl = models.OneToOneField(Wishlist, on_delete=models.CASCADE, null=True, blank=True)
    cesto = models.OneToOneField(Cesto, on_delete=models.CASCADE, null=True, blank=True)


class Encomenda(models.Model):
    morada_entrega = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto)
    cartao_numero = models.CharField(max_length=16, null=True, blank=True)

# Create your models here.
