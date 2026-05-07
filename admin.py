from django.contrib import admin
from django.utils import timezone
from .models import *
class ProcessStepTemplateInline(admin.TabularInline):
    model=ProcessStepTemplate; extra=1
@admin.register(ProcessType)
class ProcessTypeAdmin(admin.ModelAdmin):
    list_display=('name','active'); search_fields=('name',); inlines=[ProcessStepTemplateInline]
class JobStepInline(admin.TabularInline):
    model=JobStep; extra=0; readonly_fields=('completed_by','completed_at','uploaded_by','uploaded_at')
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display=('customer','process_type','district','neighborhood','block','parcel','fee','expense','paid','remaining','completed','created_at')
    search_fields=('customer__name','district','neighborhood','block','parcel','description')
    list_filter=('completed','process_type','district','created_at')
    inlines=[JobStepInline]
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(JobStep)
class JobStepAdmin(admin.ModelAdmin):
    list_display=('job','name','completed','completed_by','completed_at','document')
    list_filter=('completed','completed_at')
    search_fields=('job__customer__name','name')
    def save_model(self,request,obj,form,change):
        if obj.completed and not obj.completed_by:
            obj.completed_by=request.user; obj.completed_at=timezone.now()
        if obj.document and not obj.uploaded_by:
            obj.uploaded_by=request.user; obj.uploaded_at=timezone.now()
        super().save_model(request,obj,form,change)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('name','phone','created_at','created_by'); search_fields=('name','phone'); list_filter=('created_at',)
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('job','date','time','completed','completed_by','completed_at'); list_filter=('date','completed'); search_fields=('job__customer__name','note')
    def save_model(self,request,obj,form,change):
        if obj.completed and not obj.completed_by:
            obj.completed_by=request.user; obj.completed_at=timezone.now()
        super().save_model(request,obj,form,change)
@admin.register(ExpenseRecord)
class ExpenseRecordAdmin(admin.ModelAdmin):
    list_display=('date','description','amount','document','created_by'); list_filter=('date','created_by'); search_fields=('description',)
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(IncomingDocument)
class IncomingDocumentAdmin(admin.ModelAdmin):
    list_display=('date','number','sender','subject','document','created_by'); list_filter=('date','created_by'); search_fields=('number','sender','subject','description')
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(OutgoingDocument)
class OutgoingDocumentAdmin(admin.ModelAdmin):
    list_display=('date','number','recipient','subject','document','created_by'); list_filter=('date','created_by'); search_fields=('number','recipient','subject','description')
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(IssuedInvoice)
class IssuedInvoiceAdmin(admin.ModelAdmin):
    list_display=('date','invoice_no','billed_to','amount','document','created_by'); list_filter=('date','created_by'); search_fields=('invoice_no','billed_to','description')
    def save_model(self,request,obj,form,change):
        if not obj.created_by_id: obj.created_by=request.user
        super().save_model(request,obj,form,change)
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display=('created_at','user','method','path','ip_address'); list_filter=('created_at','user','method'); search_fields=('user__username','path','description')
    readonly_fields=('user','path','method','description','ip_address','created_at')
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','role'); list_filter=('role',)
