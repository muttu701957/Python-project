from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.utils.timezone import now
 # Import settings to use AUTH_USER_MODEL


class CustomUser(AbstractUser):
    USER_Types=[
        ('admin', 'admin'),
        ('donor','donor'),
        ('recipient','recipient'),
        ('hospital','hospital'),
    ]
    user_type=models.CharField(max_length=15,choices=USER_Types,default='admin')



from django.db import models
from django.conf import settings

class HospitalDetail(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hospital_detail'
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    total_beds = models.IntegerField()
    available_beds = models.IntegerField()
    emergency_facilities = models.TextField()

    # ✅ Added Fields with Defaults
    country = models.CharField(max_length=100, default="Unknown")
    state = models.CharField(max_length=100, default="Unknown")
    city = models.CharField(max_length=100, default="Unknown")
    pincode = models.CharField(max_length=10, default="000000")

    def __str__(self):  # ✅ Changed _str_ to __str__
        return f"{self.name} - {self.city}, {self.state}"


from django.db import models

class AddOrgan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class DonorDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="donor_profile", null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True)
    dob = models.DateField(blank=True, null=True)  # Ensure correct field type
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'),('AB+', 'AB+'), ('AB-', 'AB-')])
    contact = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()  
    country = models.CharField(max_length=100, blank=True, null=True)  
    state = models.CharField(max_length=100, blank=True, null=True)    
    city = models.CharField(max_length=100, blank=True, null=True)     
    pincode = models.CharField(max_length=10, blank=True, null=True)  
    hospital = models.ForeignKey(HospitalDetail, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name

class LivingOrganDonation(models.Model):

    donor = models.ForeignKey(DonorDetails, on_delete=models.CASCADE, related_name="living_donations")
    organ = models.ForeignKey(AddOrgan, on_delete=models.CASCADE)  # Fetch from admin-added organs
    AVAILABILITY_CHOICES = [
        ("Available", "Available"),
        ("Transplanted", "Transplanted"),
        ("Reserved", "Reserved"),
    ]
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default="Available"
    )
    date_registered = models.DateField(default=now)  # Add this field
    # Health conditions (Yes/No)
    diabetes = models.BooleanField(default=False)
    blood_pressure = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    liver_disease = models.BooleanField(default=False)
    lung_disease = models.BooleanField(default=False)
    hiv_aids = models.BooleanField(default=False)
    hepatitis = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)
    cancer_history = models.BooleanField(default=False)
    smoking_history = models.BooleanField(default=False)
    alcohol_history = models.BooleanField(default=False)
    any_surgery = models.BooleanField(default=False)
    skin_damage=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donor.full_name} - {self.organ.name} ({self.availability_status})"

class DeceasedDonation(models.Model):

    donor = models.ForeignKey(DonorDetails, on_delete=models.CASCADE, related_name="deceased_donations")
    organ = models.ForeignKey(AddOrgan, on_delete=models.CASCADE, related_name="deceased_donations")  # Add related_name here
    AVAILABILITY_CHOICES = [
        ("Available", "Available"),
        ("Transplanted", "Transplanted"),
        ("Reserved", "Reserved"),
    ]
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default="Available"
    )
    date_registered = models.DateField(default=now)  # Add this field
    # Health Conditions (Yes/No)
    diabetes = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    liver_disease = models.BooleanField(default=False)
    cancer_history = models.BooleanField(default=False)
    hiv_aids = models.BooleanField(default=False)
    hepatitis = models.BooleanField(default=False)
    smoking_history = models.BooleanField(default=False)
    alcohol_history = models.BooleanField(default=False)
    major_surgeries = models.BooleanField(default=False)

    # date_of_donation = models.DateField(auto_now_add=True)
