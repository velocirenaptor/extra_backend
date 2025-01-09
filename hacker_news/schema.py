import graphene
import graphql_jwt

import links.schema
import users.schema
import education.schema
import characters.schema

class Query(education.schema.Query, users.schema.Query, links.schema.Query, characters.schema.Query, graphene.ObjectType):
    pass

class Mutation(education.schema.Mutation, users.schema.Mutation, links.schema.Mutation, characters.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
