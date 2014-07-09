import sys
import json
import string
import operator


def getHashTags(fp):
    fo = open(fp)
    results={}
    tags=[]
    for line in fo:
        var=json.loads(line)
	if "text" in var and "entities" in var and var["entities"] is not None:
            #add hashtags to the dictionary
            tags=var["entities"]["hashtags"]
            if len(tags) !=0:
                for t in tags:
                    text=t["text"]
                    if text in results:
                        count=results[text]+1
                        results.update({text:count})
                    else:
                        results[text]=1
    return results


def main():
      
 
    #get all of the tweet texts
    tweets = getHashTags(sys.argv[1])
    sorted_x = sorted(tweets.iteritems(), key=operator.itemgetter(1), reverse=True)
    for i in range (0,10):
        print sorted_x[i][0].encode('utf-8')+" "+str(sorted_x[i][1])

    return


if __name__ == '__main__':
    main()
