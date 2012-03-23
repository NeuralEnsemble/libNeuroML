# -*- coding: utf-8 -*-
"""

Support for mapping of NeuroML 2 models to Brian

Author: Padraig Gleeson

"""


from brian import *


import exceptions


def toBrianEqnsResetThresh(lemsDoc, comp, compType):
    print "----------------------"
    eqnString = ""
    reset= ""
    thresh = ""

    allParams = compType.getParameter()
    allConsts = compType.getConstant()

    parentCTName = compType.getExtends()
    paramKw = {}
    initialization = {}

    while parentCTName is not None:
        parentCT = getComponentType(lemsDoc, parentCTName)
        allParams += parentCT.getParameter()
        allConsts += parentCT.getConstant()
        parentCTName = parentCT.getExtends()

    stateVars = []
    for td in compType.getBehavior()[0].getTimeDerivative():
        tdsv = None
        for sv in compType.getBehavior()[0].getStateVariable():
            if sv.getName() == td.getVariable():
                tdsv = sv
                stateVars.append(sv.getName())
        eqnString += "d%s/dt = %s %s\n"%(td.getVariable(), getBrianExpression(td.getValue()), getBrianUnitString(tdsv.getDimension(), ": "))

    for dv in compType.getBehavior()[0].getDerivedVariable():
        val = dv.getValue()
        if val is None:
            val = "0 * %s %s" % (getBrianUnitString(dv.getDimension()),getBrianUnitString(dv.getDimension(), ": "))
        else:
            val = "%s %s"%(getBrianExpression(val),getBrianUnitString(dv.getDimension(), ": "))

        eqnString += "%s = %s\n"%(dv.getName(), val)


    for sv in compType.getBehavior()[0].getStateVariable():
        if sv.getName() not in stateVars:
            eqnString += "%s %s\n"%(sv.getName(), getBrianUnitString(sv.getDimension(), ": "))

    for const in allConsts:
        val = splitQuantity(const.getValue())
        paramKw[const.getName()] = eval("%s * %s"%(val[0], val[1])) if len(val[1])>0 else val[0]
        eqnString += "%s %s\n"%(const.getName(), getBrianUnitString(const.getDimension(), ": "))

    for param in allParams:
        val = splitQuantity(getattr(comp, param.getName()))
        paramKw[param.getName()] = eval("%s * %s"%(val[0], val[1])) if len(val[1])>0 else float(val[0])
        eqnString += "%s %s\n"%(param.getName(), getBrianUnitString(param.getDimension(), ": "))


    for oc in compType.getBehavior()[0].getOnCondition():
        if oc.getTest().startswith('v'):
            thresh = getBrianExpression(oc.getTest())
            #thresh = "v > -55 * mV"
            for sa in oc.getStateAssignment():
                if len(reset)>0: reset += "; "
                reset += "%s = %s"%(sa.getVariable(), getBrianExpression(sa.getValue()))
                #reset = "v = -70 * mV"

    os = compType.getBehavior()[0].getOnStart()
    for sa in os.getStateAssignment():
       initialization[sa.getVariable()] = getBrianExpression(sa.getValue())

    print "Converted component %s to:\n%s\n%s\n%s\n%s\n%s\n---------------------"%(str(comp), eqnString, reset, thresh, paramKw, initialization)

    eqns = Equations(eqnString)


    return eqns, StringReset(reset), thresh, paramKw, initialization

def getBrianUnitString(dim, prefix = ""):

    if dim == "none":
        return prefix+"1"
    elif dim == "voltage":
        return prefix+"mvolt"
    elif dim == "time":
        return prefix+"msecond"
    elif dim == "current":
        return prefix+"nA"
    elif dim == "capacitance":
        return prefix+"nF"
    elif dim == "conductance":
        return prefix+"uS"


def getBrianExpression(expr):
    expr2 = expr.replace(".gt.", ">")
    expr2 = expr2.replace(".ge.", ">=")
    expr2 = expr2.replace(".lt.", "<")
    expr2 = expr2.replace(".le.", "<=")
    expr2 = expr2.replace("^", "**")

    return expr2

def getComponentType(lemsDoc, compTypeName):

    for cc in lemsDoc.getComponentType():
        #print cc
        if cc.getName().capitalize() == compTypeName.capitalize():
            return cc
            #print cc.export(sys.stdout,0)
    return None

def splitQuantity(quantity):
    if " " in quantity:
        split = quantity.split(" ")
        return split[0], split[1]

    index = len(quantity)

    while index > 0 :
        pre = quantity[:index]
        try:
            float(pre)
            post = quantity[index:]
            #print "Translated %s into (%s,%s)" %(quantity, pre, post)
            return pre, post
        except exceptions.ValueError:
            index = index -1