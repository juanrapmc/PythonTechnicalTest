from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions
from bonds.models import Bond
from bonds.serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondList(generics.ListCreateAPIView):
    serializer_class = BondSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Bond.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Save the bond instance with user info
        """
        serializer.save(user=self.request.user)
