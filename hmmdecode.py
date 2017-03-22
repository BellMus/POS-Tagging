import ast
import collections
import math
import sys
import time
def main():
    file1 = open(sys.args[1], "r")
    file2 = open("hmmoutput.txt", "w")
    file3 = open("hmmmodel.txt", "r")

    probdict={}
    backtrackdict = {}
    line=file3.readlines()
    emissionprobdict=ast.literal_eval(line[0])
    transitionprobdict=ast.literal_eval(line[1])

    def hmm(emissionprobdict,transitionprobdict,words):
        length = words.__len__()
        word1 = words[0]
        tag0 = "q0"
        for tag in emissionprobdict.keys():
            if word1 in emissionprobdict[tag].keys():
                emissionprobval=math.log(emissionprobdict[tag][word1])
                if tag in transitionprobdict[tag0].keys():
                    transmissionprobval=math.log(transitionprobdict[tag0][tag])
                totalval=(emissionprobval+transmissionprobval)
                probdict[tag]=[]
                probdict[tag] = [totalval]
                backtrackdict[tag] = [tag0]
            else:
                probdict[tag]=[]
                probdict[tag]=[0]
                backtrackdict[tag]=[tag0]
        for i in range(1,length):
            for tag in emissionprobdict.keys():
                temp={}
                for tags in transitionprobdict.keys():
                    transmissionprobval1 = 0
                    if words[i] in emissionprobdict[tag].keys():
                        emissionprobval1 = math.log(emissionprobdict[tag][words[i]])
                    else:
                        emissionprobval1 = 0
                    if tags != "q0":
                        if tag in transitionprobdict[tags].keys():
                            transmissionprobval1 = math.log(transitionprobdict[tags][tag])
                    else:
                        continue
                    totalval1=(emissionprobval1+transmissionprobval1)
                    if tags not in temp.keys():
                        temp[tags]={}
                        # if probdict[tags][i-1]==0:
                        #     temp[tags]=0
                        # else:
                        temp[tags]=totalval1+(probdict[tags][i-1])
                v = list(temp.values())
                k = list(temp.keys())
                maxprob = maximum(v)
                maxtag=k[v.index(maxprob)]
                probdict[tag].append(maxprob)
                if maxprob==0:
                    backtrackdict[tag].append("NoPath")
                else:
                    for key,val in temp.items():
                        if maxprob==val:
                            k=key
                            break
                    backtrackdict[tag].append(k)

        temp={}
        for q in probdict.keys():
            temp[q]=probdict[q][length-1]
        maxprob=maximum(temp.values())
        if maxprob==0:
            return "No sequence found"
        else:
            for key,val in temp.items():
                if maxprob==val:
                    k=key
                    break
        tag=k
        path=[tag]
        t=length-1
        while tag!='q0' and t>=0:
            if backtrackdict[tag][t]=="NoPath":
                return "No sequence found"
            else:
                tag=backtrackdict[tag][t]
                path.append(tag)
            t-=1
        return path

    def maximum(values):
        for n,i in enumerate(values):
            if i==0:
                values[n]=-sys.maxint
        return(max(values))

    for line in file1:
        words=line.split()
        path=hmm(emissionprobdict,transitionprobdict,words)
        i=path.__len__()-2
        for word in words:
            file2.write(word+"/"+path[i]+" ")
            i-=1
        file2.write("\n")

main()
