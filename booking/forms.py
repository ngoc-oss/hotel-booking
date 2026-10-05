from django import forms
from .models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=['guest_name','phone','check_in','check_out','guests']
        widgets={k:forms.DateInput(attrs={'type':'date'}) for k in ['check_in','check_out']}
