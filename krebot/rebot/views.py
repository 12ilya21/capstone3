from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.db import IntegrityError
from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
from django.http import JsonResponse
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, logout
from .models import Profile
# from django.conf import settings

import json

from .models import RestaurantInfo1, Bookmark
from .serializers import BookmarkSerializer

from django.db import IntegrityError
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import RestaurantInfo1, Bookmark
from .serializers import BookmarkSerializer

# 북마크 추가
class UserBookmarkCreateView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        restaurant_name = request.data.get('restaurant_name')
        language = request.data.get('language')  # 언어 추가
        
        if not username or not restaurant_name or not language:
            return Response({"error": "username, restaurant_name, and language are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the restaurant based on the language
            if language == 'ko':
                restaurant = RestaurantInfo1.objects.get(name_ko=restaurant_name)
            elif language == 'en':
                restaurant = RestaurantInfo1.objects.get(name_en=restaurant_name)
            elif language == 'ja':
                restaurant = RestaurantInfo1.objects.get(name_ja=restaurant_name)
            elif language == 'zh':
                restaurant = RestaurantInfo1.objects.get(name_zh=restaurant_name)
            else:
                return Response({"error": "Unsupported language"}, status=status.HTTP_400_BAD_REQUEST)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Try to get or create a new bookmark
            bookmark, created = Bookmark.objects.get_or_create(username=username, restaurant_name=restaurant.name_ko)
            
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
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        restaurant_name = request.data.get('restaurant_name')
        language = request.data.get('language')  # 사용자의 언어 정보 추가

        if not username or not restaurant_name or not language:
            return Response({"error": "username, restaurant_name, and language are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 언어에 따라 적절한 레스토랑 이름 필드 선택
        if language == 'ko':
            restaurant_name_field = 'name_ko'
        elif language == 'en':
            restaurant_name_field = 'name_en'
        elif language == 'ja':
            restaurant_name_field = 'name_ja'
        elif language == 'zh':
            restaurant_name_field = 'name_zh'
        else:
            return Response({"error": "Invalid language"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 해당 언어의 레스토랑 정보 가져오기
            restaurant = RestaurantInfo1.objects.get(**{restaurant_name_field: restaurant_name})
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # 해당 레스토랑의 북마크 삭제
            bookmark = Bookmark.objects.get(username=username, restaurant_name=restaurant.name_ko)
            bookmark.delete()

            # 레스토랑의 북마크 수 감소
            if restaurant.bookmark_count > 0:
                restaurant.bookmark_count = F('bookmark_count') - 1
                restaurant.save()

            return Response({"message": "Bookmark deleted successfully"}, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "An error occurred while deleting the bookmark"}, status=status.HTTP_400_BAD_REQUEST)

# 북마크 표시 
class BookmarkListView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        language = request.data.get('language')  # 기본값은 한국어

        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        bookmarks = Bookmark.objects.filter(username=username)
        bookmark_data = []

        for bookmark in bookmarks:
            try:
                restaurant_info = RestaurantInfo1.objects.get(name_ko=bookmark.restaurant_name)
                if language == 'en':
                    image_url = restaurant_info.image_en.url
                    restaurant_name = restaurant_info.name_en
                elif language == 'ja':
                    image_url = restaurant_info.image_ja.url
                    restaurant_name = restaurant_info.name_ja
                elif language == 'zh':
                    image_url = restaurant_info.image_zh.url
                    restaurant_name = restaurant_info.name_zh
                else:
                    image_url = restaurant_info.image_ko.url
                    restaurant_name = restaurant_info.name_ko

                bookmark_data.append({
                    'username': bookmark.username,
                    'restaurant_name': restaurant_name,
                    'image_url': image_url
                })
            except RestaurantInfo1.DoesNotExist:
                pass

        return Response(bookmark_data, status=status.HTTP_200_OK)

# 식당 좌표 넘기기
class RestaurantCoordinatesView(APIView):
    @csrf_exempt
    def post(self, request):
        restaurant_name = request.data.get('restaurant_name')
        
        if not restaurant_name:
            return Response({"error": "restaurant_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = RestaurantInfo1.objects.get(name_ko=restaurant_name)  # 변경
            data = {
                "name": restaurant.name_ko,  # 변경
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
            }
            return Response(data, status=status.HTTP_200_OK)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
# 식당 좌표 넘기기(언어 필요시)
'''
class RestaurantCoordinatesView(APIView):
    @csrf_exempt
    def post(self, request):
        restaurant_name = request.data.get('restaurant_name')
        language = request.data.get('language')  # 언어 정보 추가
        
        if not restaurant_name or not language:
            return Response({"error": "restaurant_name and language are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 언어에 따라 적절한 필드 선택
        if language == 'ko':
            name_field = 'name_ko'
        elif language == 'en':
            name_field = 'name_en'
        elif language == 'ja':
            name_field = 'name_ja'
        elif language == 'zh':
            name_field = 'name_zh'
        else:
            return Response({"error": "Unsupported language"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 선택한 언어에 따라 적절한 필드로 식당 정보 가져오기
            restaurant = RestaurantInfo1.objects.get(**{name_field: restaurant_name})
            data = {
                "name": getattr(restaurant, name_field),
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
            }
            return Response(data, status=status.HTTP_200_OK)
        except RestaurantInfo1.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
'''

# 회원가입
@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        language = data.get('language', 'en')

        if password1 != password2:
            return JsonResponse({'error': "Passwords don't match"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': "Email already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Create Profile for the new user if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=user, defaults={'language': language})

        login(request, user)
        return JsonResponse({'message': 'User registered successfully!'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 로그인
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful', 'username': user.username}, status=200)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 로그아웃
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


#@login_required
def get_user_info(request, username):
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        return JsonResponse({
            'username': user.username,
            'language': profile.language
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

# CSRF 쿠키 관련
@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
