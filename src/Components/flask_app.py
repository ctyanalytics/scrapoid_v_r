# =============================================================================
# FLASK_APP.PY is the main web framework and endpoint hub
# =============================================================================

#EXTERNAL IMPORTS
#=============================================================================
from flask import Flask,jsonify,render_template, redirect
from flask import  flash, request, session
import os
import sys


#INTERNAL IMPORTS
#=============================================================================
sys.path.append('/home/ctyanalytics/github/CtyAnalytics_lib')
import environment
import tools
import communicator
from db_tool import data_tool as dr
from scrapoid import scrapoid
from scrapoid_prototype import scrapoid as scrapoid_v2
from json import dumps
#Config and Initilization of Flask app
#=============================================================================
config = environment.get_config()
com    = communicator.communication(config)
app    = Flask(__name__)
app.secret_key = os.urandom(12)

#HOME ENDPOINT COMMERCIAL FRONT END
#=============================================================================
@app.route('/', methods=['GET'])
def home():
    com.communicate_to_concerned("system_event","Yo! A user is accessing commercial page ... we are gonna be Rich ! ")
    return render_template(config["rcore_template"])


#HOME ENDPOINT COMMERCIAL FRONT END
#=============================================================================
@app.route('/scrapoidv3/', methods=['GET'])
@app.route('/scrapoidv3', methods=['GET'])
def scrapoidv2_web():

    return render_template(config["scrapoid_template"].replace('scrapoid','scrapoidv3'))


#HOME ENDPOINT COMMERCIAL FRONT END
#=============================================================================
@app.route('/scrapoid/', methods=['GET'])
@app.route('/scrapoid', methods=['GET'])
def scrapoid_web():

    return render_template(config["scrapoid_template"])

@app.route('/scrapoid_answer_react/', methods=['GET'])
def scrapoid_answer_react():
    iteration=int(request.args["iteration"])
    current_state = str(request.args["current_state"])
    short_term_memory = str(request.args["short_term_memory"])
    scrappy = scrapoid_v2(None)

    answer=scrappy.process_web_message_vReact(iteration,current_state,short_term_memory)


    answer=dumps(answer)
    return   answer


@app.route('/scrapoid_answer/', methods=['GET'])
def scrapoid_answer():

 message=str(request.args["message"])
 step = str(request.args["step"])
 url=str(request.args["url"])
 #passing data to scrapoid
 if step=="react_test":

     return jsonify({"result": "test"})
 if step=='url':
     if str(message).replace(" ","") != ""   :
         url=message
         answer="Yum ... yum, the website is in my belly now hehe. Tell me, What do you need ?"
         return answer
 if step=='ask_element':

         answer=f"... Ok i will get you your {message}"


         scrappy = scrapoid(None,url)
         data=scrappy.listAll(scrappy.html,message)

         answer=scrappy.jsonify_with_htmls(data)

         return answer
 if step=='memorize_element':
      scrappy = scrapoid(None,url)
      import json

      info_memorization=json.loads(message)

      scrappy.memorize (info_memorization,recompute_location=True)

      return " Yo, I have memorize it sucessfully  ! need anything else ? "
 if step == 'memorization' :
     if message=='yes':
        answer = " Alright ! Please give me its number followed by its module and the name you want to give to this task as format : numer-module-script"
     else:
         answer =' I am bored ..'
     return answer
#USER HUB ENDPOINT
#=============================================================================
@app.route('/api/', methods=['GET'])
@app.route('/api', methods=['GET'])
def user_hub():
        #We push to ctyanalytics team to let know what happened:
    com.communicate_to_concerned("system_event","Yo! A user is accessing userhub.")
    session['job'] = "user_hub"
    if not session.get('logged_in'):  return render_template(config["login_template"])
    else:

        return render_template(config["user_hub_template"])


@app.route('/api/refresh_data', methods = ['GET'])
def ajax_request():

    data=dr(config, "dcore_db")
    tasks=data.get_data('tasks')
    return render_template(config["task_table_template"],tasks=tasks)

#ERROR ENDPOINT
#=============================================================================
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def notfound(error): return render_template(config["notfound_template"],error_code=error)


#LOGOUT ENDPOINT
#=============================================================================
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



#CONSUMPTION DATA ENDPOINT
#=============================================================================
@app.route('/api/consumption', methods=['GET'])
def get_tasks():
    #We push to ctyanalytics team to let know what happened:
    com.communicate_to_concerned("system_event","Yo! A user is consuming data through endpoints.")
    session['job'] = "data"
    if not session.get('logged_in'):
        session['already_filtered'] = True
        session['filters'] = request.args
        return render_template(config["login_template"])
    else:

        #INITIALIZATION OF datareader of dbbot database
        data=dr(config, "dbbot")
        already_filtered=session.get('already_filtered',False)
        if already_filtered :
            query_parameters = session.get('filters',False)
            data_value=data.get_data('consumption',query_parameters)
            session['already_filtered'] = False
        else :
            query_parameters = request.args
            data_value=data.get_data('consumption',query_parameters.to_dict())



        return jsonify(data_value)


#PUSH EVENT ENDPOINT
#=============================================================================
#Example of push request
#https://ctyanalytics.pythonanywhere.com/api/push/event?type=test_event&text= Dynamic generation of message
@app.route('/api/push/event', methods=['GET'])
def push_data():
    type=""
    text=""
    try:

      type=request.args["type"]
      text=request.args["text"]
      insert_query_event=f"INSERT INTO event ( event_type  , event_text ) VALUES ( '{type}'  , '{text}' )"

    #Now we should push the message into the database
      data=dr(config, "client_db")
      data.execute_query(insert_query_event)


     #Now we push to subscribers:
      com.communicate_to_concerned(type,"Message from endpoint: "+ str(text))

      return "TRUE"
    except:
        return "FALSE"





#CHECK IF ADMIN LOGED IN ENDPOINT
#=============================================================================
@app.route('/login', methods=['POST'])
def do_admin_login():
    com.communicate_to_concerned("system_event","Yo! A user is login.")
    if session['job'] == 'data':
        if request.form['password'] == 'password' and request.form['username'] == 'username':
             session['logged_in'] = True
        else:
            flash('wrong password!')
        return get_tasks()
    elif   session['job'] == 'user_hub':
         if request.form['password'] == 'password' and request.form['username'] == 'username':
                     session['logged_in'] = True
         else:
                    flash('wrong password!')
         return  redirect('/api')



#MAIN
#=============================================================================
if __name__ == '__main__':
    app.run(debug=True)
