from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.StringRelatedField(read_only= True)
    category = serializers.StringRelatedField(read_only= True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['vendor', 'created_at']
    
    def validate(self, data):
        if self.context['request'].user.is_customer():
            raise serializers.ValidationError("Only vendors can manage products")
        return data