import graphene
from graphene_django import DjangoObjectType
from . import models
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Field
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class CompanyConfigurationNode(DjangoObjectType):
    class Meta:
        model = models.CompanyConfiguration


class CompanyNode(DjangoObjectType):
    configuration = graphene.Field(CompanyConfigurationNode)

    class Meta:
        model = models.Company


class Query(object):
    companies = graphene.List(CompanyNode)

    def resolve_companies(self, info, **kwargs):
        query = models.Company.objects.all()
        filter = info.context.GET.get('filter', '')
        if filter is not None:
            query = query.filter(fiscalName__icontains=filter)
        return paginate(info, query)


def paginate(info, query):
    page = int(info.context.GET.get('page', 1))
    items = int(info.context.GET.get('limit', 20))
    paginator = Paginator(query, items)
    if paginator.num_pages < page or page < 1:
        return []
    results = paginator.get_page(page)
    return results
