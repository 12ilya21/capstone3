from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import IntegrityError
from .models import RestaurantInfo1, Bookmark
from .serializers import BookmarkSerializer, UserSerializer
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# User registration
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# User list view
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 북마크 생성
class UserBookmarkCreateView(APIView):
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        restaurant_name = request.data.get('restaurant_name')
        
        if not username or not restaurant_name:
            return Response({"error": "username and restaurant_name are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Try to get or create a new bookmark
            bookmark, created = Bookmark.objects.get_or_create(username=username, restaurant_name=restaurant.name)
            
            if created:
                # Increment the bookmark count for the restaurant
                restaurant.bookmark_count += 1
                restaurant.save()

            # Serialize the bookmark (newly created or existing)
            serializer = BookmarkSerializer(bookmark)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Bookmark already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
# 북마크 삭제
class UserBookmarkDeleteView(APIView):
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        restaurant_name = request.data.get('restaurant_name')

        if not username or not restaurant_name:
            return Response({"error": "username and restaurant_name are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Find the bookmark to delete
            bookmark = Bookmark.objects.get(username=username, restaurant_name=restaurant.name)
            bookmark.delete()

            # Decrement the bookmark count for the restaurant
            if restaurant.bookmark_count > 0:
                restaurant.bookmark_count -= 1
                restaurant.save()

            return Response({"message": "Bookmark deleted successfully"}, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "An error occurred while deleting the bookmark"}, status=status.HTTP_400_BAD_REQUEST)
        
# 북마크 표시
class BookmarkListView(APIView):
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        bookmarks = Bookmark.objects.filter(username=username)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 식당 좌표 넘기기
class RestaurantCoordinatesView(APIView):
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        restaurant_name = request.data.get('restaurant_name')
        
        if not restaurant_name:
            return Response({"error": "restaurant_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = RestaurantInfo1.objects.get(name=restaurant_name)
            data = {
                "name": restaurant.name,
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
            }
            return Response(data, status=status.HTTP_200_OK)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
