from rest_framework import serializers
from . models import Category, Product, OptionType, VariantOption, OptionValue, ProductVariant, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'name': {'error_messages': {'blank': "Category name is required."}}
        }

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'category_id', 'name', 'description', 'base_price']
    
    def validate_base_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Base price cannot be negative.")
        return value
    
class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'product_id', 'url', 'alt_text', 'is_primary']


class OptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionType
        fields = '__all__'

class OptionValueSerializer(serializers.ModelSerializer):
    option_type = OptionTypeSerializer(read_only=True)
    option_type_id = serializers.PrimaryKeyRelatedField(
        queryset=OptionType.objects.all(), source='option_type', write_only=True
    )
    
    class Meta:
        model = OptionValue
        fields = ['id', 'option_type', 'option_type_id', 'value']
        extra_kwargs = {
            'value': {'error_messages': {'blank': "Option value is required."}}
        }

class VariantOptionSerializer(serializers.ModelSerializer):
    # For write operations, we accept primary keys
    option_value = OptionValueSerializer(read_only=True)
    option_value_id = serializers.PrimaryKeyRelatedField(
        queryset=OptionValue.objects.all(), source='option_value', write_only=True
    )
    
    class Meta:
        model = VariantOption
        fields = ['id', 'variant', 'option_value', 'option_value_id']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=VariantOption.objects.all(),
                fields=('variant', 'option_value'),
                message="This option has already been assigned to the variant."
            )
        ]

class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    # Use a SerializerMethodField to nest variant options in read operations.
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_id', 'sku', 'price', 'stock_quantity', 'options']
    
    def get_options(self, obj):
        # Serialize related variant options.
        variant_options = obj.options.all()
        return VariantOptionSerializer(variant_options, many=True).data
    
    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Variant price cannot be negative.")
        return value
