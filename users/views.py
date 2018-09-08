from flask import Flask, jsonify, request

from common.views import APIView
from users.auth import auth_required
from users.resources import UserResource




class UserAPIView(APIView):
    @auth_required
    def get(self, user=None, **kwargs):
        return self.json_response(data=user.to_serializable_dict())


    def post(self):
        print 'hello post'
        response = {}
        user_resource = UserResource(request.json)
        if user_resource.is_valid():
            try:
                user_resource.add()
                response['user'] = user_resource.to_serializable_dict()
            except Exception as error:
                print error
                pass
        return self.json_response(data=response)

    @auth_required
    def put(self, user=None, **kwargs):
        response = {}
        user_resource = UserResource(request.json, model=user)
        if user_resource.is_valid():
            try:
                user_resource.update()
                response['user'] = user_resource.to_serializable_dict()
            except Exception as error:
                print error
                pass
        return self.json_response(data=response)

    @auth_required
    def delete(self, user=None, **kwargs):
        response = {}
        try:
            user.delete()
            response['ok'] = 'record deleted'
        except Exception as error:
            print error
            pass
        return self.json_response(data=response)

app = Flask(__name__)
app.add_url_rule('{0}/users/'.format(UserAPIView.ENDPOINT), view_func=UserAPIView.as_view('users'))

def run_app():
    app.run(host='0.0.0.0', port=8000, debug=True)
