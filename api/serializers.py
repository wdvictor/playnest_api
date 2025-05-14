from math import e
from rest_framework import serializers
from base.models import Customer, Details, Sale
from django.contrib.auth.models import User



class RegisterSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        birthday = validated_data.pop('birthday')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        details = Details.objects.create(email=validated_data['email'], birthday=birthday)
        Customer.objects.create(user=user, details=details)
        return user


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    details = DetailsSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        details = Details.objects.create(**details_data)
        user = Customer.objects.create(details=details, **validated_data)
        return user


    def update(self, instance, validated_data):
        
        details_data = validated_data.pop('details')
        details = instance.details
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        details.email = details_data.get('email', details.email)
        details.birthday = details_data.get('birthday', details.birthday)
        details.save()

        return instance




class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


    def create(self, validated_data):
        sale = Sale.objects.create(**validated_data)
        return sale
