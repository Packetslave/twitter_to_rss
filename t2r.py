#!env python -*- python-indent:4 -*-

import datetime
import feedgenerator
import json
import os
import twitter

CONFIG = os.path.join(os.path.dirname(__file__), 'config.json')

def main():
    with open(CONFIG, 'r') as f:
        config = json.loads(f.read())

    with open(config['user_file'], 'r') as f:
        screen_names = f.readlines()

    api = twitter.Api(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token_key=config['access_token_key'],
        access_token_secret=config['access_token_secret']
    )

    for user in (x.strip() for x in screen_names):
        feed = feedgenerator.Rss201rev2Feed(
            title=u"Tweets for %s" % user,
            link=u"http://twitter.com/%s" % user,
            description=u"Tweets for %s" % user,
            language=u"en")

        statuses = api.GetUserTimeline(screen_name=user)

        for status in statuses:
            pubdate = datetime.datetime.strptime(
                status.created_at, '%a %b %d %H:%M:%S +0000 %Y')

            link = 'http://twitter.com/%s/status/%s' % (user, status.id)

            feed.add_item(
                title=status.text,
                description=status.text,
                unique_id=link,
                link=link,
                pubdate=pubdate)

        with open('%s/%s.rss' % (config['feed_directory'], user), 'w') as f:
            feed.write(f, 'utf-8')


if __name__ == '__main__':
    main()
