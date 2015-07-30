#!/usr/bin/python3.4

from multiprocessing import Pool
import feedparser
import re
import time

def remove_encoding_errors(text):
    # removing all html tags
    fixed_text = re.sub("<(.*?)>", "", text)

    # removing encoding errors
    fixed_text = fixed_text.replace('&rsquo;', "'") 
    fixed_text = fixed_text.replace('&#39;', "'") 
    fixed_text = fixed_text.replace('&nbsp;', " ") 
    fixed_text = fixed_text.replace('&amp;', " and ")
    return fixed_text

def main():
    p = Pool(4)
    
    # remember slashdot and ars technica
    with open("url.txt") as u:
        urls = u.read().split()
        print("found " + str(len(urls)) + " urls")

    print("retreiving rss feeds")
    
    # retrieving the web pages
    feeds = p.map(feedparser.parse, urls)

    entries = [a for b in feeds for a in b.entries]
    title_and_summary = [t.title + '\n' + t.summary for t in entries]
    title_and_summary = [remove_encoding_errors(a) for a in title_and_summary]
    with open("summaries.txt", "w") as h:
        h.write("\n".join(title_and_summary))

    titles = [remove_encoding_errors(t.title) for t in entries]
    with open("headline.txt", "w") as h:
        h.write("\n".join(titles))

     
if __name__ == "__main__":
    start = time.time()
    main()    
    print("Job took " + str(time.time() - start) + "seconds")



