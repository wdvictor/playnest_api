from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item, Customer
from .serializers import ItemSerializer, CustomerSerializer

@api_view(['GET'])
def getData(request):
    items = Item.objects.all()
    serializers = ItemSerializer(items, many=True)
    return Response(serializers.data)


@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def addCustomer(request):
    
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        
        serializer.save()
    else:
        return Response(serializer.errors, status=400)
    return Response(serializer.data)

@api_view(['POST'])
def getCustomers(request):
    try:
        
        customers = Customer.objects.all()  
        serializer = CustomerSerializer(customers, many=True) 
        return Response(serializer.data)    
    except:
        return Response({"error": "No customers found"}, status=404)