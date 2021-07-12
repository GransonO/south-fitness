# Create your views here.
import bugsnag
import datetime
import jwt
import random

import requests
from django.core.mail import send_mail
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..profiles.models import ProfilesDB
from .models import Reset, Activation

from .serializers import UserSerializer
from ..profiles.serializers import ProfileSerializer


class Register(views.APIView):
    """
        Deal with Authentication
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Add New User to DB """
        passed_data = request.data
        try:
            # Check if it exists
            user_exists = Register.get_user_exist(passed_data)
            print("--------------- 1 -----{}".format(user_exists))
            if not user_exists:
                password_code = random.randint(10000, 99999)

                User = get_user_model()
                passed_username = (passed_data["email"]).lower()
                user_password = password_code
                user = User.objects.create_user(username=passed_username, password=user_password)
                user.first_name = passed_data["firstname"]
                user.last_name = passed_data["lastname"]
                user.email = (passed_data["email"]).lower()

                user.save()
                try:
                    # Save data to DB
                    print("--------------------------------Added to DB")
                    random_code = random.randint(1000, 9999)
                    activation_data = Activation(
                        activation_code=random_code,
                        user_email=(passed_data["email"]).lower(),
                    )
                    activation_data.save()
                    Register.send_simple_message((passed_data["email"]).lower(), passed_data["firstname"], random_code, password_code)
                except Exception as E:
                    print("Activation error: {}".format(E))
                    bugsnag.notify(
                        Exception('Activation error: {}'.format(E))
                    )
                    return Response({
                            "status": "failed",
                            "message": "Registration failed",
                            "code": 0
                            }, status.HTTP_200_OK)

                return Response({
                        "status": "success",
                        "message": "Registration success",
                        "code": 1
                        }, status.HTTP_200_OK)
            else:
                return Response({
                    "status": "failed",
                    "message": "Registration failed, user with email exists",
                    "code": 2  # User already exists
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Authenticate Post: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed error occurred",
                "message": "Registration failed",
                "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def get_user_exist(passed_data):
        """
        Check if exists
        """
        User = get_user_model()
        try:
            user_exists = User.objects.filter(username=(passed_data["email"]).lower()).exists()
            return user_exists

        except Exception as e:
            print("------------------Exception: {}".format(e))
            return False

    @staticmethod
    def send_simple_message(email, name, code, password):
        return requests.post(
            "https://api.mailgun.net/v3/sandbox51870243c7f44e3397f04b163c4f8d60.mailgun.org/messages",
            auth=("api", "d5dca3d5ce4430f5aa8973aac1fc0753-c4d287b4-289c0f7d"),
            data={"from": "South Fitness <southfitness@epitomesoftware.live>",
                  "to": [email, ],
                  "subject": 'Welcome {} to South Fitness'.format(name),
                  "html": EmailTemplates.register_email(name, code, password)})


class Login(views.APIView):
    """
        Login, Update
    """
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """ Generate the access token from refresh token"""
        User = get_user_model()
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        access_token = generate_access_token(user)
        return Response({'access_token': access_token})

    @staticmethod
    def post(request):
        """ Login """
        passed_data = request.data
        response = Response()
        try:

            User = get_user_model()
            username = (passed_data["email"]).lower()
            password = passed_data["password"]
            if (username is None) or (password is None):
                raise exceptions.AuthenticationFailed(
                    'username and password required')
            passed_user = User.objects.filter(username=username)
            if passed_user.exists():

                user = User.objects.filter(username=username).first()
                xfactor = ProfilesDB.objects.filter(email=(passed_data["email"]).lower()).first()
                profile = ProfilesDB.objects.filter(email=(passed_data["email"]).lower())
                if user is None:
                    raise exceptions.AuthenticationFailed('user not found')
                le_user = authenticate(username=username, password=password)
                if le_user is None:
                    response.data = {
                        "status": "failed",
                        "message": "Could not authenticate user",
                        "code": 1
                    }

                    return response

                serialized_user = UserSerializer(user).data
                serialized_profile = ProfileSerializer(xfactor).data

                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)

                response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                response.data = {
                    'access_token': access_token,
                    'user': serialized_user,
                    'profile': serialized_profile,
                    "status": "success",
                    "isRegistered": profile.count() > 0,
                    "message": "Login success",
                    "code": 1
                }

                return response

            else:
                return Response({
                    "status": "failed",
                    "message": "Login failed, user does not exist",
                    "code": 0  # user added to db
                }, status.HTTP_200_OK)

        except Exception as e:
            print("------------{}-----------".format(e))
            return Response({
                "status": "failed",
                "message": "Registration Failed",
                "code": 2  # Login error
            }, status.HTTP_200_OK)


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        # .decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')\
        # .decode('utf-8')

    return refresh_token


class ResetPass(views.APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        # Pass email
        # send reset code
        # Compare code attached to email
        passed_data = request.data
        try:
            # Check if it exists
            result = ProfilesDB.objects.filter(email=(passed_data["email"]).lower())
            print("--------------------------------{}".format(result.count()))
            if result.count() < 1:
                # User does not exist
                return Response({
                    "status": "reset failed",
                    "code": 0,
                    "success": False
                }, status.HTTP_200_OK)
            else:

                random_code = random.randint(1000, 9999)
                # check if reset before
                result = Reset.objects.filter(user_email=(passed_data["email"]).lower())
                print("--------------------------------{}".format(result.count()))
                if result.count() < 1:
                    # Reset object does not exist, add reset details
                    add_reset = Reset(
                        user_email=(passed_data["email"]).lower(),
                        reset_code=random_code,
                    )
                    add_reset.save()
                else:
                    # Update Reset
                    print("------------------------------Updated")
                    Reset.objects.filter(user_email=(passed_data["email"]).lower()).update(
                        reset_code=random_code,
                        )

                ResetPass.send_email((passed_data["email"]).lower(), random_code)
                return Response({
                        "status": "reset success",
                        "code": 1,
                        "success": True
                        }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Reset Post: {}'.format(E))
            )
            return Response({
                # "error": "{}".format(E),
                "status": "reset failed",
                "code": 2,
                "success": False
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):

        passed_data = request.data

        User = get_user_model()
        username = (passed_data["email"]).lower()
        password = passed_data["password"]
        reset_code = passed_data["code"]
        response = Response()

        reset = Reset.objects.filter(user_email=username, reset_code=reset_code)
        if reset.count() < 1:
            response.data = {
                "status": "Failed",
                "code": 0,
                "message": "Reset failed, wrong code passed"
            }
            return response
        else:
            passed_user = User.objects.filter(username=username)
            if passed_user.exists():
                # Update user password
                passed_user = User.objects.filter(username=username).first()
                passed_user.set_password(password)
                passed_user.save()
                response.data = {
                    "status": "success",
                    "message": "password updated",
                    "code": 1
                }
            else:
                response.data = {
                    "status": "failed",
                    "message": "user not found",
                    "code": 0
                }

            return response

    @staticmethod
    def send_email(email, code):
        print("----------------------------------------- Resetting password")
        subject = 'Password reset'
        message = EmailTemplates.reset_email(code)
        return requests.post(
            "https://api.mailgun.net/v3/sandbox51870243c7f44e3397f04b163c4f8d60.mailgun.org/messages",
            auth=("api", "d5dca3d5ce4430f5aa8973aac1fc0753-c4d287b4-289c0f7d"),
            data={"from": "South Fitness <southfitness@epitomesoftware.live>",
                  "to": [email, ],
                  "subject": subject,
                  "html": message
                  }
        )


class EmailTemplates:

    @staticmethod
    def register_email(name, code, password):
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
                            <p style="font-size: 17px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Your path to wellness starts here.</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> You have been invited to the South Fitness Training Program</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Use activation code: {} to activate your account.</p>
                            </br>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Your one time password is <strong>{}</strong>. </br> Kindly update it once you access your account</p>
                            </br>
                            </br>
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Welcome</span></p>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name, code, password)

    @staticmethod
    def reset_email(code):
        return """
            <!DOCTYPE html>
            <html lang="en">
            <body style="text-align:center;">
                <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1618138330/South_Fitness/ic_launcher.png" title="Image" width="300"/>
                <br>
                <br>
                <div style="color:#FFA500;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                    <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #FFA500; mso-line-height-alt: 14px;">
                        <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Did you requested to have your password changed?</span></strong></span></p>
                    </div>
                </div>
                <br>
                <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                    <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                        <p style="font-size: 15px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;">We received a request to reset your password. If you made the request, use the code <strong>{}</strong> to complete the process</p>
                        <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                    </div>
                </div>
            </body>
            </html>
        """.format(code)
