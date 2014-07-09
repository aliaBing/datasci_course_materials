import sys
import json

def sentimentdict(fp):
    fo = open(fp)
    scores = {}
    for line in  fo:
        term , score = line.split("\t")
        scores[term]=int(score)
    fo.close()
    return scores



def getTweetTexts(fp):
    fo = open(fp)
    #print str(len(fo.readlines()))
    deleted=0
    tweets =[]
    for line in fo:
        var=json.loads(line)
	if "text" in var:
	    tweets.append(var["text"])
	else:
 	    deleted = deleted +1
    #print len(tweets)
    #print deleted
    return tweets



def calcSentiment(tweets,dict):
    scores=[]
    for text in tweets:
	tokens = text.split()
	sent_score=0
	for token in tokens:
		if token in dict:
			sent_score=sent_score+dict[token]
	scores.append(sent_score)
    return scores	


def main():
   
    # build the sentiment score dictionary    
    dic = sentimentdict(sys.argv[1])   
 
    #get all of the tweet texts
    tweets = getTweetTexts(sys.argv[2])
    
    #calculate the sentiment per tweet 
    sentiment_scores = calcSentiment(tweets,dic)
    
    #display the sentiment scores, one at a time
    for score in sentiment_scores:
	print score
       	#print "\n"
   
    return


if __name__ == '__main__':
    main()
