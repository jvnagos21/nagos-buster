from .models import User
from .serializers import UserSerializer, LoginSerializer
from .permissions import IsAccountEmployeeOrNot
from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class UserView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, 201)


class LoginView(APIView):
    def post(self, req: Request) -> Response:
        serializer = LoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"}, 401
            )

        refresh = RefreshToken.for_user(user)

        token_dict = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(token_dict, 200)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountEmployeeOrNot]

    def get(self, req: Request, user_id=int) -> Response:
        user = get_object_or_404(User, pk=user_id)

        self.check_object_permissions(req, user)
        serializer = UserSerializer(user)

        return Response(serializer.data, 200)

    def patch(self, req: Request, user_id=int) -> Response:
        user = get_object_or_404(User, pk=user_id)

        self.check_object_permissions(req, user)

        serializer = UserSerializer(user, req.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 200)
