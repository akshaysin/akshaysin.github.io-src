#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Akshay Sinha'
SITENAME = 'An Average Joe'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'EST'

DEFAULT_LANG = 'English'

''' In addition to below MARKDOWN settings, add following block to end of index.html

        <script>
           $(document).ready(function () {
              $("table").attr("class","table table-condensed table-bordered");
           });
        </script>

 '''

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.tables':{},
    }
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGIN_PATHS = ['pelican-plugins', ]
# PLUGINS = ['i18n_subsites','disqus_static', ]
PLUGINS = ['i18n_subsites',]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

# Blogroll
LINKS = (('Resume', 'docs/Resume.pdf'),
         ('Email','https://spamty.eu/mail/v4/830/2RWUyWci8Q2f55cff1/'))

# Social widget
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/akshay-sinha-91215954'),
          ('github', 'https://github.com/akshaysin'))

# MENUITEMS = (
#     ('Email', 'https://spamty.eu/mail/v4/830/2RWUyWci8Q2f55cff1/'),
#     ('Resume', 'docs/Resume.pdf')
#     )

DEFAULT_PAGINATION = 10

BOOTSTRAP_FLUID=False
BOOTSTRAP_NAVBAR_INVERSE=True
STATIC_PATHS = [ 'docs', 'images' ]
# BANNER='images/download.jpg'
# BANNER_SUBTITLE=''
PYGMENTS_STYLE='solarizeddark'
DISPLAY_ARTICLE_INFO_ON_INDEX=True
ABOUT_ME='A confused coder'
AVATAR='images/akshay.jpg'
DISPLAY_CATEGORIES_ON_SIDEBAR=False
DISPLAY_ARCHIVE_ON_SIDEBAR=True
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'
SHARIFF = False

'''add following to the end of index.html to enable addThis analytics
<!-- Go to www.addthis.com/dashboard to customize your tools -->
<script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-5adbce4fc80f08db"></script>
'''

ADDTHIS_PROFILE = 'ra-5adbce4fc80f08db'

# for disque comments

# PLUGINS = [u"disqus_static"]

DISQUS_SITENAME = 'an-average-joe.disqus.com'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
