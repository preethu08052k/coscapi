from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required
from db import query
import datetime

class Vech_Reg(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('reg_id',type=int,required=True,help="please give reg_id")
        data=parser.parse_args()
        try:
            return query(f"""SELECT * FROM CBIT_PARKING.REGISTRATION WHERE reg_id={data['reg_id']}""")
        except:
            return {"message":"There was an error displaying the data"},500 


    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=str,required=True,help="user_id cannot be left blank!")
        parser.add_argument('full_name',type=str,required=True,help="full_name cannot be left blank!")
        parser.add_argument('home_address',type=str,required=True,help="home_address cannot be left blank!")
        parser.add_argument('licence_no',type=str,required=True,help="licence_no cannot be left blank!")
        parser.add_argument('branch_name',type=str,required=True,help="branch_name cannot be left blank!")
        parser.add_argument('vehicle_type',type=str,required=True,help="vehicle_type cannot be left blank!")
        parser.add_argument('chassis_no',type=str,required=True,help="chassis_no cannot be left blank1")
        parser.add_argument('vehicle_no',type=str,required=True,help="vehicle_no cannot be left blank!")
        parser.add_argument('reg_date',type=str,required=True,help="reg_date cannot be left blank!")
        data=parser.parse_args()
        
        try:
            query(f"""INSERT INTO CBIT_PARKING.REGISTRATION (user_id,full_name,home_address,licence_no,branch_name,vehicle_type,chassis_no,vehicle_no,reg_status,reg_date,updated_date)
                                                             VALUES('{data['user_id']}',
                                                                    '{data['full_name']}',
                                                                    '{data['home_address']}',
                                                                    '{data['licence_no']}',
                                                                    '{data['branch_name']}',
                                                                    '{data['vehicle_type']}',
                                                                    '{data['chassis_no']}',
                                                                    '{data['vehicle_no']}',
                                                                    'pending',
                                                                    '{data['reg_date']}',
                                                                    '{datetime.date.today()}')""")
        except:
            return {"message":"There was an error inserting into REGISTRATION table."},500
        return {"message":"Successfully Inserted."},201

class Reg_Status(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM CBIT_PARKING.REGISTRATION WHERE reg_status='pending'""")
        except:
            return {"message":"There was an error displaying the data"},500

    @jwt_required
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('reg_id',type=int,required=True,help="please give reg_id")
        data=parser.parse_args()
        try:
            query(f"""UPDATE CBIT_PARKING.REGISTRATION SET reg_status='approved',updated_date='{datetime.date.today()}' WHERE reg_id={data['reg_id']}""")
        except:
            return {"message":"there was an error updating the reg_status"},500
        return {"message":"successfully updated"},201

class DismissVech(Resource):
    @jwt_required
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('reg_id',type=int,required=True,help="please give reg_id")
        data=parser.parse_args()
        try:
            query(f"""UPDATE CBIT_PARKING.REGISTRATION SET reg_status='dismiss',updated_date='{datetime.date.today(),}' WHERE reg_id={data['reg_id']}""")
           
        except:
            return {"message":"there was an error updating the reg_status"},500
        return {"message":"dismissed vehicle successfully"},201

class Stats(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM CBIT_PARKING.REGISTRATION WHERE updated_date='{datetime.date.today()}'""")
        except:
            return {"message":"There was an error displaying the data"},500 
        


    
