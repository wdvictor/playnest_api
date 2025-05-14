from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.auth_untils import require_api_token
from base.models import  Customer, Sale 
from api.serializers import  SaleSerializer
from rest_framework import status
from django.db.models import Sum
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 


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
        ),
        OpenApiParameter(
            name="Authorization",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="User authentication token"
        )
    ],
    responses={
        200: SaleSerializer(many=True),
        404: OpenApiTypes.OBJECT,
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
        ),
         OpenApiParameter(
            name="Authorization",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            required=True,
            description="User authentication token"
        )
    ],
    responses={
        201: SaleSerializer,
        400: OpenApiTypes.OBJECT,
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
    description="Retrieve the top user by sales volume",
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
@permission_classes([IsAuthenticated])
@require_api_token
def top_user_by_volume(request):
    top_user = (
        Customer.objects
        .annotate(total_sales=Sum('sales__amount'))
        .order_by('-total_sales')
        .first()
    )
    
    if top_user and top_user.total_sales: # type: ignore
        data = {
            'user_id': top_user.name,
            'name': top_user.name,
            'total_sales': top_user.total_sales, # type: ignore
        }
    else:
        data = {'detail': 'No Sales Found'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    methods=["GET"],
    description="Retrieve the top user by average sale value",
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
@permission_classes([IsAuthenticated])
@require_api_token
def top_user_by_avg_sale(request):
    users = (
        Customer.objects
        .annotate(
            total_sales=Sum('sales__amount'),
            num_sales=Count('sales'),
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

    top = users.first()

    if not top:
        return Response({'detail': 'No Sales Found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'user_id': top.id, # type: ignore
        'name': top.name, 
        'average_sale': round(top.avg_sale, 2), # type: ignore
        'total_sales': float(top.total_sales), # type: ignore
        'sales_count': top.num_sales # type: ignore
    }

    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    methods=["GET"],
    description="Retrieve the top user by purchase frequency",
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
@permission_classes([IsAuthenticated])
@require_api_token
def top_user_by_purchase_frequency(request):
    users = (
        Customer.objects
        .annotate(unique_days=Count('sales__date', distinct=True))
        .filter(unique_days__gt=0)
        .order_by('-unique_days')
    )

    top = users.first()

    if not top:
        return Response({'detail': 'No Sales Found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'user_id': top.id, # type: ignore
        'name': top.name,
        'unique_purchase_days': top.unique_days # type: ignore
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@require_api_token
@permission_classes([IsAuthenticated])
def get_all_users_data(requests):
    
    clientes_data = []

    users = Customer.objects.all().prefetch_related('details')
    sales = Sale.objects.all()

    for user in users:
        
        vendas_filtradas = sales.filter(user_id=user.id).values('date', 'amount',)
        vendas_formatadas = [
            {
                "data": venda['date'].strftime('%Y-%m-%d'),
                "valor": float(venda['amount'])
            }
            for venda in vendas_filtradas
        ]

        cliente_dict = {
            "info": {
                "nomeCompleto": user.name,
                "detalhes": {
                    "email": user.details.email,
                    "nascimento": user.details.birthday.strftime('%Y-%m-%d')
                }
            },
            "estatisticas": {
                "vendas": vendas_formatadas
            }
        }
        clientes_data.append(cliente_dict)

       
    response = {
        "data": {
            "clientes": clientes_data
        },
        "meta": {
            "registroTotal": users.count(),
            "pagina": 1
        },
        "redundante": {
            "status": "ok"
        }
    }

    return Response(response)

