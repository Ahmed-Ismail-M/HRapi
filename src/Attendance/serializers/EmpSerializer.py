from Attendance.models import Employee, User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['password', 'username', 'first_name',
                  'last_name', 'email', 'is_superuser']
        extra_kwargs = {"email": {"required": True}}

    def create(self, validated_data):
        user = Employee.objects.create(**validated_data)
        group, created = Group.objects.get_or_create(name='Employee')
        group.save()
        user.groups.add(group)
        return user


class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print(User.objects.get(username=username).is_superuser)
        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                print(user)
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
