from django.conf import settings
from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # product_set = 
class Collection(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)
    # If the sku field is involved, Django will automaticallytake it as our primary id
    # and not create an id for us automatically
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators = [MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='productitems')
    # In a situation where the collection model can't be defined before the prodect, 
    # it can be stringified by 'Collection', models.PROTECT is also used so that when the collection 
    # is accidentally deleted, all products associated are not deleted.
    promotion = models.ManyToManyField(Promotion, blank=True)
    # ManyToManyField is used because a promotion can be applied to many products
    # and vice versa

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
    ] 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_GOLD)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    # The memebership_status field is made text choice for customers different memebership category, 
    # however, it's defined in the manner it is because of future editing of the default membership_status,
    # it will have to be edited in the two places it was used if not defined in the mannner it is now defined. 

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETE = 'C'
    STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (STATUS_PENDING, 'PENDING'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel Order')
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField() #This is to get small numbers that are not negative
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=6)
    customer = models.ForeignKey(Customer, 
                                 on_delete=models.CASCADE)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    # The customer field is linked to the Customer Model(Parent), because every customer will
    # have an address, the on_delete is set to CASCADE so as to delete the address attached
    # to a customer once a customer is deleted, the primary_key is True so as to prevent django from 
    # creating another id. It also a OneToOneField becaues every customer will only one address

    # NB: If a customer is to have multiple addresses e.g Local and Foreign address, we will be using a ForeignKey
    # instead of OneToOneField and the primary_key argument won't be needed.
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]

class Review(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    date = models.DateField(auto_now_add = True)

