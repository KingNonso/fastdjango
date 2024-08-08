from typing import Optional
import strawberry
import strawberry_django
from strawberry import auto

from . import models

def get_field_description(field):
    return field.help_text if field.help_text else field.verbose_name

@strawberry_django.type(models.Post)
class Post:
    """
    Defines a GraphQL type for representing a post.
    Includes fields for id, title, description, content, slug, publish status, draft status, read time, view count, and associated category.
    """
    id: auto
    title: auto
    description: auto
    content: auto
    slug: auto
    publish: auto
    draft: auto
    read_time: auto
    view_count: auto
    category: "Category" # This tells strawberry about the ForeignKey to the Category model and how to represent the Category instances on that relation

@strawberry_django.type(models.Category)
class Category:
    """
    Defines a GraphQL type for representing a category.
    Includes fields for id, title, description, slug, parent category, active status, last updated timestamp, and a list of associated posts.
    """
    id: auto
    title: auto
    description: auto
    slug: auto
    parent: auto
    active: auto
    updated: auto
    post_category: list[Post]


@strawberry_django.input(models.Post)
class PostInput:
    """
    Defines a GraphQL Input type for representing a post.
    Includes fields for id, title, description, content, slug, publish status, draft status, read time, view count, and associated category.
    """
    title: str = strawberry.field(description="The title of the post")
    description: Optional[str] = strawberry.field(
        description=get_field_description(models.Post._meta.get_field('description')),
        default=None
    )
    content: str = strawberry.field(description=get_field_description(models.Post._meta.get_field('content')))
    slug: Optional[str] = None
    publish: auto
    draft: bool
    read_time: Optional[int] = None
    view_count: Optional[int] = 0
    category_id: Optional[int] = None
