from flask import Flask
from flask import request
 




app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True)
    

    
