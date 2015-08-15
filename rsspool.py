#!/usr/bin/python3.4

from multiprocessing import Pool
import optparse
import feedparser
import re
import time

def remove_encoding_errors(text):
    # removing all html tags
    fixed_text = re.sub("<(.*?)>", "", text)

    # removing encoding errors
    fixed_text = fixed_text.replace('&rsquo;', "'") 
    fixed_text = fixed_text.replace('&#39;', "'") 
    fixed_text = fixed_text.replace('&#039;', "'") 
    fixed_text = fixed_text.replace('&nbsp;', " ") 
    fixed_text = fixed_text.replace('&amp;', " and ")
    return fixed_text

def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", action="store", default=8, type="int", 
                      help="Number of threads running")
    options, args = parser.parse_args()
            
    p = Pool(options.p)
    
    # remember slashdot and ars technica
    with open("url.txt") as u:
        urls = u.read().split()
        print("found " + str(len(urls)) + " urls")

    print("retreiving rss feeds")

    # retrieving the web pages
    feeds = p.map(feedparser.parse, urls)
    print("Processing feeds")
    entries = [a for b in feeds for a in b.entries]
    title_and_summary = [t.title + '\n' + t.summary for t in entries]
    title_and_summary = [remove_encoding_errors(a) for a in title_and_summary]
    with open("summaries.txt", "w") as h:
        h.write("\n".join(title_and_summary))

    titles = [remove_encoding_errors(t.title) for t in entries]
    with open("headline.txt", "w") as h:
        h.write("\n".join(titles))
    print("processes: ", options.p)
     
if __name__ == "__main__":
    start = time.time()
    main()    
    total_time = round(time.time() - start, 2)
    print("Job took ", total_time, "seconds")

