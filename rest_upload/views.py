from django.views.generic.base import View
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response

from bson.json_util import dumps
from .serializers import *

import xml.sax


class XmlFileHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.requiredList = []
        self.item = {}
        self.CurrentData = ""
        self.PluginName = ""
        self.RiskFactor = ""
        self.Description = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag

        if tag == "plugins":
            print("*****Plugin*****")
            title = attributes["title"]
            print("Title:", title)

    # Call when an elements ends
    def endElement(self, tag):
        if "PluginName" and "Description" and "RiskFactor" in self.item:
            self.requiredList.append(self.item)
            self.item = {}
        if self.CurrentData == "plugin_name":
            self.item.update({"PluginName": self.plugin_name})
        elif self.CurrentData == "description":
            self.item.update({"Description": self.description})
        elif self.CurrentData == "risk_factor":
            self.item.update({"RiskFactor": self.risk_factor})
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):

        if self.CurrentData == "plugin_name":
            self.plugin_name = content
        elif self.CurrentData == "description":
            self.description = content
        elif self.CurrentData == "risk_factor":
            self.risk_factor = content


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = serializer.data
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = XmlFileHandler()
        parser.setContentHandler(handler)
        parser.parse(response['file'])
        return Response(handler.requiredList)


class XMLProcessor(View):

    def post(self, request):

        plugins = request.FILES.getlist("plugins")
        if len(plugins) == 1:
            file_format = plugins[0].name.split('.')[-1]
            if file_format == 'xml':
                parser = xml.sax.make_parser()
                parser.setFeature(xml.sax.handler.feature_namespaces, 0)
                handler = XmlFileHandler()
                parser.setContentHandler(handler)
                parser.parse(plugins[0])
                return HttpResponse(dumps(handler.requiredList))
            else:
                return HttpResponse("we accept xml file only")
        else:
            return HttpResponse("plugins file required")
