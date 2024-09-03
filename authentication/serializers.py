
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number', required=False)
    image = serializers.ImageField(source='userprofile.image', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'image')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_profile_data = validated_data.pop('userprofile', {})
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            
        )
        UserProfile.objects.create(
            user=user,
            phone_number=user_profile_data.get('phone_number', ''),
            image=user_profile_data.get('image', None)
        )
        return user
    
    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop('userprofile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        # Jika password disertakan dalam pembaruan, set password baru
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()

        # Update atau buat UserProfile jika ada data terkait
        user_profile, created = UserProfile.objects.get_or_create(user=instance)
        user_profile.phone_number = user_profile_data.get('phone_number', user_profile.phone_number)
        if 'image' in user_profile_data:
            user_profile.image = user_profile_data['image']
        user_profile.save()

        return instance