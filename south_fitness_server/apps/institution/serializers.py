from rest_framework.serializers import ModelSerializer
from .models import Institutions


class InstitutionSerializer(ModelSerializer):

    class Meta:
        model = Institutions
        fields = '__all__'
