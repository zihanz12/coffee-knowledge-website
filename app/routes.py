from flask import Flask, render_template, request, make_response, flash, redirect, jsonify, session
from app import app
from app import database as db_helper
import json
import os

from multiprocessing import Process

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def radar_plot(stats, filename):
    label = list(stats.keys())
    value = list(stats.values())

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ANGLES = np.linspace(0.05, 2 * np.pi - 0.05, len(value), endpoint=False)
    GREY12 = "#1f1f1f"

    plt.rcParams.update({"font.family": "Bell MT"})
    plt.rcParams["text.color"] = GREY12
    plt.rc("axes", unicode_minus=False)

    COLORS = ["#6C5B7B","#C06C84","#F67280","#F8B195"]
    cmap = mpl.colors.LinearSegmentedColormap.from_list("my color", COLORS, N=256)
    norm = mpl.colors.Normalize(vmin=min(value), vmax=max(value))
    COLORS = cmap(norm(value))

    ax.set_theta_offset(1.2 * np.pi / 2)
    ax.set_ylim(0, 10)
    ax.bar(ANGLES, value, color=COLORS, alpha=0.9, width=0.52, zorder=10)
    ax.vlines(ANGLES, 0, 3000, color=GREY12, ls=(0, (4, 4)), zorder=11)
    ax.set_xticks(ANGLES)
    ax.set_xticklabels(label, size=12)

    if os.environ.get('GAE_ENV') != 'standard':
        plt.savefig(filename, bbox_inches='tight', transparent=True)
    else:
        import io
        import base64
        from google.cloud import storage

        client = storage.Client(project='eighth-study-354817')
        bucket = client.bucket('coffeedata')
        blob = bucket.blob('bean_stats.png')

        # temporarily save image to buffer
        buf = io.BytesIO()
        plt.savefig(buf, bbox_inches='tight', transparent=True, format='png')

        # upload buffer contents to gcs
        blob.upload_from_string(
            buf.getvalue(),
            content_type='image/png')

        buf.close()
    
    return

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
 success = db_helper.remove_task_by_id(task_id, request.cookies.get('username',None))
 
 if success:
  result = {'success': True, 'response': 'Removed task'}
  response = jsonify(result)
  response.status_code = 200
  return response
 else:
  result = {'success': False, 'response': 'Something went wrong'}
  response = jsonify(result)
  response.status_code = 400
  return response
 
@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
 data = request.get_json()
 
 success = db_helper.update_post_entry(task_id, data["description"],request.cookies.get('username',None))
 
 if success:
  result = {'success': True, 'response': 'Task Updated'}
  response = jsonify(result)
  response.status_code = 200
  return response
 else:
  result = {'success': False, 'response': 'Something went wrong'}
  response = jsonify(result)
  response.status_code = 200
  return response

@app.route("/delete/drink/<string:CoffeeName>", methods=['POST'])
def delete_drink(CoffeeName):
    try:
        username = request.cookies.get('username',None)
        if username == 'admin': 
            db_helper.remove_drink(username, CoffeeName)
            result = {'success': True, 'response': 'Removed drink'}
            response = jsonify(result)
        else:
            raise Exception("You must be admin")
    except:
        result = {'success': False, 'response': 'Something went wrong'}
        response = jsonify(result)
        response.status_code = 400
    return response

@app.route("/edit/drink/<string:CoffeeName>", methods=['POST'])
def update_drink(CoffeeName):
    data = request.get_json()
    success = db_helper.update_drink_entry(
        request.cookies.get('username',None),
        CoffeeName, 
        data['Calories']
    )
    if success:
        result = {'success': True, 'response': 'Drink Updated'}
        response = jsonify(result)
        response.status_code = 200
        return response
    else:
        result = {'success': False, 'response': 'Something went wrong'}
        response = jsonify(result)
        response.status_code = 400
        return response

@app.route("/like/drink/<string:CoffeeName>", methods=['POST'])
def like_drink(CoffeeName):
    try:
        username = request.cookies.get('username',None)
        if username:
            db_helper.like_drink(username, CoffeeName)
            result = {'success': True, 'response': 'Liked drink'}
        else:
            result = {'success': True, 'response': 'Login required'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)

@app.route("/unlike/drink/<string:CoffeeName>", methods=['POST'])
def unlike_drink(CoffeeName):
    try:
        username = request.cookies.get('username',None)
        if username:
            db_helper.unlike_drink(username, CoffeeName)
            result = {'success': True, 'response': 'Unliked drink'}
        else:
            result = {'success': True, 'response': 'Login required'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)

@app.route("/Drinks/searchDrink", methods=['POST'])
def search_drink():
    data = request.get_json()
    db_helper.search_drink(data['name'])
    result = {'success': True, 'response': 'Nothing Updated'}
    return jsonify(result)

@app.route("/searchDrink", methods=['GET'])
def search_drink_display():
    items = db_helper.fetch_drink_searches()
    return render_template("drink.html", items=items)

@app.route("/Drinks/limit-calory", methods=['POST'])
def limit_calory():
    data = request.get_json()
    db_helper.fetch_drinks_w_calory_limit(calory_limit=data['limit'])
    result = {'success': True, 'response': 'Nothing Updated'}
    return jsonify(result)

