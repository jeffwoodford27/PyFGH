import numpy as np
import scipy 

def AlphaCalc(D, counterarray, NValues):
    output = 0
    for a in reversed(range(D)):
            if(a+1 == D):
                output += counterarray[(a*2)+1]*1 
            else:
                output += counterarray[(a*2)+1]*(np.prod(NValues[:(D-1)-a]))
    return output

def AlphaAndBetaToCounter(alpha, beta, D, NValues):
    counter = scipy.zeros((D*2,1), int)
    #I am uncertain about the ability to modify the input parameters,
    #for now, I will create duplicate variables
    modalpha = alpha
    modbeta = beta
    #alpha first
    for x in range(D):
        #print("Current modalpha is: "+str(modalpha))
        if(not x+1 == D):
            npprod = np.prod(NValues[:D-(x+1)])
            
            manytimesalpha = modalpha // (npprod)
            modalpha -= manytimesalpha * (npprod)
            manytimesbeta = modbeta // (npprod)
            modbeta -= manytimesbeta * (npprod)
        else:
            manytimesalpha = modalpha // 1
            modalpha -= manytimesalpha
            manytimesbeta = modbeta // 1
            modbeta -= manytimesbeta
        #Set Values
        counter[(x*2)+1] = manytimesalpha
        counter[(x*2)] = manytimesbeta
            
        
    
    return counter

def BetaCalc(D, counterarray, NValues):
    output = 0
    for b in reversed(range(D)):
            if(b+1 == D):
                output += counterarray[(b*2)]*1   
            else:
                output += counterarray[(b*2)]*(np.prod(NValues[:(D-1)-b]))   
    return output

def DCAAdvance(D, counterArray, NValues):
    counterArray[(D*2)-1,0] += 1
    NValueC = 0
    jlcounter = 0
    for c in reversed(range(len(counterArray))):
        if (counterArray[c]>= NValues[NValueC]):
            counterArray[c] = 0
            counterArray[c-1] += 1
        jlcounter += 1
        if(jlcounter >= 2):
            jlcounter = 0
            NValueC +=1
    return counterArray
