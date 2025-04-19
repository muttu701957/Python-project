from django.contrib import admin
from .models import DonorDetails,Recipient,AddOrgan

# @admin.register(DonorDetails)
# class DonorAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'contact', 'blood_type','gender','address')  # Removed 'registered_at'
#     search_fields = ('full_name', 'email', 'contact')
#     list_filter = ('blood_type', 'gender')
#     ordering = ('full_name',)
#     list_per_page = 10



from django.contrib import admin
from .models import DonorDetails

@admin.register(DonorDetails)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'contact', 'blood_type', 'gender', 'address')
    search_fields = ('full_name', 'email', 'contact')
    list_filter = ('blood_type', 'gender')
    ordering = ('full_name',)
    list_per_page = 10

class RecipientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email","blood_type")  # Display columns
    search_fields = ("full_name", "email", "blood_type")  # Search functionality
    list_filter = ("blood_type", "gender")  # Filters for easy sorting
    ordering = ("full_name",)  # Order by name

admin.site.register(Recipient, RecipientAdmin)  # Register model with custom admin view

from django.contrib import admin
from .models import HospitalDetail

@admin.register(HospitalDetail)
class HospitalDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_number', 'available_beds')

from django.contrib import admin
from .models import AddOrgan

@admin.register(AddOrgan)
class OrganAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from newapp.models import DonorDetails, Recipient, DeceasedDonation

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organ_needed', 'blood_type', 'match_donor_link')

    def match_donor_link(self, obj):
        return format_html('<a href="match/{}/">Match Donor</a>', obj.id)
    match_donor_link.short_description = "Match Donor"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('match/<int:recipient_id>/', self.admin_site.admin_view(self.match_donors), name='match_donors'),
        ]
        return custom_urls + urls

    def match_donors(self, request, recipient_id):
        recipient = Recipient.objects.get(id=recipient_id)

        # Find donors with compatible blood type and organ availability
        matched_donors = DonorDetails.objects.filter(
            blood_type=recipient.blood_type,
            deceased_donations__organ=recipient.organ_needed
        )

        return render(request, 'admin/match_results.html', {
            'recipient': recipient,
            'matched_donors': matched_donors
        })

from django.contrib import admin
from .models import Transplant

class TransplantAdmin(admin.ModelAdmin):
    list_display = ("recipient", "hospital", "transplant_date", "status", "success")
    actions = ["mark_as_completed"]

    def mark_as_completed(self, request, queryset):
        for transplant in queryset:
            transplant.mark_as_completed()
        self.message_user(request, "Selected transplants marked as completed.")

    mark_as_completed.short_description = "Mark selected transplants as completed"

admin.site.register(Transplant, TransplantAdmin)

