Barracuda-Poller
.py Logs into the Barracuda Spam firewall and scraps the data on the dashboard.

The data is then saved to a sqlite db.
Was hoping to get it saved to a rrd but we no longer have the firewall so havent had a need to work on it.

Poller-Graph.py generates a dashboard using plotly and the sqlite db as a datasource.

I had these setup to run as a cronjob for 5 min intervals.


To get script working will need to fill in the param, loginHeaders, and dataHeaders dictionaries

You can get the passwd variable from the header in the post request when you login.

the Referer in the Header dictionaries is the http(s)://hostname:port/cgi-mod/index.cgi?locale=en_US