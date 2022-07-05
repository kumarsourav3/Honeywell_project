import pandas as pd
import xml.etree.ElementTree as et
from flask import Flask, request
import json 
from pymongo import MongoClient
import re

app = Flask(__name__) 


@app.route('/tag', methods = ['POST'])
def get_tag():
    tag_name=[]
    order=[]
    data=request.get_json()

    exe=data['exercise_no']
    seq_=data['order']

    tree=et.parse(r".\get_knowledge_base\info_files\xml\PCs\Troubleshooting"+exe+'-PC.xml')
    root=tree.getroot()

    for x in root.iter('FullTagName'):
        tag_name.append(x.text.upper().split('.')[0])
    
    for x in root.iter('DefinedSequence'):
        order.append(x.text)

    return json.dumps({"result":tag_name[int(order.index(str(seq_)))]})

@app.route('/description', methods = ['POST'])
def get_desc():
    desc=[]
    order=[]

    data=request.get_json()

    exe=data['exercise_no']
    seq_=data['order']

    tree=et.parse(r".\get_knowledge_base\info_files\xml\PCs\Troubleshooting"+exe+'-PC.xml')
    root=tree.getroot()

    for x in root.iter('Description'):
        desc.append(x.text)
    for x in root.iter('DefinedSequence'):
        order.append(x.text)
    i=int(order.index(str(seq_)))
    print("seq ",int(order.index(str(seq_))))
    return json.dumps({"result":desc[i]})

@app.route('/clue_1', methods = ['POST']) 
def first_clue():
    query=request.get_json()

    #Create a client instance of MongoDB class
    client=MongoClient()
    #Create an instance of database
    db=client.knowledge_base
    col = db.tag_info 
    data= col.find_one({"Tag":query['tag']})   
    # result=data["Info"]
    return json.dumps({"result":query['tag']})

@app.route('/clue_2', methods = ['POST']) 
def second_clue():
    query=request.get_json()

    #Create a client instance of MongoDB class
    client=MongoClient()
    #Create an instance of database
    db=client.knowledge_base
    col = db.tag_info 
    data= col.find_one({"Tag":query['tag']}) 
    if query['tag'] in data["Info"]:
        # result=re.sub(query['tag'],"******",data["Info"])
        result=data["Info"]
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
    data= col.find_one({"Tag":query['tag']}) 
    ll=data["LowLimit"]
    hl=data["HighLimit"]

    if ll!="" and hl!="":
        result="The value of tag should lie between " + ll+ " and "+ hl+"."
    else:
        result="Information regarding limits of tag is not present in KPVs."
    return json.dumps({"result":result})
   
if __name__ == "__main__":
    app.debug = True 
    app.run(port=5000)


