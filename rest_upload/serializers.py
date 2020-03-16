from rest_framework import serializers
from .models import *


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Document
        fields = ('url', 'title', 'file')
