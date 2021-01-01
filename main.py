# importing Flask class
from flask import Flask
# importing request
from flask import request
# importing views from authentication module
from authentication import views
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from plans import views as plan_views

# do initialisation of plans
plan_views.plans_initialisation()

# create app
app=Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app,views.authenticate ,views.identity)

# signup route
app.add_url_rule('/signup','signup',views.signup,methods=['POST'])
# login route
app.add_url_rule('/login','login',views.login,methods=['POST'])

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()

