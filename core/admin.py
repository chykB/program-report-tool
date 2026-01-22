from django.contrib import admin
from .models import Organization, Program, Cohort

@admin.register(Organization)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "name", )

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ("id", "program", "name", "start_date", "end_date")