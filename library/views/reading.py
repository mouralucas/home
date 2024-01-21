from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView, Response
from rest_framework import status

from base.responses import InvalidRequestError
from library.requests.reading import ReadingGetRequest, ReadingPostRequest
from library.responses.reading import ReadingPostResponse, ReadingGetResponse
from service.library.reading import Reading as ReadingService
from service.security.security import IsAuthenticated


class Reading(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Fetch all readings for a item',
                   request=ReadingPostRequest, responses={200: ReadingGetResponse, 400: InvalidRequestError})
    def get(self, *args, **kwargs):
        data = ReadingGetRequest(data=self.request.query_params)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Create a new reading for a item',
                   request=ReadingPostRequest, responses={201: ReadingPostResponse, 400: InvalidRequestError})
    def post(self, *args, **kwargs):
        data = ReadingPostRequest(data=self.request.data)
        if not data.is_valid():
            return Response(InvalidRequestError(data.errors).data, status=status.HTTP_400_BAD_REQUEST)

        item_id = data.validated_data.get('itemId')
        start_at = data.validated_data.get('startAt')
        end_at = data.validated_data.get('endAt')

        user = self.request.user.id

        response = ReadingService(owner=user, item_id=item_id).set_reading(start_at=start_at, end_at=end_at)

        return Response(response, status=response['statusCode'])


class Progress(APIView):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
