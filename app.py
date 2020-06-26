from flask import Flask, render_template, request, redirect
import ploting

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

  if request.method=='POST':
    ticker = request.form['ticker']
    series = request.form.getlist('series')
    try:
        fig = ploting.plot_series(600, 300, ticker, ploting.getdata(ticker), series)
        script, div= components(fig)
    except:
        flash("Try another ticker symbol.")

  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
