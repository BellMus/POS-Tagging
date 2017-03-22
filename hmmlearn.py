import collections
import time
import sys
def main():
    # type: () -> object
    file1=open(sys.args[1],"r")
    file2=open("hmmmodel.txt1","w")
    dict2 = {}
    dict3 = {}
    dict4 = {}
    dict5 = {}
    count = 1
    count2 = 1
    count3 = 1
    lineCount = 0
    emissionprobdict = {}
    transitionprobdict = {}
    for line in file1:
        items=line.split()
        dict1 = collections.OrderedDict()
        pos = 0
        for words in items:
            tag=words[-2:].lower()
            word=words[:-3]
            dict1[word]=tag

            # Emission Probabilities

            # if word in dict1.keys():
            if tag in dict2.keys():
                if word in dict2[tag].keys():
                    dict2[tag][word] += 1
                else:
                    dict2[tag][word] = count
            else:
                dict2[tag] = {}
                dict2[tag][word] = count

            # End Of Emission Probabilities
            # if word not in dict5.keys():
            dict5[word]=tag
            if tag in dict4.keys():
                dict4[tag] += 1
            else:
                dict4[tag] = 1
        #print("Gone Past this point ")
        lineCount += 1
        # Transition Probabilities

        tags = list(dict1.values())
        length1=len(tags)
        tag0 = "q0"
        tag1 = tags[0]

        if tag0 in dict3.keys():
            if tag1 in dict3[tag0].keys():
                dict3[tag0][tag1]  += 1
            else:
                dict3[tag0][tag1] = count3
        else:
            dict3[tag0] = {}
            dict3[tag0][tag1] = count3
        for tag in tags:
            if (pos != length1-1):
                tag1=tags[pos]
                pos += 1
                tag2 = tags[pos]
                if tag1 in dict3.keys():
                    if tag2 in dict3[tag1].keys():
                        dict3[tag1][tag2]  += 1
                    else:
                        dict3[tag1][tag2] = count2
                else:
                    dict3[tag1] = {}
                    dict3[tag1][tag2] = count2
        # End Of Transition Probabilities

    #print(str(lineCount) + "          Just before calculating emission probabilities")
    # Calculating Emission Probabilities

    for word in dict5.keys():
        wordcount=0
        for tag in dict2.keys():
            if word in dict2[tag].keys():
                wordcount+=dict2[tag][word]
        for tag in dict2.keys():
            den=wordcount
            if tag in emissionprobdict.keys():
                if word in dict2[tag].keys():
                    num=dict2[tag][word]
                else:
                    num=1
                emissionprobdict[tag][word]=float(num)/float(den)
            else:
                emissionprobdict[tag]={}
                if word in dict2[tag].keys():
                    num=dict2[tag][word]
                else:
                    num=1
                emissionprobdict[tag][word] = float(num) / float(den)
    # # file2.write("Emission probabilities:")
    # # file2.write(' ')
    # file2.write(str(emissionprobdict))

    # Calculating Transition Probabilities

    tag0="q0"
    if tag0 in dict3.keys():
        transitionprobdict[tag0] = {}
        den = sum(dict3[tag0].values()) + len(dict4.keys())
        for tags in dict3.keys():
            if tags!="q0":
                if tags in dict3[tag0].keys():
                    num=dict3[tag0][tags]+1
                else:
                    num=1
            else:
                continue
            transitionprobdict[tag0][tags]=float(num)/float(den)
    for tag1 in dict3.keys():
        if tag1!="q0":
            transitionprobdict[tag1]={}
            den = sum(dict3[tag1].values()) + len(dict4.keys())
            for tag2 in dict3.keys():
                if tag2!="q0":
                    if tag2 in dict3[tag1].keys():
                        num=dict3[tag1][tag2]+1
                    else:
                        num=1
                else:
                    continue
                transitionprobdict[tag1][tag2]=float(num)/float(den)


    file2.write('\n')
    # file2.write("Transition probabilities:")
    # file2.write(' ')
    file2.write(str(transitionprobdict))

main()
