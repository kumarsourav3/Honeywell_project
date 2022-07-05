import pandas as pd
import xml.etree.ElementTree as et
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from numpy import asarray
from numpy import savez_compressed

tree=et.parse("Distillation.xml")
root=tree.getroot()

cause={}
tag={}
n_tag=[]
n_cause=[]
cause_index_map={}

i=0
for x in root.findall("Causes/CauseDTO"):
    id_=x.find("Id")
    desc=x.find("Description")
    cause[id_.text]=desc.text
    n_cause.append(desc.text)
    cause_index_map[desc.text]=i
    i=i+1
savez_compressed('cause_index_map.npz',cause_index_map)
for x in root.findall('ProcessElements/ProcessElementDTO'):
    id_=x.find("Id")
    desc=x.find("Point")
    n_tag.append(desc.text)
    tag[id_.text]=desc.text

df=pd.DataFrame(columns=n_tag)
df.insert(0, 'Causes', n_cause)
df.set_index('Causes', inplace=True)

for rel in root.findall('Relations/CauseEffectRelationDTO'):
    ri=rel.find("Cause_Id").text
    ci=rel.find("ProcessElement_Id").text
    relation=rel.find("Relation").text
    df.at[cause[ri],tag[ci]]=int(relation)

df=df.fillna(0)

encoder = OneHotEncoder()
n_runs=[]
for column in df.columns:
    dic={}
    keys=df[column].unique().tolist()
    tag=column
    dic["tag"]=tag
    keys.sort()
    effects=[-2,-1,0,1,2]
    tag_matrix=pd.DataFrame(columns=effects)
    encoder_df = pd.DataFrame(encoder.fit_transform(df[[column]]).toarray(),columns=keys)
    for column in encoder_df.columns:
        tag_matrix[column]=encoder_df[column]
    # encoder_df
    tag_matrix.fillna(0)
    arr=tag_matrix.to_numpy()
    count = np.count_nonzero(arr == 1, axis=0).reshape((5,1)) ##along column
    effect=-2
    for i in count:
        if(i):
            dic[effect]=1
        else:
            dic[effect]=0
        effect=effect+1
        
    n_runs.append(dic)
    arr = np.divide(np.transpose(arr), count, out=np.zeros_like(np.transpose(arr)), where=count!=0)
    arr=np.transpose(arr)
    savez_compressed('p_matrices/'+str(tag)+'.npz', arr)
savez_compressed('params.npz',n_runs)
    
print("Model has been initialised with the base probability matrices.")