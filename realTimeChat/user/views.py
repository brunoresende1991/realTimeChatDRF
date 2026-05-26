from rest_framework.generics import CreateAPIView

from user.serializers import UserSerializer


class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer
