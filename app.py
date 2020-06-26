from flask import Flask, render_template, request, flash, redirect
from bokeh.embed import components
import ploting

app = Flask(__name__)
app.secret_key = 'miertmiertmiertvanez'

@app.route('/', methods=['GET', 'POST'])
def index():
  script = None
  div = None
  if request.method=='POST':
    ticker = request.form['ticker']
    series = request.form.getlist('series')
    if series==[]:
        flash('Choose a series option.')
        redirect('/')
    [df, error] = ploting.getdata(ticker)
    if error==None:
        fig = ploting.plot_series(600, 300, ticker, df, series)
        script, div= components(fig)
    elif error==1:
        flash('API did not send data. Try again in a minute.')
        redirect('/')
    elif error==2:
        flash('The ticker is invalid.')
        redirect('/')

  return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
