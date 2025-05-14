

from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.auth_untils import require_api_token
from base.models import  Customer
from api.serializers import  RegisterSerializer, CustomerSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(
    methods=["POST"],
    description="Create a new user account",
    request=RegisterSerializer,
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
        201: {
            'access': 'ACESS_TOKEN',
            'refresh': 'REFRESH_TOKEN',
        },
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['POST'])
@require_api_token
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=["POST"],
    description="Add a new user",
    request=Customer,
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
        201: Customer,
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['POST'])
@require_api_token
def add_user(request):
    serializer = CustomerSerializer(data=request.data)
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
        200: CustomerSerializer(many=True),
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
            users = Customer.objects.filter(name__icontains=data.get('data', ''))
            serializer = CustomerSerializer(users, many=True)
            return Response(serializer.data)
        
        elif filter == 'email':    
            users = Customer.objects.filter(details__email__icontains=data.get('data'))
            serializer = CustomerSerializer(users, many=True)
            return Response(serializer.data)
      
        users = Customer.objects.all()
        serializer = CustomerSerializer(users, many=True)
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
        user = Customer.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    methods=["PUT"],
    description="Update a user by ID",
    request=CustomerSerializer,
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
        200: CustomerSerializer,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['PUT'])
@require_api_token
def update_user(request, user_id):
    try:
        user = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
