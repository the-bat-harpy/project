from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morada = models.CharField(max_length=200)
    num_tel = models.CharField(max_length=12)
    cartao = models.CharField(max_length=16)
    data_nasc = models.DateField()

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

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    quantidade = models.IntegerField()
    imagens = models.OneToOneField(Imagens, on_delete=models.SET_NULL, null=True)
    tamanhos = models.ManyToManyField(Tamanho)
    cores = models.ManyToManyField(Cor)

class Estado(models.Model):
    description = models.CharField(max_length=200)

class Encomenda(models.Model):
    morada_entrega = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto)

class Wishlist(models.Model):
    produtos = models.ManyToManyField(Produto)
from django.db import models

# Create your models here.
