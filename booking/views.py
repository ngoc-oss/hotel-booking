import logging
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction,connection
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from django.contrib import messages
from prometheus_client import generate_latest,Gauge,CollectorRegistry
from .models import Room,Booking
from .forms import BookingForm
log=logging.getLogger('hotel')
def home(request):
    rooms=Room.objects.filter(active=True)
    start=request.GET.get('start'); end=request.GET.get('end')
    if start and end:
        from datetime import date
        try:
            a,b=date.fromisoformat(start),date.fromisoformat(end)
            if b<=a: raise ValueError()
            rooms=rooms.exclude(id__in=Booking.objects.filter(status='confirmed',check_in__lt=b,check_out__gt=a).values('room_id'))
        except ValueError: messages.error(request,'Khoảng ngày không hợp lệ.')
    return render(request,'home.html',{'rooms':rooms})
def signup(request):
    form=UserCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.save()); return redirect('home')
    return render(request,'form.html',{'form':form,'title':'Tạo tài khoản'})
@login_required
def reserve(request,pk):
    room=get_object_or_404(Room,pk=pk,active=True)
    form=BookingForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        data=form.cleaned_data
        with transaction.atomic():
            room=Room.objects.select_for_update().get(pk=pk)
            if not room.active: form.add_error(None,'Phòng tạm ngừng kinh doanh.')
            elif data['check_in']<timezone.localdate(): form.add_error('check_in','Không thể đặt ngày trong quá khứ.')
            elif data['guests']>room.capacity: form.add_error('guests','Vượt sức chứa phòng.')
            elif Booking.objects.filter(room=room,status='confirmed',check_in__lt=data['check_out'],check_out__gt=data['check_in']).exists(): form.add_error(None,'Phòng đã có khách trong khoảng ngày này.')
            else:
                obj=form.save(commit=False); obj.room=room; obj.user=request.user
                obj.total=(obj.check_out-obj.check_in).days*room.price; obj.save()
                log.warning('booking_created booking_id=%s room_id=%s',obj.id,room.id)
                return redirect('mine')
    return render(request,'form.html',{'form':form,'title':f'Đặt phòng {room.number} · {room.price:,.0f} đ/đêm'})
@login_required
def mine(request): return render(request,'mine.html',{'bookings':Booking.objects.filter(user=request.user).select_related('room').order_by('-id')})
@login_required
@require_POST
def cancel(request,pk):
    obj=get_object_or_404(Booking,pk=pk,user=request.user)
    obj.status='cancelled'; obj.save(update_fields=['status']); log.warning('booking_cancelled booking_id=%s',obj.id)
    return redirect('mine')
def health(request):
    try:
        with connection.cursor() as c: c.execute('SELECT 1')
        return JsonResponse({'status':'ok','database':'connected'})
    except Exception: return JsonResponse({'status':'error'},status=503)
def metrics(request):
    reg=CollectorRegistry()
    for name,value in [('hotel_rooms_total',Room.objects.count()),('hotel_bookings_confirmed',Booking.objects.filter(status='confirmed').count())]: Gauge(name,name,registry=reg).set(value)
    return HttpResponse(generate_latest(reg),content_type='text/plain; version=0.0.4')
