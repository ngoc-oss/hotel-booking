from datetime import timedelta
from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Room,Booking
class BookingTests(TestCase):
 def setUp(self):
  self.user=get_user_model().objects.create_user('guest',password='LongPass!123')
  self.room=Room.objects.create(number='101',kind='Deluxe',capacity=2,price=500000)
  self.client.force_login(self.user)
  self.start=timezone.localdate()+timedelta(days=3)
  self.data={'guest_name':'Guest','phone':'0901234567','check_in':self.start,'check_out':self.start+timedelta(days=2),'guests':2}
  self.url=f'/rooms/{self.room.id}/book/'
 def book(self): return self.client.post(self.url,self.data)
 def test_home(self): self.assertContains(self.client.get('/'),'Deluxe')
 def test_price_calculated_on_server(self):
  self.data['total']=1; self.assertEqual(self.book().status_code,302); self.assertEqual(Booking.objects.get().total,1000000)
 def test_overlap_rejected(self):
  self.book(); self.assertContains(self.book(),'Phòng đã có khách'); self.assertEqual(Booking.objects.count(),1)
 def test_adjacent_allowed(self):
  self.book(); self.data['check_in']+=timedelta(days=2); self.data['check_out']+=timedelta(days=2); self.book(); self.assertEqual(Booking.objects.count(),2)
 def test_reversed_dates(self):
  self.data['check_out']=self.start-timedelta(days=1); self.assertEqual(self.book().status_code,200); self.assertEqual(Booking.objects.count(),0)
 def test_past_date(self):
  self.data['check_in']=timezone.localdate()-timedelta(days=1); self.book(); self.assertEqual(Booking.objects.count(),0)
 def test_capacity(self):
  self.data['guests']=3; self.book(); self.assertEqual(Booking.objects.count(),0)
 def test_cancel_and_rebook(self):
  self.book(); b=Booking.objects.get(); self.client.post(f'/bookings/{b.id}/cancel/'); self.book(); self.assertEqual(Booking.objects.filter(status='confirmed').count(),1)
 def test_other_user_cannot_cancel(self):
  self.book(); b=Booking.objects.get(); other=get_user_model().objects.create_user('other'); self.client.force_login(other)
  self.assertEqual(self.client.post(f'/bookings/{b.id}/cancel/').status_code,404)
  self.assertNotContains(self.client.get('/bookings/'),'0901234567')
 def test_cancel_requires_post(self):
  self.book(); self.assertEqual(self.client.get(f'/bookings/{Booking.objects.get().id}/cancel/').status_code,405)
 def test_auth_required(self):
  self.client.logout(); self.assertEqual(self.book().status_code,302)
 def test_csrf(self):
  c=Client(enforce_csrf_checks=True); c.force_login(self.user); self.assertEqual(c.post(self.url,self.data).status_code,403)
 def test_health_and_metrics(self):
  self.assertEqual(self.client.get('/health/').json()['database'],'connected'); self.assertContains(self.client.get('/metrics'),'hotel_rooms_total')
 def test_nonstaff_no_admin(self): self.assertEqual(self.client.get('/admin/').status_code,302)
 def test_inactive_room(self):
  self.room.active=False; self.room.save(); self.assertEqual(self.book().status_code,404)
