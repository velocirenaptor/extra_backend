import graphene
from graphene_django import DjangoObjectType
from .models import Character
from users.schema import UserType
from django.db.models import Q

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character

class Query(graphene.ObjectType):
    all_characters = graphene.List(CharacterType)
    character = graphene.Field(CharacterType, id=graphene.Int(required=True))

    def resolve_all_characters(self, info):
        return Character.objects.all()

class CreateCharacter(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        source = graphene.String(required=True)
        picture = graphene.String(required=True)
        description = graphene.String()

    character = graphene.Field(CharacterType)

    def mutate(self, info, name, source, picture, description):
        character = Character(
            name=name,
            source=source,
            picture=picture,
            description=description
        )
        character.save()
        return CreateCharacter(character=character)

class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
