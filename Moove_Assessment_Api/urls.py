from django.urls import path


from .views import *


urlpatterns = [
     path('create_applicant', create_applicant, name="create_applicant"),
     path('applicants', get_applicants, name="applicant_list"),
     path('applicants/<int:pk>', get_applicants, name="single_applicant"),
     path('applicants/<pk>/update', update_applicant, name="update_applicant"),
     path('applicants/<pk>/delete', delete_applicant, name="delete_applicant"),
]
