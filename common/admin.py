from django.contrib import admin
from .models import CustomerReview, DashboardImage, CustomerMessage

# Register your models here.

admin.site.register(CustomerReview)
admin.site.register(DashboardImage)
admin.site.register(CustomerMessage)