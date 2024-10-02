from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, DonationSerializer, DonationHistorySerializer
from .models import User, Donation, DonationHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        # Validasi data
        if not request.data.get('email'):
            error_message = 'Email is required'
            print(f"Error in RegisterView: {error_message}")  # Menampilkan pesan error di konsol
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(Q(email=request.data.get('email')) | Q(username=request.data.get('username'))).exists():
            error_message = 'Username or Email is already in use'
            print(f"Error in RegisterView: {error_message}")  # Menampilkan pesan error di konsol
            return Response({'error': 'Username or Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Validasi Nomor Telepon
        phone_number = request.data.get('phone_number', '')
        if phone_number and not phone_number.isdigit():
            error_message = 'Invalid phone number'
            print(f"Error in RegisterView: {error_message}")  # Menampilkan pesan error di konsol
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Simpan user
            user = serializer.save()
            # Buat token untuk autentikasi
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': str(token), 'user': serializer.data}, status=status.HTTP_201_CREATED)
        
        print(f"Error in RegisterView: {serializer.errors}")  # Menampilkan pesan error di konsol
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, context = {'request': request})
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
            try:
                request.user.auth_token.delete()
            except AttributeError:
                # Handle the case where the user doesn't have a token
                return Response({'detail': 'No token to delete.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            print(request.FILES)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("sev"+request.FILES)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Kirim email reset password menggunakan mekanisme default Django
            user.send_password_reset_email()  # Atau logika lain sesuai kebutuhan
            return Response({"message": "Reset link has been sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        

class DonationCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Hanya user yang login yang bisa mengakses
    parser_classes = (MultiPartParser, FormParser)  

    def post(self, request):
        serializer = DonationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori', 'status_donasi', 'user']
    

class InputDonasiAPIView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            donation = Donation.objects.get(id=data.get('id'))
            previous_amount = donation.jumlah_total_donasi
            donation.jumlah_total_donasi += data.get('jumlah_total_donasi')
            donation.save()

            # Tambahkan entri riwayat
            DonationHistory.objects.create(donation=donation, change_description=f'Jumlah total donasi diupdate dari {previous_amount} menjadi {donation.jumlah_total_donasi}')
            
            return Response({'message': 'Donasi berhasil ditambahkan.', 'data': DonationSerializer(donation).data})
        except Donation.DoesNotExist:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'message': 'Donasi baru berhasil ditambahkan.', 'data': serializer.data})
        
class DonationHistoryListAPIView(generics.ListAPIView):
    queryset = DonationHistory.objects.all()
    serializer_class = DonationHistorySerializer