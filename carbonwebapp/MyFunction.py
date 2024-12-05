from .models import *
import pymysql
from django.shortcuts import render,redirect,HttpResponse
import json
import os
import numpy as np
import math
import cv2
import shutil
import csv
import hashlib
from xml.dom import minidom
import xml.etree.ElementTree as ET
import random
import datetime
import xml.dom.minidom
from time import strftime
import pandas as pd

def link():
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',database="carbonweb")
    return conn

# --------------------

# 增
def add_data(sql, *args):
    conn = link()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        conn.commit()
        print('Insert success')
        return True
    except Exception as e:
        print('Insert error:', e)
        return False
    finally:
        conn.close()


# 删
def delete_data(sql, *args):
    conn = link()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        conn.commit()
        print('Delete success')
        return True
    except Exception as e:
        print('Delete error:', e)
        return False
    finally:
        conn.close()


# 改
def update_data(sql, *args):
    conn = link()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        conn.commit()
        print('Update success')
        return True
    except Exception as e:
        print('Update error:', e)
        return False
    finally:
        conn.close()


# 查
def find_data(sql, *args):
    conn = link()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        data = cursor.fetchall()
        # print('Find success')
        return data
    except Exception as e:
        print('Find error:', e)
        return False
    finally:
        conn.close()
# --------------------

def findfactor(FactorCalssID):
    sql = 'select FactorCalssName FROM carbonwebapp_FactorCalssInfo WHERE `FactorCalssID`=(%s)'
    return find_data(sql,FactorCalssID)[0][0]

def findfactors(FactorCalssID):
    sql = 'select * FROM carbonwebapp_FactorInfo WHERE `FactorCalssID`=(%s)'
    return find_data(sql,FactorCalssID)

def findFormulaage(FormulaID):
    sql = 'select age FROM carbonwebapp_StrengthInfo WHERE `FormulaID`=(%s)'
    return find_data(sql,FormulaID)

def findFormulaStrength(FormulaID):
    sql = 'select strength FROM carbonwebapp_StrengthInfo WHERE `FormulaID`=(%s)'
    return find_data(sql,FormulaID)

def findcarbon1(min,max):
    factorlist=[]
    factorClass=FactorCalssInfo.objects.filter(FactorCalssID__range =(min,max))
    for fc in factorClass:
        dic = {}
        dic['value'] = fc.FactorCalssID
        dic['label'] = fc.FactorCalssName
        factors = FactorInfo.objects.filter(FactorCalssID=fc.FactorCalssID)
        ff=[]
        for f in factors:
            dic1={}
            dic1['label']=f.FactorName
            dic1['value']=f.FactorID
            dic1['FactorNum'] = f.FactorNum
            dic1['FactorSource']=f.FactorSource
            dic1['FactorUnit']=f.FactorUnit
            ff.append(dic1)
        dic['children']=ff
        factorlist.append(dic)
    return factorlist

def findcarbon(classid):
    factorlist=[]
    factor=FactorInfo.objects.filter(FactorCalssID =classid)
    for fc in factor:
        dic={}
        dic['value'] = fc.FactorNum
        dic['label'] = fc.FactorName
        factorlist.append(dic)
    return factorlist

def findprice(optimizeID):
    pricelist=[]
    labellist=['时间','水泥','高炉渣','飞灰','水','细骨料','粗骨料','减水剂']
    sql='select * FROM carbonwebapp_PriceInfo WHERE `optimizeID`=(%s) '
    price=find_data(sql,  optimizeID)[0]
    for i in range(0,8):
        # print(labellist[i])
        # print(labellist[i])
        dic = {}
        dic['value'] = price[i+1]
        dic['label'] = labellist[i]
        pricelist.append(dic)
    return pricelist

def findFormulaID(targetDay,targetStrength):
    sql = 'select FormulaID FROM carbonwebapp_StrengthInfo WHERE `age`=(%s) AND `Strength`>=(%s)'
    return find_data(sql, (targetDay,targetStrength))

def findFormula(FormulaID):
    sql = 'select * FROM carbonwebapp_FormulaInfo WHERE `FormulaID`=(%s) '
    return find_data(sql,FormulaID )

def calculatePrice(FormulaID,cementPrice,GBFSPrice,FAPrice,waterPrice,FAggregatePrice,CAggregatePrice,SuperplasticizerPrice):
    cementPrice=float(cementPrice)
    GBFSPrice=float(GBFSPrice)
    FAPrice=float(FAPrice)
    waterPrice=float(waterPrice)
    FAggregatePrice=float(FAggregatePrice)
    CAggregatePrice=float(CAggregatePrice)
    SuperplasticizerPrice=float(SuperplasticizerPrice)
    Formula=findFormula(FormulaID)[0]
    FormulaID,cement,GBFS,FA,water,FAggregate,CAggregate,Superplasticizer=Formula
    price=(cement*cementPrice+GBFS*GBFSPrice+FA*FAPrice+water*waterPrice+FAggregate*FAggregatePrice+CAggregate*CAggregatePrice+Superplasticizer*SuperplasticizerPrice)*0.001
    return price

