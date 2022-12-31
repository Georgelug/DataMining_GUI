from flask import Flask, jsonify, request
import pandas as pd
import json


from algorithms import *
app = Flask(__name__) # our app

theresData = False
theresEDA = False

# routes
@app.route('/getData',methods = ['POST'])
def getData():
    dataInfoTicker = request.json
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
                "EDA":eda.runProcess()
            })
    
    return jsonify({
        "message" : "Error, there is no data"
    })

@app.route("/PCA")
def PCA():
    if theresData and theresEDA:
        pca = PCA_algorithm(data,eda)
        return jsonify({
            "PCA":pca.runProcess()
        })
        
    return jsonify({
        "message" : "Error, there is no data"
    })
    
@app.route("/Model/Dtree",methods = ['POST','GET'])
def Dtree():
    if theresData and theresEDA:
        if request.method == "GET":
            global dtree
            dTree = DtreeModel(data,eda)
            global dTreeresponse
            dTreeresponse = dTree.buildModel()
            return jsonify({
                "Dtree": dTreeresponse
            })
        else:
            if dTreeresponse["status"]:
                newPronostic = dTree.newPronostic(request.json)
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
                newPronostic = rF.newPronostic(request.json)
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
                "hybrid": "The model hybrid was created successfully"
            })
        else:
            newclass = hyb.newClassification(request.json)
            if newclass["status"]:
                return jsonify({
                    "hybridModel": newclass
                })
    return jsonify({
        "message" : "Error, there is no data"
    })
    
    
@app.route("/Model/SVM/<string:kernel>",methods = ['POST','GET'])
def svm(kernel):
    if theresData and theresEDA:
        if request.method == "GET":
            global svm
            svm = SVM(data,eda,kernel)
            global svmResponse
            svmResponse = svm.buildModel()
            return jsonify({
                "randomForest": svmResponse
            })
        else:
            if svmResponse["status"]:
                newPronostic = svm.newPronostic(request.json)
                return jsonify({
                    "SVM": newPronostic
                })
    return jsonify({
        "message" : "Error, there is no data"
    })





if __name__ == "__main__":
    app.run(debug=True, port=8080)