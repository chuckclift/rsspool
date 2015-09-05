#!/usr/bin/env python3

from multiprocessing import Pool
import optparse
import feedparser
import re
import time
import sys

def cleanup(text):
    # removing all html tags
    fixed_text = re.sub("<(.*?)>", "", text)

    # bad apostrophe encodings
    fixed_text = fixed_text.replace('&rsquo;', "'") 

    # bad quote sign encodings
    fixed_text = fixed_text.replace('&quot;', '"') 

    # getting rid of &#039; and similar
    fixed_text = re.sub("&#[0-9]{1,4};", "'", fixed_text)

    # removing everything else that follows that form
    fixed_text = re.sub("&#.{1,9};", " ", fixed_text)

    fixed_text = fixed_text.replace('&amp;', " and ")
    return " ".join(fixed_text.split())

def get_feed(url):
    try:
        return feedparser.parse(url)
    except:
        print('Error with',url)
        return None

def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", action="store", default=8, type="int", 
                      help="Number of threads running")
#    parser.add_option("-v", action="store", default=False)
    options, args = parser.parse_args()
            
    p = Pool(options.p)
    
    # remember slashdot and ars technica

    # retrieving the web pages
    feeds = p.map(get_feed, [a for a in sys.stdin])
#    if parser.v:
#        print("Processing feeds")

    entries = [a for b in feeds for a in b.entries]

    title_and_summary = [t.title + '\n' + t.summary for t in entries]
    title_and_summary = [cleanup(a) for a in title_and_summary]
    with open("summaries.txt", "w") as h:
        h.write("\n".join(title_and_summary))

    titles = [cleanup(t.title) for t in entries]
    with open("headline.txt", "w") as h:
        h.write("\n".join(titles))

#    if parser.v:
#        print("processes: ", options.p)
     
if __name__ == "__main__":
    start = time.time()
    main()    
    total_time = round(time.time() - start, 2)
    print("Job took ", total_time, "seconds")

