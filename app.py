from flask import Flask, render_template, request, redirect
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TodoList')

@app.route('/')
def index():
    response = table.scan()
    tasks = response.get('Items', [])
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        table.put_item(Item={'task': task})
    return redirect('/')

@app.route('/delete/<string:task>')
def delete_task(task):
    table.delete_item(Key={'task': task})
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
