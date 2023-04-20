import graphene
from graphene_django import DjangoObjectType
from .models import Books

class BookType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ['id', 'title', 'excerpt']

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(self, info, **kwargs):
        return Books.objects.all()

schema = graphene.Schema(query=Query)