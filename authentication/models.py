from django.contrib.auth.models import User
from django.db import models

JENIS_KELAMIN = [
    ("pria","PRIA"),
    ("wanita", "WANITA"),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=JENIS_KELAMIN, default="pria")
    phone_number = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Donation(models.Model):
    KATEGORI_CHOICES = [
        ('kecelakaan_bencana', 'Kecelakaan & Bencana'),
        ('kesehatan_pendidikan', 'Kesehatan & Pendidikan'),
        ('panti_asuhan', 'Panti Asuhan'),
    ]

    STATUS_CHOICES = [
        ('berlangsung', 'Berlangsung'),
        ('selesai', 'Selesai'),
        ('batal', 'Batal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User yang membuat donasi
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    judul_donasi = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    tanggal = models.DateField()
    jumlah_total_donasi = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)  # Akumulasi donasi
    deskripsi = models.TextField()
    status_donasi = models.CharField(max_length=20, choices=STATUS_CHOICES, default='berlangsung')
    gambar = models.ImageField(upload_to='donation_images/', blank=True, null=True)  # Field untuk gambar

    def __str__(self):
        return self.judul_donasi
    
class DonationHistory(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='histories')
    updated_at = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()

    def __str__(self):
        return f'History for {self.donation.judul_donasi} at {self.updated_at}'