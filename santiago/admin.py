from django.contrib import admin
from santiago.models import ChipPackage, SecurityQuestion, UserProfile 
from santiago.models import MembershipLevel, UserMembershipLevelHistory
from santiago.models import GENDER_CHOICES, LEGAL_STATES

class ChipPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'chip_qty', 'price')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_user_name', 'member_level', 'current_level_effective_date', 'user_last_name', 'user_first_name', 'user_real_chip_balance', 'user_live_chip_balance', 'user_email', 'phone', 'street1', 'city', 'state', 'zip')
    list_filter = ('state', 'current_member_level__name')
    search_fields = ['phone', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    date_hierarchy = 'current_level_effective_date'
    
class UserMembershipHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_user_name', 'level', 'user_first_name', 'user_last_name', 'user_email', 'effective_date')
    list_filter = ('level',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    date_hierarchy = 'effective_date'

admin.site.register(ChipPackage, ChipPackageAdmin)
admin.site.register(SecurityQuestion)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MembershipLevel)
admin.site.register(UserMembershipLevelHistory, UserMembershipHistoryAdmin)
