# Create your views here.
import uuid

import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import ChatDB
from .models import GroupsDB
from .serializers import ChatSerializer
from .serializers import GroupSerializer


class Chat(views.APIView):
    """
        Add notifications details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add group to DB """
        passedData = request.data
        try:
            # Save data to DB
            message_uuid = uuid.uuid1()

            chat_data = ChatDB(
                message_id=message_uuid,
                group_id=passedData["group_id"],
                user_id=passedData["user_id"],
                message=passedData["message"],
                reply_body=passedData["reply_body"],
                username=passedData["username"],
            )
            chat_data.save()
            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Chat Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passed_data = request.data
        # Check This later
        try:
            participant = ChatDB.objects.get(message_id=passed_data["message_id"])
            serializer = ChatSerializer(
                participant, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Message Put: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class ChatsAllView(ListAPIView):
    """Get a user specific chats"""
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def get_queryset(self):
        return ChatDB.objects.filter(group_id=self.kwargs['group_id']).order_by('-createdAt')


class ChatSpecificView(ListAPIView):
    """Get a user specific chats"""
    permission_classes = [AllowAny]
    serializer_class = ChatSerializer

    def get_queryset(self):
        return ChatDB.objects.filter(
            message_id=self.kwargs['message_id']
            ).order_by('date')


class Groups(views.APIView):
    """
        Add Groups details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add group to DB """
        passedData = request.data
        try:
            # Save data to DB
            channel_uuid = uuid.uuid1()

            group_data = GroupsDB(
                created_by=passedData["user_id"],
                group_title=passedData["group_title"],
                group_id=channel_uuid,
                creator_name=passedData["creator_name"],
                institution=passedData["institution"],
                group_slogan=passedData["group_slogan"],
                group_image=passedData["group_image"],
                channel_id=channel_uuid,
            )
            group_data.save()
            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Group Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        passed_data = request.data
        # Check This later
        try:
            participant = GroupsDB.objects.get(group_id=passed_data["group_id"])
            serializer = GroupSerializer(
                participant, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Groups Put: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class GroupsAllView(ListAPIView):
    """Get a user specific chats"""
    permission_classes = [AllowAny]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return GroupsDB.objects.filter(isVerified=True).order_by('-createdAt')


class AllGroups(ListAPIView):
    """Return all ongoing groups"""
    permission_classes = [AllowAny]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return GroupsDB.objects.filter(
            is_closed=False, isVerified=True
        ).order_by('createdAt')


class InstitutionGroups(ListAPIView):
    """Return all ongoing groups"""
    permission_classes = [AllowAny]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return GroupsDB.objects.filter(
            is_closed=False, institution=self.kwargs['institute'],
            isVerified=True
        ).order_by('createdAt')

