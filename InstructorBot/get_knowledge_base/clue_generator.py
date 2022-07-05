from pymongo import MongoClient
from flask import Flask,request
import json
import re

#Setup Flask Server
app = Flask(__name__) 

# Setup url route which will generate clues
@app.route('/clue_1', methods = ['POST']) 
def first_clue():
    query=request.get_json()

    #Create a client instance of MongoDB class
    client=MongoClient()
    #Create an instance of database
    db=client.knowledge_base
    col = db.tag_info 
    data= col.find_one({"Tag":query['tag']})   
    result=data["Info"]
    return json.dumps({"result":result})

@app.route('/clue_2', methods = ['POST']) 
def second_clue():
    query=request.get_json()

    #Create a client instance of MongoDB class
    client=MongoClient()
    #Create an instance of database
    db=client.knowledge_base
    col = db.tag_info 
    data= col.find_one({"Tag":query['c_tag']}) 
    if query['c_tag'] in data["Info"]:
        result=re.sub(query['c_tag'],"******",data["Info"])
    else:
        result=data["Info"]
    return json.dumps({"result":result})

@app.route('/clue_3', methods = ['POST']) 
def third_clue():
    query=request.get_json()

    #Create a client instance of MongoDB class
    client=MongoClient()
    #Create an instance of database
    db=client.knowledge_base
    col = db.tag_info 
    data= col.find_one({"Tag":query['c_tag']}) 
    ll=data["LowLimit"]
    hl=data["HighLimit"]

    if ll!="" and hl!="":
        result="The value of tag should lie between " + ll+ " and "+ hl+"."
    else:
        result="Information regarding limits of tag is not present in KPVs."
    return json.dumps({"result":result})
   

if __name__ == "__main__": 
    app.run(port=5000)