from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from rest_framework import serializers, status

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)

@api_view(['POST'])
def createItem(request):
    try:
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            if Item.objects.filter(**request.data).exists():
                return Response({
                    'status': False,
                    'message': 'This data already exists',
                }, status=400)
            serializer.save()
            responseData = {
                'status': True,
                'message': 'Item created successfully',
                'data': serializer.data
            }
            return Response(responseData, status=status.HTTP_201_CREATED)
        else:
            formatted_errors = []

            for field, messages in serializer.errors.items():
                for msg in messages:
                    print(field, msg)
                    # Replace "this value" with field name if it exists
                    msg = msg.replace("this value", field)
                    msg = msg.replace("This field", field.capitalize())
                    # Capitalize nicely
                    # formatted_errors.append(f"{msg[0].lower() + msg[1:]}")
                    formatted_errors.append(f"{msg}")

            return Response({
                'status': False,
                'message': 'Item creation failed',
                'errors': formatted_errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except serializers.ValidationError as e:
        return Response({
            'status': False,
            'message': 'Something went wrong.',
            'errors': e.detail
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def view_items(request):
    requestData = request.query_params.dict()
    print(requestData)
    category = requestData.get('category')
    subcategory = requestData.get('subcategory')
    if category:
        if subcategory:
            items = Item.objects.filter(category=category, subcategory=subcategory)
        else:
            items = Item.objects.filter(category=category)
        serializer = ItemSerializer(items, many=True)
        responseData = {
            'status': True,
            'message': 'Items retrieved successfully',
            'data': serializer.data
        }
        return Response(responseData)
    else:
        return Response({
            'status': False,
            'message': 'Category parameter is required',
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def update_item(request, pk):
    try:
        print(pk)
        if(not pk):
            return Response({
                'status': False,
                'message': 'Item id is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        item = Item.objects.get(id=pk)
        serializer = ItemSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            responseData = {
                'status': True,
                'message': 'Item updated successfully',
                'data': serializer.data
            }
            return Response(responseData)
        else:
            formatted_errors = []

            for field, messages in serializer.errors.items():
                for msg in messages:
                    print(field, msg)
                    # Replace "this value" with field name if it exists
                    msg = msg.replace("this value", field)
                    msg = msg.replace("This field", field.capitalize())
                    formatted_errors.append(f"{msg}")

            return Response({
                'status': False,
                'message': 'Item update failed',
                'errors': formatted_errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Item.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Item not found',
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'status': False,
            'message': 'Something went wrong.',
            'errors': e.detail
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_item(request, pk):
    try:
        if(not pk):
            return Response({
                'status': False,
                'message': 'Item id is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        item = Item.objects.get(id=pk)
        item.delete()
        return Response({
            'status': True,
            'message': 'Item deleted successfully',
        })
    except Item.DoesNotExist:
        return Response({
            'status': False,
            'message': 'Item not found',
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'status': False,
            'message': 'Something went wrong.',
            'errors': e.detail
        }, status=status.HTTP_400_BAD_REQUEST)


