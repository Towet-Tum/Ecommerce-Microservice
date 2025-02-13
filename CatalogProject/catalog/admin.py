from django.contrib import admin
from .models import (
    Category, Product, OptionType, OptionValue, ProductVariant, VariantOption,
    ProductImage
)

# ---------------------------
# Inline Classes for Related Models
# ---------------------------

class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True  # Enables navigation to the variant detail
    # Include inline for variant options in the variant admin
    inlines = [VariantOptionInline]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    ordering = ('name',)
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    list_display = ('option_type', 'value')
    list_filter = ('option_type',)
    search_fields = ('value',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'price', 'stock_quantity')
    search_fields = ('sku',)
    list_filter = ('product',)
    inlines = [VariantOptionInline]

@admin.register(VariantOption)
class VariantOptionAdmin(admin.ModelAdmin):
    list_display = ('variant', 'option_value')
    list_filter = ('variant', 'option_value')
