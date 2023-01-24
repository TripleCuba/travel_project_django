from abc import ABC

import cloudinary
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Account, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'profile')


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['account']


class UpdateProfileSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    town = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('firstName', 'lastName', "phone", "country", "town")


class UpdateProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords does not match'})
        user.set_password(password)
        user.save()
        return user
