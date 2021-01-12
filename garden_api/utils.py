from gardens.serializers import UserSerializer, ProfileSerializer, GardenSerializer

def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'profile': ProfileSerializer(user.profile).data,
        # 'garden': GardenSerializer(user.garden).data,
    }