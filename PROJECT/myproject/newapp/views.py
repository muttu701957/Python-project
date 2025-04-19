
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomUser  # Ensure you have a CustomUser model
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import DonorDetailsForm,DeceasedDonationForm,LivingOrganDonationForm
from django.core.mail import send_mail
import random

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect user based on user_type
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user.user_type == 'donor':
                return redirect('donor_dashboard')
            elif user.user_type == 'recipient':
                return redirect('recipient_dashboard')
            elif user.user_type=='hospital':
                return redirect('hospital_dashboard')
            else:
                return redirect('admin_dashboard')  # Default fallback

        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'admin':
            return render(request, 'admin_register.html')
        elif user_type == 'donor':
            return render(request, 'donor_register.html')
        elif user_type == 'recipient':
            return render(request, 'recipient_register.html')
        elif user_type == 'hospital':
            return render(request, 'hospital_register.html')
    return render(request, 'register.html')


def organ_request(request):
    return render(request,'organ_request.html')


def home1(request):
    return render(request,'home1.html')

def donor_register(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            return HttpResponse("Both password fields are required!", status=400)

        if password1 != password2:
            return HttpResponse("Passwords do not match!", status=400)

        # Create donor user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, user_type='donor')
        return redirect('user_login')  # Redirect to login after registration

    return render(request, "donor_register.html")

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import AddOrgan
from .forms import OrganForm

def organ_list(request):
    organs = AddOrgan.objects.all()
    form = OrganForm()

    if request.method == "POST":
        form = OrganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organ_list')

    return render(request, 'organ_list.html', {'organs': organs, 'form': form})

def get_organs(request):
    """ API to fetch organs for dropdown selection in donation forms """
    organs = AddOrgan.objects.values_list('id', 'name')
    return JsonResponse({'organs': list(organs)})



from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model  # ✅ Use this instead of direct User model
from django.contrib import messages

User = get_user_model()  # ✅ Reference the custom user model dynamically

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)  # ✅ Use dynamic user model
            # Implement password reset logic here (send email or reset link)
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    
    return render(request, 'forgot_password.html')


def admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            return HttpResponse("Both password fields are required!", status=400)

        if password1 != password2:
            return HttpResponse("Passwords do not match!", status=400)

        # Create donor user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, user_type='donor')
        return redirect('user_login')  # Redirect to login after registration

    return render(request, "admin_register.html")


