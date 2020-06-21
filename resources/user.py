from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Register(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=str,required=True,help="User_id cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be left blank!")
        parser.add_argument('usertype',type=str,required=True,help="usertype cannot be left blank!")
        parser.add_argument('phone_no',type=str,required=True,help="Phone no. number can't be left blank!")
        parser.add_argument('email_id',type=str,required=True,help="Email ID can't be left blank!")
        data=parser.parse_args()
        if User.getUserByuser_id(data['user_id']):
            return {"message": "A user with that user_id already exists"}, 400
        try:
            query(f"""INSERT INTO USER(user_id,password,usertype,phone_no,email_id)
                                  VALUES('{data['user_id']}','{data['password']}','{data['usertype']}',
                                         '{data['phone_no']}','{data['email_id']}')""")
        except:
            return {"message": "An error occurred while registering."}, 500
        return {"message": "User created successfully."}, 201
   
class User():
    def __init__(self,user_id,password,usertype):
        self.user_id=user_id
        self.password=password
        self.usertype=usertype

    @classmethod
    def getUserByuser_id(cls,user_id):
        result=query(f"""SELECT user_id,password,usertype FROM USER WHERE user_id='{user_id}'""",return_json=False)
        if len(result)>0: return User(result[0]['user_id'],result[0]['password'],result[0]['usertype'])
        return None

class UserLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=str,required=True,help="user_id cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        parser.add_argument('usertype',type=str,required=True,help="usertype cannot be left blank!")
        data=parser.parse_args()
        user=User.getUserByuser_id(data['user_id'])
        if user and user.usertype==data['usertype'] and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.user_id,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401