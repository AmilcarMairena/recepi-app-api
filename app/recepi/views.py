from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recepi

from recepi import serializers


class BaseRecepiViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Base model to refact the classes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns objects only for authenticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user = self.request.user)



class TagViewSet(BaseRecepiViewSet):
    """Manage tags in database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer



class IngredientViewSet(BaseRecepiViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecepiViewSet(viewsets.ModelViewSet):
    """Manage recepis in database"""
    serializer_class = serializers.RecepiSerializer
    queryset = Recepi.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """REtrieve the recepis for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecepiDetailSerializer

        return self.serializer_class
