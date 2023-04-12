from .models import User
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.tokens import RefreshToken


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