def carboncalculate(FormulaID,carboncement,carbonGBFS,carbonFA,carbonwater,carbonFAggregate,carbonCAggregate,carbonSuperplasticizer):
    carboncement=float(carboncement)
    carbonGBFS=float(carbonGBFS)
    carbonFA=float(carbonFA)
    carbonwater=float(carbonwater)
    carbonFAggregate=float(carbonFAggregate)
    carbonCAggregate=float(carbonCAggregate)
    carbonSuperplasticizer=float(carbonSuperplasticizer)
    Formula=findFormula(FormulaID)[0]
    FormulaID,cement,GBFS,FA,water,FAggregate,CAggregate,Superplasticizer=Formula
    carbon=(cement*carboncement+GBFS*carbonGBFS+FA*carbonFA+water*carbonwater+FAggregate*carbonFAggregate+CAggregate*carbonCAggregate+Superplasticizer*carbonSuperplasticizer)*0.001
    return carbon

def findbestprice(optimizeID):
    sql1 = 'select min(FormulaPrice) FROM carbonwebapp_FormulaCompareInfo WHERE `optimizeID`=(%s) '
    bestcost=find_data(sql1,optimizeID )[0][0]
    sql2 = 'select * FROM carbonwebapp_FormulaCompareInfo WHERE `optimizeID`=(%s) and `FormulaPrice`=(%s)'
    data=find_data(sql2,(optimizeID,bestcost))
    # print(data)
    if data:
        FormulaID=data[0][2]
        carbon=data[0][4]
        return FormulaID,bestcost,carbon
    else:
        return False,False,False

def findbestcarbon(optimizeID):
    sql1 = 'select min(carbonFormula) FROM carbonwebapp_FormulaCompareInfo WHERE `optimizeID`=(%s) '
    bestcarbon=find_data(sql1,optimizeID )[0][0]
    sql2 = 'select * FROM carbonwebapp_FormulaCompareInfo WHERE `optimizeID`=(%s) and `carbonFormula`=(%s)'
    data=find_data(sql2,(optimizeID,bestcarbon))
    if data:
        FormulaID=data[0][2]
        cost=data[0][3]
        return FormulaID,bestcarbon,cost
    else:
        return False,False,False

def findbestformula(optimizeID):
    bestpriceFormulaID, bestcost, carbon=findbestprice(optimizeID)
    bestcarbonFormulaID, bestcarbon, cost=findbestcarbon(optimizeID)
    if bestpriceFormulaID:
        bestpriceFormula = findFormula(bestpriceFormulaID)[0]
        dic1={}
        dic1['FormulaID']=bestpriceFormulaID
        dic1['cost']=bestcost
        dic1['carbon']=carbon
        dic1['cement'] = bestpriceFormula[1]
        dic1['GBFS'] =bestpriceFormula[2]
        dic1['FA'] =bestpriceFormula[3]
        dic1['water'] =bestpriceFormula[4]
        dic1['FAggregate'] =bestpriceFormula[5]
        dic1['CAggregate'] =bestpriceFormula[6]
        dic1['Superplasticizer'] =bestpriceFormula[7]

        bestcarbonFormula = findFormula(bestcarbonFormulaID)[0]
        dic2={}
        dic2['FormulaID']=bestcarbonFormulaID
        dic2['cost']=cost
        dic2['carbon']=bestcarbon
        dic2['cement'] = bestcarbonFormula[1]
        dic2['GBFS'] =bestcarbonFormula[2]
        dic2['FA'] =bestcarbonFormula[3]
        dic2['water'] =bestcarbonFormula[4]
        dic2['FAggregate'] =bestcarbonFormula[5]
        dic2['CAggregate'] =bestcarbonFormula[6]
        dic2['Superplasticizer'] =bestcarbonFormula[7]
        return [dic1,dic2]
    else:
        return False


def modelparameter(CementComponent,bfs,fa,water,sp,cagg,fagg,age):
    CementComponent=float(CementComponent)
    bfs=float(bfs)
    fa=float(fa)
    water=float(water)
    sp=float(sp)
    cagg=float(cagg)
    fagg=float(fagg)
    age=float(age)
    Age_Water=round(age/water,2)
    Age_Cement=round(age/CementComponent,2)
    Coarse_Fine=round(cagg/fagg,2)
    youngCementComponent=round(CementComponent*(age<40),2)
    youngSuperplasticizerComponent=round(sp*(age<10),2)
    clippedAge=np.clip([age],None, 40)
    clippedWater=np.clip([water],195, None)
    hasBlastFurnaceSlag=(bfs != 0)
    hasFlyAshComponent=(fa != 0)
    hasSuperplasticizerComponent=(sp != 0)
    # pr=pd.DataFrame(data={'CementComponent': [CementComponent],'BlastFurnaceSlag': [bfs],'FlyAshComponent':[fa],'WaterComponent':[water],'SuperplasticizerComponent':[sp],'CoarseAggregateComponent':[cagg],'fagg':[fagg],'FineAggregateComponent':[age],'Age_Water':[Age_Water],'Age_Cement':[Age_Cement],'Coarse_Fine':[Coarse_Fine],'youngCementComponent':[youngCementComponent],'youngSuperplasticizerComponent':[youngSuperplasticizerComponent],'clippedAge':[clippedAge[0]],'clippedWater':[clippedWater[0]],'hasBlastFurnaceSlag':[hasBlastFurnaceSlag],'hasFlyAshComponent':[hasFlyAshComponent],'hasSuperplasticizerComponent':[hasSuperplasticizerComponent]})
    return [CementComponent,bfs,fa,water,sp,cagg,fagg,age,Age_Water,Age_Cement,Coarse_Fine,youngCementComponent,youngSuperplasticizerComponent,clippedAge[0],clippedWater[0],hasBlastFurnaceSlag,hasFlyAshComponent,hasSuperplasticizerComponent]
    # return pr


# print(findbestprice(39))