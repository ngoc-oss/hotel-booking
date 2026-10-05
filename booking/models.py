from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
class Room(models.Model):
    number=models.CharField('Số phòng',max_length=10,unique=True)
    kind=models.CharField('Hạng phòng',max_length=80)
    capacity=models.PositiveIntegerField('Số khách',default=2)
    price=models.DecimalField('Giá mỗi đêm',max_digits=12,decimal_places=0)
    description=models.TextField('Mô tả',blank=True)
    active=models.BooleanField('Đang kinh doanh',default=True)
    def __str__(self): return f'{self.number} - {self.kind}'
    class Meta:
        constraints=[models.CheckConstraint(condition=models.Q(price__gt=0),name='positive_price'),models.CheckConstraint(condition=models.Q(capacity__gt=0),name='positive_capacity')]
class Booking(models.Model):
    STATUS=[('confirmed','Đã xác nhận'),('cancelled','Đã hủy')]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    room=models.ForeignKey(Room,on_delete=models.PROTECT)
    guest_name=models.CharField('Tên khách',max_length=100)
    phone=models.CharField('Điện thoại',max_length=20)
    check_in=models.DateField('Nhận phòng')
    check_out=models.DateField('Trả phòng')
    guests=models.PositiveIntegerField('Số khách',default=1)
    total=models.DecimalField('Tổng tiền',max_digits=14,decimal_places=0)
    status=models.CharField(max_length=12,choices=STATUS,default='confirmed')
    created_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.check_in and self.check_out and self.check_out<=self.check_in: raise ValidationError('Ngày trả phải sau ngày nhận.')
        if self.guests<1 or (self.room_id and self.guests>self.room.capacity): raise ValidationError('Số khách không phù hợp sức chứa.')
    class Meta:
        constraints=[models.CheckConstraint(condition=models.Q(check_out__gt=models.F('check_in')),name='valid_dates'),models.CheckConstraint(condition=models.Q(guests__gt=0),name='positive_guests')]
