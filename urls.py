from django.urls import path
from . import views
app_name='takip'
urlpatterns=[
 path('',views.home,name='home'),
 path('export/evrak/',views.export_evrak_excel,name='export_evrak_excel'),
 path('export/musteri-odeme/',views.export_customer_payment_excel,name='export_customer_payment_excel'),
]
