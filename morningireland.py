#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
# pylint: disable=bad-indentation, line-too-long

"""A script to scrape the Morning Ireland feed and extract the parts I care about"""

import re
from datetime import datetime
import requests
import xmltodict


FEED_URL = "http://www.rte.ie/radio1/podcast/podcast_morningireland.xml"
LOCAL_URL = "http://yoursite.com/"

r = requests.get(FEED_URL)
rte_xml = r.text
y = xmltodict.parse(rte_xml)
already_seen = []

build_time = datetime.now().strftime("%a, %d %b %Y, %H:%M:%S +0000")
current_year = datetime.now().strftime("%Y")

output = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>RTE - Morning Ireland - Best Bits</title>
    <itunes:author>RTE:Ireland</itunes:author>
    <link>http://www.rte.ie/radio1/morningireland/</link>
    <description>The best bits of the Morning Ireland feed</description>
    <itunes:subtitle>The most listened to show in Ireland, Morning Ireland brings
    you the news from home and abroad. Regular bulletins and updates, backed up
    by a series of reports and in-depth interviews, from 7am to 9am every
    week-day morning.

    This feed contains only the bit I care about: It Says In The Papers.</itunes:subtitle>
    <itunes:summary>The best bits of Morning Ireland.</itunes:summary>
    <language>en-ie</language>
    <copyright>RTE {current_year}</copyright>
    <itunes:owner>
      <itunes:name>John Kelly</itunes:name>
      <itunes:email>johnke@gmail.com</itunes:email>
    </itunes:owner>
    <itunes:image href="{LOCAL_URL}/morningireland/morning-ireland-450.jpg" />
    <lastBuildDate>{build_time}</lastBuildDate>
    <image>
      <url>{LOCAL_URL}/morningireland/morning-ireland-144.jpg</url>
      <title>RTE - Morning Ireland</title>
      <link>http://www.rte.ie/radio1/morningireland/</link>
      <height>144</height>
      <width>144</width>
    </image>
    <category>News &amp; Politics</category>
    <itunes:category text="News &amp; Politics" />
    <itunes:explicit>no</itunes:explicit>"""


def generate_episode_text(episode):
  """Once we have the episode we care about, extract the information we care about
  and output an xml item for that episode"""
  title = episode.get('title') or ""
  link = episode.get('link') or ""
  description = episode.get('description') or ""
  itunes_subtitle = episode.get('itunes:subtitle') or ""
  itunes_summary = episode.get('itunes:summary') or ""
  itunes_duration = episode.get('itunes:duration') or ""
  itunes_author = "RTE Radio 1"
  pub_date = episode.get('pubDate') or ""

  episode_text = f"""
        <item>
                <title>{title}</title>
                <itunes:author>{itunes_author}</itunes:author>
                <link>{link}</link>
                <description>{description}</description>
                <itunes:subtitle>{itunes_subtitle}</itunes:subtitle>
                <itunes:summary>{itunes_summary}</itunes:summary>
                <itunes:duration>{itunes_duration}</itunes:duration>
                <guid isParmaLink="false">{link}</guid>
                <enclosure type="audio/mpeg" url="{link}" />
                <pubDate>{pub_date}</pubDate>
                <itunes:explicit>no</itunes:explicit>
        </item>
  """
  return episode_text


for ep in y['rss']['channel']['item']:
  match = re.search("(8.10am.*In The Papers)", ep['title'], re.I | re.M)
  if match:
      output += generate_episode_text(ep)

output += """
   </channel>
</rss>"""

print(output)
