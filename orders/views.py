from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer
from accounts.models import User

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer()

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_vendor():
            return Order.objects.filter(vendor=user)
        return Order.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        if self.request.user.is_vendor():
            raise permissions.exceptions.PermissionDenied("Vendors cannot create orders")
        serializer.save(customer=self.request.user)

class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_vendor():
            return Order.objects.filter(vendor=user)
        return Order.objects.filter(customer=user)
    
    def perform_update(self, serializer):
        # Only allow vendors to update status
        if self.request.user.is_customer():
            raise permissions.exceptions.PermissionDenied("Customers can't update orders")
        serializer.save()