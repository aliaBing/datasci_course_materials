import sys
import json
import string





def getTweetTexts(fp):
    fo = open(fp)
    #print str(len(fo.readlines()))
    deleted=0
    tweets =[]
    for line in fo:
        var=json.loads(line)
	if "text" in var:
	    tweets.append((var["text"]).encode('utf-8'))
	else:
 	    deleted = deleted +1
    #print len(tweets)
    #print deleted
    return tweets










def main():
   
                   
 
    #get all of the tweet texts
    tweets = getTweetTexts(sys.argv[1])
    
    freq={}    

    for t in tweets:
        #print t.translate(string.maketrans("",""), string.punctuation)
        words=t.split()
        for w in words:
            temp=w.lstrip(string.punctuation)
            temp=temp.rstrip(string.punctuation)
            temp=temp.lower() 
            
            if temp in freq:
                count=freq[temp]+1
                freq.update({temp:count})
            else:
                freq[temp]=1


    for token, count in freq.iteritems():
        print token+" "+str(count)
  
    return


if __name__ == '__main__':
    main()
