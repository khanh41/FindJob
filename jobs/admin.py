from django.contrib import admin
from .models import *

admin.site.register(Contact)
admin.site.register(JobListing)
admin.site.register(ApplyJob)

admin.site.register(JobComment)

class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
            obj.save()

class JobCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'date_posted')
    
            