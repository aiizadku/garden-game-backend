from rest_framework.serializers import ModelSerializer
from .models import Garden, Plant, Plants_in_garden

class PlantSerializer(ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'flower_name', 'region', 'cost', 'level', 'time_to_mature', 'exp_value', 'currency', 'desc')

class GardenSerializer(ModelSerializer):
    class Meta:
        model = Garden
        fields = ('user_id', 'rows', 'columns')

class Plants_in_gardenSerializer(ModelSerializer):
    class Meta:
        model = Plants_in_garden
        fields = ('plant_id', 'garden_id', 'harvested', 'watered', 'remaining_time', 'row_num', 'column_num')
