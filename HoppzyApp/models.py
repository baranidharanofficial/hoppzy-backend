from django.db import models


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"


class Insurance(models.Model):
    provider = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return f"Insurance by {self.provider}, expires on {self.expiry_date}"


class Ratings(models.Model):
    average_rating = models.DecimalField(max_digits=3, decimal_places=1)
    total_reviews = models.IntegerField()

    def __str__(self):
        return f"Rating: {self.average_rating} ({self.total_reviews} reviews)"


class Bike(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    model = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    engine_cc = models.IntegerField(default=0)  # Set to 0 for electric bikes
    fuel_type = models.CharField(max_length=20)
    mileage = models.DecimalField(
        max_digits=5, decimal_places=1)  # km per charge/fuel
    rental_price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    rental_price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    availability_status = models.CharField(max_length=20, default="available")

    # ForeignKey and OneToOne relationships
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="bikes")
    insurance = models.OneToOneField(
        Insurance, on_delete=models.SET_NULL, null=True)
    ratings = models.OneToOneField(
        Ratings, on_delete=models.SET_NULL, null=True)

    features = models.JSONField()  # To store a list of features as JSON

    def __str__(self):
        return f"{self.brand} {self.model} - {self.registration_number}"


class Image(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255, blank=True)
    bike = models.ForeignKey(Bike, related_name='images',
                             on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description or self.url
