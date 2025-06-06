from django.urls import path
from . import views # Ensure correct import
from .views import match_donor_to_recipient, complete_transplant

urlpatterns = [
    path('login/', views.user_login, name='user_login'),  # ✅ Ensure this exists
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('donor_register/', views.donor_register, name='donor_register'),
    path('recipient_register/', views.recipient_register, name='recipient_register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('register_donor',views.register_donor,name='register_donor'),
    path('organ_donation_status/',views.organ_donation_status,name='organ_donation_status'),
    path('update_donor_status/',views.update_donor_status,name='update_donor_status'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('index/',views.index,name='index'),
    path('home1',views.home1,name='home1'),
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('about/',views.about_us,name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('donor_profile/<int:donor_id>/', views.donor_profile, name='donor_profile'),
    path('add_details/', views.add_details, name='add_details'),
    path('living_donation/', views.living_donation, name='living_donation'),
    path('deceased_donation/', views.deceased_donation, name='deceased_donation'),
    path('success/', views.success_page, name='success_page'), 
    path('success1/', views.success_page1, name='success_page1'), 
    path('success2/', views.success_page2, name='success_page2'), 
    path('add-organ/', views.add_organ, name='add-organ'),
    path('list-organs/', views.list_organs, name='list-organs'),
    path('list_donors/', views.list_donors, name='list_donors'),
    path('delete_donor/<int:donor_id>/', views.delete_donor, name='delete_donor'),
    # path('admin/delete_donor/<int:donor_id>/', views.delete_donor, name='delete_donor'),

    path('update_profile/<int:donor_id>/', views.update_profile, name='update_profile'),

    path('list_recipients/', views.list_recipients, name='list_recipients'),
    path('list_hospitals/', views.list_hospitals, name='list_hospitals'),
    path('add_organ/',views.add_organ,name='add_organ'),
    path("add_recipient/", views.add_recipient, name="add_recipient"),
    path("matching_status/", views.matching_status, name="matching_status"),
    path("update_recipient_status/<int:recipient_id>/", views.update_recipient_status, name="update_recipient_status"),
    path("approve_donation/<int:donation_id>/", views.approve_donation, name="approve_donation"),
    path("hospital_dashboard/", views.hospital_dashboard, name="hospital_dashboard"),
    path("list_living_donations/", views.list_living_donations, name="list_living_donations"),
    path("list_deceased_donations/", views.list_deceased_donations, name="list_deceased_donations"),
    path("approve_living_donor/<int:donor_id>/", views.approve_living_donor, name="approve_living_donor"),
    path("verify_deceased_donor/<int:donor_id>/", views.verify_deceased_donor, name="verify_deceased_donor"),
    path("delete_living_donor/<int:donor_id>/", views.delete_living_donor, name="delete_living_donor"),
    path("delete_deceased_donor/<int:donor_id>/", views.delete_deceased_donor, name="delete_deceased_donor"),
    path('hospital_register/',views.hospital_register,name='hospital_register'),
    path('hospital_details/', views.hospital_details, name='hospital_details'),
    path('recipient_profile/<int:recipient_id>/', views.recipient_profile, name='recipient_profile'),
    path('update_recipient/<int:recipient_id>/', views.update_recipient, name='update_recipient'),
    path('recipient_notifications/', views.recipient_notifications, name='recipient_notifications'),
    path('upload_documents/', views.upload_documents, name='upload_documents'),
    path('registered_donors/',views.registered_donors,name='registered_donors'),
    path('update_recipient/',views.update_recipient,name='update_recipient'),
    path('organ_request/',views.organ_request,name='organ_request'),
    path('test/', views.some_view, name='test_view'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('transplant-matching/', views.transplant_matching, name='transplant_matching'),
    path('organ-tracking/', views.organ_tracking, name='organ_tracking'),
    path('emergency-requests/', views.emergency_requests, name='emergency_requests'),
    path('hospital_reports/', views.hospital_reports, name='hospital_reports'),
    path('assign_donor/<int:donor_id>/<int:hospital_id>/', views.assign_donor_to_hospital, name='assign_donor_to_hospital'),
    path('assign_recipient/<int:recipient_id>/<int:hospital_id>/', views.assign_recipient_to_hospital, name='assign_recipient_to_hospital'),
    path('admin/organs/', views.organ_list, name='organ_list'),
    path('api/organs/', views.get_organs, name='get_organs'),  # API for fetching organs
    path('admin/match/<int:recipient_id>/', views.match_result, name='match_result'),
    path('available-organs/', views.available_organs, name='available_organs'),  # ✅ Add this # ✅ Add this
    path('available-donors/', views.available_donors, name='available_donors'),
    path('match_list/', views.match_list, name='match_list'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('create/', views.create_match, name='create_match'),

    path('match/', views.match_donors_and_recipients, name='match_donors_and_recipients'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/', views.match_list, name='match_list'),
    path('match/',views. match_donors_and_recipients, name='match_donors_and_recipients'),
    path('confirm/<int:match_id>/', views.confirm_transplant, name='confirm_transplant'),

    
    path('recipient/match/<int:recipient_id>/', match_donor_to_recipient, name='match_donor_to_recipient'),
    path('recipient/complete_transplant/<int:recipient_id>/', complete_transplant, name='complete_transplant'),

    path('admin_legal_documents/', views.admin_legal_documents, name='admin_legal_documents'),
    path('legal-documents/verify/living/<int:doc_id>/', views.verify_living_doc, name='verify_living_doc'),
    # path('legal-documents/reject/living/<int:doc_id>/', views.reject_living_doc, name='reject_living_doc'),
    path('legal-documents/verify/deceased/<int:doc_id>/', views.verify_deceased_doc, name='verify_deceased_doc'),
    # path('legal-documents/reject/deceased/<int:doc_id>/', views.reject_deceased_doc, name='reject_deceased_doc'),

    path('admin_recipient_documents/', views.admin_recipient_documents, name='admin_recipient_documents'),
    path('legal-documents/verify/recipient/<int:doc_id>/', views.verify_recipient_doc, name='verify_recipient_doc'),
    # path('legal-documents/reject/recipient/<int:doc_id>/', views.reject_recipient_doc, name='reject_recipient_doc'),
    path("view_donations/", views.view_donations, name="view_donations"),
    path('check-matches/<int:donor_id>/',views. check_matches, name='check_matches'),
    path('matching_status/<int:recipient_id>/', views.matching_status, name='matching_status'),
    path('notifications/', views.get_notifications, name='recipient-notifications'),
    path('notifications/send/', views.send_notification, name='send-notification'),
    path('notifications/<int:notification_id>/mark_as_read/', views.mark_notification_as_read, name='mark-notification-read'),
    path('admin_notifications/', views.admin_notifications, name='admin_notifications'),
    path("recipient_notifications/", views.recipient_notifications, name="recipient_notifications"),
    path("respond_to_notification/<int:notification_id>/", views.respond_to_notification, name="respond_to_notification"),
    path('confirm_transplant/', views.confirm_transplant, name='confirm_transplant'),
    path('schedule_transplant/', views.schedule_transplant, name='schedule_transplant'),
    path('mark_transplant_completed/<int:transplant_id>/', views.mark_transplant_completed, name='mark_transplant_completed'),
    path('transplant_status/<int:transplant_id>/', views.transplant_status, name='transplant_status'),
    path('confirm_attendance/<int:transplant_id>/',views.confirm_attendance, name='confirm_attendance'),  # ✅ Add this line
    path('transplant-updates/', views.transplant_updates, name='transplant_updates'),
    path('transplant-success/<int:transplant_id>/', views.mark_transplant_success, name='mark_transplant_success'),
    path("donor_notifications/", views.donor_notifications, name="donor_notifications"),
    path("generate_report/<int:transplant_id>/", views.generate_transplant_report, name="generate_report"),
    path('update_status/<int:doc_id>/<str:doc_type>/<str:action>/', views.update_document_status, name="update_document_status"),
    # path('approve_compensation/<int:transplant_id>/', views.approve_compensation, name='approve_compensation'),
    path('approve_compensation/<int:donor_id>/', views.approve_compensation, name='approve_compensation'),
    path("add_payment/<int:transplant_id>/", views.add_payment_page, name="add_payment_page"),
    path("process_payment/<int:transplant_id>/", views.process_payment, name="process_payment"),
    path('donor_transactions/', views.donor_transactions, name='donor_transactions'),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('dashboard_detail/', views.dashboard_detail, name='dashboard_detail'),
]
    
  





