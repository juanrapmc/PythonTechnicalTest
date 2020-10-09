from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions, filters
from bonds.models import Bond
from bonds.serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondList(generics.ListCreateAPIView):
    serializer_class = BondSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Bond.objects.all()
        user = self.request.user
        legal_name = self.request.query_params.get("legal_name", None)
        if legal_name is not None:
            queryset = Bond.objects.filter(user=user, legal_name=legal_name)
        else:
            queryset = Bond.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        """
        Save the bond instance with user info
        """
        serializer.save(user=self.request.user)
