from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=255)

    industry = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DataSource(models.Model):

    SOURCE_CHOICES = [
        ('SAP', 'SAP'),
        ('UTILITY', 'UTILITY'),
        ('TRAVEL', 'TRAVEL'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50,
        default='PENDING'
    )

    def __str__(self):
        return self.source_type


class EmissionRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    scope = models.CharField(max_length=20)

    category = models.CharField(max_length=100)

    activity_type = models.CharField(max_length=100)

    raw_value = models.FloatField()

    normalized_value = models.FloatField(
        null=True,
        blank=True
    )

    unit = models.CharField(max_length=50)

    normalized_unit = models.CharField(max_length=50)

    emission_factor = models.FloatField(default=0)

    co2e = models.FloatField(default=0)

    is_suspicious = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity_type


class AuditLog(models.Model):

    record = models.ForeignKey(
        EmissionRecord,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=100)

    old_value = models.TextField(
        null=True,
        blank=True
    )

    new_value = models.TextField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action