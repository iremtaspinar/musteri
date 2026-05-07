from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.TextChoices):
    ADMIN='admin','Yönetici'
    PARTNER='partner','Ortak'
    STAFF='staff','Personel'

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.STAFF)
    def __str__(self): return f"{self.user.username} - {self.get_role_display()}"

class Customer(models.Model):
    name=models.CharField('Müşteri Adı',max_length=255)
    phone=models.CharField('Telefon',max_length=50,blank=True)
    note=models.TextField('Not',blank=True)
    created_at=models.DateTimeField('Kayıt Tarihi',auto_now_add=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name='Müşteri'; verbose_name_plural='Müşteriler'; ordering=['name']
    def __str__(self): return self.name

class ProcessType(models.Model):
    name=models.CharField('İşlem Adı',max_length=255,unique=True)
    active=models.BooleanField('Aktif',default=True)
    class Meta:
        verbose_name='İşlem Tanımı'; verbose_name_plural='İşlem Tanımları'
    def __str__(self): return self.name

class ProcessStepTemplate(models.Model):
    process_type=models.ForeignKey(ProcessType,verbose_name='İşlem',on_delete=models.CASCADE,related_name='step_templates')
    name=models.CharField('Alt Başlık / İşlem Adımı',max_length=255)
    order=models.PositiveIntegerField('Sıra',default=1)
    class Meta:
        verbose_name='İşlem Adımı Şablonu'; verbose_name_plural='İşlem Adımı Şablonları'; ordering=['process_type','order']
    def __str__(self): return f"{self.process_type} - {self.name}"

class Job(models.Model):
    customer=models.ForeignKey(Customer,verbose_name='Müşteri',on_delete=models.CASCADE,related_name='jobs')
    process_type=models.ForeignKey(ProcessType,verbose_name='İşlem Türü',on_delete=models.SET_NULL,null=True,blank=True)
    district=models.CharField('İlçe',max_length=120,blank=True)
    neighborhood=models.CharField('Mahalle',max_length=120,blank=True)
    block=models.CharField('Ada',max_length=80,blank=True)
    parcel=models.CharField('Parsel',max_length=80,blank=True)
    description=models.TextField('Açıklama',blank=True)
    fee=models.DecimalField('Ücret',max_digits=14,decimal_places=2,default=0)
    expense=models.DecimalField('Masraf',max_digits=14,decimal_places=2,default=0)
    paid=models.DecimalField('Alınan',max_digits=14,decimal_places=2,default=0)
    completed=models.BooleanField('Tamamlandı',default=False)
    created_at=models.DateTimeField('Kayıt Tarihi',auto_now_add=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name='İş'; verbose_name_plural='İşler'; ordering=['-created_at']
    @property
    def total(self): return self.fee+self.expense
    @property
    def remaining(self): return max(self.total-self.paid,0)
    def __str__(self): return f"{self.customer} - {self.process_type or self.description}"

class JobStep(models.Model):
    job=models.ForeignKey(Job,verbose_name='İş',on_delete=models.CASCADE,related_name='steps')
    name=models.CharField('İşlem Adımı',max_length=255)
    completed=models.BooleanField('Tamamlandı',default=False)
    completed_by=models.ForeignKey(User,verbose_name='Tamamlayan',on_delete=models.SET_NULL,null=True,blank=True)
    completed_at=models.DateTimeField('Tamamlanma Zamanı',null=True,blank=True)
    document=models.FileField('Belge',upload_to='job_steps/%Y/%m/',blank=True,null=True)
    uploaded_by=models.ForeignKey(User,verbose_name='Belge Yükleyen',on_delete=models.SET_NULL,null=True,blank=True,related_name='uploaded_step_docs')
    uploaded_at=models.DateTimeField('Belge Yükleme Zamanı',null=True,blank=True)
    class Meta:
        verbose_name='İşlem Adımı'; verbose_name_plural='İşlem Adımları'
    def __str__(self): return f"{self.job} - {self.name}"

class Appointment(models.Model):
    job=models.ForeignKey(Job,verbose_name='İş',on_delete=models.CASCADE,related_name='appointments')
    date=models.DateField('Randevu Tarihi')
    time=models.TimeField('Saat',null=True,blank=True)
    note=models.TextField('Not',blank=True)
    completed=models.BooleanField('Arazi Tamamlandı',default=False)
    completed_by=models.ForeignKey(User,verbose_name='Tamamlayan',on_delete=models.SET_NULL,null=True,blank=True)
    completed_at=models.DateTimeField('Tamamlanma Zamanı',null=True,blank=True)
    class Meta:
        verbose_name='Randevu'; verbose_name_plural='Randevular'; ordering=['date','time']
    def __str__(self): return f"{self.job} - {self.date} {self.time or ''}"

class ExpenseRecord(models.Model):
    description=models.CharField('Gider Açıklaması',max_length=255)
    amount=models.DecimalField('Tutar',max_digits=14,decimal_places=2)
    date=models.DateField('Tarih',default=timezone.localdate)
    document=models.FileField('Gider Belgesi',upload_to='expenses/%Y/%m/',blank=True,null=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField('Kayıt Zamanı',auto_now_add=True)
    class Meta:
        verbose_name='Gider'; verbose_name_plural='Giderler'; ordering=['-date']
    def __str__(self): return f"{self.description} - {self.amount}"

class IncomingDocument(models.Model):
    date=models.DateField('Tarih')
    number=models.CharField('Sayı',max_length=120)
    sender=models.CharField('Geldiği Yer',max_length=255)
    subject=models.CharField('Konu',max_length=255)
    description=models.TextField('Açıklama',blank=True)
    document=models.FileField('Evrak Dosyası',upload_to='incoming_docs/%Y/%m/',blank=True,null=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField('Kayıt Zamanı',auto_now_add=True)
    class Meta:
        verbose_name='Gelen Evrak'; verbose_name_plural='Gelen Evraklar'; ordering=['date','number']
    def __str__(self): return f"{self.date} - {self.number} - {self.subject}"

class OutgoingDocument(models.Model):
    date=models.DateField('Tarih')
    number=models.CharField('Sayısı',max_length=120)
    subject=models.CharField('Konu',max_length=255)
    recipient=models.CharField('Gönderildiği Yer',max_length=255)
    description=models.TextField('Açıklama',blank=True)
    document=models.FileField('Evrak Dosyası',upload_to='outgoing_docs/%Y/%m/',blank=True,null=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField('Kayıt Zamanı',auto_now_add=True)
    class Meta:
        verbose_name='Giden Evrak'; verbose_name_plural='Giden Evraklar'; ordering=['date','number']
    def __str__(self): return f"{self.date} - {self.number} - {self.subject}"

class IssuedInvoice(models.Model):
    date=models.DateField('Fatura Tarihi')
    invoice_no=models.CharField('Fatura No',max_length=120,blank=True)
    billed_to=models.CharField('Kime Kesildi',max_length=255)
    amount=models.DecimalField('Miktar',max_digits=14,decimal_places=2)
    description=models.TextField('Açıklama',blank=True)
    document=models.FileField('Fatura Dosyası',upload_to='issued_invoices/%Y/%m/',blank=True,null=True)
    created_by=models.ForeignKey(User,verbose_name='Kaydeden',on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField('Kayıt Zamanı',auto_now_add=True)
    class Meta:
        verbose_name='Kesilen Fatura'; verbose_name_plural='Kesilen Faturalar'; ordering=['-date']
    def __str__(self): return f"{self.billed_to} - {self.amount}"

class ActivityLog(models.Model):
    user=models.ForeignKey(User,verbose_name='Kullanıcı',on_delete=models.SET_NULL,null=True,blank=True)
    path=models.CharField('Sayfa',max_length=500)
    method=models.CharField('İşlem Tipi',max_length=20)
    description=models.TextField('Açıklama',blank=True)
    ip_address=models.GenericIPAddressField('IP',null=True,blank=True)
    created_at=models.DateTimeField('Zaman',auto_now_add=True)
    class Meta:
        verbose_name='Kullanıcı İşlem Kaydı'; verbose_name_plural='Kullanıcı İşlem Kayıtları'; ordering=['-created_at']
    def __str__(self): return f"{self.user} - {self.method} - {self.created_at}"
