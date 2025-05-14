

from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.auth_untils import require_api_token
from base.models import  User, Sale 
from api.serializers import  UserSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 


@extend_schema(
    methods=["POST"],
    description="Add a new user",
    request=UserSerializer,
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="API authentication token"
        )
    ],
    responses={
        201: UserSerializer,
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['POST'])
@require_api_token
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    methods=["POST"],
    description="Retrieve all users with optional filters",
    request=OpenApiTypes.OBJECT,
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="API authentication token"
        )
    ],
    responses={
        200: UserSerializer(many=True),
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['POST'])
@require_api_token
def get_all_users(request):
    try:
        data = request.data 
        filter = data.get('filter', None)
        if filter == 'name':
            users = User.objects.filter(name__icontains=data.get('data', ''))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        
        elif filter == 'email':    
            users = User.objects.filter(details__email__icontains=data.get('data'))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
      
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({"error": "No users found"}, status=404)

@extend_schema(
    methods=["DELETE"],
    description="Delete a user by ID",
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="API authentication token"
        ),
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the user to delete"
        )
    ],
    responses={
        204: None,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['DELETE'])
@require_api_token
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    methods=["PUT"],
    description="Update a user by ID",
    request=UserSerializer,
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="API authentication token"
        ),
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the user to update"
        )
    ],
    responses={
        200: UserSerializer,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['PUT'])
@require_api_token
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
