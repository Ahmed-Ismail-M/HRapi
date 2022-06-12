from rest_framework import generics
from Attendance.serializers.AttSerializer import AttendanceSerializer

class AddAttendance(generics.GenericAPIView):
    """Generic view to register a new user"""

    serializer_class = AttendanceSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     group, created = Group.objects.get_or_create(name='Employee')
    #     group.save()
    #     user.groups.add(group)
    #     login(request, user)
    #     token, created = Token.objects.get_or_create(user=serializer.instance)
    #     return Response(
    #         {"token": token.key, "user_id": user.id}, status=status.HTTP_201_CREATED
    #     )
