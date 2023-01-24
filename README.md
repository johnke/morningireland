# morningireland - best bits

I really like [RTÉ's Morning Ireland](https://www.rte.ie/radio/radio1/morning-ireland/) and find its summary of "it says in the papers" to be extremely useful for following what's happening in the news but their podcast feed dumps dozens of stories each day, so this is a python script that will extract the bits we care about and dump them as a custom RSS feed that you can subscribe to in your podcatcher.

## Installation

(On an internet-accessible server).

Install requirements:

```bash
pip install -r requirements.txt
```

Clone the repo and configure:

```bash
cd /var/www/sites/yoursite.com
git clone https://github.com/johnke/morningireland.git
```

Change the `LOCAL_URL` variable to the URL where you will be accessing the output.

## Usage

```bash
cd /var/www/sites/yoursite.com/mornigngireland
python morningireland.py > feed.xml
```

Alternatively, set up a cronjob to automatically update the feed.

```bash
30 * * * * python /var/www/sites/yoursite.com/mornigngireland/morningireland.py > /var/www/sites/yoursite.com/mornigngireland/feed.xml
```

Add the podcast to your podcatcher by subscribing to <http://yoursite.com/morningireland/feed.xml>.

## Feedback

Got any suggestions? [Open an issue](https://github.com/johnke/morningireland/issues)!
