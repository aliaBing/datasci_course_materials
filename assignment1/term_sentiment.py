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


def calcSentiment(tweets, dict):
    scores = []
    newTokensDict = {}
    temp = []
    for text in tweets:
        tokens = text.split()
        sent_score = 0
        for token in tokens:
            # CLEANUP punctuations
            cleanToken = token.lstrip(string.punctuation)
            cleanToken = cleanToken.rstrip(string.punctuation)
            cleanToken = cleanToken.lower()
            if cleanToken == "":
                continue
            # cleanToken=cleanToken.strip()
            if cleanToken in dict:
                sent_score = sent_score + dict[cleanToken]
            else:
                temp.append(cleanToken)

        scores.append(sent_score)
        for cleanToken in temp:
            if cleanToken in newTokensDict:
                # update the list of scores
                tempList = []
                tempList = newTokensDict[cleanToken]
                tempList.append(sent_score)
                newTokensDict.update({cleanToken: tempList})
                # print "updating existing token in dict: clean Token: "+ cleanToken + str(newTokensDict[cleanToken])
            else:
                # add this token to the dictionary
                tempList = [sent_score]
                newTokensDict[cleanToken] = tempList
                # print "adding new token to Dict:  clean token: " + cleanToken

    return scores, newTokensDict


def printNewSentimentScores(dict):
    # print len(dict)
    for token, scores in dict.iteritems():
        positives = float(len([x for x in scores if x > 0]))
        negatives = float(len([x for x in scores if x < 0]))
        if positives + negatives == 0:
            sentiment = 0
        else:
            sentiment = 5 * ((positives - negatives) / (positives + negatives))
        # print str(token)+"\tpositives\t" + str(positives) + "\tnegatives\t" + str(negatives) + "\tsentiment\t" + str(sentiment)
        #if negatives>positives:
        #print "\nfound one\t********************************"
        print token + " " + str(sentiment)


def main():
    # build the sentiment score dictionary
    dic = sentimentdict(sys.argv[1])

    # get all of the tweet texts
    tweets = gettweettexts(sys.argv[2])

    # calculate the sentiment per tweet and get back the new Terms Dictionary
    sentiment_scores, newTokensDict = calcSentiment(tweets, dic)

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
