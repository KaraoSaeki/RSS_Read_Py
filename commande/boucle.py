import feedparser

from flux import list_flux, list_activated_flux

def reading_rss(feed):
    NewsFeed = feedparser.parse(feed)
    for entry in NewsFeed.entries:
        title, link, desc = entry.title, entry.link, entry.description
        return title, link, desc


def boucle_active():
    for flux in list_flux:
        if list_activated_flux[flux]:
            boucle = True
            while boucle:
                feed = feedparser.parse(list_flux[flux])
                for entry in feed.entries:
                    title, link, desc = entry.title, entry.link, entry.description
                    return title, link, desc