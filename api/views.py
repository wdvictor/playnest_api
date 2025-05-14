from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.auth_untils import require_api_token
from base.models import  Customer, Sale 
from .serializers import  CustomerSerializer, SaleSerializer
from rest_framework import status
from django.db.models import Sum
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
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

@extend_schema(
    methods=["GET"],
    description="Retrieve all sales",
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
        200: SaleSerializer(many=True),
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@require_api_token
def get_all_sales(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)

    if not sales:
        return Response({"error": "No sales found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.data)

@extend_schema(
    methods=["PUT"],
    description="Add a new sale",
    request=SaleSerializer,
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
        201: SaleSerializer,
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['PUT'])
@require_api_token
def add_sale(request):
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=["GET"],
    description="Retrieve total sales per day",
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
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@require_api_token
def total_sales_per_day(request):
    stats = (
        Sale.objects
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    if not stats:
        return Response({'detail': 'No Sales Found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(stats, status=status.HTTP_200_OK)

@extend_schema(
    methods=["GET"],
    description="Retrieve the top customer by sales volume",
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
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@require_api_token
def top_customer_by_volume(request):
    top_customer = (
        Customer.objects
        .annotate(total_sales=Sum('sale__amount'))
        .order_by('-total_sales')
        .first()
    )
    
    if top_customer and top_customer.total_sales: # type: ignore
        data = {
            'customer_id': top_customer.name,
            'name': top_customer.name,
            'total_sales': top_customer.total_sales, # type: ignore
        }
    else:
        data = {'detail': 'No Sales Found'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    methods=["GET"],
    description="Retrieve the top customer by average sale value",
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
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@require_api_token
def top_customer_by_avg_sale(request):
    customers = (
        Customer.objects
        .annotate(
            total_sales=Sum('sale__amount'),
            num_sales=Count('sale'),
        )
        .filter(num_sales__gt=0) 
        .annotate(
            avg_sale=ExpressionWrapper(
                F('total_sales') / F('num_sales'),
                output_field=FloatField()
            )
        )
        .order_by('-avg_sale')
    )

    top = customers.first()

    if not top:
        return Response({'detail': 'No Sales Found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'customer_id': top.id, # type: ignore
        'name': top.name, 
        'average_sale': round(top.avg_sale, 2), # type: ignore
        'total_sales': float(top.total_sales), # type: ignore
        'sales_count': top.num_sales # type: ignore
    }

    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    methods=["GET"],
    description="Retrieve the top customer by purchase frequency",
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
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@require_api_token
def top_customer_by_purchase_frequency(request):
    customers = (
        Customer.objects
        .annotate(unique_days=Count('sale__date', distinct=True))
        .filter(unique_days__gt=0)
        .order_by('-unique_days')
    )

    top = customers.first()

    if not top:
        return Response({'detail': 'No Sales Found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'customer_id': top.id, # type: ignore
        'name': top.name,
        'unique_purchase_days': top.unique_days # type: ignore
    }

    return Response(data, status=status.HTTP_200_OK)

