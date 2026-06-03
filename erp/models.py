from django.db import models

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
