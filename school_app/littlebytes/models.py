import uuid
# from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return '{} ({})'.format(self.name, self.unit)

class Sandwich(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    ingredients = models.ManyToManyField(Ingredient, through='SandwichRecipe')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sandwiches"
   
class Box(models.Model):
    barcode = models.CharField(primary_key=True, max_length=12)
    contents = models.ManyToManyField(Sandwich, through='BoxContents')
    
    def __str__(self):
        return self.barcode
    
    class Meta:
        verbose_name_plural = "Boxes"
   
class BoxContents(models.Model):
    box = models.ForeignKey('Box', on_delete=models.PROTECT)
    sandwich = models.ForeignKey('Sandwich', on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.box, self.sandwich)

    class Meta:
        verbose_name_plural = "Box Contents"
   
class SandwichRecipe(models.Model):
    sandwich = models.ForeignKey('Sandwich', on_delete=models.PROTECT)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.PROTECT)
    ingredient_amount = models.FloatField()
    
    def __str__(self):
        return '{} - {}'.format(self.sandwich, self.ingredient)

    class Meta:
        verbose_name_plural = "Sandwich Recipes"

class Store(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    tax = models.DecimalField(max_digits=10, decimal_places=3)
    location = models.CharField(max_length=500)
    ingredients = models.ManyToManyField(Ingredient, through='Inventory')

    def __str__(self):
        return '{} - {}'.format(self.id, self.location)

class Inventory(models.Model):
    name = models.ForeignKey('Ingredient', on_delete=models.PROTECT)
    store = models.ForeignKey('Store', on_delete=models.PROTECT)
    #need a validator for postive values for both stock and cost_per_unit
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    date_exp = models.DateTimeField()
    date_enter = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.store.id, self.name)
   
    class Meta:
        verbose_name_plural = "Inventories"

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uniqe ID
    box = models.ForeignKey('Box', on_delete=models.PROTECT)
    store = models.ForeignKey('Store', on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    transaction_type = models.CharField(max_length=1) #c for catering, w for walk-in
    gross = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return '{} - {}'.format(self.store, self.id)
