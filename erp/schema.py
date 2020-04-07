import graphene
from graphene_django import DjangoObjectType
from . import models, forms
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Field
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from graphene_django.forms.mutation import DjangoModelFormMutation
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User, Group
from graphql_jwt.decorators import login_required


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

class PermissionNode(DjangoObjectType):
    
    class Meta:
        model = Permission

class RoleNode(DjangoObjectType):
    permissions = graphene.List(PermissionNode)
    
    class Meta:
        model = Group

class UserNode(DjangoObjectType):

    class Meta:
        model = User
        exclude = ['username','password']

class Auth(graphene.ObjectType):
    viewer = graphene.Field(UserNode)
    
    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        return user
class EmployeeNode(DjangoObjectType):
    company = graphene.Field(CompanyNode)
    user = graphene.Field(UserNode)
    fullName = graphene.String()

    class Meta:
        model = models.Employee
        exclude = ['name', 'lastName']

    def resolve_fullName(self, indo):
        return f'{self.name} {self.lastName}'

class Query(object):
    companies = graphene.List(CompanyNode)
    configurations = graphene.List(CompanyConfigurationNode)
    employees = graphene.List(EmployeeNode)
    users = graphene.List(UserNode)

    @login_required
    def resolve_companies(self, info, **kwargs):
        query = models.Company.objects.all()
        return paginate(info, query)


    @login_required
    def resolve_configurations(self, info, **kwargs):
        query = models.CompanyConfiguration.objects.all()
        return paginate(info, query)
    
    @login_required
    def resolve_users(self, info, **kwargs):
        query = User.objects.all()
        return paginate(info, query)

    @login_required
    def resolve_employees(self, info, **kwargs):
        query = models.Employee.objects.all()
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
    if paginator.num_pages < page:
        return []
    try:
        return paginator.get_page(page)
    except:
        return []


class CompanyMutation(DjangoModelFormMutation):
    company = graphene.Field(CompanyNode)

    class Meta:
        form_class = forms.CompanyForm


class CompanyConfigMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        shortName = graphene.String()
        primaryColor = graphene.String()
        secondaryColor = graphene.String()
        company = graphene.String()
    companyConfig = graphene.Field(lambda: CompanyConfigurationNode)

    @login_required
    def mutate(root, info, **kwargs):
        instance = get_object_or_404(models.Company, id=kwargs.get('company'))
        kwargs['company'] = instance
        if kwargs['id'] == '':
            del kwargs['id']
            comcon = models.CompanyConfiguration.objects.get_or_create(**kwargs)[0]
        else:
            comcon = models.CompanyConfiguration.objects.filter(id=kwargs['id']).update(**kwargs)
            comcon = models.CompanyConfiguration.objects.get(id=kwargs['id'])
        return CompanyConfigMutation(companyConfig=comcon)


class DeleteCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @login_required
    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class ActivateCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @login_required
    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"]).update(isActive=True)
        return cls(ok=True)

class DesactivateCompaniesListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @login_required
    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Company.objects.filter(id__in=kwargs["id"]).update(isActive=False)
        return cls(ok=True)

class EmployeeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required= True) 
        lastName = graphene.String(required= True)
        email = graphene.String(required= True)
        company = graphene.String()
        user = graphene.String()
        
    employeeResponse = graphene.Field(EmployeeNode)

    @login_required
    def mutate(root, info, **kwargs):
        company = get_object_or_404(models.Company, id=int(kwargs.get('company')))
        user = get_object_or_404(User, id=int(kwargs.get('user')))
        kwargs['company'] = company
        kwargs['user'] = user
        if kwargs['id'] == '':
            del kwargs['id']
            employee = models.Employee.objects.get_or_create(**kwargs)[0]
        else:
            employee = models.Employee.objects.filter(id=kwargs['id']).update(**kwargs)
            employee = models.Employee.objects.get(id=kwargs['id'])
        return EmployeeMutation(employeeResponse=employee)




class DesactivateEmployeeListMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.List(graphene.Int)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = models.Emloyee.objects.filter(id__in=kwargs["id"]).update(isActive=False)
        print(f'OBJ es {obj}')
        return cls(ok=True)


class UserPermissionMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        user = graphene.Int(required=True)
        permissions = graphene.List(graphene.Int, required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = get_object_or_404(User, id=kwargs['user'])
        permissions = Permission.objects.filter(id__in=kwargs["permissions"])
        user.user_permissions.set(permissions)
        return cls(ok=True)

class UserRoleMutation(graphene.Mutation):
    ok = graphene.Boolean()
    description = graphene.String()

    class Arguments:
        user = graphene.Int(required=True)
        roles = graphene.List(graphene.Int, required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = get_object_or_404(User, id=kwargs['user'])
        roles = Group.objects.filter(id__in=kwargs["roles"])
        if roles.count() == 0:
            return cls(ok=False,description='No existen roles')
        user.groups.set(roles)
        return cls(ok=True,description='Roles agregados satisfactoriamente')

class RoleMutation(DjangoModelFormMutation):

    class Meta:
        form_class = forms.RoleForm

class UserMutation(DjangoModelFormMutation):
    
    class Meta:
        form_class = forms.UserForm

class Mutation(graphene.ObjectType):
    add_company = CompanyMutation.Field()
    delete_companies = DeleteCompaniesListMutation.Field()
    activate_companies = ActivateCompaniesListMutation.Field()
    desactivate_companies = DesactivateCompaniesListMutation.Field()
    add_configuration = CompanyConfigMutation.Field()
    add_employee = EmployeeMutation.Field()
    add_user_permissions = UserPermissionMutation.Field()
    add_user_groups = UserRoleMutation.Field()
    add_groups = RoleMutation.Field()