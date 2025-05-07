from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def signup(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User ' + user.username + ' created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @api_view(['GET'])
    def logout_view(request):
        logout(request)
        return Response({'message': 'Logged out successfully'})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def user_view(request):
        return Response({'username': request.user.username})