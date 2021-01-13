from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Garden, User, Plant, Plants_in_garden, Game
from .serializers import PlantSerializer, Plants_in_gardenSerializer, GardenSerializer, UserSerializer, UserSerializerWithToken, ProfileSerializer, AllPlantsSerializer
import json
# from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt

# Helper Functions
def _get_user(user_id):
    """Returns corresponding user object or None."""
    try:
        return User.objects.get(id=user_id)
    except:
        return None


def _get_plant(plant_id):
    """Returns corresponding plant object or None."""
    try:
        return Plant.objects.get(id=plant_id)
    except:
        return None


def _get_garden(garden_id):
    """Returns corresponding garden object or None."""
    try:
        return Garden.objects.get(id=garden_id)
    except:
        return None


def _get_plant_in_garden(garden_id, row_number, column_number):
    """Returns corresponding plant_in_garden or None."""
    plant = Plants_in_garden.objects.filter(garden_id=garden_id).filter(
        row_num=row_number).filter(column_num=column_number)
    if len(plant) > 0:  # Should only be 1 plant in that location
        return plant[0]
    else:
        return None


# Route functions
# @csrf_exempt
@api_view(['POST'])
def harvest(request):
    """
    Called when harvesting a plant.\n
    Post data must include plant_id and user_id.
    """
    
    # Look up plant info in Plant table
    data = json.load(request)
    #print(f'data: {data}')
    #print(f'plant id: {data["plantId"]}')
    plant = _get_plant(data["plantId"])
    #print(plant)
    exp = 0
    currency = 0
    if plant:
        exp = plant.exp_value
        currency = plant.currency
        #print(f"exp: {exp}, currency: {currency}")
    else:
        return JsonResponse({"status": f"Error: Unable to find plant with ID {data.plantId}"}, status=400)

    # Get current user
    # Add currency and exp to user
    #print(request.user)
    request.user.profile.xp += exp
    request.user.profile.current_balance += currency
    #print(f"Total: {request.user.profile.xp} xp and ${request.user.profile.currency}")
    request.user.save()
    return JsonResponse({"status": f"Received harvest request: Added {exp} exp and {currency} currency"}, status=200)


'''
let data = {
    "row": rowColData[0],
    "column": rowColData[1],
    "plantId": plantId
}
'''

@api_view(["POST"])
def plant(request):
    """
    Called when planting in a garden.\n
    Post data must include plantId, row, column (to add later: is_raining).
    Adds new plant at location row, column.
    """
    print("PLANTING A PLANT!")
    data = json.load(request)
    plant = _get_plant(data["plantId"])
    if plant is None:
        return JsonResponse({"status": "Plant not found"}, status=400)

    new_plant = Plants_in_garden.objects.create(
        plant_id=plant,
        row_num=data["row"],
        column_num=data["column"],
        garden_id=request.user.garden,
        harvested=False,
        watered=False,
        remaining_time=plant.time_to_mature)
    new_plant.save()

    return JsonResponse({"status": "Received plant request"}, status=200)


def water(request):
    """
    Called when adding or removing the watered status to a plant.\n
    Post data must include user_id, garden_id, row_number, column_number, is_watered
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
    return JsonResponse({"status": "Received water request"}, status=200)


def water_all(request):
    """
    Called when watering the entire garden (rain).\n
    Post data must include user_id, garden_id, is_watered.\n
    Sets all existing plants' watered status in garden to is_watered.
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
    return JsonResponse({"status": "Received water_all request"}, status=200)


def save(request):
    """
    Called on logout.\n
    Post data must include user_id, garden_id, plant_statuses (as an array).\n
    plant_statuses should include {watered, remaining_time, plant_id, column_number, row_number}
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
    return JsonResponse({"status": "Received save request"}, status=200)


def load(request):
    """
    Called on login.\n
    Post data must include user_id, garden_id.\n
    Returns {plant_statuses: [ {watered, remaining_time, time_to_mature, plant_id, column_number, row_number}, ... ]
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
    return JsonResponse({"status": "Received load request"}, status=200)

@api_view(['GET'])
def available_plants(request):
    """
    Called when opening seed buying menu.\n
    Returns {"plants": [ {plant info}, ... ]} filtered by user level,\n
    where user level is >= 1.
    """
    #print(request.user.id)
    filter_level = request.user.profile.current_level
    data = list(Plant.objects.filter(level__lte=filter_level))
    serialized_data = AllPlantsSerializer(data).all_plants

    return JsonResponse(serialized_data, status=200)


def set_is_new(request):
    pass
# Relies on User
# def set_is_new(request):
#     if request.method != "POST":
#         return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
#     post_data = json.load(request)
#     print(post_data)
#     user = _get_user(post_data["user_id"])
#     is_new = post_data["is_new"]
#     if user:
#         print("User found")
#         user.is_new = is_new
#         return JsonResponse({"status": f"User is_new set to {is_new}."}, status=200)
#     return JsonResponse({"status": f"Error 400: Cannot find user."}, status=400)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def plant_detail(request, plant_id):
    plant = _get_plant(plant_id)
    if plant is None:
        return JsonResponse({"status": "Invalid plant ID"}, status=400)
    data = PlantSerializer(plant)
    return JsonResponse(data.data, status=200)

class ProfileViewSet(ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    serializer_class = ProfileSerializer
    queryset = Game.objects.all()

