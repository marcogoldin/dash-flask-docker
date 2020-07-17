from flask import Flask, render_template, Response, redirect, url_for, request, session, abort, send_file
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

import dash
from dash import callback_context
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

user_pwd, user_names = users_info()

from navbar import Navbar
nav = Navbar()

# this is needed to secure each Dash app behind login
def protect_views(app):
	for view_func in app.server.view_functions:
		if view_func.startswith(app.config['url_base_pathname']):
			app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])
	
	return app


server = Flask(__name__)

server.config.update(
	DEBUG = True,
	SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "login"


# i know, this is lazy, but you can implement your own login/registration model if needed
class User(UserMixin):

	def __init__(self, id):
		self.id = id
		self.name = str(id)
		self.password = "my-super-secret-password"
		
	def __repr__(self):
		return "%d/%s/%s" % (self.id, self.name, self.password)


# quick user creation, if needed you can implement a more robust approach
users = [User("user1@domain.com"),User("user2@domain.com"),User("user3@domain.com")]

# route to login
@server.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']        
		if password == "my-super-secret-password":
			id = username
			user = User(id)
			login_user(user)
			return render_template("home.html")
		else:
			return abort(401)
	else:
		return render_template("login.html")


# route to logout
@server.route("/logout")
@login_required
def logout():
	session.clear()
	return redirect(url_for("login"))


# handle a failed login with cutom logics and template
@server.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')
	
	
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
	return User(userid)

# first Dash app
dash_app1 = dash.Dash(
	__name__,
	server = server,
	url_base_pathname='/app1/', 
	suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MATERIA],
	meta_tags=[
		{"name": "viewport", "content": "width=device-width, initial-scale=1"}
	])

dash_app1.title = 'First Dash App'

dash_app1.layout = dbc.Container([
	dcc.Location(id='url', refresh=False),
	nav,
	dbc.Button("Dash app 1 button!", id='download', color="warning", className="mr-1", href="", n_clicks=0, style={"margin":"1rem 0 1rem 0"}),
	], fluid=True)


dash_app1 = protect_views(dash_app1)


#second Dash app
dash_app2 = dash.Dash(
	__name__,
	server = server,
	url_base_pathname='/app2/', 
	suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MATERIA],
	meta_tags=[
		{"name": "viewport", "content": "width=device-width, initial-scale=1"}
	])

dash_app2.title = 'Second Dash App'

dash_app2.layout = dbc.Container([
	dcc.Location(id='url', refresh=False),
	nav,
	dbc.Button("Dash app 2 button!", id='download', color="warning", className="mr-1", href="", n_clicks=0, style={"margin":"1rem 0 1rem 0"}),
	], fluid=True)


dash_app2 = protect_views(dash_app1)


# Flask Home
@server.route('/')
@login_required
def home():
	return render_template('home.html')

# dash app 1 routing
@server.route('/dash1')
def render_dashboard1():
	return redirect('/app1')

# dash app 2 routing
@server.route('/dash2')
def render_dashboard2():
	return redirect('/app2')

# DAH CALLBACKS HERE
# @dash_app1.callback(Output('',''),[Input('','')])
# def callback_func():
# 	...

# @dash_app2.callback(Output('',''),[Input('','')])
# def callback_func():
# 	...
	

# if needed you can also leverage Flask routing to serve static file from all apps
# remember to check the correct volume mounted in docker-compose.yml
@dash_app1.server.route("/static_file_download/")
def serve_file_app1():

	return send_file(
		"/root/app/static/data/file-name",
		attachment_filename='file-name.***',
		as_attachment=True,
	)

@dash_app2.server.route("/static_file_download/")
def serve_file_app2():

	return send_file(
		"/root/app/static/data/file-name",
		attachment_filename='file-name.***',
		as_attachment=True,
	)
