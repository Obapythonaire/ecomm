from django.urls import path
from django.urls.conf import include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
# router.register('collections', views.CollectionViewSet)


products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('reviews', views.ReviewsViewSet, basename='product-reviews')

carts_routers = routers.NestedDefaultRouter(router, 'carts', lookup='cart_pk')
carts_routers.register('items', views.CartItemViewSet, basename='cart-items')
# URLConf
urlpatterns = router.urls + products_routers.urls + carts_routers.urls

# urlpatterns = [
#     # path("products", views.product_list, name="products"),
#     # path("products/<int:id>/", views.product_detail, name="product_detail"),
#     # path("collections", views.collection_list, name="collections"),
#     # path("collections/<int:id>/", views.collection_detail, name="collection_detail"),
#     path("products", views.ProductList.as_view(), name="products"),
#     path("products/<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
#     path("collections", views.CollectionList.as_view(), name="collections"),
#     path("collections/<int:pk>/", views.CollectionDetail.as_view(), name="collection_detail"),
# ]