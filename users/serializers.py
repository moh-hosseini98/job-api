from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password



class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=True,write_only=True,validators=[validate_password])
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=50,required=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "type_profile", "email", "password",)


    def create(self,validated_data):
        user = User.objects.create(
            **validated_data
        )    
        user.set_password(validated_data['password'])
        user.save()
        return user