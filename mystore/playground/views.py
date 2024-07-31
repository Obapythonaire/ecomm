from django.shortcuts import render
from django.http import HttpResponse
from store.models import *
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg

# def calculate():
#     x = 1
#     y = 2
#     return x


def say_hello(request):
    # x = calculate()
    # queryset = Product.objects.filter(title__icontains='Coffee' & 'Tea')
    # Any of the following can be used  to get inventory less than 10 and unit price lt 20
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)

    # You can also use the Q module to filter objects the (~) is for NOT
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) &
    #     ~Q(unit_price__lt=20)
    #     )
    
    # Also F objects can be used to query fields eg filtering where inventory = price
    # queryset = Product.objects.filter(inventory=F('unit_price'))

    # Sorting of queries
    # queryset = Product.objects.order_by('title', 'unit_price')[:30]


    # Values/valueslist are used in getting only selected parts of a model and not all column of the model

    # Exercise: Get/Query all products that are ordered and arrage them by title.
    # First go to the OrderItem model and get all product_id, remove the duplicates winth distinct function
    # products = OrderItem.objects.values('product_id').distinct()
    # Next pass in the ids gotten into Product model to get all prodects associted with the ids
    # Lastly, order with the title in ascending order as requeted
    # queryset = Product.objects.filter(id__in=products).order_by('title')

    # Deferring can be used but with carefulness so as not endup with uninteded behaviour
    # queryset = Product.objects.only('title') #This end up getting 3000+ queries which is not intended
    # queryset = Product.objects.defer('description')[:50]

    # Selecting objects
    # For instance querying Products model with related name collection and title will be wrong to do 
    # product.collection.title in the html its better gotten by
    # queryset = Product.objects.select_related('collection').all()
    # Note: select_related=1 (ForeignKey)
    # prefetch_related = n (ManyToManyField)

    # Exercise:Write a query to get the last 5 orders with their customers and items (incl. product)
    # Solution
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # queryset1 = OrderItem.objects.select_related('product')
    # queryset2 = OrderItem.objects.values('order_id').distinct()

    # Aggregate
    # result = Product.objects.filter(collection__id=1).aggregate(
    #     count=Count('id'), minimum_price=Min('unit_price'),
    #     maximum_price=Max('unit_price'),
    #     maverage_price=Avg('unit_price'))
    
    # Annotate: This is used to add additional attributes to object when querying them
    # from django.db.models import Value, F
    # queryset = Customer.objects.annotate(is_new=Value(True), new_id=F('id')+1)[:50]

    # Calling a database functions, this is used to call functions which can perform operations like CONCAT
    # from django.db.models import Value, F, Func

    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name= Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    #     )[:50]
    # Also, this can be used
    # from django.db.models import Value, F, Func
    # from django.db.models.functions import Concat
    # queryset = Customer.objects.annotate(
    # # CONCAT
    # full_name= Concat('last_name', Value(' '), 'first_name'))[:50]

    # Grouping Orders, this is to see how many orders each customer has made
    # from django.db.models import Value, F, Func, Count
    # queryset = Customer.objects.annotate(orders_count= Count('order'))[:50]

    # ExpressionWrapper: This used when annotating complex/big ....
    # from django.db.models import Value, F, Func, ExpressionWrapper, DecimalField
    # discounted_price = ExpressionWrapper(F('unit_price') *0.8, output_field=DecimalField())

    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price)[:50]

    # Querying generic relationship with content type
    from django.contrib.contenttypes.models import ContentType
    from tags.models import TaggedItem

    content_type = ContentType.objects.get_for_model(Product)

    queryset = TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=1
            )

    # Creating items, there are two approachs
    # Method 1, longer but best as intellisense automatically update rename field in models
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # collection.id
    # # method 2
    # collection = Collection.objects.create(title='a', featured_product_id=1)
    # collection.id

    # To update data, its better by using the update method
    # Collection.objects.filter(pk=11).update(featured_product=None)

    # To delete Objects
    collection = Collection(pk=1)
    collection.delete()
    # To delete multiple objects eg all collections with id more than 5
    Collection.objects.filter(id__gt=5).delete()

    # Transaction: This is used to only save if the whole code block is executed else, it will be
    # rolled back
    from django.db import transaction
    # The whole function can be wrapped in a transaction or some part of the function
    # For the whole function use; @transaction.atomic at the top of the function or

    with transaction.atomic():
        order = Order()
        order.customer_id =1 
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 1
        item.save()

    context = {
        'queryset': list(queryset),
        'name': 'Mosh',
        # 'result': result,
    }
    return render(request, 'hello.html',  context)
