import os
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .MyFunction import *
import pickle
import datetime
from django.forms.models import model_to_dict
from django.contrib.auth.forms import UserCreationForm
from multiprocessing import Process
from django.db.models.aggregates import Count

def index(request):
    return render(request,'login.html')

def login(request):
    User = request.POST.get('User')
    Pass = request.POST.get('Pass')
    c1 = UserInfo.objects.filter(User=User, Pass=Pass).count()
    if c1:
        UID = UserInfo.objects.filter(User=User, Pass=Pass)[0].UID
        User = UserInfo.objects.filter(UID=UID)[0].User
        authority = UserInfo.objects.filter(UID=UID)[0].authority
        if authority == '1':
            return render(request, 'main.html', locals())
        else:
            return render(request, 'login.html', {'script': "alert", 'wrong': '管理员未授权请联系管理员', 'user': User})
    else:
        return render(request, 'login.html', locals())

# def distribute(request):


def disrtribute(request):

    return render(request,'main.html', locals())

def slump(request):

    return render(request,'slump.html', locals())

def register(request):

    return render(request,'register.html', locals())

def saveregister(request):
    User=request.POST.get('User')
    Pass=request.POST.get('Pass')
    Mail=request.POST.get('Mail')
    c = UserInfo.objects.filter(User=User).count()
    if c == 0:
        UserInfo(User=User,Pass=Pass,Mail=Mail,authority='1').save()
    return render(request,'login.html', {'script':"alert",'wrong':'注册成功','user':User})
                  
def strength(request):
    ifcreat = request.POST.get('ifcreat')
    FormulaID = request.POST.get('FormulaID')
    delete = request.POST.get('delete')
    if ifcreat:
        creatform = request.POST.getlist('creatform')
        cement,GBFS,FA,water,FAggregate,CAggregate,Superplasticizer=creatform
        if FormulaInfo.objects.filter(cement=cement, GBFS=GBFS, FA=FA,water=water,FAggregate=FAggregate,CAggregate=CAggregate,Superplasticizer=Superplasticizer).count() == 0:
            newFormula=FormulaInfo(cement=cement, GBFS=GBFS, FA=FA,water=water,FAggregate=FAggregate,CAggregate=CAggregate,Superplasticizer=Superplasticizer)
            newFormula.save()
            FormulaID=newFormula.FormulaID
            pr=[]
            with open('E:\\05 cangku\CarbonWeb\carbonweb\carbonwebapp\static\model\concreteEreg.pickle', 'rb') as fr:
                model1 = pickle.load(fr)
            for age in range(0, 366):
                # Age_Water, Age_Cement, Coarse_Fine, youngCementComponent, youngSuperplasticizerComponent, clippedAge, clippedWater, hasBlastFurnaceSlag, hasFlyAshComponent, hasSuperplasticizerComponent=modelparameter(cement,GBFS,FA,water,Superplasticizer,CAggregate,FAggregate,age)
                # XX=[cement,GBFS,FA,water,FAggregate,CAggregate,Superplasticizer,age,Age_Water, Age_Cement, Coarse_Fine, youngCementComponent, youngSuperplasticizerComponent, clippedAge, clippedWater, hasBlastFurnaceSlag, hasFlyAshComponent, hasSuperplasticizerComponent]
                XX = modelparameter(cement, GBFS, FA, water, Superplasticizer, CAggregate, FAggregate, age)
                pr.append(XX)
            ppre=model1.predict(pr)
            for index,p in enumerate(ppre):
                # if StrengthInfo.objects.filter(FormulaID=FormulaID,Strength=round(p,2)).count() == 0:
                StrengthInfo(FormulaID=FormulaID,age=index,Strength=round(p,2)).save()

    Formulas=FormulaInfo.objects.filter()
    Formula=[]
    for f in Formulas:
        dic={}
        dic['FormulaID']=f.FormulaID
        dic['cement']=f.cement
        dic['GBFS']=f.GBFS
        dic['FA']=f.FA
        dic['water']=f.water
        dic['FAggregate']=f.FAggregate
        dic['CAggregate']=f.CAggregate
        dic['Superplasticizer']=f.Superplasticizer
        Formula.append(dic)
    # agestrength=[]
    if FormulaID:
        FormulaID1=FormulaID
        if delete:
            StrengthInfo.objects.filter(FormulaID=FormulaID1).delete()
            FormulaInfo.objects.filter(FormulaID=FormulaID1).delete()
        ages=[]
        Strengths=[]
        for agestr in StrengthInfo.objects.filter(FormulaID=FormulaID):
            ages.append(agestr.age)
            Strengths.append(agestr.Strength)
        agestrength={}
        agestrength['title']={'left': 'center','text': '%s 号配方'%(FormulaID)}
        agestrength['tooltip']= {'trigger': 'axis','formatter': '第{b}天抗压强度: {c}MPa', }
        agestrength['grid'] = {'left':'5%','bottom': '5%'}
        agestrength['xAxis']={'type': 'category','name': "day", 'data': ages}
        agestrength['yAxis']={'type': 'value','name': "MPa"}
        agestrength['series']=[{'type': 'line','data': Strengths,'name': "抗压强度"}]
    return render(request,'strength.html', locals())

