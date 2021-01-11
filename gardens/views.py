from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Garden, User, Plant, Plants_in_garden
from .serializers import PlantSerializer, Plants_in_gardenSerializer, GardenSerializer, UserSerializer, UserSerializerWithToken
import json
# from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


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
def harvest(request):
    """
    Called when harvesting a plant.\n
    Post data must include plant_id and user_id.
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)

    # Look up plant info in Plant table
    exp = 0
    currency = 0
    # Add currency and exp to user
    # User.objects.
    return JsonResponse({"status": f"Received harvest request: Added {exp} exp and {currency} currency"}, status=200)


def plant(request):
    """
    Called when planting in a garden.\n
    Post data must include user_id, plant_id, row_number, column_number, is_raining.
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
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


def available_plants(request):
    """
    Called when buying a plant.\n
    Post data must include user_id.\n
    Returns {"plants": [ {plant info}, ... ]} filtered by user level,\n
    where user level is >= 1.
    """
    if request.method != "POST":
        return JsonResponse({"status": f"Error 405: Expected POST method. Received {request.method}"}, status=405)
    return JsonResponse({"plants": ["plant info", "plant info"]}, status=200)


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


# Shop tables
def all_plants(request):
    response = [{
        'id': 1,
        'name': 'Tutorial Flower',
        'cost': 0,
        'level': 0,
        'time_to_mature': 00.01,
        'exp_value': 40,
        'currency': 10,
        'region': 'Isle de Mikes',
        'desc': 'A Simple flower to teach you the ways of the garden.'
    },
        {
            'id': 2,
            'name': 'Emmay Bud',
            'cost': 2,
            'level': 1,
            'time_to_mature': 05.00,
            'exp_value': 5,
            'currency': 3,
            'region': 'Kahului',
            'desc': 'Strange bud that comes from a far away island.'
    },
        {
            'id': 3,
            'name': 'J Hideout',
            'cost': 2,
            'level': 1,
            'time_to_mature': 05.00,
            'exp_value': 5,
            'currency': 3,
            'region': 'Missouri',
            'desc': 'Inexplicably fades in and out of view as if seen through a low-quality camera.'
    },
        {
            'id': 4,
            'name': 'Silly-Dilly',
            'cost': 3,
            'level': 2,
            'time_to_mature': 08.00,
            'exp_value': 5,
            'currency': 5,
            'region': 'Ellenton',
            'desc': 'Is said to be the top in the leather community but no one knows what he means because he never leaves his garden.'
    },
        {
            'id': 5,
            'name': 'Jerelily',
            'cost': 3,
            'level': 2,
            'time_to_mature': 08.00,
            'exp_value': 5,
            'currency': 5,
            'region': 'Qubec',
            'desc': 'Though not native to the reagion, the Jerelily found its way to the frozen area of the North.'
    },
        {
            'id': 6,
            'name': 'Timint',
            'cost': 5,
            'level': 3,
            'time_to_mature': 11.00,
            'exp_value': 5,
            'currency': 9,
            'region': 'New Orleans',
            'desc': 'The Timint has forced itself to become purple through sheer wilpower.'
    },
        {
            'id': 7,
            'name': 'Augie Beauty',
            'cost': 7,
            'level': 3,
            'time_to_mature': 11.00,
            'exp_value': 5,
            'currency': 11,
            'region': 'Chicago',
            'desc': 'If you ever need a link for any topic the Augie Beauty has you covered.'
    },
        {
            'id': 8,
            'name': 'Geovannirod',
            'cost': 10,
            'level': 4,
            'time_to_mature': 14.00,
            'exp_value': 5,
            'currency': 14,
            'region': 'River Grove',
            'desc': 'The Geovannirod has a heart of gold and legend says it has written a book about soccer.'
    },
        {
            'id': 9,
            'name': 'Heather',
            'cost': 10,
            'level': 4,
            'time_to_mature': 14.00,
            'exp_value': 5,
            'currency': 14,
            'region': 'Columbia',
            'desc': 'You will often see the Heather flower solving puzzles while dreaming about going for a nice hike.'
    },
        {
            'id': 10,
            'name': 'Tom Blossom',
            'cost': 12,
            'level': 5,
            'time_to_mature': 17.00,
            'exp_value': 5,
            'currency': 17,
            'region': 'Zoomtopia',
            'desc': 'Often near a brick surrounding. The Tom Blossom gets excited when talking about bank drop boxes.'
    },
        {
            'id': 11,
            'name': 'Noalion',
            'cost': 12,
            'level': 5,
            'time_to_mature': 17.00,
            'exp_value': 5,
            'currency': 17,
            'region': 'Slackville',
            'desc': 'Ever so entergetic, the Noalion spends time being surrounded by birds.'
    }]
    return JsonResponse(response, safe=False)
