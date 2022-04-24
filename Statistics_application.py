import csv
from flask import Flask
from flask import request
from flask import render_template
import pandas as pd

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def index():
        return  render_template('index_1.html')

@app.route('/data', methods = ['GET', 'POST'])
def data():
    if request.method == "POST":
        f = request.form['csvfile']
        data = []
        with open(f) as file:
            csvfile = pd.read_csv(file)
            total_rows=len(csvfile.axes[0])
            total_cols=len(csvfile.axes[1])
            missin_values_in_each_column = csvfile.isnull().sum()/len(csvfile)
            my_max = csvfile.max(axis=0)
            my_min = csvfile.min(axis=0)
            
            
            calculate =[("Number of Rows: "+str(total_rows)),
                        ("Number of Columns: "+str(total_cols))]

            for row in calculate:
                data.append(row)
            n=1
            for row in my_min:
                data.append('Minimum value in ' +str(n) +' column: ' + str(row))
                n=n+1
            n=1
            for row in my_max:
                data.append('Maximum value in ' +str(n)+' column: ' + str(row))
                n=n+1
            n=1
            for row in missin_values_in_each_column:
                data.append('% of missing value in ' +str(n)+' column: ' + str(row))
                n=n+1
            n=1
            b=0
            
            for row in my_max:
                a = csvfile.iloc[0:,b:n]
                c = a.quantile(0.1)
                list=[]
                for d in c:
                    d=str(d)
                    war=d.split('\n')
                    list.append(war[0])
                    
                data.append("10th percentile in "+str(n)+" column: "+ str(list[0]))
                n=n+1
                b=b+1
            n=1
            b=0
            for row in my_max:
                a = csvfile.iloc[0:,b:n]
                c = a.quantile(0.9)
                list=[]
                for d in c:
                    d=str(d)
                    war=d.split('\n')
                    list.append(war[0])
                    
                data.append("90th percentile in "+str(n)+" column: "+ str(list[0]))
                n=n+1
                b=b+1
            n=1
            b=0
            for row in my_max:
                a = csvfile.iloc[0:,b:n]
                c = a.mean()
                list=[]
                for d in c:
                    d=str(d)
                    war=d.split('\n')
                    list.append(war[0])
                    
                data.append("Mean in "+str(n)+" column: "+ str(list[0]))
                n=n+1
                b=b+1 
            data_representation = pd.DataFrame(data)
            data_representation.to_csv('file.csv')
            return render_template('data_1.html', data=data_representation.to_html(header = False, index = False))
            

if __name__ =='__main__':
    app.run(debug = True)