from django.contrib import admin
from .models import Application, Person, IdDoc, AddressDoc, Address, CryptoAddressAnalysis, CryptoTransactionAnalysis
# Register your models here.

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    fields = ('client', 'applicant_id', 'inspection_id', 'correlation_id', 'status', 'review_status', 'last_updated','review_answer', 'review_reject_type', 'moderation_comment', 'client_comment', 'reject_labels', 'created_at', 'access_token_for_sdk')
    list_display = ('client','status', 'review_status', 'last_updated')
    readonly_fields = ('client','applicant_id', 'inspection_id', 'correlation_id', 'status', 'review_status', 'last_updated', 'review_answer',  'review_reject_type', 'moderation_comment', 'client_comment', 'reject_labels', 'created_at', 'access_token_for_sdk')

    # def get_uuid(self, obj):
    #     return obj.user.uuid
    # get_uuid.short_description = 'UUID'
    # get_uuid.admin_order_field = 'User UUID'
    #'review_answer', 'review_reject_type', 'moderation_comment', 'client_comment', 'reject_labels'

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('client','last_name')
    pass

@admin.register(IdDoc)
class IdDocAdmin(admin.ModelAdmin):
    list_display = ('client',)
    pass

@admin.register(AddressDoc)
class AddressDocAdmin(admin.ModelAdmin):
    list_display = ('client',)
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(CryptoAddressAnalysis)
class CryptoAddressAnalysisAdmin(admin.ModelAdmin):
    list_display = ('address','analysis_result', 'risk_score', 'created_at', 'last_updated_global', 'last_updated_fast')
    readonly_fields = ('address','analysis_result', 'risk_score', 'created_at', 'last_updated_global', 'last_updated_fast', 'dark_market_signal', 'dark_service_signal', 'exchange_signal', 'gambling_signal', 'illegal_service_signal', 'marketplace_signal', 'miner_signal', 'mixer_signal', 'payment_signal', 'ransom_signal', 'scam_signal', 'stolen_coins_signal', 'trusted_exchange_signal', 'wallet_signal')

CryptoTransactionAnalysis

@admin.register(CryptoTransactionAnalysis)
class CryptoTransactionAnalysisAdmin(admin.ModelAdmin):
    list_display = ('address','analysis_result', 'risk_score', 'created_at')
    readonly_fields = ('address','analysis_result', 'risk_score', 'created_at', 'dark_market_signal', 'dark_service_signal', 'exchange_signal', 'gambling_signal', 'illegal_service_signal', 'marketplace_signal', 'miner_signal', 'mixer_signal', 'payment_signal', 'ransom_signal', 'scam_signal', 'stolen_coins_signal', 'trusted_exchange_signal', 'wallet_signal')
