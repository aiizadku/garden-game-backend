from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Game, Garden, Plant, Plants_in_garden

class PlantSerializer(ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'flower_name', 'region', 'cost', 'level', 'time_to_mature', 'exp_value', 'currency', 'desc')

class GardenSerializer(ModelSerializer):
    class Meta:
        model = Garden
        fields = ('user', 'rows', 'columns')

class Plants_in_gardenSerializer(ModelSerializer):
    class Meta:
        model = Plants_in_garden
        fields = ('plant_id', 'garden_id', 'harvested', 'watered', 'remaining_time', 'row_num', 'column_num')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'

