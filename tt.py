from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
from flask import Flask
from flask import render_template, request
import re
from happytransformer import HappyWordPrediction
    
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "/tt"
app.config["APPLICATION_ROOT"] = APP_ROOT

happy_wp = HappyWordPrediction("BERT", "TurkuNLP/bert-base-finnish-cased-v1")


with open("kirosanat.txt") as f:
    re_parts=[]
    for line in f:
        line=line.strip()
        re_parts.append(f"({line})")
    kiro_re=re.compile("|".join(re_parts))

@app.route("/")
def index():
    return render_template("index.html",app_root=APP_ROOT)

@app.route("/predict",methods=["POST"])
def predict():
    global happy_wp
    inpsentence=request.json["sentencein"].replace("SANA","[MASK]",1)
    if "[MASK]" not in inpsentence:
        return {"predictions_html":"Et muistanut laittaa yksi SANA."}
    predictions = happy_wp.predict_mask(inpsentence,top_k=10)
    predictions = [p for p in predictions if not kiro_re.match(p.token)]
    print(list(predictions))
    predictions_html=render_template("result.html",predictions=predictions)
    return {"predictions_html":predictions_html}

