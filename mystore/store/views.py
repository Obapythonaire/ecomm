# from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# from rest_framework.mixins import ListModelMixin, CreateModelMixin 
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .models import Product, Collection, OrderItem, Review, CartItem, Cart, Customer, Order
from store.serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
# from rest_framework import status
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly

# Create your views here.

# Now viewset will be used to make our app more RESTful
class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.select_related('collection').all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    permission_classes = [IsAdminOrReadOnly]
    # pagination_class = PageNumberPagination

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error': 'Products can not be deleted because it is associated with an order item'})
        return super().destroy(request, *args, **kwargs)


# Using Generic views
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
# Using CBV
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('ok')

# Using FBV
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif  request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('ok')

# Using Generic views
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count()>0:
#             return Response({'error': 'Products can not be deleted because it is associated with an order item'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Using CBV
# class ProductDetail(APIView):
    
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def post(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count()>0:
#             return Response({'error': 'Products can not be deleted because it is associated with an order item'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# Using FBV
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method =='GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         if product.orderitems.count()>0:
#             return Response({'error': 'Products can not be deleted because it is associated with an order item'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# Using ViewSet
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
            return Response({'error': 'Products can not be deleted because it is associated with a product item'})
        return super().destroy(request, *args, **kwargs)

# Using Generic views
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}
# Using CBV
# class CollectionList(APIView):
#     def get(self, request):
#         queryset = Collection.objects.all()
#         serializer = CollectionSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# @api_view(['GET', 'POST'])
# def collection_list(request) :
    # if request.method == 'GET':
    #     queryset = Collection.objects.all()
    #     serializer = CollectionSerializer(
    #         queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

# Using Generic Views
# class CollectionDetail(RetrieveUpdateDestroyAPIView): 
#     queryset = Collection
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.productitems.count()>0:
#             return Response({'error': 'Products can not be deleted because it is associated with a product item'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Using CBV
# class CollectionDetail(APIView):
#     def get(self, request, id):
#         collection = get_object_or_404(Collection, pk=id)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)

#     def put(self, request, id):
#         collection = get_object_or_404(Collection, pk=id)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, request, id):
#         collection = get_object_or_404(Collection, pk=id)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Using FBV
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection, pk=id)
#     if request.method =='GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewsViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CartItemViewSet(ModelViewSet):
    #  queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['pk'])

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if CartItem.objects.filter(items_id=kwargs['pk']).count()>0:
            return Response({'error': 'Cart can not be deleted because it is not empty'})
        return super().destroy(request, *args, **kwargs)
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated]) 
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data= request.data,
            context= {'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
      