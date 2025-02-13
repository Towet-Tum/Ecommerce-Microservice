from django.db import models

class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        help_text="Parent category for hierarchical organization"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    product_count = models.PositiveIntegerField(default=0) 

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Default price if variant-specific pricing is not used"
    )
    # Additional fields like brand, weight, etc., can be added here.

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['product', 'is_primary']),
        ]

    def __str__(self):
        return f"Image for {self.product.name}"



class OptionType(models.Model):
    name = models.CharField(max_length=63, unique=True, help_text="E.g., 'Color', 'Size'")

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    option_type = models.ForeignKey(
        OptionType,
        on_delete=models.CASCADE,
        related_name='values'
    )
    value = models.CharField(max_length=63, help_text="E.g., 'Red', 'Small'")

    class Meta:
        unique_together = (('option_type', 'value'),)
        indexes = [
            models.Index(fields=['option_type', 'value']),
        ]

    def __str__(self):
        return f"{self.option_type.name}: {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Variant-specific price; if null, use product.base_price"
    )
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product.name} - SKU: {self.sku}"


class VariantOption(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option_value = models.ForeignKey(
        OptionValue,
        on_delete=models.CASCADE,
        related_name='variant_options'
    )

    class Meta:
        unique_together = (('variant', 'option_value'),)
        indexes = [
            models.Index(fields=['variant', 'option_value']),
        ]

    def __str__(self):
        return f"{self.variant.sku}: {self.option_value}"