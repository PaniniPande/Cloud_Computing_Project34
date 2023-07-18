from flask import Flask, render_template, request
import pyodbc


app = Flask(__name__)

Panini_driver = '{ODBC Driver 18 for SQL Server}'
Panini_database = 'ADB'
Panini_server = 'tcp:adbassignments15.database.windows.net,1433'
Panini_username = "pxp4144"
Panini_password = "Paridhi@15"
Panini_conn = pyodbc.connect('DRIVER='+Panini_driver+';SERVER='+Panini_server+';DATABASE='+Panini_database+';UID='+Panini_username+';PWD='+Panini_password)
Panini_cursor = Panini_conn.cursor() 


# ************************************************************************************************************************************************************************************************

@app.route('/task1', methods=['POST', 'GET'])
def BAR():
    if request.method == 'POST':
        partition = int(request.form['n'])
        r1 = int(request.form['r1'])
        r2 = int(request.form['r2'])

        s1 = "SELECT MIN(d1.s) as Min, MAX(d1.S) as Max FROM data d1 JOIN data d2 ON d1.s = d2.s AND d1.t = d2.t WHERE d1.R BETWEEN '"+str(r1)+"' AND '"+str(r2)+"'"
        Panini_cursor.execute(s1)

        row = Panini_cursor.fetchone()
        min_s = int(row.Min)
        max_S = int(row.Max)

        s_range = max_S - min_s
        interval = s_range // partition

        result1 = []
        for i in range(partition):
            start_value = min_s + (i * interval)
            end_value = start_value + interval
            if i!=0:
                start_value+=1
                

            query2 = "SELECT COUNT(*) FROM data WHERE S >= "+str(start_value)+" AND S <= "+str(end_value)+" AND R BETWEEN '"+str(r1)+"' AND '"+str(r2)+"'"
            Panini_cursor.execute(query2)
            row = Panini_cursor.fetchone()
            count = int(row[0])

            result1.append([start_value, end_value, count])

        return render_template('Task1.html', result1=result1)

    return render_template('index.html')

# ************************************************************************************************************************************************************************************************

@app.route('/task2', methods=["POST", "GET"])
def partitionbymags():
    if request.method == 'POST':
        partition = int(request.form['n'])
        r1 = int(request.form['r1'])
        r2 = int(request.form['r2'])

        s1 = "SELECT MIN(d1.s) as Min, MAX(d1.S) as Max FROM data d1 JOIN data d2 ON d1.s = d2.s AND d1.t = d2.t WHERE d1.R BETWEEN '"+str(r1)+"' AND '"+str(r2)+"'"
        Panini_cursor.execute(s1)

        row = Panini_cursor.fetchone()
        min_s = int(row.Min)
        max_S = int(row.Max)

        s_range = max_S - min_s
        interval = s_range // partition

        result1 = []
        for i in range(partition):
            start_value = min_s + (i * interval)
            end_value = start_value + interval
            if i!=0:
                start_value+=1
            query2 = "SELECT COUNT(*) FROM data WHERE S >= "+str(start_value)+" AND S <= "+str(end_value)+" AND R BETWEEN '"+str(r1)+"' AND '"+str(r2)+"'"
            Panini_cursor.execute(query2)
            row = Panini_cursor.fetchone()
            count = int(row[0])

            result1.append([start_value, end_value, count])

        return render_template('Task2.html', result1=result1)

    return render_template('index.html')

# ************************************************************************************************************************************************************************************************



@app.route('/task3', methods=['POST','GET'])
def ShowScatterPlot():
        r1 = str(request.form['r1'])
        r2 = str(request.form['r2'])
        # s1 = "select top 100 mag, data.depth from data order by time desc"
        s1 = "select S,T from data where R between '"+r1+"' and '"+r2+"' "
        Panini_cursor.execute(s1)
        r = Panini_cursor.fetchall()
        s_values = [row[0] for row in r]
        average_s = sum(s_values) / len(s_values)
        return render_template('Task3.html', msg="done",r=r,average_s=average_s)



# ************************************************************************************************************************************************************************************************



@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/Task4")
def task4():
    return render_template('Task4.html') 

@app.route("/fetch_data3")
def task3():
    return render_template('fetch3.html') 

@app.route("/fetch_data2")
def task2():
    return render_template('fetch2.html') 

@app.route("/fetch_data1")
def tas():
    return render_template('fetch1.html') 
@app.route("/chart")
def ch():
    return render_template('chart.html')
@app.route("/horizontalchart")
def hch():
    return render_template('horizontalchart.html')
@app.route("/scatterchart")
def sch():
    return render_template('scatter.html')



if __name__ == '__main__':
    app.run(debug=True)
