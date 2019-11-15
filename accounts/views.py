from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User, Lector, Rate
from accounts.serializers import LectorSerializer, RegisterSerializer, UpdateUserSerializer, \
    VisitorSerializer, CreateRateSerializer, ReadUpdateRateSerializer
from meetenjoy.core import IsNotAuthenticated, IsLector, IsVisitor


class RegistrationAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, context={"request": request})
            if not serializer.is_valid():
                response_data = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
            else:
                user = serializer.save()
                login(request, user)
                response_data = {}
                response_status = status.HTTP_201_CREATED
            return Response(response_data, status=response_status)


class RetrieveUpdateUserAPIView(RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class RetrieveUpdateLectorAPIView(RetrieveUpdateAPIView):
    serializer_class = LectorSerializer
    permission_classes = [IsAuthenticated, IsLector]

    def get_object(self):
        return self.request.user.lector


class LectorListAPIView(ListAPIView):
    serializer_class = LectorSerializer
    queryset = Lector.objects.all()


class RetrieveUpdateVisitorAPIView(RetrieveUpdateAPIView):
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated, IsVisitor]

    def get_object(self):
        return self.request.user.visitor


class CreateRateLectorView(CreateAPIView):
    serializer_class = CreateRateSerializer
    permission_classes = [IsAuthenticated, IsVisitor]

    def create(self, request, *args, **kwargs):
        visitor = request.user.visitor
        lector = get_object_or_404(Lector, id=request.data.get("lector"))
        if lector in visitor.rated_lectors.all():
            return Response({"message": "Lector with this id already rated be current visitor"},
                            status=status.HTTP_400_BAD_REQUEST)
        data = {
            "visitor": visitor.id,
            "lector": lector.id,
            "rate": request.data.get("rate"),
            "comment": request.data.get("comment"),
        }
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateRateLectorView(RetrieveUpdateAPIView):
    serializer_class = ReadUpdateRateSerializer
    permission_classes = [IsAuthenticated, IsVisitor]

    def get_queryset(self):
        visitor = self.request.user.get_visitor()
        if visitor is not None:
            return visitor.rates.all()
        return Rate.objects.none()
