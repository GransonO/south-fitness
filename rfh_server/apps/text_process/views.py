from leoprofanity import LeoProfanity
from rest_framework import views, status
from rest_framework.response import Response


class Processing(views.APIView):
    """ Processing  """

    @staticmethod
    def get(request):
        passed_data = request.data
        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"The server is woke as needed"}, status.HTTP_200_OK)

    @staticmethod
    def post(request):
        fil = LeoProfanity()
        passed_data = request.data

        body = passed_data['body']
        words_list = body.split()
        fill_words = fil.list()
        z_list = []

        for x in words_list:
            if x in fill_words:
                z_list.append(x)

        is_profane = fil.check(body)

        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"isProfane": is_profane, "words": z_list}, status.HTTP_200_OK)
