from django.db import models

class Customer(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Potensial'), ('active', 'Faol'),
        ('vip', 'VIP'), ('inactive', 'Nofaol'),
    ]
    name = models.CharField(max_length=200, verbose_name="Ism Familiya")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon")
    email = models.EmailField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lead')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('call', 'Qo\'ng\'iroq'), ('message', 'Xabar'),
        ('email', 'Email'), ('visit', 'Tashrif'),
        ('order', 'Buyurtma'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=300, verbose_name="Mavzu")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Muloqot"
        verbose_name_plural = "Muloqotlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.name} - {self.get_interaction_type_display()}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Past'), ('medium', 'O\'rta'), ('high', 'Yuqori'),
    ]
    STATUS_CHOICES = [
        ('todo', 'Bajarilmagan'), ('inprogress', 'Jarayonda'),
        ('done', 'Bajarildi'),
    ]
    title = models.CharField(max_length=300, verbose_name="Vazifa")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
