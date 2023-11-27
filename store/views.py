
# from typing import Collection
from django.db.models import Value,Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from store.filters import ProductFilter
from store.pagination import DefaultPagination
from .models import Product,OrderItem,Collection,Review
from .serializers import CollectionSerializer, ProductSerializer,ReviewSerializer

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title','description']
    Ordering_fields = ['unit_price','last_updated']
    

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() >0:
            return Response({'error':'Product cannot be deleted because it is  associated with order item'}
                            ,status=status.HTTP_405_METHOD_NOT_ALLOWED)                           
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request,pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collections.products.count() > 0:  # type: ignore
            return Response({'error':'Collection cannot be deleted becauseit is  associated with product'}
                            ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return  Review.objects.filter(product_id= self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk'],}
        

    
    
