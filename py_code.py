import numpy as np
import requests
import simplejson as json
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource,CustomJS
from bokeh.models.widgets import Slider, TextInput
from datetime import datetime


#r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/FB/data.csv')
#r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/FB/data.json')

a = pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/FB/data.csv')

#datetime.strptime('2013-01-23', '%Y-%m-%d').date()
#[datetime.strptime(i, '%Y-%m-%d').date() for i in a['Date']]

#[datetime.strptime(i, '%Y-%m-%d').date() for i in a['Date'] \
#        if datetime.strptime(i, '%Y-%m-%d').date() >= datetime.now().date() - timedelta(days=30)]

#start = df.index.searchsorted(datetime.now().date())
#end = df.index.searchsorted(datetime.now().date()-timedelta(days=30))
#pd.to_datetime(a['Date'])
a['Date'] = pd.to_datetime(a['Date'])
mask = (a['Date'] > datetime.now().date() - timedelta(days=30)) & (a['Date'] <= datetime.now().date())
a_small = a.loc[mask]
#show(p)

x =list(a['Date'])
y=list(a['Close'])
source = ColumnDataSource(data=dict(x=x, y=y))

#print(source)
#print(source.data)
p = figure(title="Share prices for the last 30 days", x_axis_label='Date', y_axis_label='Price / USD')
#p.line(a_small['Date'], a_small['Close'], legend= 'FB',color='purple',line_width=2)
p.line(x, y, legend= 'FB',color='purple',line_width=2)
p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
        ))
p.xaxis.major_label_orientation = np.pi/4

# x.ix[(x-(datetime.now().date() - timedelta(days=7))).abs().argsort()[0]] finds the closest day

def callback(source=source, window=None):
    data = source.data
    f = cb_obj.value
    x,y = data['x'],data['y']
    t = x.ix[(x-(datetime.now().date() - timedelta(days=7))).abs().argsort()[0]]
    x,y = [[x[i],y[i]] for i in range(len(x)) if x[i].date()> datetime.now().date() - timedelta(days=f)]
    source.trigger('change')


#days = Slider(title="Days", value=1, start=1, end=3, callback=CustomJS.from_py_func(callback))


output_file("templates/share_prices.html")
#layout = column(days, p)

show(p)
#inputs = widgetbox(days)
#show(row(inputs, p, width=800))

#curdoc().add_root(row(inputs, p, width=800))
#curdoc().title = "Sliders"

