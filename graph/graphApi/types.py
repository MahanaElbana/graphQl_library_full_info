
''' DjangoObjectType allows us to convert our Django model into an object type '''

from graphene_django.types import DjangoObjectType
from .models import Category ,Book
import graphene 

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"
        #exclude = ('description',) 
        extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return "this categories of my liberary"

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"
