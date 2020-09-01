from django.contrib import admin
from .models import Notes,UserProfile

# Register your models here.
class NotesAdmin(admin.ModelAdmin):
	list_display=('title','user','content','publish','updated_at')
	prepopulated_fields={'slug':('title',)} 

class ProfileAdmin(admin.ModelAdmin):
	list_display=('first_name','last_name','birthday','bio','profilepic','hobby')


admin.site.register(Notes,NotesAdmin)
admin.site.register(UserProfile,ProfileAdmin)