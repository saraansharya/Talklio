#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 09:51:19 2022

@author: saraansharya
"""

from flask import Flask, request
import random
import re
from postgres_wrapper import PGWrapper 

postgres_config = config = {
    "database": "hackathon_db",
    "user": "username",
    "password": "quoted password",
    "host": "localhost",
    "port": 5432,
}


app = Flask(__name__)
postgres_db_con = PGWrapper(postgres_config)
postgres_db_con.connect()
def questionFormatting(user_id,question):
    question = re.sub('\_',' ',question)
    question_id = random.randint(100000,999999)
    query = "INSERT INTO ucl_hackathon.questions (question_id, question_text, user_id) VALUES (%s, %s, %s)"
    postgres_db_con.cursor.execute(query,(str(question_id),str(question), str(user_id)))
    return question_id


def createUser(firstName, lastName, email):
    user_id = random.randint(100000,999999)
    query = "INSERT INTO ucl_hackathon.users (user_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
    postgres_db_con.cursor.execute(query,(str(user_id),str(firstName), str(lastName), str(email)))
    return user_id

def insertAnswer(user_id,question_id,answer):
    answer = re.sub('\_',' ',answer)
    answer_id = random.randint(100000,999999)
    query = "INSERT INTO ucl_hackathon.answers (answer_id, question_id, answer_text, user_id) VALUES (%s, %s, %s, %s)"
    postgres_db_con.cursor.execute(query,(str(answer_id),str(question_id),str(answer), str(user_id)))
    return answer_id
    
# Example URL: http://localhost:5000/latest/loadQuestion?question_id=10
@app.route("/latest/loadQuestion")
def api_loadQuestion():
    # input validations
    if request.args.get('question_id') is None:
        return('Please add a valid question id')
    try:
        question_id = str(request.args.get('question_id'))
        
        results = postgres_db_con.query_as_list_of_dicts("SELECT * FROM ucl_hackathon.questions WHERE question_id="+str(question_id))
        output = {}
        question_id_list = []
        question = []
        for dictionary in results:
            question_id_list.append(dictionary['question_id'])
            question.append(dictionary['question_text'])
        output['question_id'] = question_id_list
        output['question'] = question
    
        results_answers = postgres_db_con.query_as_list_of_dicts("SELECT * FROM ucl_hackathon.answers WHERE question_id="+str(question_id))
        answers = []
        for dictionary in results_answers:
            
            answers.append(dictionary['answer_text'])
        
        output['answer_text'] = answers
        
    except:
       return('The question has some invalid characters')
    
    
    
    # everyting was OK
    return output


# Example URL: http://localhost:5000/latest/addUser?firstName=abc&lastName=xyz&email=abc.xyz@gmail.com
@app.route("/latest/addUser")
def api_addUser():
    try:
        firstName = str(request.args.get('firstName'))
    except:
        return('The question has some invalid characters')
    try:
        lastName = str(request.args.get('lastName'))
    except:
        return('The answer has some invalid characters')
    try:
        email = str(request.args.get('email'))
    except:
        return('The answer has some invalid characters')
    
    userID = createUser(firstName, lastName, email)
    # everyting was OK
    return {"text":"Thanks for signing up", "userID":userID}
    

# Example URL: http://localhost:5000/latest/addQuestion?x=Where_do_I_get_good_stuff&user_id=1111
@app.route("/latest/addQuestion")
def api_addQuestion():
    # input validations
    if request.args.get('x') is None:
        return('Please add a valid question')
    if request.args.get('user_id') is None:
        return('Please add a valid question')
    try:
        question = str(request.args.get('x'))
    except:
        return('The question has some invalid characters')
    try:
        user_id = str(request.args.get('user_id'))
    except:
        return('The question has some invalid characters')
    
    question_id = questionFormatting(user_id,question)
    
    # everyting was OK
    return {"text": "Thanks for your question", "question_id":question_id}

# Example URL: http://localhost:5000/latest/addAnswer?question_id=10&answer=100&user_id=1111
@app.route("/latest/addAnswer")
def api_addAnswer():
    # input validations
    if request.args.get('question_id') is None:
        return('Please select a valid question')
    if request.args.get('answer') is None:
        return('Please add a valid answer')
    if request.args.get('user_id') is None:
        return('Please add a valid answer')
    try:
        question_id = str(request.args.get('question_id'))
    except:
        return('The question has some invalid characters')
    try:
        answer = str(request.args.get('answer'))
    except:
        return('The answer has some invalid characters')
    try:
        user_id = str(request.args.get('user_id'))
    except:
        return('The question has some invalid characters')
    answer_id = insertAnswer(user_id, question_id,answer)
    
    # everyting was OK
    return {"text":"Thanks for your answer", "answer_id": answer_id}



# any other URL (custom handling of 404 error)
@app.errorhandler(404)
def page_not_found(e):
    return "Incorrect API endpoint"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)