import graphene
import erp.schema


class Query(erp.schema.Query, graphene.ObjectType):
    pass

class Mutation(erp.schema.Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)