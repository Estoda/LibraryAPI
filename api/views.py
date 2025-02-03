from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import viewsets, generics, permissions, status
from .serializers import UserSerializer, BookSerializer, TransactionSerializer
from .models import User, Book, Transaction
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


class UserListCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "User has been deleted!"})


class BookListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response(status=404)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book:
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=404)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book:
            serializer = BookSerializer(book)
            if serializer.is_valid():
                book.delete()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=404)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            # Remove tokens from JSON response for security
            del response.data["access"]
            del response.data["refresh"]
        return response


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.user.is_authenticated:  # Check if the user is already authenticated
            return Response(
                {"message": "You are already logged in."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = authenticate(
                username=request.data["username"], password=request.data["password"]
            )
            if user:
                refresh = RefreshToken.for_user(user)
                response = Response(
                    {
                        "message": "Registration Successful",
                        "user": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
                response.set_cookie(
                    key="access_token",
                    value=str(refresh.access_token),
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                )
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                )
            return response
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()  # Blacklist the token (invalidate it)
            except Exception as e:
                pass
        response = Response(
            {"message": "Successfully logged out!"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CheckoutBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        if book.stock > 0:
            book.stock -= 1
            book.save()
            transaction = Transaction.objects.create(book=book, user=request.user)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Book out of stock"}, status=status.HTTP_400_BAD_REQUEST
        )


class TransactionsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id)
        if transaction.return_date is None:
            transaction.return_date = timezone.now()
            transaction.book.stock += 1
            transaction.book.save()
            transaction.save()
            return Response({"message": "Book returned successfully"})
        return Response(
            {"error": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
