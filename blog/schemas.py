from ninja import ModelSchema
from .models import Post


# Schemas from Django models:
# https://django-ninja.rest-framework.com/guides/response/django-pydantic/
class PostIn(ModelSchema):
    class Config:
        model = Post
        model_exclude = ["id", "author", "created_on"]


class PostOut(ModelSchema):
    class Config:
        model = Post
        model_fields = ["id", "author", "title", "body", "created_on"]
