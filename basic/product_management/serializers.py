# myapp/serializers.py
from rest_framework import serializers
from .models import Product, Purchase

class ProductCreationSerializer(serializers.Serializer):
    product_name = serializers.CharField( error_messages={
            "required":"E40011"
        })
    quantity = serializers.IntegerField()


   


    def validate(self, data):
       
        product_name = data["product_name"]
        quantity = data["quantity"]

        if not product_name:
            raise serializers.ValidationError("Product name is required")
        if not quantity:
            raise serializers.ValidationError("product quantity is required")
        return data
        
    def validate_quantity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be an integer")
        if value < 1 or value > 100:
            raise serializers.ValidationError("Quantity must be between 1 and 100.")
        return value
            

        

        

      
   


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity']

    def validate_quantity(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError("Quantity must be between 1 and 100.")
        return value

class PurchaseSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name')
    class Meta:
        model = Purchase
        fields = ['id', 'product', 'quantity', 'product_name']
