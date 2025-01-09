from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
import json
from django.contrib.auth import get_user_model
from characters.schema import schema
from characters.models import Character  

CREATE_USER_MUTATION = '''
mutation createUserMutation($email: String!, $password: String!, $username: String!) {
    createUser(email: $email, password: $password, username: $username) {
        user {
            username
            password
        }
    }
}
'''

LOGIN_USER_MUTATION = '''
mutation TokenAuthMutation($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
        token
    }
}
'''

CHARACTERS_QUERY = '''
{
    characters {
        name
        source
        picture
        description
    }
}
'''

CREATE_CHARACTER_MUTATION = '''
mutation createCharacterMutation($name: String!, $source: String!, $picture: String!, $description: String) {
    createCharacter(name: $name, source: $source, picture: $picture, description: $description) {
        character {
            name
            source
            picture
            description
        }
    }
}
'''

class CharacterTests(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/graphql/"
    GRAPHQL_SCHEMA = schema
    
    def setUp(self):
        response_user = self.query(
            CREATE_USER_MUTATION,
            variables={'email': 'ren0@gmail.com', 'username': 'ren0', 'password': '1234'}
        )
        content_user = json.loads(response_user.content)
        self.assertResponseNoErrors(response_user)

        response_token = self.query(
            LOGIN_USER_MUTATION,
            variables={'username': 'ren0', 'password': '1234'}
        )
        content_token = json.loads(response_token.content)
        self.assertResponseNoErrors(response_token)

        token = content_token['data']['tokenAuth']['token']
        self.headers = {"Authorization": f"JWT {token}"}

    #test 1 - creating a character successfully
    def test_create_character_mutation(self):
        response = self.query(
            CREATE_CHARACTER_MUTATION,
            variables={
                'name': 'Diddy Kong',
                'source': 'Donkey Kong Country',
                'picture': 'https://static.wikia.nocookie.net/ultimatepopculture/images/b/ba/DiddyReturns.png/revision/latest?cb=20190916195208',
                'description': 'hes a funny lil monkey from donkey kong country',
            },
            headers=self.headers
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content['data']['createCharacter']['character'], 
            {"name": "Diddy Kong", "source": "Donkey Kong Country", "picture": "https://static.wikia.nocookie.net/ultimatepopculture/images/b/ba/DiddyReturns.png/revision/latest?cb=20190916195208", "description": "hes a funny lil monkey from donkey kong country"}
        )

    #test 2 - test mutation missing a field
    def test_create_character_mutation_missing_fields(self):
        response = self.query(
            CREATE_CHARACTER_MUTATION,
            variables={
                'source': 'Super Mario',
                'picture': 'https://example.com/picture.png',
                'description': 'A brave plumber.',
            },
            headers=self.headers
        )
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIn('name', content['errors'][0]['message'])

    #test 3 - test mutation has invalid input
    def test_create_character_mutation_invalid_field_types(self):
        response = self.query(
            CREATE_CHARACTER_MUTATION,
            variables={
                'name': 123,  # Invalid data type for 'name'
                'source': 'Super Mario',
                'picture': 'https://example.com/picture.png',
                'description': 'A brave plumber.',
            },
            headers=self.headers
        )
        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIn('name', content['errors'][0]['message'])  
