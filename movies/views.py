from rest_framework.views import APIView, Response, Request
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from .permissions import IsAdmOrReadOnly
from django.shortcuts import get_object_or_404


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def post(self, req: Request) -> Response:
        serializer = MovieSerializer(
            data=req.data, context={"added_by": req.user.email}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user)

        return Response(serializer.data, 201)

    def get(self, req: Request):
        movies = Movie.objects.order_by("id")

        page = self.paginate_queryset(movies, req)

        serializer = MovieSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, req: Request, movie_id=int) -> Response:
        movies = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movies)

        return Response(serializer.data, 200)

    def delete(self, req: Request, movie_id=int) -> Response:
        movies = get_object_or_404(Movie, pk=movie_id)
        movies.delete()

        return Response(status=204)


class MovieOrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id=int) -> Response:
        movies = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieOrderSerializer(
            data=req.data,
            context=[{"buyed_by": req.user.email}, {"buyed_by": movie_id}],
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user, movie=movies)

        return Response(serializer.data, 201)
