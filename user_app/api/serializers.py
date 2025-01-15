from django.contrib.auth.models import User
from rest_framework import serializers, status

class RegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'password2']
    extra_kwargs = {
      'password': {'write_only':True}
    }

  #validate and save
  def save (self):
    username = self.validated_data['username']
    if User.objects.filter(username=username).exists():
      raise serializers.ValidationError({'error':'username alredy exist'})

    password = self.validated_data['password']
    password2 = self.validated_data['password2']
    
    if password != password2:
      raise serializers.ValidationError({'error':'password is not matche'})
    
    if len(password) < 8 :
      raise serializers.ValidationError({'error': 'password must be more then 8 characters'})
    
    email = self.validated_data['email']
    
    if User.objects.filter(email=email).exists():
      raise serializers.ValidationError({'error':'email already exist'})
    
    account = User(email=email, username=self.validated_data['username'])
    account.set_password(password)
    account.save()
    
    return account
  

