from django import forms
from .models import CustomUser,DonorDetails,Recipient,DeceasedDonation,LivingOrganDonation,HospitalDetail,RecipientOrganNeeded,AddOrgan,MedicalDocument,Notification


class DonorDetailsForm(forms.ModelForm):
    dob = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = DonorDetails
        fields = [
            "full_name",
            "email",
            "dob",
            "gender",
            "blood_type",
            "contact",
            "address",
            "country",
            "state",
            "city",
            "pincode"
        ]


class OrganForm(forms.ModelForm):
    class Meta:
        model = AddOrgan
        fields = ['name']

from django import forms
from .models import LivingOrganDonation, AddOrgan

class LivingOrganDonationForm(forms.ModelForm):
    organ = forms.ModelChoiceField(
        queryset=AddOrgan.objects.all(),  # Fetch organs dynamically
        empty_label="🔽 Choose an Organ",
        widget=forms.Select(attrs={"class": "form-select border-primary"}),
    )

    class Meta:
        model = LivingOrganDonation
        fields = ["organ", "diabetes", "blood_pressure", "heart_disease", "kidney_disease",
                  "liver_disease", "lung_disease", "hiv_aids", "hepatitis", "obesity",
                  "cancer_history", "smoking_history", "alcohol_history", "any_surgery"]


from django import forms
from .models import DeceasedDonation

class DeceasedDonationForm(forms.ModelForm):
    class Meta:
        model = DeceasedDonation
        fields = [
            'organ', 'diabetes', 'hypertension', 'heart_disease', 'kidney_disease',
            'liver_disease', 'cancer_history', 'hiv_aids', 'hepatitis', 'smoking_history',
            'alcohol_history', 'major_surgeries'
        ]
        widgets = {
            'organ': forms.Select(attrs={'class': 'form-select'}),
            'diabetes': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'hypertension': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'heart_disease': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'kidney_disease': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'liver_disease': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'cancer_history': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'hiv_aids': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'hepatitis': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'smoking_history': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'alcohol_history': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            'major_surgeries': forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Convert "Yes"/"No" to True/False explicitly
        for field in [
            "diabetes", "hypertension", "heart_disease",
            "kidney_disease", "liver_disease", "cancer_history",
            "hiv_aids", "hepatitis", "smoking_history",
            "alcohol_history", "major_surgeries"
        ]:
            value = self.data.get(field)

            if value == "Yes":
                cleaned_data[field] = True
            elif value == "No":
                cleaned_data[field] = False

        return cleaned_data


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            'full_name', 'email', 'dob', 'gender', 'blood_type', 
            'contact', 'address', 'country', 'state', 'city'
        ]  # Removed organ_needed, medical_condition, urgency_level

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter your address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'India'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.matching_status = "Pending"  # Automatically set to 'Pending'
        if commit:
            instance.save()
        return instance
    


from django import forms
from .models import DonorDetails

class DonorDetailsForm(forms.ModelForm):
    class Meta:
        model = DonorDetails
        fields = ['full_name', 'email', 'contact', 'blood_type', 'address', 'city', 'state', 'country', 'gender']  # Added 'gender'




class RecipientOrganNeededForm(forms.ModelForm):
    class Meta:
        model = RecipientOrganNeeded
        fields = [
            'organ_neededrequest', 'urgency_level', 
            'diabetes', 'blood_pressure', 'heart_disease', 
            'kidney_disease', 'liver_disease', 'lung_disease', 
            'hiv_aids', 'hepatitis', 'cancer_history', 
            'autoimmune_disease', 'neurological_disorder', 'blood_disorder', 
            'obesity', 'smoking_history', 'alcohol_history', 'previous_transplant'
        ]

        widgets = {
            "organ_neededrequest": forms.Select(attrs={'class': 'form-control'}),  # ✅ Ensure correct field name
            "urgency_level": forms.Select(attrs={'class': 'form-control'}),
            "diabetes": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "blood_pressure": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "heart_disease": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "kidney_disease": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "liver_disease": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "lung_disease": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "hiv_aids": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "hepatitis": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "cancer_history": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "autoimmune_disease": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "neurological_disorder": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "blood_disorder": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "obesity": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "smoking_history": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "alcohol_history": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "previous_transplant": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
        }


    def clean(self):
        cleaned_data = super().clean()

        # Convert "Yes"/"No" to True/False explicitly
        for field in [
            "diabetes", "hypertension", "heart_disease",
            "kidney_disease", "liver_disease", "cancer_history",
            "hiv_aids", "hepatitis", "smoking_history",
            "alcohol_history", "major_surgeries"
        ]:
            value = self.data.get(field)

            if value == "Yes":
                cleaned_data[field] = True
            elif value == "No":
                cleaned_data[field] = False

        return cleaned_data



class HospitalDetailForm(forms.ModelForm):
    class Meta:
        model = HospitalDetail
        fields = [
            'name', 'location', 'contact_number', 'email', 'total_beds',
            'available_beds', 'emergency_facilities', 'country', 'state', 'city', 'pincode'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'total_beds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Beds'}),
            'available_beds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available Beds'}),
            'emergency_facilities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Emergency Facilities', 'rows': 3}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        }

# from django import forms
# from .models import Notification, CustomUser

# class NotificationForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type='recipient'), label="Select Recipient")

#     class Meta:
#         model = Notification
#         fields = ['user', 'message', 'status']
class NotificationForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='recipient'),
        empty_label="Select a Recipient",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'status']



# forms.py
# from django import forms
# from .models import Transplant, Recipient

# class TransplantForm(forms.ModelForm):
#     recipient = forms.ModelChoiceField(queryset=Recipient.objects.all(), required=True, label='Select Recipient')
    
#     class Meta:
#         model = Transplant
#         fields = ['recipient', 'donor', 'hospital', 'transplant_date', 'status']
#         widgets = {
#             'transplant_date': forms.DateInput(attrs={'type': 'date'}),
#             'status': forms.Select(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Completed', 'Completed')])
#         }
from django import forms
from .models import Transplant, Recipient, DonorDetails, LivingOrganDonation

class TransplantForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=Recipient.objects.all(), required=True, label='Select Recipient')

    # Only donors who have a LivingOrganDonation entry
    donor = forms.ModelChoiceField(
        queryset=DonorDetails.objects.filter(living_donations__isnull=False).distinct(),
        required=False, 
        label='Select Living Donor'
    )

    class Meta:
        model = Transplant
        fields = ['recipient', 'donor', 'hospital', 'transplant_date', 'status']
        widgets = {
            'transplant_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[
                ('Pending', 'Pending'), 
                ('Scheduled', 'Scheduled'), 
                ('Completed', 'Completed')
            ])
        }

    def clean(self):
        cleaned_data = super().clean()
        donor = cleaned_data.get("donor")

        # Ensure living_donation is True only when a donor is selected
        cleaned_data["living_donation"] = donor is not None

        return cleaned_data


from django import forms
from .models import Compensation

class CompensationForm(forms.ModelForm):
    class Meta:
        model = Compensation
        fields = ['amount', 'approved']

