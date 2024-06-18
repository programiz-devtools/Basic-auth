# myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Product, Purchase
from .serializers import ProductSerializer, PurchaseSerializer,ProductCreationSerializer
from rest_framework import serializers
from user_management.permission import IsCustomAuthenticated
from basic.authentication import CustomAuthentication
from product_management.pagination import CustomPagination
from rest_framework.authentication import SessionAuthentication
from user_management.permission import IsSessionAuthenticated
from django.db import transaction
from django.db.models import F
from django.utils.dateparse import parse_date
from decimal import Decimal
from datetime import date


def handle_validation_error(e):
   
    response={}
   
    try:
        error_message = str(e).split("ErrorDetail(string='")[1].split("'")[0]

        return Response(
                {"message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
     
           
    except Exception as e:
        return Response(
            
           {"message":"Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
 
        )


class ProductCreateView(generics.CreateAPIView):
    # permission_classes=[IsCustomAuthenticated]
    # authentication_classes=[CustomAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductCreationSerializer

    def create(self, request, *args, **kwargs):
      
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            product = Product.objects.create(name=serializer.validated_data["product_name"],quantity=serializer.validated_data["quantity"])
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            print(serializer.errors.get("qauntity"))
            return handle_validation_error(e)
            
        

      
       
class ProductListView(generics.ListAPIView):
    permission_classes=[IsCustomAuthenticated]
    authentication_classes=[CustomAuthentication]
    pagination_class=CustomPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.ListAPIView):
    permission_classes = [IsCustomAuthenticated]
    authentication_classes = [CustomAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        
        try:
            product = Product.objects.get(id=product_id)
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
class PurchaseCreateView(generics.CreateAPIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsSessionAuthenticated]
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)
                if product.quantity < quantity:
                    raise serializers.ValidationError("Not enough quantity available.")
                
                product.quantity = F('quantity') - quantity
                product.save()

                purchase = Purchase.objects.create(
                    product=product,
                    quantity=quantity,
                )
                return Response(PurchaseSerializer(purchase).data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
           

class PurchaseListView(generics.ListAPIView):
    permission_classes=[IsSessionAuthenticated]
    authentication_classes=[SessionAuthentication]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