def carbon(request):
    ifcreat = request.POST.get('ifcreat')
    OptimizeID = request.POST.get('OptimizeID')
    delete = request.POST.get('delete')
    factorlistcement=findcarbon(1)
    factorlistGBFS=findcarbon(2)
    factorlistFA =findcarbon(2)
    factorlistwater=findcarbon(4)
    factorlistFAggregate=findcarbon(3)
    factorlistCAggregate=findcarbon(3)
    factorlistSuperplasticizer=findcarbon(5)
    if ifcreat:
        creatform = request.POST.getlist('creatform')
        # print(creatform)
        targetDay,targetStrength,cementPrice,GBFSPrice,FAPrice,waterPrice,FAggregatePrice,CAggregatePrice,SuperplasticizerPrice,carboncement,carbonGBFS,carbonFA,carbonwater,carbonFAggregate,carbonCAggregate,carbonSuperplasticizer=creatform
        targetslump=0#塌落度，没做
        FormulaIDs=findFormulaID(targetDay,targetStrength)
        # Optimize=OptimizeInfo(TargetDay=targetDay,TargetStrength=targetStrength,TargetSlump=targetslump)
        # if OptimizeInfo.objects.filter(TargetDay=targetDay,TargetStrength=targetStrength,TargetSlump=targetslump).count() == 0:
        Optimize=OptimizeInfo(TargetDay=targetDay,TargetStrength=targetStrength,TargetSlump=targetslump)
        Optimize.save()
        OptimizeID=Optimize.OptimizeID
        date = datetime.date.today()
        PriceInfo(OptimizeID=OptimizeID,time =date  ,cement=cementPrice ,GBFS=GBFSPrice ,FA=FAPrice ,water=waterPrice ,FAggregate=FAggregatePrice ,CAggregate=CAggregatePrice,Superplasticizer=SuperplasticizerPrice).save()
        carbonInfo(OptimizeID=OptimizeID,time = date ,cement=carboncement ,GBFS=carbonGBFS ,FA=carbonFA ,water=carbonwater ,FAggregate= carbonFAggregate,CAggregate=carbonCAggregate,Superplasticizer=carbonSuperplasticizer).save()
        for id in FormulaIDs:
            FormulaID=id[0]
            price=round(calculatePrice(id[0],cementPrice,GBFSPrice,FAPrice,waterPrice,FAggregatePrice,CAggregatePrice,SuperplasticizerPrice),2)
            carbon=round(carboncalculate(id[0],carboncement,carbonGBFS,carbonFA,carbonwater,carbonFAggregate,carbonCAggregate,carbonSuperplasticizer),2)
            if FormulaCompareInfo.objects.filter(OptimizeID=OptimizeID,FormulaID=FormulaID,FormulaPrice=price,carbonFormula=carbon).count() == 0:
                FormulaCompareInfo(OptimizeID=OptimizeID,FormulaID=FormulaID,FormulaPrice=price,carbonFormula=carbon).save()
        bestpriceFormulaID,bestprice,carbon=findbestprice(OptimizeID)
        bestcarbonFormulaID,bestcarbon,cost=findbestcarbon(OptimizeID)
        OptimizeInfo.objects.filter(OptimizeID=OptimizeID).update(bestCost=bestprice, bestCarbon=bestcarbon,bestCostFormulaID=bestpriceFormulaID,bestCarbonFormulaID=bestcarbonFormulaID)
    Optimizess = OptimizeInfo.objects.filter()
    Optimizes = []
    for o in Optimizess:
        dic = {}
        dic['OptimizeID'] = o.OptimizeID
        dic['TargetDay'] = o.TargetDay
        dic['TargetStrength'] = o.TargetStrength
        dic['TargetSlump'] = o.TargetSlump
        dic['bestCost'] = o.bestCost
        dic['bestCarbon'] = o.bestCarbon
        dic['bestCostFormulaID'] = o.bestCostFormulaID
        dic['bestCarbonFormulaID'] = o.bestCarbonFormulaID
        Optimizes.append(dic)
    if OptimizeID:
        OptimizeID1 = OptimizeID
        if delete:
            FormulaCompareInfo.objects.filter(OptimizeID=OptimizeID1).delete()
            OptimizeInfo.objects.filter(OptimizeID=OptimizeID1).delete()
        costscarbons=[]
        for cc in FormulaCompareInfo.objects.filter(OptimizeID=OptimizeID1).order_by('FormulaPrice'):
            costscarbons.append([cc.FormulaPrice,cc.carbonFormula])
        # for c in costscarbons:
        bestpriceFormulaID,bestprice,carbon=findbestprice(OptimizeID1)
        bestcarbonFormulaID,bestcarbon,cost=findbestcarbon(OptimizeID1)
        costCarbon={}
        costCarbon['title']={'left': 'center','text': '%s 号优化方案'%(OptimizeID1)}
        costCarbon['tooltip']= {'trigger': 'axis','formatter': '{c}', }
        # costCarbon['tooltip']= {'position': 'top','trigger': 'axis'}
        costCarbon['grid'] = {'left':'5%','right':'15%','bottom': '5%'}
        costCarbon['xAxis']={'scale': 'true','name': "kgCO2e/m3" }
        costCarbon['yAxis']={'scale': 'true','name': "元/m3"}
        costCarbon['series']=[{'type': 'effectScatter','symbolSize': '20','data': [[bestprice ,carbon],[cost, bestcarbon]]},{'type': 'scatter','data': costscarbons }]
        Best=findbestformula(OptimizeID1)
        # print(Best)
        PricePrice=findprice(OptimizeID1)
        # Best1=[]
        # Best1['FormulaID']=bestpriceFormulaID
    # print(factorlist1)
    return render(request,'carbon.html', locals())

def factor(request):
    # pageval = request.POST.get('pageval')
    factorlistcement=findcarbon(1)
    factorlistGBFS=findcarbon(2)
    factorlistFA =findcarbon(2)
    factorlistwater=findcarbon(4)
    factorlistFAggregate=findcarbon(3)
    factorlistCAggregate=findcarbon(3)
    factorlistSuperplasticizer=findcarbon(5)
    factorlistTransport=findcarbon(6)
    factorlistenergy=findcarbon(7)
    factorlist=[]
    factorClasslist = []
    factors=FactorInfo.objects.filter()
    factorClass=FactorCalssInfo.objects.filter()
    for fc in factorClass:
        dic = {}
        dic['text'] = fc.FactorCalssName
        dic['value'] = fc.FactorCalssName
        factorClasslist.append(dic)
    for f in factors:
        dic1={}
        dic1['FactorName']=f.FactorName
        dic1['FactorCalss']=findfactor(f.FactorCalssID)
        dic1['FactorNum']=f.FactorNum
        dic1['FactorSource']=f.FactorSource
        dic1['FactorUnit']=f.FactorUnit
        factorlist.append(dic1)

    return render(request,'factor.html', locals())
# Create your views here.
