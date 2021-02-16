# Create your views here.
import bugsnag
import datetime
import jwt
import random

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
                User = get_user_model()
                passed_username = passed_data["email"]
                user_password = passed_data['password']
                user = User.objects.create_user(username=passed_username, password=user_password)
                user.first_name = passed_data["firstname"]
                user.last_name = passed_data["lastname"]
                user.email = passed_data["email"]

                user.save()
                try:
                    # Save data to DB
                    print("--------------------------------Added to DB")
                    random_code = random.randint(1000, 9999)
                    activation_data = Activation(
                        activation_code=random_code,
                        user_email=passed_data["email"],
                    )
                    activation_data.save()
                    Register.send_email(passed_data["email"], passed_data["firstname"], random_code)
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
            user_exists = User.objects.filter(username=passed_data["email"]).exists()
            return user_exists

        except Exception as e:
            print("------------------Exception: {}".format(e))
            return False

    @staticmethod
    def send_email(email, name, code):
        subject = 'Welcome {} to South Fitness'.format(name)
        body = 'Your path to wellness starts here. Use activation code: {} to activate your account.'.format(code)
        message = """
                    <html>
                    <head></head>
                    <body>
                        <h2>Well hello there enthusiast</h2>
                        <p>{}</p>
                        <h5>For you</h5>
                    </body>
                    </html>
                    """.format(body)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)


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
            username = passed_data["email"]
            password = passed_data["password"]
            if (username is None) or (password is None):
                raise exceptions.AuthenticationFailed(
                    'username and password required')
            participant = ProfilesDB.objects.filter(email=passed_data["email"])
            passed_user = User.objects.filter(username=username)
            if passed_user.exists():

                user = User.objects.filter(username=username).first()
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

                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)

                response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                response.data = {
                    'access_token': access_token,
                    'user': serialized_user,
                    "status": "success",
                    "isRegistered": participant.count() > 0,
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
            result = Reset.objects.filter(user_email=passed_data["email"])
            print("--------------------------------{}".format(result.count()))
            if result.count() < 1:
                # Save data to DB
                print("--------------------------------Added to DB")
                random_code = random.randint(1000, 9999)
                reset_data = Reset(
                    reset_code=random_code,
                    user_email=passed_data["email"],
                )
                reset_data.save()
                ResetPass.send_email(passed_data["email"], random_code)
                return Response({
                    "status": "reset success",
                    "code": 1,
                    "success": True
                    }, status.HTTP_200_OK)
            else:
                # Update Reset
                print("------------------------------Updated")
                random_code = random.randint(1000, 9999)
                Reset.objects.filter(user_email=passed_data["email"]).update(
                    reset_code=random_code,
                    )
                ResetPass.send_email(passed_data["email"], random_code)
                return Response({
                        "status": "reset success",
                        "code": 1,
                        "success": True
                        }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('ProfilesRef Post: {}'.format(E))
            )
            return Response({
                # "error": "{}".format(E),
                "status": "reset failed",
                "code": 0,
                "success": False
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):

        passed_data = request.data

        User = get_user_model()
        username = passed_data["email"]
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
        body = 'We received a request to reset your password. If you made the request, use the code {} to complete the process'.format(code)
        message = """
                    <html>
                    <head></head>
                    <body>
                        <h2>Well hello there enthusiast</h2>
                        <p>{}</p>
                        <h5>For you</h5>
                    </body>
                    </html>
                    """.format(body)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message=body, from_email=email_from, recipient_list=recipient_list, html_message=message)
