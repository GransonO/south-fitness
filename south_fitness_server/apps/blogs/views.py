# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import BlogsDB
from .serializers import BlogSerializer


class Blog(views.APIView):
    """
        Add Blog details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add Blog to DB """
        passed_data = request.data
        try:
            blog_data = BlogsDB(
                blog_id=passed_data["blog_id"],
                uploaded_by=passed_data["uploaded_by"],
                uploader_id=passed_data["uploader_id"],
                title=passed_data["title"],
                body=passed_data["body"],
                image_url=passed_data["image_url"],
                views_count=passed_data["views_count"],
                reading_duration=passed_data["reading_duration"]
            )
            blog_data.save()
            return Response({
                "status": "success",
                "code": 1
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Blog Post: {}'.format(E))
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
            blog = BlogsDB.objects.get(blog_id=passed_data["blog_id"])
            serializer = BlogSerializer(
                blog, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                    "status": "success",
                    "code": 1
                    }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Blog update: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class BlogAllView(ListAPIView):
    """Get all blogs"""
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer

    def get_queryset(self):
        return BlogsDB.objects.filter().order_by('-createdAt')


class BlogSpecificView(ListAPIView):
    """Get a user specific blog"""
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer

    def get_queryset(self):
        return BlogsDB.objects.filter(
            blog_id=self.kwargs['blog_id']
            ).order_by('-createdAt')
