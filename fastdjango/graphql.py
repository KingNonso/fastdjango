import os
import django
import datetime

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastdjango.settings')

# Initialize Django
django.setup()

import strawberry
import strawberry_django
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from strawberry_django.optimizer import DjangoOptimizerExtension

from myapp.graphql_types import Category, Post, PostInput
from myapp import models

@strawberry.type
class User:
    """
    Defines a GraphQL type representing a User with name and age fields.
    """
    name: str
    age: int

@strawberry.type
class Query:
    """
    Defines a Query class with fields for categories and posts. 
    Includes a method to retrieve a user with the name "Patrick" and age 100.
    """
    categories: list[Category] = strawberry_django.field(description="Retrieves a list of categories")
    posts: list[Post] = strawberry_django.field(description="Retrieves a list of blog posts")

    @strawberry.field(description="Retrieves a single User detail")
    def user(self) -> User:
        return User(name="Patrick", age=100)
    
@strawberry.type
class Mutation:

    @strawberry.mutation(description="Create a new category")
    async def create_category(self, title: str, description: str) -> Category:
        """
        Creates a new category.
        """
        category = await models.Category.objects.acreate(title=title, description=description)
        return category
    
    @strawberry.mutation(description="Create a new post and places it within the provide category ID")
    async def create_post(self, input: PostInput) -> Post:
        """
        Creates a new post
        """
        category = await models.Category.objects.aget(pk=input.category_id)
        post_instance = models.Post(
            title=input.title,
            description=input.description,
            content=input.content,
            slug=input.slug,
            publish=input.publish,
            draft=input.draft,
            read_time=input.read_time,
            view_count=input.view_count,
            category=category # CategoryModel.objects.get(pk=input.category_id)  # Assuming category is represented by its ID
        )
        await post_instance.asave()

        return post_instance

schema = strawberry.Schema(
    query=Query,  # A Query is like a Get request in REST
    mutation=Mutation,  # A Mutation is like a Post request in REST
    extensions=[DjangoOptimizerExtension]
)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)




