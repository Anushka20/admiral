# importing Flask class, render_template
from flask import Flask, render_template
# importing request
from flask import request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# importing views from plan module
from plan import views as plan_views
# importing views from authentication module
from authentication import views as authentication_views
# importing views from user module
from user import views as user_views
# do initialisation of plan table in database
plan_views.plans_initialisation()
# do initialisation of user table in database
authentication_views.users_initialisation()
# do initialisation of user_plan table in database
user_views.user_plan_initialisation()
# importing datetime
import datetime

# create app
app=Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# to increase expiration time of 
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)

jwt = JWT(app,authentication_views.authenticate ,authentication_views.identity)

def index():
    return render_template('home.html')

def car_insurance():
    return render_template('car_insurance.html')

def home_insurance():
    return render_template('home_insurance.html')

# home route
app.add_url_rule('/','index',index)
# car insurance route
app.add_url_rule('/car_insurance','car_insurance', car_insurance)
# home insurance route
app.add_url_rule('/home_insurance', 'home_insurance', home_insurance)
# signup route
app.add_url_rule('/signup','signup',authentication_views.signup,methods=['POST', 'GET'])
# login route
app.add_url_rule('/login','login',authentication_views.login,methods=['POST','GET'])
# user profile
app.add_url_rule('/user_profile','user_profile',user_views.user_profile, methods=['POST'])
# update car insurance type of user
app.add_url_rule('/update/car_insurance_type','update_car_insurance_type',plan_views.update_car_insurance_plan, methods=['POST'])
# update home insurance type of user
app.add_url_rule('/update/home_insurance_type','update_home_insurance_type',plan_views.update_home_insurance_plan, methods=['POST'])
# update user profile
app.add_url_rule('/update/profile', 'update_profile', user_views.update_profile, methods=['POST'])
# get user plans
app.add_url_rule('/user/plans', 'get_user_plans', plan_views.get_user_plans, methods=['POST'])
# delete user plan
app.add_url_rule('/user/plan/delete', 'delete_insurance', plan_views.delete_insurance, methods=['POST'])
# delete user account
app.add_url_rule('/user/account/delete', 'delete_account', user_views.delete_account, methods=['POST'])

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()

