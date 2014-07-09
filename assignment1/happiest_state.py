import sys
import json
import string

def sentimentdict(fp):
    fo = open(fp)
    scores = {}
    for line in  fo:
        term , score = line.split("\t")
        scores[term]=int(score)
    fo.close()
    return scores


def getStateFromPlace(var):
    country_code = var["country_code"].encode('utf-8')
    if country_code=="us" or country_code=="US":
        full_name=var["full_name"]
        l=len(full_name)
        return full_name[l-2:l]
    else:
        return None

def getStateFromUser(var):
    if "location" in var:
        return var["location"].encode('utf-8')
    else:
        return None
    

def getLocation(tDict):
    #check for text first, if no text return None
    if not("text" in tDict):
        return None

    if "place" in tDict and tDict["place"]!=None:
        #use place
        return getStateFromPlace(tDict["place"])
    else:
        return None
        #if "user" in tDict:
            #use user home place
            #return getStateFromUser(tDict["user"])
        #else:
            #return None
    

def getTweetLocation(fp):
    fo = open(fp)
    #print str(len(fo.readlines()))
    deleted=0
    tweetsLocation={}
    for line in fo:
        tweetObjDict=json.loads(line)
        location=getLocation(tweetObjDict)
	if location!=None:
            text=tweetObjDict["text"].encode('utf-8')
	    if location in tweetsLocation:
                #update the list of tweets for this location
                temp=tweetsLocation[location]
                temp.append(text)
                tweetsLocation.update({location:temp})
            else:
                #add a new location:[tweetText] to the tweetsLocation dic
                temp=[]
                temp.append(text)
                tweetsLocation[location]=temp
	else:
 	    deleted = deleted +1
    #print len(tweets)
    #print deleted
    return tweetsLocation



def calcAverageSentiment(tweets,dict):
    for text in tweets:
	tokens = text.split()
	sent_score=0
        count=0
	for token in tokens:
            cleanToken=token.lstrip(string.punctuation)
            cleanToken=cleanToken.rstrip(string.punctuation)
            cleanToken=cleanToken.lower()
            if cleanToken in dict:
                sent_score=sent_score+dict[cleanToken]
                count = count+1
	
    if count==0:
        return 0
    else:
        return float(sent_score)/float(count)	


def main():
   
    # build the sentiment score dictionary    
    dic = sentimentdict(sys.argv[1])   
 
    #get all of the tweet texts per location
    tweetsLocation = getTweetLocation(sys.argv[2])
    
    stateScores={}
    maxState=""
    maxScore=0
    for k in tweetsLocation.keys():
        s = calcAverageSentiment(tweetsLocation[k],dic)
        stateScores[k]=s
        if s > maxScore:
            maxState=k
            maxScore=s

    print maxState

    return


if __name__ == '__main__':
    main()
