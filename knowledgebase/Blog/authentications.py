from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


#Register API
class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })

class ChangePassword(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer




