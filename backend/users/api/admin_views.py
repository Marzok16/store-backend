from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_user_admin(request):
    """
    Make a user admin (superuser only)
    """
    if not request.user.is_superuser:
        return Response(
            {"error": "Superuser access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    if not user_id:
        return Response(
            {"error": "user_id is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    user.is_staff = True
    user.save()
    
    serializer = UserSerializer(user)
    return Response({
        "message": f"User {user.email} is now an admin",
        "user": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """
    List all users (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    users = User.objects.all().order_by('-date_joined')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
