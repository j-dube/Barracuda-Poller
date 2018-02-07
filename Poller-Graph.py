#!python3
# -*- coding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import sqlite3
import os.path
import time

# Creates DB Connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "barracuda.sqlite")
db = sqlite3.connect(db_path)
c = db.cursor()

datet = time.strftime('%Y-%m-%d %H:%M:%S')

c.execute('SELECT Timestamp, in_queue, out_queue FROM main.Health')
results = c.fetchall()

####
# Creates Graph for Queue Status
###
layout = go.Layout(
    title='Barracuda Queue Status',
    xaxis=dict(
        title='Time',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1h', step='hour', stepmode='backward'),
                dict(count=8, label='8h', step='hour', stepmode='backward'),
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=5, label='5d', step='day', stepmode='backward'),
                dict(count=7, label='7d', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=4, label='4m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    ),
    yaxis=dict(title='Messages in Queue'),
    legend=dict(orientation="h", y=-1),
    showlegend=True
)
graphx, iny, outy = [], [], []
loop = 0
for z in results:
    graphx.insert(loop, z[0])
    iny.insert(loop, z[1])
    outy.insert(loop, z[2])
    loop += 1

# Create a trace
inqueue = go.Scatter(
    x=graphx,
    dx=5,
    y=iny,
    name='In Queue'
)

# Create a trace
outqueue = go.Scatter(
    x=graphx,
    dx=5,
    y=outy,
    name='Out Queue'
)
data = [inqueue, outqueue]
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='Cuda-Queue.html', show_link=False, auto_open=False)
'''
###
# Creates Total Mail Graph
###
c.execute('SELECT in_total,out_total, outStats.Timestamp FROM main.outStats,main.InStats ORDER BY outStats.Timestamp')
results = c.fetchall()

layout = go.Layout(
    title='Barracuda Mail Totals',
    xaxis=dict(
        title='Time',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1h', step='hour', stepmode='backward'),
                dict(count=8, label='8h', step='hour', stepmode='backward'),
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=5, label='5d', step='day', stepmode='backward'),
                dict(count=7, label='7d', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=4, label='4m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'),
    yaxis=dict(title='Messages', side='left', autorange=True, color='Blue'),
    yaxis2=dict(title='Messages', side='right', overlaying='y', autorange=True, color='Orange'),
    legend=dict(orientation="h", y=-1),
    showlegend=True
)

iny, outy, time = [], [], []
loop, loopx = 0, 0
for z in results:
    if loop % 30 == 0:
        iny.insert(loopx, (z[0]))
        outy.insert(loopx, (z[1]))
        time.insert(loopx, (z[2]))
        loopx += 1
    loop += 1

# Create a trace
inqueue = go.Scatter(
    x=time,
    y=iny,
    name='In Total'
)

# Create a trace
outqueue = go.Scatter(
    x=time,
    y=outy,
    yaxis='y2',
    name='Out Total'
)
data = [inqueue, outqueue]
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='Cuda-Messages-Total.html', show_link=False, auto_open=False)
'''
###
# Creates Health 1 Graph
###
c.execute('SELECT sys_load, cpu_fan_1, sys_fan_2, mail_log_stor, firmware_stor FROM main.Health')
results = c.fetchall()

layout = go.Layout(
    title='Barracuda Health Status',
    xaxis=dict(
        title='Time',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1h', step='hour', stepmode='backward'),
                dict(count=8, label='8h', step='hour', stepmode='backward'),
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=5, label='5d', step='day', stepmode='backward'),
                dict(count=7, label='7d', step='day', stepmode='backward'),
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=4, label='4m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    ),
    yaxis=dict(title='Percent', side='right', range=[0, 100]),
    yaxis2=dict(title='RPM', side='left', overlaying='y', type='log', autorange=True),
    legend=dict(orientation="h", y=-1),
    showlegend=True
)
sysly, cpufny, sysfny, mailsty, fwsty = [], [], [], [], []
loop = 0
for z in results:
    sysly.insert(loop, z[0])
    cpufny.insert(loop, z[1])
    sysfny.insert(loop, z[2])
    mailsty.insert(loop, z[3])
    fwsty.insert(loop, z[4])
    loop += 1
sysload = go.Scatter(
    x=graphx,
    y=sysly,
    name='System Load'
)

cpufan = go.Scatter(
    x=graphx,
    y=cpufny,
    name='CPU 1 Fan Speed',
    yaxis='y2'
)
sysfan = go.Scatter(
    x=graphx,
    y=sysfny,
    name='System Fan Speed',
    yaxis='y2'
)
mailstor = go.Scatter(
    x=graphx,
    y=mailsty,
    name='Mail/Log Storage'
)
fwstor = go.Scatter(
    x=graphx,
    y=fwsty,
    name='Firmware Storage'
)
data = [sysload, mailstor, fwstor, cpufan, sysfan]
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='Cuda-Health-1.html', show_link=False, auto_open=False)

###
# Creates In Detail Breakout graph
###
c.execute(
    'SELECT in_blocked, in_blocked_virus, in_rate_control, in_quar, in_allowed_tag, in_allowed FROM main.InStats WHERE Timestamp = (SELECT MAX(Timestamp) FROM main.InStats);')
results = c.fetchone()
results = tuple(results)
fig = {
    'data': [{'labels': ['Blocked', 'Blocked: Virus', 'Rate Controlled', 'Quarantined', 'Allowed: Tagged', 'Allowed'],
              'values': results,
              'type': 'pie',
              'pull': .2,
              'textinfo': 'value+label'
              }],
    'layout': {'title': 'Inbound Email Breakdown'}
}
plotly.offline.plot(fig, filename='Cuda-In-Messages-Breakdown.html', show_link=False, auto_open=False)

###
# Creates Out Detail Breakout graph
###
c.execute(
    'SELECT out_blocked_pol, out_blocked_spam, out_blocked_virus, out_rate_cont, out_quar, out_encrypt, out_redi, out_sent FROM main.outStats WHERE Timestamp = (SELECT MAX(Timestamp) FROM main.InStats);')
results = c.fetchone()
results = tuple(results)
fig = {
    'data': [{'labels': ['Blocked: Policy', 'Blocked: Spam', 'Blocked: Virus', 'Rate Controlled', 'Quarantined',
                         'Encrypted', 'Redirected', 'Sent '],
              'values': results,
              'type': 'pie',
              'pull': .2,
              'textinfo': 'value+label'
              }],
    'layout': {'title': 'Outbound Email Breakdown'}
}
plotly.offline.plot(fig, filename='Cuda-Out-Messages-Breakdown.html', show_link=False, auto_open=False)

db.close()
print("Graphs Created")
