from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import cloudinary.uploader
from rest_framework.authtoken.models import Token
from ..models import Profile
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UpdateProfileSerializer, \
    CreateProfileSerializer, ProfileSerializer, UpdateProfileImageSerializer


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Success"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            print(token)
            data['token'] = token
            profile = CreateProfileSerializer(data={'account': account.id})
            if profile.is_valid():
                profile.save()
        else:
            for i in serializer.errors:
                print(i)
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_view(request):
    user = request.user
    serializer = UserProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_profile(request):
    profile_id = request.user.profile.id
    profile = Profile.objects.filter(id=profile_id).first()
    request_data = request.data

    serializer = UpdateProfileSerializer(instance=profile, data=request_data)

    if serializer.is_valid():
        serializer.save()
        profile = Profile.objects.filter(id=request.user.profile.id).first()
        data = {
            'is_success': True,
            'message': 'Your profile was updated successfully',
            'user': {
                'firstName': profile.firstName,
                'lastName': profile.lastName,
                'phone': profile.phone,
                'town': profile.town,
                'country': profile.country,
            }
        }
    else:
        data = {
            'is_success': False,
            'message': 'something went wrong, please try again'}
    return Response(data)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_profile_image(request):
    profile = Profile.objects.filter(account=request.user.id).first()
    request_img = request.FILES
    serializer = UpdateProfileImageSerializer(profile, data=request_img)
    if serializer.is_valid():
        serializer.save()
        data = {'message': 'Success'}
    else:
        data = {'message': 'error'}
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_profile_view(request):
    profile = Profile.objects.filter(account=request.user.id).first()
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)
