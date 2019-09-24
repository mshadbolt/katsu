from rest_framework import viewsets, pagination
from .serializers import *
from .models import *


class LargeResultsSetPagination(pagination.PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page_size'
	max_page_size = 10000


class VariantViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing variants

	post:
	Create a new variant

	"""
	queryset = Variant.objects.all()
	serializer_class = VariantSerializer
	pagination_class = LargeResultsSetPagination
	# TODO filtering
	# filter_backends = (DjangoFilterBackend,)
	# filter_class = VariantFilter


class PhenotypicFeatureViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing phenotypic features

	post:
	Create a new phenotypic feature

	"""
	queryset = PhenotypicFeature.objects.all()
	serializer_class = PhenotypicFeatureSerializer
	pagination_class = LargeResultsSetPagination


class ProcedureViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing procedures

	post:
	Create a new procedure

	"""
	queryset = Procedure.objects.all()
	serializer_class = ProcedureSerializer
	pagination_class = LargeResultsSetPagination


class HtsFileViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing HTS files

	post:
	Create a new HTS file

	"""
	queryset = HtsFile.objects.all()
	serializer_class = HtsFileSerializer
	pagination_class = LargeResultsSetPagination


class GeneViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing genes

	post:
	Create a new gene

	"""
	queryset = Gene.objects.all()
	serializer_class = GeneSerializer
	pagination_class = LargeResultsSetPagination


class DiseaseViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing diseases

	post:
	Create a new disease

	"""
	queryset = Disease.objects.all()
	serializer_class = DiseaseSerializer
	pagination_class = LargeResultsSetPagination


class ResourceViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing resources

	post:
	Create a new resource

	"""
	queryset = Resource.objects.all()
	serializer_class = ResourceSerializer
	pagination_class = LargeResultsSetPagination


class UpdateViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing updates

	post:
	Create a new update

	"""
	queryset = Update.objects.all()
	serializer_class = UpdateSerializer
	pagination_class = LargeResultsSetPagination


class ExternalReferenceViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing external references

	post:
	Create a new external reference

	"""
	queryset = ExternalReference.objects.all()
	serializer_class = ExternalReferenceSerializer
	pagination_class = LargeResultsSetPagination


class MetaDataViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing metadata records

	post:
	Create a new metadata record

	"""
	queryset = MetaData.objects.all()
	serializer_class = MetaDataSerializer
	pagination_class = LargeResultsSetPagination


class IndividualViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing individuals

	post:
	Create a new individual

	"""
	queryset = Individual.objects.all()
	serializer_class = IndividualSerializer
	pagination_class = LargeResultsSetPagination


class BiosampleViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing biosamples

	post:
	Create a new biosample
	"""
	queryset = Biosample.objects.all()
	serializer_class = BiosampleSerializer
	pagination_class = LargeResultsSetPagination


class PhenopacketViewSet(viewsets.ModelViewSet):
	"""
	get:
	Return a list of all existing phenopackets

	post:
	Create a new phenopacket

	"""
	queryset = Phenopacket.objects.all()
	serializer_class = PhenopacketSerializer
	pagination_class = LargeResultsSetPagination
