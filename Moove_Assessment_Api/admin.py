from django.contrib import admin

# Register your models here.
from Moove_Assessment_Api.models import Applicant

admin.site.site_header = 'Applicant Admin Dashboard'

admin.site.register(Applicant)
