import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.auth_untils import require_api_token
from base.models import  Customer, Sale 
from .serializers import  CustomerSerializer, SaleSerializer
from rest_framework import status
from django.db.models import Sum
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper


logger = logging.getLogger(__name__)

@api_view(['POST'])
@require_api_token
def add_customer(request):
    
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        
        serializer.save()
    else:
        return Response(serializer.errors, status=400)
    return Response(serializer.data)

@api_view(['POST'])
@require_api_token
def get_all_Customers(request):
    try:
        data = request.data 
        filter = data.get('filter', None)
        
        if filter == 'name':
            customers= Customer.objects.filter(name__icontains=data.get('data', ''))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        
        elif filter == 'email':    
            customers = Customer.objects.filter(details__email__icontains=data.get('data', ))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
      
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        logger.error(f'Error at get_all_customers {str(e)}', exc_info=True)

        return Response({"error": "No customers found"}, status=404)
    
@api_view(['DELETE'])
@require_api_token
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response({'message': 'Cliented deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f'Error at delete_customer {str(e)}', exc_info=True)

        return Response({'error': 'Client Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@require_api_token
def update_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Client Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@require_api_token
def get_all_sales(request):
    try:
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error at get_all_sales {str(e)}', exc_info=True)
        return Response({"error": "No sales found"}, status=404)
    



@api_view(['PUT'])
@require_api_token
def add_sale(request):
       
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@require_api_token
def total_sales_per_day(request):
    stats = (
        Sale.objects
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )
    return Response(stats)


@api_view(['GET'])
@require_api_token
def top_customer_by_volume(request):
    top_customer = (
        Customer.objects
        .annotate(total_sales=Sum('sale__amount'))
        .order_by('-total_sales')
        .first()
    )

    if top_customer and top_customer.total_sales:
        data = {
            'customer_id': top_customer.name,
            'name': top_customer.name,
            'total_sales': top_customer.total_sales,
        }
    else:
        data = {'detail': 'No Sales Found'}

    return Response(data)



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

    if top:
        data = {
            'customer_id': top.id,
            'name': top.name,
            'average_sale': round(top.avg_sale, 2),
            'total_sales': float(top.total_sales),
            'sales_count': top.num_sales
        }
    else:
        data = {'detail': 'No Sales Found'}

    return Response(data)


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

    if top:
        data = {
            'customer_id': top.id,
            'name': top.name,
            'unique_purchase_days': top.unique_days
        }
    else:
        data = {'detail': 'No Sales Found'}

    return Response(data)
