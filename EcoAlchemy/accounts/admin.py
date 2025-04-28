from django.contrib import admin
from .models import UserProfile, IndustryApplication

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'company_name', 'green_credits')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'company_name')

@admin.register(IndustryApplication)
class IndustryApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'status', 'application_date')
    list_filter = ('status',)
    actions = ['approve_application', 'reject_application']

    def approve_application(self, request, queryset):
        for application in queryset.filter(status='pending'):
            application.status = 'approved'
            application.user.profile.user_type = 'industry'
            application.user.profile.save()
            application.save()
        self.message_user(request, "Selected applications have been approved.")
    approve_application.short_description = "Approve selected applications"

    def reject_application(self, request, queryset):
        for application in queryset.filter(status='pending'):
            application.status = 'rejected'
            application.save()
        self.message_user(request, "Selected applications have been rejected.")
    reject_application.short_description = "Reject selected applications"
# Register your models here.
