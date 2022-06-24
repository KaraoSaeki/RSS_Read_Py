import feedparser

def reading_rss(feed):
    NewsFeed = feedparser.parse(feed)
    for entry in NewsFeed.entries:
        title, link, desc = entry.title, entry.link, entry.description
        return title, link, desc