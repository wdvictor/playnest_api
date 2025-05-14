from rest_framework import serializers
from base.models import User, Details, Sale



class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    details = DetailsSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        details = Details.objects.create(**details_data)
        user = User.objects.create(details=details, **validated_data)
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
