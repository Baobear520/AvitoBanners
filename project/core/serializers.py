from rest_framework import serializers
from core.models import AvitoUser


class AdminAvitoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AvitoUser
        fields = "__all__"

class UserAvitoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AvitoUser
        fields = ['username','password','email','first_name','last_name']



class CreateAvitoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AvitoUser
        fields = ['username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user