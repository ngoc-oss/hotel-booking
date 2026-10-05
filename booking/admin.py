from django.contrib import admin
from .models import Room,Booking
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['number','kind','capacity','price','active']; list_filter=['kind','active']; search_fields=['number','kind']
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=['id','guest_name','room','check_in','check_out','total','status']; list_filter=['status']; search_fields=['guest_name','phone']
    readonly_fields=['user','room','guest_name','phone','check_in','check_out','guests','total','status','created_at']
    def has_add_permission(self,request): return False
    def has_delete_permission(self,request,obj=None): return False
    actions=['cancel']
    @admin.action(description='Hủy các đơn đã chọn')
    def cancel(self,request,queryset): queryset.update(status='cancelled')
