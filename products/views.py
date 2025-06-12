from rest_framework import generics, permissions
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_vendor()

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsVendor()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor]
    
    def perform_update(self, serializer):
        if serializer.instance.vendor != self.request.user:
            raise permissions.exceptions.PermissionDenied("You don't own this product")
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]