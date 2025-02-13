from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . serializers import CategorySerializer, ProductImageSerializer, ProductSerializer
from . models import Category, Product


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all categories.
    POST: Create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a category.
    PUT/PATCH: Update a category.
    DELETE: Delete a category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# --- Products ---
class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: List all products along with aggregate statistics.
    POST: Create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        # Get the standard list response.
        response = super().list(request, *args, **kwargs)
        # Calculate aggregates.
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        # Return combined response.
        return Response({
            "total_products": total_products,
            "total_categories": total_categories,
            "products": response.data
        })

    def perform_create(self, serializer):
        # Save the product instance.
        product = serializer.save()

        # Ensure that base_price is set (default to 0.00 if missing)
        if product.base_price is None:
            product.base_price = 0.00
            product.save(update_fields=['base_price'])

        # Send a notification email to the admin upon product creation.
        subject = "New Product Created"
        message = (
            f"A new product '{product.name}' has been created in the category '{product.category}'.\n\n"
            f"Description: {product.description}\n"
            f"Base Price: {product.base_price}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        # Update category analytics: update product_count field.
        # Assumes Category model has a 'product_count' field.
        category = product.category
        category.product_count = category.products.count()
        category.save(update_fields=['product_count'])

        return product


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single product.
    PUT/PATCH: Update a product.
    DELETE: Delete a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
