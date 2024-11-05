from rest_framework import serializers
from .models import Bike, Location, Insurance, Ratings, Image


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude', 'city', 'state', 'country']


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ['id', 'provider', 'expiry_date']


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['id', 'average_rating', 'total_reviews']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'description', 'bike']


class BikeSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Nested serializer
    # Nested serializer, allow null
    insurance = InsuranceSerializer(allow_null=True)
    # Nested serializer, allow null
    ratings = RatingsSerializer(allow_null=True)
    # Nested serializer for images
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Bike
        fields = [
            'id', 'model', 'category', 'brand', 'registration_number',
            'year', 'color', 'engine_cc', 'fuel_type', 'mileage',
            'rental_price_per_hour', 'rental_price_per_day',
            'availability_status', 'location', 'insurance', 'ratings',
            'features', 'images'
        ]

    def create(self, validated_data):
        # Extract nested objects from the validated data
        location_data = validated_data.pop('location')
        insurance_data = validated_data.pop('insurance', None)
        ratings_data = validated_data.pop('ratings', None)
        images_data = validated_data.pop('images', [])

        # Create Location instance
        location = Location.objects.create(**location_data)

        # Create Insurance instance if provided
        insurance = Insurance.objects.create(
            **insurance_data) if insurance_data else None

        # Create Ratings instance if provided
        ratings = Ratings.objects.create(
            **ratings_data) if ratings_data else None

        # Create Bike instance
        bike = Bike.objects.create(
            location=location, insurance=insurance, ratings=ratings, **validated_data)

        # Create Image instances
        for image_data in images_data:
            Image.objects.create(bike=bike, **image_data)

        return bike

    def update(self, instance, validated_data):
        # Similar logic for updating the instance
        location_data = validated_data.pop('location', None)
        insurance_data = validated_data.pop('insurance', None)
        ratings_data = validated_data.pop('ratings', None)
        images_data = validated_data.pop('images', [])

        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        if insurance_data:
            if instance.insurance:
                for attr, value in insurance_data.items():
                    setattr(instance.insurance, attr, value)
                instance.insurance.save()
            else:
                instance.insurance = Insurance.objects.create(**insurance_data)

        if ratings_data:
            if instance.ratings:
                for attr, value in ratings_data.items():
                    setattr(instance.ratings, attr, value)
                instance.ratings.save()
            else:
                instance.ratings = Ratings.objects.create(**ratings_data)

        for image_data in images_data or []:
            if 'id' in image_data:
                image = Image.objects.get(id=image_data['id'])
                image.url = image_data.get('url', image.url)
                image.description = image_data.get(
                    'description', image.description)
                image.save()
            else:
                Image.objects.create(bike=instance, **image_data)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
