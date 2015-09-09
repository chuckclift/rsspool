#!/usr/bin/env python3

from multiprocessing.pool import ThreadPool as Pool
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
    options, args = parser.parse_args()
            
    p = Pool(options.p)
    
    # remember slashdot and ars technica

    # retrieving the web pages
    feeds = p.map(get_feed, [a for a in sys.stdin])

    entries = [a for b in feeds for a in b.entries]

    titles = [cleanup(t.title) for t in entries]
    sys.stdout.write('\n'.join(titles) + '\n')
     
if __name__ == "__main__":
    main()    

