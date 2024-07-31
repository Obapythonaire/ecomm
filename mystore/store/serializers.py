from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.StringRelatedField()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.SerializerMethodField(method_name='total_products')

    def total_products(self, collection: Collection):
        return collection.productitems.count()
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id',  'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'quantity', 'total_price'] 


class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_car_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No Cart with the given ID')
        if Cart.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id

    def save(self, **kwargs):
        # print(self.validated_data['cart_id'])
        # print(self.context['user_id'])
        with transaction.atomic:

            cart_id = self.validated_data['cart_id']
            (customer, created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            order =  Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                                .select_related('product') \
                                .filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order
