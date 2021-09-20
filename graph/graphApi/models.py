from django.db import models


class Category(models.Model):
    cat_name    = models.CharField(max_length=50)
    description = models.TextField(max_length=350)
    
    def __str__(self):
        return self.cat_name 
        
class Book(models.Model):
    book_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    publish_date = models.DateField()
    cat_id = models.ForeignKey(Category , on_delete=models.CASCADE)