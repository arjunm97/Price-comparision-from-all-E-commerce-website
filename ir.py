# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 00:43:30 2019

@author: Arjun
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import tkinter as tk

###getting input GUI########

def get_class():  
    print (var.get())

def get_entry(): 
    print (ent.get())


root = tk.Tk()

var = tk.StringVar()#word

ent = tk.Entry(root,textvariable = var)

btn1 = tk.Button(root, text="Enter details", command=get_class)

ent.pack()

btn1.pack()

root.mainloop()
###### GUI END#########

key=var.get()

#### Getting products from flipakrt

#URL="https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
URL_flip="https://www.flipkart.com/search?q="+key+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
r_flip = requests.get(URL_flip) 

c_flip=r_flip.content
soup_f=BeautifulSoup(c_flip,"html.parser")

all=soup_f.find_all("div",{"class":"_1UoZlX"})
print(len(all))
#print(all)
#print(all[0].find("div",{"class":"_1vC4OE _2rQ-NK"}).text)

###Getting info
l=[]
com_f=[]
for item in all:
    d={}
    com={}
    #name
    print(item.find("div",{"class":"_3wU53n"}).text)
    d["Name"]=item.find("div",{"class":"_3wU53n"}).text
    com["Name"]=item.find("div",{"class":"_3wU53n"}).text
    #price
    print(item.find("div",{"class":"_1vC4OE _2rQ-NK"}).text)
    d["Price"]=item.find("div",{"class":"_1vC4OE _2rQ-NK"}).text.replace("₹","").replace(" ","")
    com["Price"]=item.find("div",{"class":"_1vC4OE _2rQ-NK"}).text.replace("₹","").replace(" ","")
    #rating
    print(item.find("div",{"class":"hGSR34"}).text)
    d["Rating"]=item.find("div",{"class":"hGSR34"}).text
    com["Rating"]=item.find("div",{"class":"hGSR34"}).text
    #features
    print(item.find_all("li",{"class":"tVe95H"})[0].text)
    d["feature1"]=item.find_all("li",{"class":"tVe95H"})[0].text
    print(item.find_all("li",{"class":"tVe95H"})[1].text)
    d["feature2"]=item.find_all("li",{"class":"tVe95H"})[1].text
    print(item.find_all("li",{"class":"tVe95H"})[2].text)
    d["feature3"]=item.find_all("li",{"class":"tVe95H"})[2].text
    print(item.find_all("li",{"class":"tVe95H"})[3].text)
    d["feature4"]=item.find_all("li",{"class":"tVe95H"})[3].text
    try:
        print(item.find_all("li",{"class":"tVe95H"})[4].text)
        d["feature5"]=item.find_all("li",{"class":"tVe95H"})[4].text
    except:pass
    l.append(d)
    com_f.append(com)
    print()
   

###Getting products from Snapdeal


URL_snap="https://www.snapdeal.com/search?clickSrc=top_searches&keyword="+key+"&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy"
r_s= requests.get(URL_snap) 

c_s=r_s.content
soup_s=BeautifulSoup(c_s,"html.parser")

all_s=soup_s.find_all("div",{"class":"product-tuple-description "})


#print(len(all_s))



i=[]

for item in all_s:
    d={}
    d["Name"]=item.find("p",{"class":"product-title"}).text
    d["Price"]=item.find("span",{"class":"lfloat product-price"}).text.replace("Rs","").replace(".","")
    try:
        d["Rating"]=item.find("p",{"class":"product-rating-count"}).text.replace("(","").replace(")","")
    except:
        d["Rating"]=0
        
    i.append(d)
    
#print(i)






#storing the data into a dataframe


df_f=pd.DataFrame(com_f)
df_s=pd.DataFrame(i)
df_final = pd.concat([df_f, df_s], ignore_index=True)

df_final.to_csv("Output.csv")