

from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.auth_untils import require_api_token
from base.models import  Customer, Sale 
from api.serializers import  CustomerSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 


@extend_schema(
    methods=["POST"],
    description="Add a new customer",
    request=CustomerSerializer,
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
        201: CustomerSerializer,
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['POST'])
@require_api_token
def add_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    methods=["POST"],
    description="Retrieve all customers with optional filters",
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
def get_all_customers(request):
    try:
        data = request.data 
        filter = data.get('filter', None)
        if filter == 'name':
            customers = Customer.objects.filter(name__icontains=data.get('data', ''))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        
        elif filter == 'email':    
            customers = Customer.objects.filter(details__email__icontains=data.get('data'))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
      
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({"error": "No customers found"}, status=404)

@extend_schema(
    methods=["DELETE"],
    description="Delete a customer by ID",
    parameters=[
        OpenApiParameter(
            name="X-API-KEY",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="API authentication token"
        ),
        OpenApiParameter(
            name="customer_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the customer to delete"
        )
    ],
    responses={
        204: None,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['DELETE'])
@require_api_token
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'Customer Not Found'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    methods=["PUT"],
    description="Update a customer by ID",
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
            name="customer_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description="ID of the customer to update"
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
def update_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