class DeceasedDonationFile(models.Model):
    donation = models.ForeignKey(DeceasedDonation, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="deceased_donation_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)  # <-- Add this field
    rejected = models.BooleanField(default=False)  # <-- Add this field

class Recipient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="recipient_profile", null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    
    GENDER_CHOICES = [
        ('Male', 'Male'), 
        ('Female', 'Female'), 
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), 
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    
    contact = models.CharField(max_length=15)
    address = models.TextField()
    
    # Location fields
    country = models.CharField(max_length=100, blank=True, null=True)  
    state = models.CharField(max_length=100, blank=True, null=True)    
    city = models.CharField(max_length=100, blank=True, null=True)   
    # Hidden field (Only hospital staff can update)
    matching_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Matched', 'Matched'),
        ('Transplanted', 'Transplanted'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    
    hospital = models.ForeignKey(HospitalDetail, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name

class RecipientOrganNeeded(models.Model):

    URGENCY_LEVELS = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name="organs_needed")  # Multiple requests per recipient

    organ_neededrequest = models.ForeignKey(AddOrgan, on_delete=models.CASCADE, related_name="organs_needed")  # Add related_name here
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='Low')

    # Medical Conditions
    diabetes = models.BooleanField(default=False)
    blood_pressure = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    liver_disease = models.BooleanField(default=False)
    lung_disease = models.BooleanField(default=False)
    hiv_aids = models.BooleanField(default=False)
    hepatitis = models.BooleanField(default=False)
    cancer_history = models.BooleanField(default=False)
    autoimmune_disease = models.BooleanField(default=False)
    neurological_disorder = models.BooleanField(default=False)
    blood_disorder = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)
    smoking_history = models.BooleanField(default=False)
    alcohol_history = models.BooleanField(default=False)
    previous_transplant = models.BooleanField(default=False)
    requested_date = models.DateTimeField(auto_now_add=True)  # Ensure this field exists


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # ✅ FIXED: Import timezone

class TransplantMatch(models.Model):
    donor = models.ForeignKey('DonorDetails', on_delete=models.CASCADE)
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE)
    match_date = models.DateTimeField(default=timezone.now)  # ✅ FIXED
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):  # ✅ Changed self.donor.name to self.donor.full_name
        return f"Match: {self.donor.full_name} → {self.recipient.full_name}"

    


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TransplantAllocation(models.Model):  # Renamed from TransplantMatchRecord
    donor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    donor_object_id = models.PositiveIntegerField()
    donor = GenericForeignKey('donor_content_type', 'donor_object_id')  # ✅ Can store Living or Deceased donor
    recipient = models.ForeignKey(RecipientOrganNeeded, on_delete=models.CASCADE)
    organ = models.CharField(max_length=100)
    match_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')], 
        default='Pending'
    )

    def __str__(self):
        return f"Allocation: {self.donor} → {self.recipient} ({self.organ})"



from django.db import models
from django.utils import timezone

class OrganTracking(models.Model):
    organ_type = models.CharField(max_length=50, choices=[
        ('Heart', 'Heart'),
        ('Kidney', 'Kidney'),
        ('Liver', 'Liver'),
        ('Lungs', 'Lungs'),
        ('Pancreas', 'Pancreas'),
        ('Intestine', 'Intestine'),
    ])
    donor = models.ForeignKey('DonorDetails', on_delete=models.CASCADE)
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, null=True, blank=True)
    hospital_source = models.CharField(max_length=100)  # Where organ is coming from
    hospital_destination = models.CharField(max_length=100)  # Where organ is going
    transport_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Delayed', 'Delayed')
    ], default='Pending')
    dispatch_time = models.DateTimeField(default=timezone.now)
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    current_location = models.CharField(max_length=100, blank=True, null=True)
    tracking_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"Organ: {self.organ_type} | Status: {self.transport_status}"


