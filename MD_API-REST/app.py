from flask import Flask, jsonify, request, redirect, url_for
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
                req = request.json
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
                "hybrid": "The model hybrid was created successfully"
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
    
    
@app.route("/Model/SVM/<string:kernel>",methods = ['POST','GET'])
def svm(kernel):
    if theresData and theresEDA:
        if request.method == "GET":
            global svm
            svm = SVM_Model(data,eda,kernel)
            global svmResponse
            svmResponse = svm.buildModel()
            return jsonify({
                "randomForest": svmResponse
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





if __name__ == "__main__":
    app.run(debug=True, port=8080)