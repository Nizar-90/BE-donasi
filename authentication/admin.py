from django.contrib import admin
from .models import UserProfile, Donation, DonationHistory
admin.site.register(UserProfile)
admin.site.register(Donation)
admin.site.register(DonationHistory)
