from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
from flask import Flask
from flask import render_template, request

from happytransformer import HappyWordPrediction
    
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = ""
app.config["APPLICATION_ROOT"] = APP_ROOT

happy_wp = HappyWordPrediction("BERT", "TurkuNLP/bert-base-finnish-cased-v1")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    global happy_wp
    inpsentence=request.json["sentencein"].replace("SANA","[MASK]",1)
    if "[MASK]" not in inpsentence:
        return {"predictions_html":"Et muistanut laittaa yksi SANA."}
    predictions = happy_wp.predict_mask(inpsentence,top_k=5)
    print(list(predictions))
    predictions_html=render_template("result.html",predictions=predictions)
    return {"predictions_html":predictions_html}

