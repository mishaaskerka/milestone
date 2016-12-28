from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
from datetime import timedelta
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import DatetimeTickFormatter
from bokeh.layouts import row, widgetbox, column
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
import colorsys

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('my_index.html')
    if request.method == 'POST':
        app.vars['n_days'] = request.form['n_days']
        app.vars['ticker'] = request.form['ticker'].split(',')
        with open('{0}_{1}.txt'.format(app.vars['ticker'],app.vars['n_days']),'w') as f:
            f.write('Company Name: {0}\n'.format(app.vars['ticker']))
            f.write('Last N Days: {0}\n\n'.format(app.vars['n_days']))
        return redirect('/calculated_plot')

@app.route('/calculated_plot',methods=['GET','POST'])
def calculated_plot():
    colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*plt.cm.rainbow(mpl.colors.Normalize()(range(len(app.vars['ticker']))))]
    p = figure(title="Stock share prices for the last {0} days".format(app.vars['n_days']), x_axis_label='Date', y_axis_label='Price / USD')
    for i, ii in enumerate(app.vars['ticker']):
        print(ii)
        a = pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/{0}/data.csv'.format(ii))
        a['Date'] = pd.to_datetime(a['Date'])
        mask = (a['Date'] > datetime.now().date() - timedelta(days=int(app.vars['n_days']))) & (a['Date'] <= datetime.now().date())
        a_small = a.loc[mask]
        p.line(a_small['Date'], a_small['Close'],color=colors[i], legend= '{0}'.format(ii),line_width=2)
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
            ))
    p.xaxis.major_label_orientation = np.pi/4
    output_file("templates/share_prices.html")
    save(p)
    return render_template("share_prices.html")  
    

if __name__ == '__main__':
  app.run(port=33507)
