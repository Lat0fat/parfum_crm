from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Brend nomi")
    country = models.CharField(max_length=100, verbose_name="Mamlakat", blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"

    def __str__(self):
        return self.name

class Parfum(models.Model):
    GENDER_CHOICES = [
        ('female', 'Ayollar uchun'),
        ('male', 'Erkaklar uchun'),
        ('unisex', 'Uniseks'),
    ]
    SIZE_CHOICES = [
        ('30ml', '30 ml'), ('50ml', '50 ml'),
        ('100ml', '100 ml'), ('150ml', '150 ml'),
    ]

    name = models.CharField(max_length=300, verbose_name="Parfum nomi")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brend")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    description = models.TextField(verbose_name="Tavsif", blank=True)
    top_notes = models.CharField(max_length=300, verbose_name="Yuqori notalar", blank=True)
    heart_notes = models.CharField(max_length=300, verbose_name="Yurak notalar", blank=True)
    base_notes = models.CharField(max_length=300, verbose_name="Asosiy notalar", blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='100ml')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx (so'm)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi miqdor")
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5)
    sold_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parfum"
        verbose_name_plural = "Parfumlar"

    def __str__(self):
        return f"{self.brand} - {self.name}"

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price:
            return int((1 - self.discount_price / self.price) * 100)
        return 0

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'), ('confirmed', 'Tasdiqlangan'),
        ('processing', 'Jarayonda'), ('shipped', 'Yuborilgan'),
        ('delivered', 'Yetkazilgan'), ('cancelled', 'Bekor qilingan'),
    ]
    customer_name = models.CharField(max_length=200, verbose_name="Mijoz ismi")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefon")
    customer_email = models.EmailField(blank=True)
    address = models.TextField(verbose_name="Manzil")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    parfum = models.ForeignKey(Parfum, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.parfum.name} x {self.quantity}"
