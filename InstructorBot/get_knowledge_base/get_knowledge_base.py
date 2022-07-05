import nltk
import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import json
import pymongo
import xml.etree.cElementTree as et
import os
import spacy
from spacy import displacy

poppler_path=r'C:\Users\H501271\Downloads\Release-22.04.0-0\poppler-22.04.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\H501271\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def get_list_d(file):
    tag=[]
    description=[]
    reader=pdfplumber.open(file)
    for num_page in range(len(reader.pages)):
        tables=reader.pages[num_page].extract_tables(table_settings={"vertical_strategy": "lines", 
        "horizontal_strategy": "lines"})
        for table in tables:
            n_table=[]
            for row in table:
                while "" in row:
                    row.remove("")
                while None in row:
                    row.remove(None)
                n_table.append(row)

            if "Tag" in n_table[0] and "Description" in n_table[0]:
                di=n_table[0].index("Description")
                ti=n_table[0].index("Tag")
                for row in n_table[1:]:
                    tag.append(row[ti])
                    description.append(row[di])

    df=pd.DataFrame(list(zip(tag, description)),columns=['Tag','Description'])
    df=df.drop_duplicates(keep='first')
    df=df.reset_index(drop=True)
    
    return df

n=int(input("Enter the number of pdf files which contain list of tags: "))
dfs=[]
while(n):
    tag_file=input("Enter the path to pdf file : ")
    df=get_list_d(tag_file)
    dfs.append(df)
    n=n-1
df_all=pd.concat(dfs,ignore_index=True)

input_path=input('Enter the path to your folder of files that contain information about tags:')
file_names=os.listdir(input_path)
images=[]
print("Reading pdf files and converting them to images...")
for file in file_names:
    images.extend(convert_from_path(input_path+'/'+file, poppler_path=poppler_path))

print("....")
pages=[]
for f in file_names:
    pdf=pdfplumber.open(input_path+'/'+f)
    pages.extend(pdf.pages)

all_images_wt=[]
i=0
print("Collecting snaps of only text...")
for page in pages:
    img=images[i]
    bboxes = [
            table.bbox
            for table in page.find_tables()
        ]
    h_page=page.height
    word_top=page.extract_words()[0]['top']
    ratio=(img.size[1]*1.0)/h_page
    crop_left=0
    crop_right=page.width*ratio
    crop_top=word_top*ratio
    crop_bottom=h_page*ratio
    any_table=0
    n_tables=len(bboxes)
    n=1
    for bbox in bboxes:
            any_table=1
            x0, top, x1, bottom = bbox
            crop_bottom=top*ratio
            if crop_top<crop_bottom:
                all_images_wt.append(img.crop((crop_left, crop_top, crop_right, crop_bottom)))
            crop_top=bottom*ratio
            if(n==n_tables):
                all_images_wt.append(img.crop((crop_left, crop_top, crop_right, h_page*ratio))) 
            n=n+1
    if(any_table==0):
        all_images_wt.append(img)
    i=i+1       

print("Reading text from images...")      
all_text=''
for img in all_images_wt:
    ocr_text = pytesseract.image_to_string(img)
    all_text=all_text+ocr_text


lines=re.split('\.|\.\n\n|\n\n',all_text)
new_text=[]
for line in lines:
    line = line.replace('\n',' ')
    line=re.sub('\s+',' ',line)
    if len(line.split(' ')) > 5 and "following" not in line:
        new_text.append(line)

print("Loading en_core_web_sm model...")  
nlp = spacy.load("en_core_web_sm")

des=[]
print("Extracting sentences that define tag...")
for tag in df_all["Tag"]:
    description=''
    for para in new_text :
        if tag in para:
            description=description+'.'+para
        elif tag[2:] in para:
            description=description+'.'+para
#         elif str(df2[(df2["Tag"]==tag)]["Description"]) in para:
#             description=description+'.'+para
    sent=description.split('.')
    tag_info=[]
    for s in sent:
        if s=='':
            continue
        tag_info.append(s.strip())

    para='. '.join(tag_info)
    re_inf=[]
    for s in para.split('.'):
        doc=nlp(s.strip())
        for token in doc:

            if (token.text==tag and ((token.dep_=="nsubj" and (token.head.tag_== "VBZ" or token.head.tag_ == "VBN" or token.head.tag_ == "VBP"))or (token.dep_=='appos' and (token.head.head.tag_ == "VBZ" or token.head.head.tag_ == "VBN" or token.head.head.tag_ == "VBP")))):
                re_inf.append(s.strip())
    des.append('.'.join(re_inf))

df_all["Add_info"]=des  
path_kpv=input("Enter the path to KPV files : ")
roots_kpv=[]
files_kpv=os.listdir(path_kpv)
for file in files_kpv:
    tree=et.parse(path_kpv+'/'+file)
    roots_kpv.append(tree.getroot())

lower_limit=[]
high_limit=[]
tag_name=[]
unit=[]
print("Reading limits of tags from KPV files...")
for i in range(0,8):
    root=roots_kpv[i]

    for elem in root.findall('Items/EvaluationItemBase/LowLimitsTrend/XmlRepresentation'):
          lower_limit.append(elem.text.split(',')[-1].split(':')[-1])
          tag_name.append(elem.text.split(',')[0].split('.')[0])
          unit.append(elem.text.split(',')[1])

    for elem in root.findall('Items/EvaluationItemBase/HighLimitsTrend/XmlRepresentation'):
          high_limit.append(elem.text.split(',')[-1].split(':')[-1])


df_kpv = pd.DataFrame(list(zip(tag_name, lower_limit,high_limit,unit)), columns=["Tag", "LowLimits", "HighLimits", "Unit"])
df_kpv = df_kpv.drop_duplicates(subset=['Tag'])
df_kpv=df_kpv.reset_index(drop=True)

df_new=pd.DataFrame(columns=['Tag','Info','LowLimit','HighLimit'])
for index,row in df_all.iterrows():
    ll=''
    hl=''
    tag=row["Tag"]
    if row["Add_info"]=="":
        info=row["Description"]
    else:
        info=row["Add_info"]
    arr=df_kpv[df_kpv['Tag'] == tag].index
    
    if(len(arr)):
      i=arr[0]
      ll=df_kpv.iloc[i]["LowLimits"]
      hl=df_kpv.iloc[i]["HighLimits"]
    row = {'Tag': tag,'Info':info,'LowLimit':ll,'HighLimit':hl}
    df_new = df_new.append(row, ignore_index = True)
print("Saving to tag_info.json file...")
df_new.to_json('tag_info.json',orient="records")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
database=myclient.knowledge_base
database.tag_info.drop()
collection=database.tag_info
with open('tag_info.json') as file:
    data_tag = json.load(file)

collection.insert_many(data_tag)
print("Data loaded to MongoDB server, mongodb://localhost:27017/")

    
