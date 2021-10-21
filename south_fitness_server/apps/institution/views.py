import random
import uuid

import bugsnag
from rest_framework import views,  status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..authentication.models import Activation
from ..profiles.models import ProfilesDB
from ..profiles.serializers import ProfileSerializer
from .models import Institutions
from .serializers import InstitutionSerializer
from django.contrib.auth import get_user_model
import os

from dotenv import load_dotenv
from mailjet_rest import Client


class Institution(views.APIView):
    """
        Add notifications details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            # Save data to DB
            the_id = uuid.uuid1()
            serializer = InstitutionSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(institute_id=the_id)

            institute = request.data
            if Institution().get_user_exist((institute["institute_admin_email"]).lower()):
                """User exists, update their institution"""

                profile_data = ProfilesDB.objects.filter(email=(institute["institute_admin_email"]).lower())
                profile_data.update(institution=institute["institute_name"], institution_id=the_id)
            else:
                random_code = random.randint(1000, 9999)
                user_password = "SF-{}".format(random.randint(1000, 9999))
                Institution().send_welcome_email(
                    institute["institute_admin_email"].lower(),
                    institute["institute_admin_name"],
                    institute["institute_name"],
                    random_code,
                    user_password)

                # Save data to DB
                activation_data = Activation(
                    activation_code=random_code,
                    user_email=(institute["institute_admin_email"]).lower(),
                    user_type="ADMIN",
                    institution=institute["institute_name"],
                    institution_id=the_id,
                )
                activation_data.save()

                admin_name = (institute["institute_admin_name"]).split(" ")
                if len(admin_name) > 1:
                    f_name = admin_name[0]
                    s_name = admin_name[1]
                else:
                    f_name = admin_name[0]
                    s_name = admin_name[0]

                user = get_user_model()
                passed_username = (institute["institute_admin_email"]).lower()
                user = user.objects.create_user(username=passed_username, password=user_password)
                user.first_name = f_name
                user.last_name = s_name
                user.email = (institute["institute_admin_email"]).lower()

                user.save()
            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Admin Profile Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """ Add appointment to DB """
        institute = Institutions.objects.get(institute_id=request.data["institute_id"])
        try:
            # Save data to DB
            serializer = InstitutionSerializer(institute, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "status": "success",
                "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Appointment Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def get_user_exist(email):
        """
        Check if profile exists
        """
        try:
            user_exists = ProfilesDB.objects.filter(email=email.lower()).exists()
            return user_exists

        except Exception as e:
            print("------------------Exception: {}".format(e))
            return False

    @staticmethod
    def send_welcome_email(email, name, institution, code, password):
        subject = 'South Fitness {} Admin Invite'.format(institution)
        admin_reg_link = "https://southfitness-dash.web.app/register_admin?passed_code={}&email={}&name={}".format(
            code, email, name)
        message = EmailTemplates.welcome_email(name, institution, admin_reg_link, password)
        load_dotenv()
        api_key = os.environ['MJ_API_KEY_PUBLIC']
        api_secret = os.environ['MJ_API_KEY_PRIVATE']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "southfitness@epitomesoftware.live",
                        "Name": "South Fitness"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": ""
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": message
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code

    @staticmethod
    def send_notification_email(email, name, institution):
        subject = 'South Fitness {} Admin Invite'.format(institution)
        message = EmailTemplates.notify_email(name, institution)
        load_dotenv()
        api_key = os.environ['MJ_API_KEY_PUBLIC']
        api_secret = os.environ['MJ_API_KEY_PRIVATE']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "southfitness@epitomesoftware.live",
                        "Name": "South Fitness"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": ""
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": message
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result.status_code


class AddTheAdmin(views.APIView):
    """Add Admins details"""
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        passed_data = request.data

        try:
            active_profile = Activation.objects.filter(
                user_email=passed_data["email"],
                activation_code=int(passed_data["activation_code"])
            )
            if len(active_profile) < 1:
                # Account not created
                return Response(
                    {
                        "status": "failed",
                        "message": "Account not found"
                    },
                    status.HTTP_200_OK
                )
            else:
                # Save data to DB
                profile_data = ProfileSerializer(data=passed_data, partial=True)
                profile_data.is_valid()
                profile_data.save(
                    is_active=True,
                    user_type="ADMIN",
                    institution=active_profile[0].institution,
                    institution_id=active_profile[0].institution_id,
                    user_id=uuid.uuid1()
                )

                # Update user password
                user = get_user_model()
                passed_user = user.objects.filter(username=passed_data["email"]).first()
                passed_user.set_password(passed_data["password"])
                passed_user.save()
                return Response({
                    "status": "success",
                    "code": 1
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Profile Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)


class EmailTemplates:

    @staticmethod
    def welcome_email(name, institution, admin_reg_link, password):
        return """
        <!DOCTYPE html>
            <html lang="en">
                <body style="text-align:center;">
                    <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1618138330/South_Fitness/ic_launcher.png" title="Image" width="300"/>
                    </br>
                    <div style="color:#FFA500;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                        <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #FFA500; mso-line-height-alt: 14px;">
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Well hello {}</span></strong></span></p>
                        </div>
                    </div>
                    <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                        <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> You have been invited to the South Fitness platform as an Admin for {}</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Use the link below to register and access the admin platform</p>
                            </br>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> <a href={}><strong>Admin registration portal</strong></a> </p>
                            </br>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Use <strong>{}</strong> as your temporay password </p>
                            </br>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Thank you for choosing to partner with us in you fitness journey 😌</p>
                            </br>
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Welcome</span></p>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name, institution, admin_reg_link, password)

    @staticmethod
    def notify_email(name, institution):
        return """
                <!DOCTYPE html>
                    <html lang="en">
                        <body style="text-align:center;">
                            <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1618138330/South_Fitness/ic_launcher.png" title="Image" width="300"/>
                            </br>
                            <div style="color:#FFA500;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                                <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #FFA500; mso-line-height-alt: 14px;">
                                    <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Well hello {}</span></strong></span></p>
                                </div>
                            </div>
                            <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                                <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                                    <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                                    <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> You have been invited to the South Fitness platform as an Admin for {}</p>
                                    <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                                    </br>
                                    <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Thank you for choosing to partner with us in you fitness journey 😌</p>
                                    </br>
                                    <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Welcome</span></p>
                                </div>
                            </div>
                        </body>
                    </html>
                """.format(name, institution)


class AllInstitutions(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = InstitutionSerializer

    def get_queryset(self):
        return Institutions.objects.filter(is_active=True).order_by('createdAt')


class SpecificInstitutions(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = InstitutionSerializer

    def get_queryset(self):
        return Institutions.objects.filter(institute_id=self.kwargs["institute_id"]).order_by('createdAt')
