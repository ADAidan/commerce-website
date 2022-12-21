from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField()
    category = models.CharField(max_length=64)
    image = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Owner")
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"""
        {self.id}: {self.name} - {self.description} 
        price: ${self.price} category: {self.category}
        Created: {self.date_created}
        """

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"User: {self.user} - {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"User: {self.user} Watchlist: {self.listings}"
