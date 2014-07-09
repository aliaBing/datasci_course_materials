import sys
import json
import string

# new test for push

def sentimentdict(fp):
    fo = open(fp)
    scores = {}
    for line in fo:
        tokens = line.split()
        if len(tokens) > 2:
            continue
        term = tokens[0]
        term = term.lower()
        score = int(tokens[1])
        # print term,score
        scores[term] = score
    fo.close()
    return scores


def gettweettexts(fp):
    fo = open(fp)
    tweets = []
    for line in fo:
        var = json.loads(line)
        if "text" in var:
            tweets.append(var["text"].encode('utf-8'))
    return tweets


def calcSentiment(tweets, dic):
    newTokensDict = {}
    for text in tweets:
        tokens = text.split()
        positives=0
        negatives=0
        count=1
        temp=[]
        for token in tokens:
            # CLEANUP punctuations
            cleanToken = token.lstrip(string.punctuation)
            cleanToken = cleanToken.rstrip(string.punctuation)
            cleanToken = cleanToken.lower()
            if cleanToken == "":
                continue
            # cleanToken=cleanToken.strip()
            if cleanToken in dic:
                if dic[cleanToken] > 0:
                    positives += 1
                    count +=1
                else:
                    negatives += 1
                    count+=1
            else:
                temp.append(cleanToken)

        #go over all of the new terms and add them to the new dict
        for newTerm in temp:
            if newTerm in newTokensDict:
                #update its count
                currentScore=newTokensDict[newTerm]
                newScore=float(currentScore + (float(positives-negatives)/float(count))) * 0.5
                newTokensDict.update({newTerm:newScore})
            else:
                #add this new term
                newTokensDict[newTerm]=float(positives-negatives)/float(count)



    return newTokensDict


def printNewSentimentScores(dict):
    # print len(dict)
    for token, score in dict.iteritems():
        print token + " " + str(score)


def main():
    # build the sentiment score dictionary
    dic = sentimentdict(sys.argv[1])

    # get all of the tweet texts
    tweets = gettweettexts(sys.argv[2])

    # calculate the sentiment per tweet and get back the new Terms Dictionary
    newTokensDict = calcSentiment(tweets, dic)

    #calculate and print the new Sentiment scores for new terms
    printNewSentimentScores(newTokensDict)


    #display the sentiment scores, one at a time
    #for score in sentiment_scores:
    #print score
    #print "\n"

    #print "size of tweets" + str(len(tweets))
    #print "size of scores" + str(len(sentiment_scores))
    #print "size of the new term dictionary" + str(len(newTokensDict))
    return


if __name__ == '__main__':
    main()
