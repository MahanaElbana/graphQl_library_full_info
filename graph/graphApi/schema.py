import graphene
from graphene_django import DjangoObjectType
from .models import Category , Book
from .types import  CategoryType, BookType

#!   ------------- Query  ------------------------
'''1] The query type [Query] contains a resolve method for each argument
    of data that can be requested. This resolve method describes the logic 
    behind the fetching of data from the data base.

  2] Remember the name resolve is important and must be 
  [followed by the name of field you want to return the data for.]

  
 '''
class Query(graphene.ObjectType):
    '''
Each variable i.e all_books,book,all_categories,category corresponds to a GraphQL query
all_books & all_categories returns a List of BookType and CategoryType respectively
resolvers for all these fields is just fetching the data from the Models and returning it

    '''
    #!                     return                     to            return 
    #! resolve_all_books    ==>    Book.objects.all() ==> all_books   ==>   BookType

    #* all_books query will return a list of all the BookType instances .
    all_books = graphene.List(BookType)

    #* book query will return one BookType instance,given by an integer ID.
    book = graphene.Field(BookType, book_id=graphene.Int())
    
    #* -- Every query in the schema maps to a resolver method
    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, book_id):
        return Book.objects.get(pk=book_id)

   #------------------ category ------------------------#
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(BookType, category_id=graphene.Int())
    
    
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all() 

    def resolve_book(self, info, category_id):
        return Category.objects.get(pk=category_id) 

#!   ------------- Mutation  ------------------------
categorypro = graphene.Field(CategoryType)

class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()             
    cat_name  =graphene.String()  
    description  =graphene.String()  

# -- for creating category 
class CreateCategory(graphene.Mutation):
    class Arguments:
        category_data = CategoryInput(required=True)

    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, category_data=None):
        category_instance = Category( 
            cat_name =category_data.cat_name ,
            description =category_data.description ,
        )
        category_instance.save()
        return CreateCategory(category=category_instance)    

# -- for updating category 
class UpdateCategory(graphene.Mutation):
    class Arguments:
        category_data = CategoryInput(required=True)

    #category = graphene.Field(CategoryType)
    category = categorypro

    @staticmethod
    def mutate(root, info, category_data=None):

        category_instance = Category.objects.get(pk=category_data.id)

        if category_instance:
            category_instance.cat_name = category_data.cat_name
            category_instance.description = category_data.description
            category_instance.save()

            return UpdateCategory(category=category_instance)
        return UpdateCategory(book=None)

# --- for deleting  category
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = categorypro

    @staticmethod
    def mutate(root, info, id):
        category_instance = Category.objects.get(pk=id)
        category_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

schema = graphene.Schema(query=Query ,mutation=Mutation)        
      

'''
     --------------- Building GraphQL APIs in Django with Graphene ------------
  
  introduction :- 
     1] GraphQL is an open-source data query and manipulation language for APIs,
     2] it is a runtime for fulfilling queries with existing data.
     3] It was developed internally by Facebook in 2012 before being publicly released in 2015. 
     4] It allows clients to define the structure of the data required,
     5] and the same structure of the data is returned from the server,
     6] therefore preventing unnecessary data from being returned.
  
  GraphQL has three primary operations :-
   1] Queries => for reading data,
   2] Mutations => for writing data, 
   3] and Subscriptions for automatically receiving real-time data updates.
   A GraphQL server provides clients with a predefined schema – a model of the data that can be requested. 
   The schema serves as common ground between the client and the server.

 -------------- for fetching one item of books --------------
##!  query {                        ##!  query {  
##!    book(bookId: 1) {            ##!     book(categoryId: 1) {   
##!      id                         ##!      id 
##!     bookName                    ##!      catName, 
##!      authorName                 ##!      description,
##!      publishDate                ##!     }
##!      catId{id}                  ##!  }
##!    }                            ##!
##!  }                              ##!
 -------------- for fetching a list items of books --------------
query {
 allBooks {
    id
   bookName
    authorName
    publishDate
    catId{id}
  }
}

mutation createMutation {
  createCategory(categoryData: { catName: "languages",
            description: "books in learning languages" }) {
    category {
     catName
     description
    }
  }
}

mutation deleteMutation{
  deleteCategory(id: 6) {
    category {
      id
    } 
  }
}

'''



