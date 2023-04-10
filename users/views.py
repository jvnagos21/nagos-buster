from rest_framework.views import APIView, Response, Request, status
from .models import User
from .serializers import UserSerializer


class UserView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, 201)
