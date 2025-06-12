from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name','quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal','product_name']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price
    
    def get_product_name(self, obj):
        return obj.product.name
    
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    


    class Meta:
        model = Order
        fields = ['id', 'customer', 'vendor', 'status', 'payment_method',
                  'total_amount', 'shipping_address', 'created_at', 'items']
        read_only_fields = ['customer', 'vendor', 'total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context.get('request')
        customer = request.user

        # Get vendor from first product (assuming all products are from same vendor)
        first_product = items_data[0]['product']
        vendor = first_product.vendor

        # Remove customer/vendor from validated_data if already included to avoid duplication
        validated_data.pop('customer', None)
        validated_data.pop('vendor', None)

        order = Order.objects.create(
            customer=customer,
            vendor=vendor,
            total_amount=0,  # temporary value
            **validated_data
        )

        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price
            subtotal = price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total += subtotal

        order.total_amount = total
        order.save()

        return order
