from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

from Moove_Assessment_Api.models import Applicant
import requests
from Moove_Assessment.settings import REST_COUNTRY_API_URL


class SerializerHttpError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


def country_validator(value: str):
    """
    Validates the country
    :param value:
    :return:
    """
    try:
        name = f"{value}?fullText=true"
        url = REST_COUNTRY_API_URL + name
        request = requests.get(url)
        response = request.json()
        if not isinstance(response, list):
            raise serializers.ValidationError('This is an invalid country, perhaps check the spelling')
    except requests.exceptions.ConnectionError:
        raise SerializerHttpError("Error validating the country, please try later")


def age_validator(value):
    """
    checks to see if the age is between 20 - 60
    """
    if value < 20 or value > 60:
        raise serializers.ValidationError('The age should not be less than 20 or more than 60')


class ApplicantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=5, required=True)
    family_name = serializers.CharField(max_length=5, required=True)
    address = serializers.CharField(max_length=10, required=True)
    country_of_origin = serializers.CharField(max_length=100, validators=[country_validator], required=True)
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(validators=[age_validator], required=True)
    hired = serializers.BooleanField(default=False)

    class Meta:
        model = Applicant
        fields = ["id", "name", "family_name", "address", "email", "country_of_origin", "age", "hired"]


class EditApplicantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=5, required=False)
    family_name = serializers.CharField(max_length=5, required=False)
    address = serializers.CharField(max_length=10, required=False)
    country_of_origin = serializers.CharField(max_length=100, validators=[country_validator], required=True)
    email = serializers.EmailField(required=False)
    age = serializers.IntegerField(validators=[age_validator], required=False)
    hired = serializers.BooleanField(default=False)

    class Meta:
        model = Applicant
        fields = ["id", "name", "family_name", "address", "email", "country_of_origin", "age", "hired"]