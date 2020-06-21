from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import Register,UserLogin
from resources.registration import Vech_Reg,Reg_Status,DismissVech,Stats
from resources.payments import FinePayments

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='coscskillup'
api=Api(app)
jwt=JWTManager(app)



@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401


api.add_resource(Register,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(Vech_Reg,'/vechreg')
api.add_resource(Reg_Status,'/pending')
api.add_resource(DismissVech,'/dismiss')
api.add_resource(Stats,'/regstats')
api.add_resource(FinePayments,'/fine')

if __name__=='__main__':
    app.run()
