def AlphaCalc(D, counterarray, NValues):
    output = 0
    for a in reversed(range(D)):
            if(a+1 == D):
                output += counterarray[(a*2)+1]*1 
            else:
                output += counterarray[(a*2)+1]*(np.prod(NValues[:(D-1)-a]))
    return output

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
