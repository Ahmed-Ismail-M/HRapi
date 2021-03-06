from rest_framework import generics
from Attendance.serializers.EmpSerializer import EmployeeRegisterSerializer, EmployeeLoginSerializer
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response


class RegisterAPI(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(
            {"user_id": user.id}, status=status.HTTP_201_CREATED
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = EmployeeLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.validated_data["user"]
        login(request, user)
        return Response(
            {"user_id": user.id}, status=status.HTTP_200_OK
        )
