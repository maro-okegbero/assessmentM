from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import VerifyApiKey
from .serializer import *


@api_view(['POST'])
@permission_classes([VerifyApiKey])
def create_applicant(request):
    """
    handles applicant creation request
    """
    serializer = ApplicantSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
@permission_classes([VerifyApiKey])
def get_applicants(request, pk=None):
    """

    :param request:
    :param pk:
    :return:
    """

    if pk:
        try:
            applicant = Applicant.objects.get(id=pk)
            serializer = ApplicantSerializer(applicant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Applicant.DoesNotExist:
            error = {"message": "No applicant exists with this id"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    applicant = Applicant.objects.all()
    serializer = ApplicantSerializer(applicant, many=True)
    print(serializer, "hello===============")
    print("I got here.....................")
    response = serializer.data
    print(response)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([VerifyApiKey])
def delete_applicant(request, pk):
    """
    delete an applicant object
    :param request:
    :param pk:
    :return:
    """

    try:
        applicant = Applicant.objects.get(id=pk)
        applicant.delete()
        return Response({"message": "Applicant deleted successfully"}, status=status.HTTP_201_CREATED)

    except Applicant.DoesNotExist:
        error = {"message": "No applicant exists with this id"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([VerifyApiKey])
def update_applicant(request, pk):
    """
    update an applicant object
    :param request:
    :param pk:
    :return:
    """

    try:
        applicant = Applicant.objects.get(id=pk)
        data = request.data
        serializer = EditApplicantSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.update(applicant, validated_data)
            return Response({"message": "Applicant object updated successfully"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Applicant.DoesNotExist:
        error = {"message": "No applicant exists with this id"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)