class MedicalDocument(models.Model):
    organ_request = models.ForeignKey(RecipientOrganNeeded, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to='medical_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)  # <-- Add this field
    rejected = models.BooleanField(default=False)  # <-- Add this field

    def __str__(self):
        return f"Document for {self.organ_request.recipient} uploaded on {self.uploaded_at}"


class LivingDonationDocument(models.Model):
    donation = models.ForeignKey(LivingOrganDonation, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to='living_donation_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)  # <-- Add this field
    rejected = models.BooleanField(default=False)  # <-- Add this field

    def __str__(self):
        return f"Document for {self.donation.donor} uploaded on {self.uploaded_at}"


from django.db import models
from newapp.models import DonorDetails, Recipient

class OrganMatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed')
    ]
    
    donor = models.ForeignKey(DonorDetails, on_delete=models.CASCADE, related_name="matches")
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name="matches")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    matched_at = models.DateTimeField(auto_now_add=True)  # Timestamp of match creation

    def __str__(self):
        return f"Match: {self.donor.full_name} → {self.recipient.full_name} ({self.status})"  # ✅ Removed extra parentheses

# from django.db import models
# from newapp.models import CustomUser  # Import your CustomUser model

# class Notification(models.Model):
#     STATUS_CHOICES = [
#         ('unread', 'Unread'),
#         ('read', 'Read'),
#     ]

#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
#     message = models.TextField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.username}: {self.message[:30]}"
from django.db import models
from newapp.models import CustomUser  # Import your CustomUser model

class Notification(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    RESPONSE_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_notifications")  # Admin who sent the notification
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")  # Recipient of the notification
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES, default='pending')  # Track recipient response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"


# class Transplant(models.Model):
#     recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
#     donor = models.ForeignKey(DonorDetails, on_delete=models.SET_NULL, null=True, blank=True)
#     hospital = models.ForeignKey(HospitalDetail, on_delete=models.SET_NULL, null=True)
#     transplant_date = models.DateField()
#     status = models.CharField(
#         max_length=50,
#         choices=[
#             ('Pending', 'Pending'),
#             ('Scheduled', 'Scheduled'),
#             ('Completed', 'Completed')
#         ],
#         default='Pending'
#     )
#     attended = models.BooleanField(default=False)  # ✅ New field to track attendance
#     success = models.BooleanField(default=False)  # ✅ New field to track transplant success
#     living_donation = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Transplant for {self.recipient.user.username} - {self.status}"
    
#     def mark_as_completed(self):
#         """ Marks the transplant as completed only if attended """
#         if self.attended:
#             self.status = 'Completed'
#             self.success = True
#             self.save()

class Transplant(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    donor = models.ForeignKey(DonorDetails, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(HospitalDetail, on_delete=models.SET_NULL, null=True)
    transplant_date = models.DateField()

    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )

    # ✅ Separate Attendance Tracking for Recipients and Donors
    recipient_attended = models.BooleanField(default=False)
    donor_attended = models.BooleanField(default=False)  # Only applies to Living Donation

    success = models.BooleanField(default=False)
    living_donation = models.BooleanField(default=False)  # True = Living, False = Deceased

    def __str__(self):
        return f"Transplant for {self.recipient.user.username} - {self.status}"

    def mark_as_completed(self):
        """Marks the transplant as completed only if attendance is met"""
        if self.living_donation:
            # ✅ Living Donation: Both Recipient and Donor must attend
            if self.recipient_attended and self.donor_attended:
                self.status = 'Completed'
                self.success = True
                self.save()
        else:
            # ✅ Deceased Donation: Only Recipient attendance is required
            if self.recipient_attended:
                self.status = 'Completed'
                self.success = True
                self.save()


from django.db import models
from django.conf import settings
from datetime import datetime

class Report(models.Model):
    REPORT_TYPES = [
        ("Transplant Success Rate", "Transplant Success Rate"),
        ("Donor Trends", "Donor Trends"),
        ("Hospital Performance", "Hospital Performance"),
    ]

    id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=255, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} - {self.generated_at}"


from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

class Compensation(models.Model):
    donor = models.OneToOneField(DonorDetails, on_delete=models.CASCADE, related_name="compensation")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Admin sets this amount
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        """Ensure only living donors receive compensation."""
        if not self.donor.living_donations.exists():
            raise ValidationError("Compensation can only be given to living donors.")

    def save(self, *args, **kwargs):
        """Validate before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compensation: ${self.amount} | Approved: {self.approved}"
