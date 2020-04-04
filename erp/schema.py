import graphene
from graphene_django import DjangoObjectType
from . import models, forms
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Field
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from graphene_django.forms.mutation import DjangoModelFormMutation
from django.shortcuts import get_object_or_404




class CompanyConfigurationNode(DjangoObjectType):
    logo = graphene.String()
    class Meta:
        model = models.CompanyConfiguration

    def resolve_logo(self, info, **kwargs):
        return self.logoUrl



class CompanyNode(DjangoObjectType):
    configuration = graphene.Field(CompanyConfigurationNode)

    class Meta:
        model = models.Company
class Query(object):
    companies = graphene.List(CompanyNode)
    configurations = graphene.List(CompanyConfigurationNode)

    def resolve_companies(self, info, **kwargs):
        query = models.Company.objects.all()
        return paginate(info, query)

    def resolve_configurations(self, info, **kwargs):
        query = models.CompanyConfiguration.objects.all()
        return paginate(info, query)


def paginate(info, query):
    filters = info.context.GET
    newFilters = {}
    for x,y in filters.items():
        y =  filters.getlist(f'{x}')
        if x not in ['page', 'limit']:
            if len(y) > 1:
                try:
                    int(y[0])
                    int(y[1])
                except:
                    newFilters[f'{x}__in'] = y
                else:
                    newFilters[f'{x}__range'] = [int(i) for i in y]
            else:
                try:
                    int(y[0])
                except:
                    newFilters[f'{x}__icontains'] = y[0]
                else:
                    newFilters[f'{x}'] = int(y[0])
    query = query.filter(**newFilters)
    items = int(info.context.GET.get('limit',0))
    if items == 0:
        return query
    else:
        paginator = Paginator(query, items)
    page = int(info.context.GET.get('page', 1))
    if paginator.num_pages < page or page < 1:
        return []
    try:
        return paginator.get_page(page)
    except:
        return []


class CompanyMutation(DjangoModelFormMutation):
    company = graphene.Field(CompanyNode)

    class Meta:
        form_class = forms.CompanyForm


class CreateCompanyConfig(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        shortName = graphene.String()
        primaryColor = graphene.String()
        secondaryColor = graphene.String()
        company = graphene.String()
    companyConfig = graphene.Field(lambda: CompanyConfigurationNode)

    def mutate(root, info, **kwargs):
        instance = get_object_or_404(models.Company, id=int(kwargs.get('company')))
        kwargs['company'] = instance
        if kwargs['id'] == '':
            del kwargs['id']
            comcon = models.CompanyConfiguration.objects.get_or_create(**kwargs)[0]
        else:
            comcon = models.CompanyConfiguration.objects.filter(id=kwargs['id']).update(**kwargs)
            comcon = models.CompanyConfiguration.objects.get(id=kwargs['id'])
        return CreateCompanyConfig(companyConfig=comcon)





# class CompanyConfigurationMutation(graphene.ObjectType):
    # configuration = CreateCompanyConfig.Field()

    # class Meta:
        # form_class = forms.CompanyConfigurationForm




class DeleteCompanyMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.get(id=kwargs["id"])
        obj.delete()
        return cls(ok=True)





class DeleteCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class ActivateCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"]).update(isActive=True)
        return cls(ok=True)

class DesactivateCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"]).update(isActive=False)
        return cls(ok=True)

class Mutation(graphene.ObjectType):
    add_company = CompanyMutation.Field()
    add_configuration = CreateCompanyConfig.Field()
    delete_company = DeleteCompanyMutation.Field()
    delete_companies = DeleteCompaniesListMutation.Field()
    activate_companies = ActivateCompaniesListMutation.Field()
    desactivate_companies = DesactivateCompaniesListMutation.Field()