@app.route("/limit-calory", methods=['GET'])
def limit_display():
    items = db_helper.fetch_limits()
    return render_template("drink.html", items=items)


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    db_helper.insert_new_task(data['description'], request.cookies.get('username',None))
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/create_drink", methods=['POST'])
def create_drink():
    data = request.get_json()
    db_helper.insert_new_task(data['description'], request.cookies.get('username',None))
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/")
def homepage():
    """ returns rendered homepage """
    return render_template("home.html")   

@app.route("/Section")
def sectionpage():
    """ returns rendered homepage """
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("section.html", loginstatus = loginouttext)

@app.route("/Lab")
def categorypage():
    """ returns rendered homepage """
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("category.html", loginstatus = loginouttext)

@app.route("/CategorySearch",methods=["POST"])
def CategorySearch():
    search_category = request.form['query']

    post_result = db_helper.advance_query_post(search_category) 
    drink_result = db_helper.recommandDrink(search_category)
    recipe_result = db_helper.search_category(search_category)

    filename = "/static/img/category/"+search_category.lower().replace(' ', '_')+".png"

    return jsonify({'htmlresponse': render_template('category_spec.html', category=search_category, filename=filename, post_result=post_result, recipe_result=recipe_result, drink_result=drink_result)})



@app.route("/Beans")
def beanpage():
    """ returns rendered homepage """
    items = db_helper.fetch_beans()
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("bean.html", items=items, loginstatus = loginouttext)

@app.route("/BeanSearch",methods=["POST"])
def BeanSearch():
    bean_id = request.form['query']

    bean_stats = db_helper.fetch_bean_stats(bean_id) 
    farm_info = db_helper.fetch_bean_farm(bean_id)
    
    if os.environ.get('GAE_ENV') != 'standard':
        img_file = "/static/img/bean_stats.png"
    else:
        img_file = "https://storage.cloud.google.com/coffeedata/bean_stats.png"

    p = Process(target=radar_plot, args=(bean_stats[0], "app"+img_file))
    p.start()
    p.join()

    return jsonify({'htmlresponse': render_template('bean_spec.html', bean_id=bean_id, bean_stats=bean_stats, farm_info=farm_info, img_file=img_file)})


@app.route("/Fact", methods = ['GET','POST'])
def drinkpage():
    """ returns rendered homepage """
    items, search = db_helper.fetch_drinks(request.cookies.get('username',None))
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("drink.html", items=items, loginout=loginout, loginstatus=loginouttext, search=search)

@app.route("/Fact/<string:search>", methods = ['GET','POST'])
def drink_page_after(search):
    """ returns rendered homepage """
    search = json.loads(search)
    items, search = db_helper.fetch_drinks(request.cookies.get('username',None), search)
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("drink.html", items=items, loginout=loginout, loginstatus=loginouttext, search=search)

@app.route("/createuser", methods = ['GET'])
def create_userg():
    return render_template("create_user.html", loginstatus ='Login')
    
@app.route('/createuserbackend', methods = ['POST'])
def create_user():
    data = request.get_json()
    db_helper.insert_user(data['username'],data['password'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route('/loginbackend', methods = ['POST'])
def user():
    data = request.get_json()
    pa = db_helper.userinfo(data['username'])
    
    if pa is None:
        result = {'success': True, 'response': 'create new'}
        print(result)
        response = jsonify(result)
        response.status_code = 400
        return response

    elif data['password'] == pa[0]:
        print("yes!")
        result = {'success': True, 'response': 'Successful login'}
        response = jsonify(result)
        response.set_cookie('username', data['username'])
        response.status_code = 200
        print(response)
        return response
    else:
        result = {'success': False, 'response': 'Something went wrong'}
        response = jsonify(result)
        response.delete_cookie('username')
        response.status_code = 400
        print(response)
        return response
    

@app.route('/login', methods = ['GET'])
def userg():
    return render_template("login.html", loginstatus ='Login')


# button only needs to point to this endpoint, no ajax needed
@app.route('/logout', methods = ['GET'])
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('username',"no user")
   return '<h1>welcome ' + name + '</h1>'

@app.route("/deleteacc", methods=['POST'])
def deleteuser():
    success = db_helper.delete_user(request.cookies.get('username'))
    if success:
        result = {'success': True, 'response': 'Removed task'}
        response = jsonify(result)
        response.status_code = 200
    else:
        print('fail')
        result = {'success': False, 'response': 'Something went wrong'}
        response = jsonify(result)
        response.status_code = 400
    response.delete_cookie('username')
    return response

@app.route("/Posts")
def postpage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    loginout = request.cookies.get('username',None)
    if loginout is None:
        loginouttext = "Login"
    else:
        loginouttext = "Logout"
    return render_template("post.html", items=items, loginstatus = loginouttext)

## added by zihan
@app.route("/ajaxlivesearch",methods=["POST"])
def ajaxlivesearch():
    search_word = request.form['query']
    print(search_word)  # where deos this go---oh its goes to terminal
    post_result = db_helper.search_posts(search_word) 
    numrows = len(post_result)
    print(numrows)
    return jsonify({'htmlresponse': render_template('response.html', items = post_result, numrows = numrows)})
