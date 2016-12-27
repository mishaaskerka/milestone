from flask import Flask, render_template, request, redirect
import numpy as np
import requests
import simplejson as json
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import DatetimeTickFormatter
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource,CustomJS
from bokeh.models.widgets import Slider, TextInput
from datetime import datetime

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('my_index.html')
    #else:
    if request.method == 'POST':
        #return render_template('my_index.html')
        #print('lalalal')
        app.vars['n_days'] = request.form['n_days']
        app.vars['ticker'] = request.form['ticker']
        print(app.vars['n_days'],app.vars['ticker'])
        with open('{0}_{1}.txt'.format(app.vars['ticker'],app.vars['n_days']),'w') as f:
            f.write('Company Name: {0}\n'.format(app.vars['ticker']))
            f.write('Last N Days: {0}\n\n'.format(app.vars['n_days']))
        return redirect('/calculated_plot')
        #return render_template('my_index.html')
        #return share_prices.html
        #return redirect('/share_prices.html')
        #return render_template("share_prices.html")  

@app.route('/calculated_plot',methods=['GET','POST'])
def calculated_plot():

    a = pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/{0}/data.csv'.format(app.vars['ticker']))
    a['Date'] = pd.to_datetime(a['Date'])
    mask = (a['Date'] > datetime.now().date() - timedelta(days=int(app.vars['n_days']))) & (a['Date'] <= datetime.now().date())
    a_small = a.loc[mask]
    print(a_small)
    p = figure(title="Share prices for the last {0} days".format(app.vars['n_days']), x_axis_label='Date', y_axis_label='Price / USD')
    p.line(a_small['Date'], a_small['Close'], legend= '{0}'.format(app.vars['ticker']),color='purple',line_width=2)
    #p.line(x, y, legend= 'FB',color='purple',line_width=2)
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
            ))
    p.xaxis.major_label_orientation = np.pi/4
    output_file("templates/share_prices.html")
    #show(p)
    save(p)
    return render_template("share_prices.html")  
    #return app.send_static_file("share_prices.html")  
    #return templates/share_prices.html
    

if __name__ == '__main__':
  app.run(port=33507,debug=True)
