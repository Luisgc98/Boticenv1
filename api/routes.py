import markdown
import os
from flask import Flask, current_app, redirect
from api import app, babel
from flask_restful import Api,request
from api.routes_helper import Setup, Alive, NextJob, JobScript, JobEvidendeDetails, ScreenShotDetails, FailurePrintScreen, JobEvidence, JobStatus

#Internationalization
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en','es'])

@app.route('/')
def index():
    return redirect(current_app.config['PORTAL_URL'], code=302)

# Related to REST Api documentation
@app.route("/api/")
def apiIndex():
    """Generates API's documentation page"""
    # Open the README.md file to show its content
    with open(os.path.dirname(app.root_path) + "/README.md", 'r') as doc:
        # Reads the file's content
        content = doc.read()
        # Converts it to HTML
        return markdown.markdown(content)

# For Rest API.
api = Api(app, prefix= app.config['API_PREFIX'])

# add REST resources
api.add_resource(Setup, '/bot/setup') #POST
api.add_resource(Alive, '/bot/alive') #POST 
api.add_resource(NextJob, '/job/next') #GET
api.add_resource(JobScript, '/script') #GET
api.add_resource(JobEvidendeDetails, '/job') #POST
api.add_resource(ScreenShotDetails, '/job/screenshot') #POST
api.add_resource(FailurePrintScreen, '/job/failure') #POST
api.add_resource(JobEvidence, '/job/evidence') #POST
api.add_resource(JobStatus, '/job/status') #POST