import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from booking.models import Room
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        for number,kind,capacity,price in [('101','Standard Garden',2,550000),('102','Standard Garden',2,550000),('201','Deluxe Balcony',3,850000),('202','Deluxe Balcony',3,850000),('301','Family Suite',4,1250000),('401','Executive Suite',2,1650000)]:
            Room.objects.get_or_create(number=number,defaults={'kind':kind,'capacity':capacity,'price':price,'description':'Không gian thoáng, Wi-Fi, điều hòa, phòng tắm riêng.'})
        User=get_user_model()
        if not User.objects.filter(username='admin').exists(): User.objects.create_superuser('admin','admin@example.test',os.environ['ADMIN_PASSWORD'])
        self.stdout.write('Seed completed; existing accounts preserved.')