def recipient_register(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            return HttpResponse("Both password fields are required!", status=400)

        if password1 != password2:
            return HttpResponse("Passwords do not match!", status=400)

        # Create recipient user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, user_type='recipient')
        return redirect('user_login')  # Redirect to login after registration

    return render(request, "recipient_register.html")

def hospital_register(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not password1 or not password2:
            return HttpResponse("Both password fields are required!", status=400)

        if password1 != password2:
            return HttpResponse("Passwords do not match!", status=400)

        # Create recipient user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, user_type='hospital')
        return redirect('user_login')  # Redirect to login after registration

    return render(request, "hospital_register.html")

def admin_dashboard(request):
    user=request.user
    
    if not user.user_type == 'admin':
        return redirect('no_access')
    
    context={
        'user':user
    }
    return render(request, 'admin_dashboard.html', context)
    
def donor_dashboard(request):
    user = request.user
    
    if not user.user_type == 'donor':
        return redirect('no_access')
    
    context = {
        'user': user,
    }
    return render(request, 'donor_dashboard.html', context)
# from django.shortcuts import render
# from .models import DonorDetails

# def donor_dashboard(request):
#     user = request.user
    
#     # Fetch donor details, if available
#     donor_details = DonorDetails.objects.filter(user=user).first()

#     # Default values for first-time users
#     donation_count = donor_details.donation_count if donor_details else 0
#     pending_matches = MatchingRequests.objects.filter(user=user, status="Pending").count() if donor_details else 0
#     notification_count = Notifications.objects.filter(user=user, is_read=False).count() if donor_details else 0
#     profile_completion = donor_details.profile_completion if donor_details else 0  # Assuming percentage

#     context = {
#         'donation_count': donation_count,
#         'pending_matches': pending_matches,
#         'notification_count': notification_count,
#         'profile_completion': profile_completion
#     }
#     return render(request, 'donor_dashboard.html', context)


def recipient_dashboard(request):
    user = request.user
    
    if not user.user_type == 'recipient':
        return redirect('no_access')
    
    context = {
        'user': user,
    }
    return render(request, 'recipient_dashboard.html', context)




def user_logout(request):
    logout(request)
    return redirect('user_login')

def no_access(request):
    return render(request, 'no_access.html')

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request, 'home.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def about_us(request):
    return render(request, 'about.html')


def register_donor(request):
    return render(request, 'register.donor.html')

def update_donor_status(request):
    return render(request, 'update_donor_status.html')

def organ_donation_status(request):
    return render(request, 'organ_donation_status.html')


# from django.shortcuts import render
# from django.core.mail import send_mail
# from django.contrib import messages

# def contact(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         message = request.POST['message']

#         # You can process the message here (e.g., save to DB or send an email)
#         send_mail(
#             f'Hello, I am interested in donating an organ. Please guide me on the next steps. {name}',  # Subject
#             message,  # Message content
#             email,  # From email
#             # ['admin@organdonation.com'], 
#             #  # To email (Admin)
#             ['01fe22bca032@kletech.ac.in'], 
#         )

#         messages.success(request, "Your message has been sent successfully!")
    
#     return render(request, 'contact.html')


from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_type = request.POST.get('contact_type')

        subject = f'Organ Donation Inquiry from {contact_type} - {name}'
        full_message = f'''
📩 New Organ Donation Contact Form Submission

🧑 Name: {name}
📧 Email: {email}
🙋 Type: {contact_type}

📝 Message:
{message}
'''

        email_message = EmailMessage(
            subject=subject,
            body=full_message,
            from_email=settings.EMAIL_HOST_USER,
            to=['01fe22bca032@kletech.ac.in'],  # Your email
            reply_to=[email]  # 👈 This sets reply-to correctly
        )
        email_message.send()

        messages.success(request, "Your message has been sent successfully!")

    return render(request, 'contact.html')


from .models import DonorDetails, Recipient, DeceasedDonation, RecipientOrganNeeded  # Import your model
 # Import your model
from .forms import DonorDetailsForm ,OrganForm,RecipientForm # Import your form (if using Django forms)


def some_view(request):
    print(RecipientOrganNeeded.objects.all())  # Debugging step
    return HttpResponse("Check the terminal for output.")






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DonorDetails, CustomUser, HospitalDetail
from .forms import DonorDetailsForm

def add_details(request):
    hospitals = HospitalDetail.objects.all()  # Fetch all hospitals

    if request.method == "POST":
        print("🔥 Received POST Data:", request.POST)  # Debugging

        email = request.POST.get("email")  # Get email from form

        # ✅ Ensure the donor exists in CustomUser first
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist. Please register first.")
            return redirect("donor_register")

        # ✅ Check if DonorDetails already exists
        donor, created = DonorDetails.objects.get_or_create(email=email)

        form = DonorDetailsForm(request.POST, instance=donor)  # Bind form to existing donor record
        if form.is_valid():
            donor = form.save(commit=False)
            donor.dob = request.POST.get("dob")
            donor.pincode = request.POST.get("pincode")

            # ✅ Assign selected hospital
            hospital_id = request.POST.get("hospital_id")
            if hospital_id:
                try:
                    donor.hospital = HospitalDetail.objects.get(id=hospital_id)
                except HospitalDetail.DoesNotExist:
                    messages.error(request, "Invalid hospital selection.")
                    return redirect("add_details")

            donor.save()

            print("✅ Data Updated Successfully for:", donor.email)
            messages.success(request, "Your details have been saved successfully!")
            return redirect("success_page1")
        else:
            print("❌ Form Errors:", form.errors)  # Debugging

    else:
        form = DonorDetailsForm()

    return render(request, "add_details.html", {"form": form, "hospitals": hospitals})


def view_profile(request):
    return render(request,'view_profile.html')


from django.shortcuts import render, redirect
from .models import AddOrgan
from .forms import OrganForm

def add_organ(request):
    form = OrganForm()

    if request.method == "POST":
        form = OrganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_organ')  # Ensure this name exists in `urls.py`

    # Fetch existing organs to display in the template
    organs = AddOrgan.objects.all()

    return render(request, 'add_organ.html', {'form': form, 'organs': organs})



from django.shortcuts import render, get_object_or_404
from newapp.models import DonorDetails, LivingOrganDonation, DeceasedDonation

def donor_profile(request, donor_id):
    donor = get_object_or_404(DonorDetails, id=donor_id)
    
    living_donations = donor.living_donations.all().distinct()
    deceased_donation = DeceasedDonation.objects.filter(donor=donor).first()

    # living_donations = donor.living_donations.filter(documents__verified=True).distinct()
    # deceased_donation = DeceasedDonation.objects.filter(donor=donor, files__verified=True).first()
    
    return render(request, 'donor_profile.html', {
        'donor': donor,
        'living_donations': living_donations,
        'deceased_donation': deceased_donation  # Pass a QuerySet instead of a single object
    })



from django.shortcuts import render, get_object_or_404
from .models import DonorDetails

def donor_dashboard(request):
    donor = None

    if request.user.is_authenticated:
        donor = DonorDetails.objects.filter(user=request.user).first()

    return render(request, 'donor_dashboard.html', {'donor': donor})
from django.shortcuts import render, get_object_or_404, redirect
from .models import DonorDetails
from .forms import DonorDetailsForm
from django.contrib import messages  # For success/error messages

def update_profile(request, donor_id):  
    donor = get_object_or_404(DonorDetails, id=donor_id)

    if request.method == 'POST':
        form = DonorDetailsForm(request.POST, instance=donor)
        print("Form Data Received:", request.POST)  # Debugging: Check received data
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('donor_dashboard')  # Ensure this URL exists in urls.py
        else:
            print("Form Errors:", form.errors)  # Debugging: Check validation errors
            messages.error(request, "Profile update failed. Please correct the errors.")

    else:
        form = DonorDetailsForm(instance=donor)

    return render(request, 'update_profile.html', {'form': form, 'donor': donor})



from django.shortcuts import render, get_object_or_404
from .models import Recipient, RecipientOrganNeeded

def recipient_profile(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    organ_needed = RecipientOrganNeeded.objects.filter(recipient=recipient).first()
    
    return render(request, 'recipient_profile.html', {
        'recipient': recipient,
        'organ_needed': organ_needed
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipient
from .forms import RecipientForm

def update_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)

    if request.method == "POST":
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            return redirect('recipient_profile', recipient_id=recipient.id)  # Redirect to updated profile
    else:
        form = RecipientForm(instance=recipient)

    return render(request, 'update_recipient.html', {'form': form, 'recipient': recipient})


def recipient_dashboard(request):
    recipient = Recipient.objects.filter(user=request.user).first()

    total_requests = 0
    matched_donors = 0
    transplant = None
    notification_count = 0  # Initialize notification count

    if recipient:
        total_requests = RecipientOrganNeeded.objects.filter(recipient=recipient).count()
        matched_donors = OrganMatch.objects.filter(recipient=recipient).count()
        transplant = Transplant.objects.filter(recipient=recipient).first()
        
        # ✅ Correct query for unread notifications
        notification_count = Notification.objects.filter(user=request.user, status='unread').count()

    context = {
        'recipient': recipient,
        'total_requests': total_requests,
        'matched_donors': matched_donors,
        'transplant': transplant,
        'notification_count': notification_count  # ✅ Pass the count to the template
    }

    print(f"User: {request.user}, Notifications: {notification_count}")  # Debugging output

    return render(request, 'recipient_dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipient, HospitalDetail
from .forms import RecipientForm

@login_required
def add_recipient(request):
    hospitals = HospitalDetail.objects.all()  # ✅ Fetch all hospitals for selection

    if request.method == "POST":
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)  # Do not save yet
            recipient.user = request.user  # Assign logged-in user

            # ✅ Assign Hospital
            hospital_id = request.POST.get("hospital_id")
            if hospital_id:
                try:
                    recipient.hospital = HospitalDetail.objects.get(id=hospital_id)
                except HospitalDetail.DoesNotExist:
                    messages.error(request, "Selected hospital does not exist.")
                    return redirect("add_recipient")

            recipient.save()  # Now save with user & hospital assigned
            messages.success(request, "Your details have been saved successfully!")
            return redirect("success_page2")  # Redirect to success page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipientForm()

    return render(request, "add_recipient.html", {"form": form, "hospitals": hospitals})  # ✅ Pass hospitals to template


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import DonorDetails, LivingOrganDonation, AddOrgan, LivingDonationDocument
# from .forms import LivingOrganDonationForm

# @login_required
# def living_donation(request):
#     health_features = [
#         "diabetes", "blood_pressure", "heart_disease",
#         "kidney_disease", "liver_disease", "lung_disease",
#         "hiv_aids", "hepatitis", "obesity",
#         "cancer_history", "smoking_history", "alcohol_history", "any_surgery"
#     ]

#     organs = AddOrgan.objects.all()  # Fetch organs from the database

#     try:
#         donor = DonorDetails.objects.get(user=request.user)
#     except DonorDetails.DoesNotExist:
#         donor = None

#     if request.method == "POST":
#         form = LivingOrganDonationForm(request.POST)

#         if form.is_valid():
#             if donor:
#                 living_donation = form.save(commit=False)
#                 living_donation.donor = donor
#                 living_donation.save()

#                 # Handle multiple file uploads
#                 files = request.FILES.getlist("files")
#                 for file in files:
#                     LivingDonationDocument.objects.create(donation=living_donation, file=file)

#                 messages.success(request, "✅ Organ donation request submitted successfully with documents!")
#                 return redirect('success_page1')
#             else:
#                 form.add_error(None, "❌ Error: No donor profile found for this user.")
#         else:
#             messages.error(request, "❌ There was an error in your submission. Please check the form.")

#     else:
#         form = LivingOrganDonationForm()

#     return render(request, "living_donation.html", {
#         "form": form,
#         "health_features": health_features,
#         "organs": organs,  # Send organs to template
#     })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonorDetails, LivingOrganDonation, AddOrgan, LivingDonationDocument
from .forms import LivingOrganDonationForm

@login_required
def living_donation(request):
    health_features = [
        "diabetes", "blood_pressure", "heart_disease",
        "kidney_disease", "liver_disease", "lung_disease",
        "hiv_aids", "hepatitis", "obesity",
        "cancer_history", "smoking_history", "alcohol_history",
        "any_surgery", "skin_damage"
    ]

    organs = AddOrgan.objects.all()

    try:
        donor = DonorDetails.objects.get(user=request.user)
    except DonorDetails.DoesNotExist:
        donor = None

    if request.method == "POST":
        form = LivingOrganDonationForm(request.POST)

        if form.is_valid():
            if donor:
                living_donation = form.save(commit=False)
                living_donation.donor = donor

                # 🔁 Convert "Yes"/"No" to True/False for health fields
                for feature in health_features:
                    value = request.POST.get(feature)
                    setattr(living_donation, feature, True if value == "Yes" else False)

                living_donation.save()

                # ✅ Multiple File Upload
                files = request.FILES.getlist("files")
                for file in files:
                    LivingDonationDocument.objects.create(donation=living_donation, file=file)

                messages.success(request, "✅ Organ donation request submitted successfully with documents!")
                return redirect('success_page1')
            else:
                form.add_error(None, "❌ Error: No donor profile found for this user.")
        else:
            messages.error(request, "❌ There was an error in your submission. Please check the form.")
    else:
        form = LivingOrganDonationForm()

    return render(request, "living_donation.html", {
        "form": form,
        "health_features": health_features,
        "organs": organs,
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipient, RecipientOrganNeeded, AddOrgan, MedicalDocument
@login_required
def organ_request(request):
    try:
        recipient = Recipient.objects.get(user=request.user)
    except Recipient.DoesNotExist:
        messages.error(request, "❌ No recipient profile found. Please complete your profile.")
        return redirect("recipient_profile")

    organs = AddOrgan.objects.all()

    health_features = [
        "diabetes", "blood_pressure", "heart_disease",
        "kidney_disease", "liver_disease", "lung_disease",
        "hiv_aids", "hepatitis", "cancer_history",
        "autoimmune_disease", "neurological_disorder", "blood_disorder",
        "obesity", "smoking_history", "alcohol_history", "previous_transplant"
    ]

    if request.method == "POST":
        organ_id = request.POST.get("organ_neededrequest")
        urgency_level = request.POST.get("urgency_level")  # ✅ Get urgency level from form
        files = request.FILES.getlist("files")  # ✅ Get multiple uploaded files

        if not organ_id:
            messages.error(request, "❌ Please select an organ.")
            return redirect("organ_request")

        try:
            organ_needed = AddOrgan.objects.get(id=organ_id)
        except AddOrgan.DoesNotExist:
            messages.error(request, "❌ Invalid organ selection.")
            return redirect("organ_request")

        # ✅ Validate urgency level
        valid_urgency_levels = ["Low", "Moderate", "High"]
        if urgency_level not in valid_urgency_levels:
            messages.error(request, "❌ Invalid urgency level selection.")
            return redirect("organ_request")

        # ✅ Create the organ request
        organ_request = RecipientOrganNeeded.objects.create(
            recipient=recipient,
            organ_neededrequest=organ_needed,
            urgency_level=urgency_level,  # ✅ Store the urgency level correctly
            **{feature: request.POST.get(feature) == "Yes" for feature in health_features}
        )

        # ✅ Save multiple medical documents if uploaded
        if files:
            for file in files:
                MedicalDocument.objects.create(
                    organ_request=organ_request,
                    file=file
                )

        messages.success(request, "✅ Organ request and documents submitted successfully!")
        return redirect("success_page2")

    return render(request, "organ_request.html", {
        "organs": organs,
        "health_features": health_features,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonorDetails, DeceasedDonation, DeceasedDonationFile, AddOrgan
from .forms import DeceasedDonationForm

@login_required
def deceased_donation(request):
    health_features = [
        "diabetes", "hypertension", "heart_disease",
        "kidney_disease", "liver_disease", "cancer_history",
        "hiv_aids", "hepatitis", "smoking_history",
        "alcohol_history", "major_surgeries"
    ]

    try:
        donor = DonorDetails.objects.get(user=request.user)
    except DonorDetails.DoesNotExist:
        donor = None

    # Fetch admin-added organs
    organs = AddOrgan.objects.all()

    if request.method == "POST":
        form = DeceasedDonationForm(request.POST, request.FILES)

        if form.is_valid():
            if donor:
                deceased_donation = form.save(commit=False)
                deceased_donation.donor = donor
                deceased_donation.save()

                # ✅ Correct file upload handling
                files = request.FILES.getlist("files")  
                for file in files:
                    DeceasedDonationFile.objects.create(donation=deceased_donation, file=file)

                messages.success(request, "✅ Deceased donation request submitted successfully with documents!")
                return redirect('success_page1')
            else:
                form.add_error(None, "❌ Error: No donor profile found for this user.")
        else:
            messages.error(request, "❌ Form submission error. Please check your inputs.")

    else:
        form = DeceasedDonationForm()

    return render(request, "deceased_donation.html", {
        "form": form,
        "organs": organs,
        "health_features": health_features,
    })


def recipient_notifications(request):
    return render(request, 'recipient_notifications.html')  # Create a template for this

def upload_documents(request):
    return render(request,'uplaod_documents.html')


from django.db.models.signals import post_save
from django.dispatch import receiver
from newapp.models import CustomUser
from newapp.models import DonorDetails

@receiver(post_save, sender=CustomUser)
def create_donor_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "donor_profile"):
        DonorDetails.objects.create(user=instance, full_name=instance.username, email=instance.email)

def success_page(request):
    return render(request, 'success.html')  # Make sure you have a 'success.html' template

def success_page1(request):
    return render(request, 'success1.html')  # Make sure you have a 'success.html' template

def success_page2(request):
    return render(request, 'success2.html')  # Make sure you have a 'success.html' template

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Add Organ View


# List Organs View
from django.shortcuts import render
from newapp.models import AddOrgan
from django.db.models import Count

def list_organs(request):
    organs_with_donor_counts = AddOrgan.objects.annotate(
        donor_count=Count('deceased_donations')
    ).values('name', 'donor_count')

    return render(request, 'list_organs.html', {'organ_donor_counts': organs_with_donor_counts})


# List Donors View
from django.shortcuts import render
from .models import DonorDetails

def list_donors(request):
    donors = DonorDetails.objects.all()  # Fetch all donors
    return render(request, 'list_donors.html', {'donors': donors})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import DonorDetails

def delete_donor(request, donor_id):
    if request.method == "DELETE":
        donor = get_object_or_404(DonorDetails, id=donor_id)
        donor.delete()
        return JsonResponse({"success": True, "message": "Donor deleted successfully"})
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


# # List Recipients View
# def list_recipients(request):
#     recipients = Recipient.objects.all()  # Fetch all recipients
#     return render(request, 'list_recipients.html', {'recipients': recipients})

from django.shortcuts import render
from django.db.models import Case, When, Value, IntegerField
from .models import RecipientOrganNeeded

def list_recipients(request):
    recipients = RecipientOrganNeeded.objects.select_related('recipient', 'organ_neededrequest').all().order_by(
        Case(
            When(urgency_level="Critical", then=Value(1)),
            When(urgency_level="High", then=Value(2)),
            When(urgency_level="Moderate", then=Value(3)),
            When(urgency_level="Low", then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )
    )
    
    return render(request, 'list_recipients.html', {'recipients': recipients})


# List Hospital Staff View
from django.shortcuts import render
from newapp.models import HospitalDetail

def list_hospitals(request):
    hospitals = HospitalDetail.objects.all()  # Fetch all hospitals
    return render(request, 'list_hospitals.html', {'hospitals': hospitals})

def matching_status(request):
    recipients = Recipient.objects.all()  # Fetch all recipients
    return render(request, "matching_status.html", {"recipients": recipients})

def update_recipient_status(request, recipient_id):
    recipient = Recipient.objects.get(id=recipient_id)
    
    if request.method == "POST":
        new_status = request.POST.get("matching_status")
        if new_status in ["Pending", "Matched", "Transplanted", "Rejected"]:  # Only valid statuses
            recipient.matching_status = new_status
            recipient.save()
            return redirect("list_recipients")

    return render(request, "update_recipient_status.html", {"recipient": recipient})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipient,HospitalDetail
from django.core.exceptions import ObjectDoesNotExist  

def hospital_dashboard(request):
    recipients = Recipient.objects.all()
    living_donations = LivingOrganDonation.objects.all()
    deceased_donations = DeceasedDonation.objects.all()

    context = {
        "recipients": recipients,
        "living_donations": living_donations,
        "deceased_donations": deceased_donations,
    }
    return render(request, "hospital_dashboard.html", context)

def approve_donation(request, donation_id):
    donation = get_object_or_404(LivingOrganDonation, id=donation_id)
    
    if request.method == "POST":
        approval_status = request.POST.get("approval_status") == "on"
        donation.approval_status = approval_status
        donation.save()
        return redirect("hospital_staff_dashboard")

    return render(request, "approve_donation.html", {"donation": donation})

# ✅ List of Living Donors
def list_living_donations(request):
    living_donors = LivingOrganDonation.objects.all()
    return render(request, "list_living_donations.html", {"living_donors": living_donors})

# ✅ List of Deceased Donors
def list_deceased_donations(request):
    deceased_donors = DeceasedDonation.objects.all()
    return render(request, "list_deceased_donations.html", {"deceased_donors": deceased_donors})

# ✅ Approve Living Donor
def approve_living_donor(request, donor_id):
    donor = get_object_or_404(LivingOrganDonation, id=donor_id)
    donor.approved = True  # Mark as approved
    donor.save()
    return redirect("list_living_donations")  # Redirect back to list

from django.shortcuts import render
from .models import DonorDetails, LivingOrganDonation, DeceasedDonation

def registered_donors(request):
    donors = DonorDetails.objects.all()

    donor_data = {}

    for donor in donors:
        donor_name = donor.full_name
        if donor_name not in donor_data:
            donor_data[donor_name] = {
                "full_name": donor.full_name,
                "blood_type": donor.blood_type,
                "donations": []
            }
        
        # Fetch living organ donations
        living_donations = LivingOrganDonation.objects.filter(donor=donor)
        for living in living_donations:
            donor_data[donor_name]["donations"].append({
                "organ": living.organ, "type": "Living Donor"
            })
        
        # Fetch deceased organ donations
        deceased_donations = DeceasedDonation.objects.filter(donor=donor)
        for deceased in deceased_donations:
            donor_data[donor_name]["donations"].append({
                "organ": deceased.organ, "type": "Deceased Donor"
            })

    return render(request, 'registered_donors.html', {"donors": donor_data.values()})

# ✅ Verify Deceased Donor
def verify_deceased_donor(request, donor_id):
    donor = get_object_or_404(DeceasedDonation, id=donor_id)
    donor.verified = True  # Mark as verified
    donor.save()
    return redirect("list_deceased_donations")  # Redirect back to list

# ✅ Delete Living Donor
def delete_living_donor(request, donor_id):
    donor = get_object_or_404(LivingOrganDonation, id=donor_id)
    donor.delete()
    return redirect("list_living_donations")  # Redirect back to list

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RecipientOrganNeeded, Recipient

@login_required
def view_requests(request):
    try:
        recipient = request.user.recipient_profile  # Use related_name from Recipient model
        requests = RecipientOrganNeeded.objects.filter(recipient=recipient)
        return render(request, 'view_requests.html', {'requests': requests})
    except Recipient.DoesNotExist:
        return render(request, 'view_requests.html', {'error': "Recipient profile not found."})




# ✅ Delete Deceased Donor
def delete_deceased_donor(request, donor_id):
    donor = get_object_or_404(DeceasedDonation, id=donor_id)
    donor.delete()
    return redirect("list_deceased_donations")  # Redirect back to list

from django.shortcuts import get_object_or_404


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HospitalDetailForm
from .models import HospitalDetail

@login_required
def hospital_details(request):
    """ Handles hospital registration and updates. """
    try:
        hospital_detail = request.user.hospital_detail  # Fetch hospital details if they exist
    except HospitalDetail.DoesNotExist:
        hospital_detail = None

    if request.method == 'POST':
        form = HospitalDetailForm(request.POST, instance=hospital_detail)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.user = request.user
            detail.save()
            return redirect('success_page')  # ✅ Redirect to success page
    else:
        form = HospitalDetailForm()

    return render(request, 'hospital_details.html', {'form': form})


from .models import TransplantMatch

@login_required
def transplant_matching(request):
    matches = TransplantMatch.objects.all()
    return render(request, 'transplant_matching.html', {'matches': matches})

from django.shortcuts import render
from .models import OrganTracking  # Ensure the model is correctly imported

def organ_tracking(request):
    organs = OrganTracking.objects.all()  # Fetch all organ tracking data
    return render(request, 'organ_tracking.html', {'organs': organs})

@login_required
def emergency_requests(request):
    urgent_requests = RecipientOrganNeeded.objects.filter(urgency_level="High")
    return render(request, 'emergency_requests.html', {'urgent_requests': urgent_requests})

@login_required
def hospital_reports(request):
    return render(request, 'hospital_reports.html')


@login_required
def assign_donor_to_hospital(request, donor_id, hospital_id):
    donor = get_object_or_404(DonorDetails, id=donor_id)
    hospital = get_object_or_404(HospitalDetail, id=hospital_id)
    donor.hospital = hospital
    donor.save()
    return redirect('list_donors')

# Assign a recipient to a hospital
@login_required
def assign_recipient_to_hospital(request, recipient_id, hospital_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    hospital = get_object_or_404(HospitalDetail, id=hospital_id)
    recipient.hospital = hospital
    recipient.save()
    return redirect('list_recipients')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import DeceasedDonation, AddOrgan

@login_required
def donor_list_by_organ(request):
    # Fetch all donated organs and count the number of donors for each organ
    organ_donor_counts = DeceasedDonation.objects.values('organ__name').annotate(donor_count=Count('donor')).order_by('-donor_count')

    # Fetch the list of donors grouped by organ
    organ_donors = {}
    for organ in AddOrgan.objects.all():
        donors = DeceasedDonation.objects.filter(organ=organ).values('donor__name', 'donor__email')
        organ_donors[organ.name] = donors

    return render(request, "donor_list_by_organ.html", {
        "organ_donor_counts": organ_donor_counts,
        "organ_donors": organ_donors,
    })


from django.db.models import Count


def admin_dashboard(request):
    # Count donors per organ
    organ_donor_counts = AddOrgan.objects.annotate(donor_count=Count('deceased_donations'))

    context = {
        "organ_donor_counts": organ_donor_counts
    }
    return render(request, "admin_dashboard.html", context)


from django.shortcuts import render, get_object_or_404
from newapp.models import DonorDetails, Recipient, DeceasedDonation

def match_result(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)

    # Find donors with compatible blood type and organ availability
    matched_donors = DonorDetails.objects.filter(
        blood_type=recipient.blood_type,
        deceased_donations__organ=recipient.organ_needed
    )

    return render(request, 'admin/match_results.html', {
        'recipient': recipient,
        'matched_donors': matched_donors
    })


from django.shortcuts import render
from .models import LivingOrganDonation, DeceasedDonation

def available_organs(request):
    living_organs = LivingOrganDonation.objects.filter(availability_status="Available")
    deceased_organs = DeceasedDonation.objects.filter(availability_status="Available")

    context = {
        'living_organs': living_organs,
        'deceased_organs': deceased_organs,
    }
    return render(request, 'available_organs.html', context)

from django.shortcuts import render
from .models import LivingOrganDonation, DeceasedDonation

def available_donors(request):
    living_organs = LivingOrganDonation.objects.filter(availability_status="Available")
    deceased_organs = DeceasedDonation.objects.filter(availability_status="Available")

    context = {
        'living_organs': living_organs,
        'deceased_organs': deceased_organs,
    }
    return render(request, 'available_donors.html', context)
from django.shortcuts import render, get_object_or_404
from .models import LivingOrganDonation, Recipient

def match_donors(recipient):
    """Find a compatible donor for a given recipient."""
    matched_donors = LivingOrganDonation.objects.filter(
        organ_type=recipient.organ_needed,  # Match organ type
        blood_group=recipient.blood_group,  # Match blood type
        availability_status="Available"     # Ensure organ is available
    ).order_by('date_added')  # Prioritize by earliest donor

    return matched_donors  # Returns a list of matching donors

def request_organ(request, recipient_id):
    """Handles organ requests from recipients."""
    recipient = get_object_or_404(Recipient, id=recipient_id)
    matched_donors = match_donors(recipient)

    if matched_donors.exists():
        selected_donor = matched_donors.first()  # Select the first available match
        RecipientOrganNeeded.objects.create(
            recipient=recipient,
            organ=selected_donor,
            status="Pending"
        )
        selected_donor.availability_status = "Pending"
        selected_donor.save()
    
    return render(request, 'request_confirmation.html', {'matched_donors': matched_donors})

from django.shortcuts import render, get_object_or_404
from .models import TransplantAllocation
from django.http import HttpResponse

# View to list all transplant organ matches
def match_list(request):
    matches = TransplantAllocation.objects.all()
    return render(request, 'match_list.html', {'matches': matches})

# View to display details of a specific match
def match_detail(request, match_id):
    match = get_object_or_404(TransplantAllocation, id=match_id)
    return render(request, 'match_detail.html', {'match': match})


from django.shortcuts import render, redirect
from .models import TransplantAllocation, DeceasedDonation, RecipientOrganNeeded

def create_match(request):
    if request.method == 'POST':
        donor_id = request.POST.get('donor')
        recipient_id = request.POST.get('recipient')
        status = request.POST.get('status')

        donor = DeceasedDonation.objects.get(id=donor_id)
        recipient = RecipientOrganNeeded.objects.get(id=recipient_id)

        # Create and save the new match
        TransplantAllocation.objects.create(
            donor=donor,
            recipient=recipient,
            status=status
        )

        return redirect('match_list')  # Redirect to the match list after creation

    # Fetch all donors and recipients for the form
    donors = DeceasedDonation.objects.all()
    recipients = RecipientOrganNeeded.objects.all()

    # Debugging: Print the recipients and check if full_name is accessed correctly
    print(f"Recipients count: {recipients.count()}")
    for recipient in recipients:
        print(f"Recipient Name: {recipient.recipient.full_name}")  # Access full_name of linked recipient

    return render(request, 'create_match.html', {'donors': donors, 'recipients': recipients})

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from newapp.models import RecipientOrganNeeded, LivingOrganDonation, DeceasedDonation, TransplantAllocation

# Matching function (same as before)
def match_donors_and_recipients(request):
    matched_pairs = []
    recipients = RecipientOrganNeeded.objects.all()

    for recipient in recipients:
        organ_needed = recipient.organ_neededrequest
        blood_type = recipient.recipient.blood_type

        # 1️⃣ Match with LIVING DONORS
        living_donor = LivingOrganDonation.objects.filter(
            organ=organ_needed, donor__blood_type=blood_type, availability_status="Available"
        ).first()

        if living_donor:
            match = TransplantAllocation.objects.create(
                donor_content_type=ContentType.objects.get_for_model(LivingOrganDonation),
                donor_object_id=living_donor.id,
                recipient=recipient,
                organ=organ_needed,
                match_date=timezone.now(),
                status="Pending"
            )
            matched_pairs.append(match)

            # Update donor status
            living_donor.availability_status = "Transplanted"
            living_donor.save()

            continue

        # 2️⃣ Match with DECEASED DONORS
        deceased_donor = DeceasedDonation.objects.filter(
            organ=organ_needed, availability_status="Available"
        ).order_by('-id').first()

        if deceased_donor:
            match = TransplantAllocation.objects.create(
                donor_content_type=ContentType.objects.get_for_model(DeceasedDonation),
                donor_object_id=deceased_donor.id,
                recipient=recipient,
                organ=organ_needed,
                match_date=timezone.now(),
                status="Pending"
            )
            matched_pairs.append(match)

            # Update donor status
            deceased_donor.availability_status = "Transplanted"
            deceased_donor.save()

    return redirect('match_list')

# ✅ Confirm transplant and update status
def confirm_transplant(request, match_id):
    match = get_object_or_404(TransplantAllocation, id=match_id)

    if match.status == "Pending":
        match.status = "Completed"
        match.save()
        messages.success(request, "Transplant confirmed successfully!")
    else:
        messages.error(request, "This transplant is already completed.")

    return redirect('match_list')

# ✅ Display matches in the template
def match_list(request):
    matches = TransplantAllocation.objects.all()
    return render(request, 'matches.html', {'matches': matches})



def complete_transplant(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    match = OrganMatch.objects.filter(recipient=recipient).first()

    if match:
        match.status = 'completed'
        match.save()

        # Update recipient status
        recipient.matching_status = 'Transplanted'
        recipient.save()

        messages.success(request, f"Transplant completed for {recipient.full_name}!")
    else:
        messages.error(request, "No match found for this recipient.")

    return redirect('list_recipients')











# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from .models import Recipient, OrganMatch
# from newapp.models import LivingOrganDonation, DeceasedDonation

# def match_donor_to_recipient(request, recipient_id):
#     recipient = get_object_or_404(Recipient, id=recipient_id)
#     print(f"🔍 Finding donor for recipient: {recipient.full_name}")

#     # Ensure recipient is still pending before matching
#     if recipient.matching_status != 'Pending':
#         messages.warning(request, 'Recipient is already matched or transplanted.')
#         return redirect('list_recipients')

#     # Retrieve the recipient's organ request
#     recipient_organ_needed = recipient.organs_needed.first()
#     if not recipient_organ_needed:
#         messages.error(request, 'No organ request found for this recipient.')
#         return redirect('list_recipients')

#     required_organ_name = recipient_organ_needed.organ_neededrequest.name

#     # 1) Try to find a Living Organ Donation
#     living_donation = LivingOrganDonation.objects.filter(
#         organ__name=required_organ_name,
#         availability_status="Available",
#         donor__blood_type=recipient.blood_type
#     ).first()

#     if living_donation:
#         # We found a living donor
#         print(f"✅ Found a living donor: {living_donation.donor.full_name}")
#         create_organ_match(recipient, living_donation, donation_type="living")
#         messages.success(request, f"Living donor {living_donation.donor.full_name} matched with {recipient.full_name}.")
#         return redirect('list_recipients')

#     # 2) If no living donor found, try DeceasedDonation
#     deceased_donation = DeceasedDonation.objects.filter(
#         organ__name=required_organ_name,
#         availability_status="Available"
#     ).first()

#     if deceased_donation:
#         # We found a deceased donation
#         print(f"✅ Found a deceased donor record (ID: {deceased_donation.id})")
#         create_organ_match(recipient, deceased_donation, donation_type="deceased")
#         messages.success(request, f"Deceased donor organ matched with {recipient.full_name}.")
#     else:
#         print("❌ No matching living or deceased donor found.")
#         messages.error(request, 'No matching donor found (living or deceased).')

#     return redirect('list_recipients')












from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Recipient, OrganMatch
from newapp.models import LivingOrganDonation, DeceasedDonation

def create_organ_match(recipient, donation, donation_type):
    # Create the OrganMatch record
    OrganMatch.objects.create(
        recipient=recipient,
        donor=donation.donor,
        donation_type=donation_type,
        organ_name=donation.organ.name
    )
    # Update recipient and donation status
    recipient.matching_status = "Matched"
    recipient.save()

    # Reserve the donation to prevent reuse
    donation.availability_status = "Reserved"
    donation.save()


def match_donor_to_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    print(f"🔍 Finding donor for recipient: {recipient.full_name}")

    # Ensure recipient is still pending before matching
    if recipient.matching_status != 'Pending':
        messages.warning(request, 'Recipient is already matched or transplanted.')
        return redirect('list_recipients')

    # Retrieve the recipient's organ request
    recipient_organ_needed = recipient.organs_needed.first()
    if not recipient_organ_needed:
        messages.error(request, 'No organ request found for this recipient.')
        return redirect('list_recipients')

    required_organ_name = recipient_organ_needed.organ_neededrequest.name
    required_blood_type = recipient.blood_type

    # 1) Try to find a suitable Living Donor (available and matching blood type)
    living_donation = LivingOrganDonation.objects.filter(
        organ__name=required_organ_name,
        donor__blood_type=required_blood_type,
        availability_status="Available"
    ).exclude(availability_status__in=["Reserved", "Transplanted"]).first()

    if living_donation:
        print(f"✅ Found a living donor: {living_donation.donor.full_name}")
        create_organ_match(recipient, living_donation, donation_type="living")
        messages.success(request, f"Living donor {living_donation.donor.full_name} matched with {recipient.full_name}.")
        return redirect('list_recipients')

    # 2) If no living donor found, try Deceased Donation (available)
    deceased_donation = DeceasedDonation.objects.filter(
        organ__name=required_organ_name,
        availability_status="Available"
    ).exclude(availability_status__in=["Reserved", "Transplanted"]).first()

    if deceased_donation:
        print(f"✅ Found a deceased donor organ (Donor: {deceased_donation.donor.full_name})")
        create_organ_match(recipient, deceased_donation, donation_type="deceased")
        messages.success(request, f"Deceased donor organ matched with {recipient.full_name}.")
    else:
        print("❌ No matching living or deceased donor found.")
        messages.error(request, 'No matching donor found (living or deceased).')

    return redirect('list_recipients')





def create_organ_match(recipient, donation, donation_type="living"):
    """
    Creates an OrganMatch record for either a living or deceased donation.
    Updates the recipient status and marks the donation as reserved.
    """
    if donation_type == "living":
        donor = donation.donor  # Living donation has a direct donor

    elif donation_type == "deceased":
        donor = donation.donor  # Correctly referencing deceased donor

    # Ensure donor exists before creating a match
    if donor:
        OrganMatch.objects.create(donor=donor, recipient=recipient, status='approved')
        recipient.matching_status = 'Matched'
        recipient.save()

        # Mark the donation as reserved
        donation.availability_status = "Reserved"
        donation.save()
    else:
        print("❌ Error: No valid donor found for donation type:", donation_type)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from newapp.models import LivingDonationDocument, DeceasedDonationFile

def admin_legal_documents(request):
    living_docs = LivingDonationDocument.objects.all().order_by('-uploaded_at')
    deceased_docs = DeceasedDonationFile.objects.all().order_by('-uploaded_at')
    return render(request, 'admin_legal_documents.html', {
        'living_docs': living_docs,
        'deceased_docs': deceased_docs,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from newapp.models import LivingDonationDocument, DeceasedDonationFile

def verify_living_doc(request, doc_id):
    doc = get_object_or_404(LivingDonationDocument, id=doc_id)
    if not doc.verified:
        doc.verified = True
        doc.save()
        messages.success(request, "Living donation document verified!")
    else:
        messages.info(request, "This document is already verified.")
    return redirect('admin_legal_documents')

def verify_deceased_doc(request, doc_id):
    doc = get_object_or_404(DeceasedDonationFile, id=doc_id)
    if not doc.verified:
        doc.verified = True
        doc.save()
        messages.success(request, "Deceased donation document verified!")
    else:
        messages.info(request, "This document is already verified.")
    return redirect('admin_legal_documents')


def admin_recipient_documents(request):
    # Query your recipient legal documents.
    # This assumes you have a model similar to LegalDocument for recipients.
    recipient_docs = MedicalDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'admin_recipient_documents.html', {'recipient_docs': recipient_docs})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import MedicalDocument  # adjust the model name if needed

def verify_recipient_doc(request, doc_id):
    doc = get_object_or_404(MedicalDocument, id=doc_id)
    if not doc.verified:
        doc.verified = True
        doc.save()
        messages.success(request, "Recipient document verified!")
    else:
        messages.info(request, "This document is already verified.")
    return redirect('admin_recipient_documents')


# from django.shortcuts import render
# from .models import DonorDetails, LivingOrganDonation, DeceasedDonation, Notification, Transplant

# def donor_dashboard(request):
#     donor = DonorDetails.objects.filter(user=request.user).first()

#     living_donations = LivingOrganDonation.objects.filter(donor=donor)
#     deceased_donations = DeceasedDonation.objects.filter(donor=donor)

#     donation_count = living_donations.count() + deceased_donations.count()
#     notifications = Notification.objects.filter(user=request.user, status="read")
#     notification_count = notifications.count()

#     # 🔹 Fetch the transplant status for this donor
#     transplant = Transplant.objects.filter(donor=donor).order_by('-transplant_date').first()

#     context = {
#         "donor": donor,
#         "living_donations": living_donations,
#         "deceased_donations": deceased_donations,
#         "donation_count": donation_count,
#         "notification_count": notification_count,
#         "transplant": transplant,  # Add transplant data
#     }
#     return render(request, "donor_dashboard.html", context)
from django.shortcuts import render
from .models import DonorDetails, LivingOrganDonation, DeceasedDonation, Notification, Transplant, Compensation

def donor_dashboard(request):
    donor = DonorDetails.objects.filter(user=request.user).first()

    living_donations = LivingOrganDonation.objects.filter(donor=donor)
    deceased_donations = DeceasedDonation.objects.filter(donor=donor)

    donation_count = living_donations.count() + deceased_donations.count()
    notifications = Notification.objects.filter(user=request.user, status="unread")
    notification_count = notifications.count()

    # 🔹 Fetch the transplant status for this donor
    transplant = Transplant.objects.filter(donor=donor).order_by('-transplant_date').first()

    # 🔹 Fetch the compensation status for this donor
    compensation = Compensation.objects.filter(donor=donor, approved=True).first()

    context = {
        "donor": donor,
        "living_donations": living_donations,
        "deceased_donations": deceased_donations,
        "donation_count": donation_count,
        "notification_count": notification_count,
        "transplant": transplant,  # Add transplant data
        "compensation": compensation,  # Add payment data
    }
    return render(request, "donor_dashboard.html", context)

from django.shortcuts import render

def donor_transactions(request):
    return render(request, "donor_transactions.html")

from django.shortcuts import render
from .models import Compensation, DonorDetails

def compensation_status(request):
    donor = DonorDetails.objects.filter(user=request.user).first()
    compensation = Compensation.objects.filter(donor=donor).first()

    print("DEBUG: Donor Object:", donor)
    print("DEBUG: Compensation Object:", compensation)

    context = {
        "compensation": compensation
    }
    return render(request, "compensation_status.html", context)


from django.shortcuts import render
from .models import Compensation, DonorDetails

def donor_transactions(request):
    donor = DonorDetails.objects.filter(user=request.user).first()
    compensation = Compensation.objects.filter(donor=donor).first()

    print("DEBUG: Donor Object ->", donor)
    print("DEBUG: Compensation Object ->", compensation)

    context = {
        "compensation": compensation
    }
    return render(request, "donor_transactions.html", context)


def view_donations(request):
    donor = DonorDetails.objects.filter(user=request.user).first()
    living_donations = LivingOrganDonation.objects.filter(donor=donor)
    deceased_donations = DeceasedDonation.objects.filter(donor=donor)

    context = {
        "living_donations": living_donations,
        "deceased_donations": deceased_donations,
    }
    return render(request, "view_donations.html", context)

from django.shortcuts import render, get_object_or_404
from .models import DonorDetails, OrganMatch

def check_matches(request, donor_id):
    donor = get_object_or_404(DonorDetails, id=donor_id)
    matched_recipients = OrganMatch.objects.filter(donor=donor)

    return render(request, 'check_matches.html', {
        'donor': donor,
        'matched_recipients': matched_recipients
    })

from django.shortcuts import render, get_object_or_404
from .models import OrganMatch, LivingOrganDonation, DeceasedDonation

def matching_status(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    matches = OrganMatch.objects.filter(recipient=recipient).select_related('donor')

    matched_data = []
    for match in matches:
        # Find if the donor is in LivingOrganDonation
        living_donation = LivingOrganDonation.objects.filter(donor=match.donor).first()
        deceased_donation = DeceasedDonation.objects.filter(donor=match.donor).first()

        organ_name = None
        donation_type = None

        if living_donation:
            organ_name = living_donation.organ.name
            donation_type = "Living"
        elif deceased_donation:
            organ_name = deceased_donation.organ.name
            donation_type = "Deceased"

        matched_data.append({
            "donor": match.donor.full_name,
            "organ_name": organ_name,
            "donation_type": donation_type
        })

    return render(request, "matching_status.html", {
        "recipient": recipient,
        "matches": matched_data
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from .forms import NotificationForm

@login_required
def recipient_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')  # Get notifications for logged-in recipient

    context = {'notifications': notifications}
    return render(request, 'recipient_notifications.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def donor_notifications(request):
    """ Display notifications for the logged-in donor """
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "donor_notifications.html", {"notifications": notifications})


# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import Notification

# @login_required
# def get_notifications(request):
#     if request.user.user_type != 'recipient':  # Ensure only recipients can access
#         return JsonResponse({'error': 'Only recipients can view notifications'}, status=403)

#     notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

#     # ✅ Manual conversion of queryset to JSON format
#     data = [
#         {
#             'id': notification.id,
#             'user': notification.user.id,
#             'message': notification.message,
#             'status': notification.status,
#             'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format date manually
#         }
#         for notification in notifications
#     ]

#     return JsonResponse(data, safe=False)  # Return as JSON

# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from .models import Notification

# User = get_user_model()

# @csrf_exempt  # ✅ Allow POST requests (for testing without CSRF token)
# def send_notification(request):
#     if request.method == 'POST':
#         admin_user = request.user

#         if admin_user.user_type != 'admin':
#             return JsonResponse({'error': 'Only admin can send notifications'}, status=403)

#         recipient_id = request.POST.get('recipient_id')
#         message = request.POST.get('message')

#         if not recipient_id or not message:
#             return JsonResponse({'error': 'Recipient ID and message are required'}, status=400)

#         recipient = get_object_or_404(User, id=recipient_id, user_type='recipient')

#         # ✅ Manually create and save notification
#         notification = Notification(user=recipient, message=message)
#         notification.save()

#         return JsonResponse({'message': 'Notification sent successfully'})
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from .models import Notification

# def mark_notification_as_read(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id, user=request.user)

#     # ✅ Manually update notification status
#     notification.status = 'read'
#     notification.save()

#     return JsonResponse({'message': 'Notification marked as read'})


# import json
# def admin_notifications(request):
#     if request.method == "POST":
#         print(f"Received POST data: {json.dumps(request.POST.dict())}")  # Debugging

#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             notification = form.save(commit=False)

#             recipient_id = request.POST.get("recipient")
#             print(f"Selected Recipient ID: {recipient_id}")  # Debugging

#             if recipient_id:
#                 try:
#                     recipient = CustomUser.objects.get(id=recipient_id, user_type='recipient')
#                     notification.user = recipient
#                     print(f"✅ Recipient Found: {recipient.username}")  # Debugging
#                 except CustomUser.DoesNotExist:
#                     messages.error(request, "❌ Invalid recipient selected.")
#                     return redirect("admin_notifications")

#             notification.sender = request.user  
#             notification.save()
#             messages.success(request, "✅ Notification sent successfully!")
#             return redirect("admin_notifications")

#     else:
#         form = NotificationForm()

#     notifications = Notification.objects.all()
#     return render(request, "admin_notifications.html", {"form": form, "notifications": notifications})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@login_required
def get_notifications(request):
    if request.user.user_type != 'recipient' and request.user.user_type != 'donor':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    data = [
        {
            'id': notification.id,
            'message': notification.message,
            'status': notification.status,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for notification in notifications
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def send_notification(request):
    if request.method == 'POST':
        admin_user = request.user

        if admin_user.user_type != 'admin':
            return JsonResponse({'error': 'Only admins can send notifications'}, status=403)

        recipient_id = request.POST.get('recipient_id')
        message = request.POST.get('message')

        if not recipient_id or not message:
            return JsonResponse({'error': 'Recipient ID and message are required'}, status=400)

        recipient = get_object_or_404(User, id=recipient_id)

        # ✅ Only allow notifications to recipients or living donors
        if recipient.user_type == 'recipient' or (recipient.user_type == 'donor' and recipient.donordetails.living_donor):
            notification = Notification(user=recipient, sender=admin_user, message=message)
            notification.save()
            return JsonResponse({'message': 'Notification sent successfully'})
        else:
            return JsonResponse({'error': 'Admins can only notify recipients or living donors'}, status=403)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.status = 'read'
    notification.save()
    return JsonResponse({'message': 'Notification marked as read'})

# from django.shortcuts import render
# from newapp.models import CustomUser, DonorDetails, Recipient, Notification

# def admin_notifications(request):
#     # Fetch recipients linked to CustomUser
#     recipients = Recipient.objects.select_related("user").all()

#     # Fetch living donors (users who have a donor profile and listed living organ donations)
#     living_donors = DonorDetails.objects.filter(living_donations__isnull=False).select_related("user").distinct()

#     return render(request, "admin_notifications.html", {
#         "recipients": recipients,
#         "living_donors": living_donors,
#         "notifications": Notification.objects.all().order_by("-created_at"),
#     })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from newapp.models import CustomUser, DonorDetails, Notification

@login_required
def admin_notifications(request):
    recipients = Recipient.objects.select_related("user").all()
    living_donors = DonorDetails.objects.filter(living_donations__isnull=False).distinct()

    if request.method == "POST":
        user_id = request.POST.get("user_id")  # Get recipient/living donor ID
        message = request.POST.get("message")  # Get notification message
        sender = request.user  # Logged-in admin user as sender

        if user_id and message:
            try:
                user = CustomUser.objects.get(id=user_id)

                # Create Notification with sender
                Notification.objects.create(
                    sender=sender,
                    user=user,
                    message=message,
                    status="unread"
                )

                messages.success(request, "Notification sent successfully!")
                return redirect("admin_notifications")

            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid recipient or donor selected.")

        else:
            messages.error(request, "Please select a user and enter a message.")

    return render(request, "admin_notifications.html", {
        "recipients": recipients,
        "living_donors": living_donors,
        "notifications": Notification.objects.all().order_by("-created_at"),
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from newapp.models import Notification

@login_required
def recipient_notifications(request):
    """Display notifications for the recipient."""
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "recipient_notifications.html", {"notifications": notifications})

@login_required
def respond_to_notification(request, notification_id):
    """Handle recipient's response (Confirm/Reject)."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    if request.method == "POST":
        response = request.POST.get("response")

        if response == "confirm":
            notification.response = "confirmed"  # Correct response update
            messages.success(request, "You have confirmed the donation process.")
        elif response == "reject":
            notification.response = "rejected"
            messages.warning(request, "You have rejected the donation process.")

        notification.status = "read"  # ✅ Mark notification as "read" after response
        notification.save()

    return redirect("recipient_notifications")


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from newapp.models import Transplant

@login_required
def confirm_attendance(request, transplant_id):
    transplant = get_object_or_404(Transplant, id=transplant_id)

    # Only allow confirmation if the user is a living donor or recipient
    if request.user == transplant.recipient.user or (transplant.living_donation and request.user == transplant.donor.user):
        transplant.attended = True  
        transplant.success = True  
        transplant.save()
    
    return redirect('transplant_status', transplant_id=transplant.id)

from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render, redirect
from newapp.models import Transplant
from newapp.forms import TransplantForm

# @staff_member_required
# def schedule_transplant(request):
#     """Allows admin to schedule a transplant and assign a recipient, donor, and hospital."""
    
#     if request.method == 'POST':
#         form = TransplantForm(request.POST)
#         if form.is_valid():
#             transplant = form.save(commit=False)
#             transplant.status = 'Scheduled'  # Set status as 'Scheduled'
#             transplant.save()
#             return redirect('transplant_status', transplant_id=transplant.id)  # Redirect to status page

#     else:
#         form = TransplantForm()

#     return render(request, 'schedule_transplant.html', {'form': form})
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from newapp.models import Transplant
from newapp.forms import TransplantForm

@staff_member_required
def schedule_transplant(request):
    """Allows admin to schedule a transplant and store it in the database properly."""

    if request.method == 'POST':
        form = TransplantForm(request.POST)

        if form.is_valid():
            transplant = form.save(commit=False)

            # Set living_donation status
            transplant.living_donation = transplant.donor is not None  
            transplant.status = 'Scheduled'  # Update transplant status
            
            try:
                transplant.save()  # Save to the database
                messages.success(request, "Transplant scheduled successfully!")
                return redirect('transplant_status', transplant_id=transplant.id)  # Redirect after saving
            except Exception as e:
                print("Error saving transplant:", e)  # Debugging output
                messages.error(request, "An error occurred while saving the transplant.")

        else:
            print("Form Errors:", form.errors)  # Debugging output
            messages.error(request, "Invalid form submission. Please check your inputs.")

    else:
        form = TransplantForm()

    return render(request, 'schedule_transplant.html', {'form': form})


@staff_member_required
def mark_transplant_completed(request, transplant_id):
    """ Marks a transplant as completed """
    transplant = get_object_or_404(Transplant, id=transplant_id)
    transplant.status = 'Completed'
    transplant.save()
    return redirect('transplant_status')

from django.shortcuts import render
from newapp.models import Recipient

def admin_dashboard(request):
    recipients = Recipient.objects.all()  # Fetch all recipients
    return render(request, 'admin_dashboard.html', {'recipients': recipients})

from django.shortcuts import render, get_object_or_404
from newapp.models import Transplant

def transplant_status(request, transplant_id):
    transplant = get_object_or_404(Transplant, id=transplant_id)

    context = {
        'transplant': transplant
    }
    return render(request, 'transplant_status.html', context)

@login_required
def confirm_attendance(request, transplant_id):
    transplant = get_object_or_404(Transplant, id=transplant_id)

    updated = False

    # ✅ Allow recipient to confirm attendance
    if transplant.recipient.user == request.user:
        transplant.recipient_attended = True
        updated = True

    # ✅ Allow ONLY living donors to confirm attendance
    elif transplant.living_donation and transplant.donor and transplant.donor.user == request.user:
        transplant.donor_attended = True
        updated = True

    if updated:
        transplant.save()  # Save the attendance confirmation

        # Now, mark the transplant as completed if the conditions are met
        transplant.mark_as_completed()

        messages.success(request, "✅ Attendance confirmed and transplant successfully marked as completed!")
    else:
        messages.error(request, "❌ You are not authorized to confirm attendance.")

    # Redirect to the transplant status page to reflect updated status
    return redirect('transplant_status', transplant_id=transplant.id)

from django.shortcuts import render, get_object_or_404
from .models import Transplant

def transplant_updates(request):
    transplants = Transplant.objects.all()  # Fetch all transplant records
    return render(request, 'transplant_updates.html', {'transplants': transplants})



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Transplant

def mark_transplant_success(request, transplant_id):
    transplant = get_object_or_404(Transplant, id=transplant_id)

    # Check if the transplant is living or deceased
    if transplant.living_donation:
        # For living donation, both recipient and donor must attend
        if transplant.recipient_attended and transplant.donor_attended:
            transplant.status = 'Completed'
            transplant.success = True  # Explicitly set success to True
            transplant.save()  # Save the changes to the database
            messages.success(request, "Transplant successfully marked as completed!")
        else:
            messages.error(request, "Both recipient and donor need to attend for transplant completion.")
    else:
        # For deceased donation, only recipient needs to attend
        if transplant.recipient_attended:
            transplant.status = 'Completed'
            transplant.success = True  # Explicitly set success to True
            transplant.save()  # Save the changes to the database
            messages.success(request, "Transplant successfully marked as completed!")
        else:
            messages.error(request, "Recipient needs to attend for transplant completion.")

    return redirect('transplant_status', transplant_id=transplant.id)



import pdfkit
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from datetime import datetime
from .models import Transplant, LivingOrganDonation, DeceasedDonation, Report

# Set up wkhtmltopdf configuration
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def generate_transplant_report(request, transplant_id):
    if not request.user.is_superuser:  # Ensure only admin can generate reports
        return HttpResponse("Unauthorized", status=403)

    transplant = get_object_or_404(Transplant, id=transplant_id)

    if transplant.status != "Completed":  # Ensure transplant is successful
        return HttpResponse("Report can only be generated after a successful transplant.", status=400)

    donor_name = None  # Default: No donor name displayed

    # Check if the donor belongs to Living or Deceased Donations
    if LivingOrganDonation.objects.filter(donor=transplant.donor).exists():
        donor_name = transplant.donor.full_name  # Show living donor's name

    # Render the template with transplant details
    context = {
        "recipient_name": transplant.recipient.user.username,
        "donor_name": donor_name,  # Will be None for deceased donations
        "transplant_date": transplant.transplant_date,
        "hospital_name": transplant.hospital.name,
        "status": transplant.status,
    }

    html_content = render(request, "report_template.html", context).content.decode("utf-8")

    # Generate PDF using wkhtmltopdf
    report_path = f"media/reports/transplant_report_{transplant_id}.pdf"
    pdfkit.from_string(html_content, report_path, configuration=pdfkit_config)

    # Save report in the database
    Report.objects.create(
        report_type="Transplant Success Report",
        generated_by=request.user,
        file_path=report_path,
        generated_at=datetime.now()
    )

    return HttpResponse(f"Report generated successfully: <a href='/{report_path}' target='_blank'>Download Report</a>")
# Make sure this code saves the document status in the database
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import LivingDonationDocument, DeceasedDonationFile, MedicalDocument

def update_document_status(request, doc_id, doc_type, action):
    if request.method == "POST":
        # Get the document based on the doc_type
        if doc_type == "living":
            doc = get_object_or_404(LivingDonationDocument, id=doc_id)
        elif doc_type == "deceased":
            doc = get_object_or_404(DeceasedDonationFile, id=doc_id)
        elif doc_type == "recipient":
            doc = get_object_or_404(MedicalDocument, id=doc_id)
        else:
            return JsonResponse({"success": False, "error": "Invalid document type."})

        # Handle the action (verify or reject)
        if action == "verify":
            doc.verified = True
            doc.rejected = False
        elif action == "reject":
            doc.rejected = True
            doc.verified = False
        else:
            return JsonResponse({"success": False, "error": "Invalid action."})

        # Save the document after updating
        doc.save()

        # Redirect to the previous page after saving
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return JsonResponse({"success": False, "error": "Invalid request."})

from django.contrib import messages
from .models import Transplant, Compensation

def approve_compensation(request, transplant_id):
    transplant = get_object_or_404(Transplant, id=transplant_id)
    
    # Ensure a compensation record exists
    compensation, created = Compensation.objects.get_or_create(transplant=transplant)

    # Approve the payment
    compensation.approved = True
    compensation.amount = 1000  # Or any logic to calculate amount
    compensation.save()

    messages.success(request, "Compensation approved successfully!")
    return redirect('transplant_updates')  # Redirect back to the page



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transplant, Compensation

@login_required
def add_payment_page(request, transplant_id):
    """ Renders the payment page only for living donors. """
    transplant = get_object_or_404(Transplant, id=transplant_id)

    # Ensure payment is only for living donors
    if not transplant.living_donation or not transplant.donor:
        messages.error(request, "Payment is only applicable for living donors.")
        return redirect("transplant_updates")

    return render(request, "add_payment.html", {"transplant": transplant})


@login_required
def process_payment(request, transplant_id):
    """ Handles the payment submission. """
    transplant = get_object_or_404(Transplant, id=transplant_id)

    # Ensure payment is only for living donors
    if not transplant.living_donation or not transplant.donor:
        messages.error(request, "Payment is only applicable for living donors.")
        return redirect("transplant_updates")

    if request.method == "POST":
        amount = request.POST.get("amount")

        # Validate amount
        if not amount or float(amount) <= 0:
            messages.error(request, "Invalid amount.")
            return redirect("add_payment_page", transplant_id=transplant.id)

        # Save payment
        compensation, created = Compensation.objects.get_or_create(
            donor=transplant.donor,
            defaults={"amount": amount, "approved": True, "approved_by": request.user}
        )

        if not created:
            compensation.amount = amount
            compensation.approved = True
            compensation.approved_by = request.user
            compensation.save()

        messages.success(request, f"Payment of ${amount} approved successfully!")
        return redirect("transplant_updates")

    return redirect("transplant_updates")

from django.shortcuts import render, redirect, get_object_or_404
from .models import DonorDetails, LivingOrganDonation, DeceasedDonation, AddOrgan

def update_profile(request, donor_id):
    donor = get_object_or_404(DonorDetails, id=donor_id)
    living = donor.living_donations.first()
    deceased = donor.deceased_donations.first()
    organs = AddOrgan.objects.all()

    if request.method == "POST":
        # Update donor profile fields
        donor.full_name = request.POST.get("full_name")
        donor.email = request.POST.get("email")
        donor.dob = request.POST.get("dob")
        donor.gender = request.POST.get("gender")
        donor.contact = request.POST.get("contact")
        donor.blood_type = request.POST.get("blood_type")
        donor.address = request.POST.get("address")
        donor.city = request.POST.get("city")
        donor.state = request.POST.get("state")
        donor.country = request.POST.get("country")
        donor.pincode = request.POST.get("pincode")
        donor.save()

        # --- Living Donation ---
        living_organ_id = request.POST.get("living_organ")
        if living_organ_id:
            if not living:
                living = LivingOrganDonation(donor=donor)
            living.organ_id = living_organ_id

            living_fields = [
                "diabetes", "blood_pressure", "heart_disease",
                "kidney_disease", "liver_disease", "lung_disease",
                "hiv_aids", "hepatitis", "obesity", "cancer_history",
                "smoking_history", "alcohol_history", "any_surgery", "skin_damage"
            ]

            for field in living_fields:
                setattr(living, field, f'living_{field}' in request.POST)

            living.save()

        # --- Deceased Donation ---
        deceased_organ_id = request.POST.get("deceased_organ")
        if deceased_organ_id:
            if not deceased:
                deceased = DeceasedDonation(donor=donor)
            deceased.organ_id = deceased_organ_id

            deceased_fields = [
                "diabetes", "hypertension", "heart_disease",
                "kidney_disease", "liver_disease", "cancer_history",
                "hiv_aids", "hepatitis", "smoking_history",
                "alcohol_history", "major_surgeries"
            ]

            for field in deceased_fields:
                setattr(deceased, field, f'deceased_{field}' in request.POST)

            deceased.save()

        return redirect('donor_profile', donor_id=donor.id)

    return render(request, 'update_profile.html', {
        'donor': donor,
        'living': living,
        'deceased': deceased,
        'organs': organs
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            reset_link = f"http://127.0.0.1:8000/reset_password/{user.id}/"  # Replace with token logic in future

            # Send password reset email
            send_mail(
    subject='Reset Your Password',
    message=f"Hi {user.username},\nClick this link to reset your password:\n{reset_link}",
    from_email=settings.EMAIL_HOST_USER,  # ✅ Use from settings
    recipient_list=[email],
    fail_silently=False,  # ✅ See the error if any
)


            messages.success(request, f"Reset link sent to {email}. (Demo link: {reset_link})")
            return redirect('forgot_password')

        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")

    return render(request, 'forgot_password.html')


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. You can now log in.")
            return redirect('user_login')

    return render(request, 'reset_password.html')



from .models import Recipient  

from django.shortcuts import render
from .models import CustomUser
from .models import Notification
from .models import Transplant

def dashboard_detail(request):
    pending_recipient_list = RecipientOrganNeeded.objects.filter(
    recipient__matching_status="Pending"
).select_related('recipient', 'organ_neededrequest')
    transplant_list = Transplant.objects.filter(status="Completed")
    user_list = CustomUser.objects.filter(user_type__in=["donor", "recipient", "hospital_staff"])
    notification_list = Notification.objects.filter(status="Unread")

    context = {
        "pending_matches": pending_recipient_list.count(),
        "successful_transplants": transplant_list.count(),
        "active_users": user_list.count(),
        "unread_notifications": notification_list.count(),

        # LISTS to show in table
        "pending_recipients": pending_recipient_list,
        "successful_transplant_list": transplant_list,
        "active_user_list": user_list,
        "unread_notification_list": notification_list,
    }
    return render(request, "dashboard_detail.html", context)
