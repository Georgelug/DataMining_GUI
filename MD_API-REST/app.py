from flask import Flask, jsonify, request,send_file
from flask_cors import CORS
import pandas as pd

from algorithms import *
app = Flask(__name__) # our app
CORS(app)

theresData = False
theresEDA = False

# routes
@app.route('/getData',methods = ['POST'])
def getData():
    dataInfoTicker = request.json
    print(dataInfoTicker)
    global data
    data = Data(
        ticker = dataInfoTicker["ticker"],
        name = dataInfoTicker["name"],
        date_start = dataInfoTicker["date_start"],
        date_end = dataInfoTicker["date_end"]
    )
    global theresData
    theresData = data.data
    print(data.getDataInformation())
    return jsonify({
        "message":"Ticker found" if theresData else "Ticker not found",
        "Data" : data.getDataInformation() if theresData else None,
    })

@app.route("/")
def ping():
    return jsonify({"message":"API MD Connection succesfully"})

    
@app.route("/EDA")
def EDA():
    if theresData:
        global eda
        eda = EDA_algorithm(data)
        global theresEDA
        theresEDA = True
        return jsonify({
                "eda":eda.runProcess()
            })
    
    return jsonify({
        "message" : "Error, there is no data"
    })

@app.route("/PCA")
def PCA():
    if theresData and theresEDA:
        pca = PCA_algorithm(data,eda)
        return jsonify({
            "pca":pca.runProcess()
        })
        
    return jsonify({
        "message" : "Error, there is no data"
    })

@app.route("/Model")
def menuModel():
    if theresData and theresEDA:
        return jsonify({
                    "models_available": {
                        1 : "Decision Tree Regressor",
                        2 : "Random Forest Regressor",
                        3 : "Hybrid model (kmeans + Random Forest classifier)",
                        4 : "Support Vector Classification"
                    }
                })
    return jsonify({
        "message" : "Error, there is no data"
    })
@app.route("/Model/Dtree",methods = ['POST','GET'])
def Dtree():
    if theresData and theresEDA:
        if request.method == "GET":
            global dTree
            dTree = DtreeModel(data,eda)
            global dTreeresponse
            dTreeresponse = dTree.buildModel()
            return jsonify({
                "Dtree": dTreeresponse
            })
        else:
            if dTreeresponse["status"]:
                print(request.json)
                req = request.json
                print(type(req))
                dfreq = pd.DataFrame.from_dict(req)
                newPronostic = dTree.newPronostic(dfreq)
                return jsonify({
                    "dTree": newPronostic
                })
    return jsonify({
        "message" : "Error, there is no data"
    })
        
@app.route("/Model/randomForest",methods = ['POST','GET'])
def randomForest():
    if theresData and theresEDA:
        if request.method == "GET":
            global rF
            rF = randomForestModel(data,eda)
            global rfResponse
            rfResponse = rF.buildModel()
            return jsonify({
                "randomForest": rfResponse
            })
        else:
            if rfResponse["status"]:
                req = request.json
                dfreq = pd.DataFrame.from_dict(req)
                newPronostic = rF.newPronostic(dfreq)
                return jsonify({
                    "dTree": newPronostic
                })
    return jsonify({
        "message" : "Error, there is no data"
    })
    

@app.route("/Model/hybrid",methods = ['POST','GET'])
def hybrid():
    if theresData and theresEDA:
        if request.method == "GET":
            global hyb
            hyb = Hybrid_kmeansRandomForest(data)
            return jsonify({
                "hybridmodel": "The model hybrid was created successfully"
            })
        else:
            req = request.json
            dfreq = pd.DataFrame.from_dict(req)
            newclass = hyb.newClassification(dfreq)
            print(newclass)
            if newclass["status"]:
                return jsonify({
                    "hybridModel": newclass
                })
    return jsonify({
        "message" : "Error, there is no data"
    })
    
# kernel: linear, poly, rbf o sigmoid
@app.route("/Model/SVM/<string:kernel>",methods = ['POST','GET'])
def svm(kernel):
    if theresData and theresEDA:
        if request.method == "GET":
            global svm
            svm = SVM_Model(data,eda,kernel)
            print(kernel)
            global svmResponse
            svmResponse = svm.buildModel()
            return jsonify({
                "SVM": svmResponse
            })
        else:
            if svmResponse["status"]:
                req = request.json
                dfreq = pd.DataFrame.from_dict(req)
                newPronostic = svm.newPronostic(dfreq)
                return jsonify({
                    "SVM": newPronostic
                })
    return jsonify({
        "message" : "Error, there is no data"
    })

@app.route('/get_heatmap/<string:name>')
def get_image(name):
    try:
        fileName = f"./images/{name}_heatmapCorrelations.png"
        return send_file(fileName)
    except Exception as e:
        return jsonify({
                    "message" : "Error, something is wrong",
                    "Error": f"{e}"
                })
        
@app.route('/get_histogram/<string:name>')
def get_histogram(name):
    try:
        fileName = f"./images/{name}_histograms.png"
        return send_file(fileName)
    except Exception as e:
        return jsonify({
                    "message" : "Error, something is wrong",
                    "Error": f"{e}"
                })
        
@app.route('/get_plotVariance/<string:name>')
def get_plotVariance(name):
    try:
        fileName = f"./images/{name}_numberOfPrincipalComponents_plot.png"
        return send_file(fileName)
    except Exception as e:
        return jsonify({
                    "message" : "Error, something is wrong",
                    "Error": f"{e}"
                })
        
@app.route('/get_mainPlot/<string:name>')
def get_mainPlot(name):
    try:
        fileName = f"./images/{name}_mainGrafic.png"
        return send_file(fileName)
    except Exception as e:
        return jsonify({
                    "message" : "Error, something is wrong",
                    "Error": f"{e}"
                })
        




if __name__ == "__main__":
    app.run(debug=True, port=3000)