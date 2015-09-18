#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WK3 Assignment. Using CSV, URLLIB2 and RE amongst other modules."""

import argparse, csv, datetime, operator, re, urllib2


def downloadData(url):
    """Fetching the data from a URL."""
    content = urllib2.urlopen(url)
    return content


def processData(content):
    """Processing the content of the CSV file."""
    dictionary = csv.reader(content)
    dateFormat = "%Y-%m-%d %H:%M:%S"
    hits = 0
    imgHits = 0 
    safari = chrome = firefox = msie = 0

    times = {} 
    for i in range(0, 24):
        times[i] = 0

    for row in dictionary:
        result = {"path":row[0], "date":row[1], "browser": row[2], "status": row[3], "size": row[4]}

        date = datetime.datetime.strptime(result["date"], dateFormat)
        times[date.hour] = times[date.hour] + 1

        hits += 1
        if re.search(r"\.(?:jpg|jpeg|gif|png)$", result["path"], re.I | re.M):
            imgHits += 1

        elif re.search("chrome/\d+", result["browser"], re.I):
            chrome += 1

        elif re.search("safari", result["browser"], re.I) and not re.search("chrome/\d+", result["browser"], re.I):
            safari += 1

        elif re.search("firefox", result["browser"], re.I):
            firefox += 1

        elif re.search("msie", result["browser"], re.I):
            msie += 1

    imageRequest = (float(imgHits) / hits) * 100
    browsers = {"Safari": safari, "Chrome":chrome, "Firefox": firefox, "MSIE":msie}

    print "Results are shown below:"
    print "Image requests account for {0:0.1f}% of all requests.".format(imageRequest)
    print "The most popular browser is %s." % (max(browsers.iteritems(), key=operator.itemgetter(1))[0])

    tempTimes = times

    for i in range(0, 24):
        id = (max(tempTimes.iteritems(), key=operator.itemgetter(1))[0])
        print "Hour %02d has %s hits." % (id, tempTimes[id])
        tempTimes.pop(id)
    

def main():
    """Main function that runs when programm is called."""
    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--url", help="Enter the URL to fetch a CSV file.")
    args = url_parser.parse_args()

    if args.url:
        try:
            csvData = downloadData(args.url)
            processData(csvData)       

        except:
            print "This URL is invalid."
    else:
        print "Please make sure to insert a URL."

if __name__ == "__main__":
    main()
