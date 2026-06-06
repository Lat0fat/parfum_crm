from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Brend nomi")

    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Parfum(models.Model):
    GENDER_CHOICES = [
        ('female', 'Ayollar uchun'), ('male', 'Erkaklar uchun'), ('unisex', 'Uniseks'),
    ]
    SIZE_CHOICES = [
        ('30ml', '30 ml'), ('50ml', '50 ml'), ('100ml', '100 ml'), ('150ml', '150 ml'),
    ]
    name = models.CharField(max_length=300, verbose_name="Nomi")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='parfums')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='100ml')
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    top_notes = models.CharField(max_length=300, blank=True)
    heart_notes = models.CharField(max_length=300, blank=True)
    base_notes = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parfum"
        verbose_name_plural = "Parfumlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} – {self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'), ('confirmed', 'Tasdiqlangan'),
        ('processing', 'Jarayonda'), ('shipped', 'Yuborilgan'),
        ('delivered', 'Yetkazilgan'), ('cancelled', 'Bekor'),
    ]
    customer = models.ForeignKey(
        'crm.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk} – {self.customer_name}"


class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Yetkazib beruvchi")
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Yetkazib beruvchi"
        verbose_name_plural = "Yetkazib beruvchilar"

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ombor nomi")
    location = models.CharField(max_length=300, blank=True)
    manager = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Ombor"
        verbose_name_plural = "Omborlar"

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    TYPE_CHOICES = [
        ('in', 'Kirim'), ('out', 'Chiqim'), ('return', 'Qaytarish'),
    ]
    parfum_name = models.CharField(max_length=300)
    movement_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Harakat"
        verbose_name_plural = "Ombor harakatlari"
        ordering = ['-created_at']

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.parfum_name} x{self.quantity}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('purchase', 'Xarid'), ('delivery', 'Yetkazib berish'),
        ('marketing', 'Marketing'), ('salary', 'Maosh'),
        ('rent', 'Ijara'), ('other', 'Boshqa'),
    ]
    title = models.CharField(max_length=300, verbose_name="Xarajat nomi")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.amount:,} so'm"
