import numpy as np                # Para crear vectores y matrices n dimensionales
import pandas as pd  
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns
import yfinance as yf
from datetime import datetime
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score 
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.svm import SVC
from kneed import KneeLocator

class Data:
    def __init__(self,ticker,name,date_start = '2019-1-1',date_end = '2022-1-1',interval = '1d'):
        self.ticker : str = ticker
        self.name : str = name
        self.date_start : str = date_start
        self.date_end : str = date_end
        self.interval : str = interval
        try:
            self.data : yf.Ticker = yf.Ticker(ticker)
            self.Hist : np = self.data.history(start = self.date_start, end = self.date_end, interval=interval)
        except Exception as e:
            print(e)
            self.data = None
    # setters and getters
    def setHistory(self,hist):
        self.Hist = hist
    def getTicker(self) -> str:
        return self.ticker
    
    def getName(self)-> str:
        return self.name
    
    def getInterval(self)-> str:
        return self.interval
    
    def getData(self) -> yf.Ticker:
        return self.data
    
    def getHistory(self) -> np:
        return self.Hist
    
    def getDateRange(self) -> dict:
        return {
                "start" : self.date_start, 
                "end" : self.date_end, 
                "date_diference" : str(datetime.strptime(self.date_end, '%Y-%m-%d') - datetime.strptime(self.date_start, '%Y-%m-%d'))
                }
        
    def getDataInformation(self) -> dict:
        return {
            "ticker": self.getTicker(),
            "name": self.getName(),
            "dates": self.getDateRange(),
            "interval": self.getInterval(),
            "data": str(self.getData()),
            "history": self.getHistory().to_json(orient = 'records')
        }

class EDA_algorithm:
    def __init__(self , data):
        self.data : Data = data
    
    # Step 1: Description of the data structure
    def getDescriptionOfData(self) -> dict:
        shape = self.data.getHistory().shape
        dTypes = self.data.getHistory().dtypes.to_dict()
        dTypes_dict = {i : str(dTypes[i]) for i in dTypes}
        return {
            "Company": self.data.getName(),
            "Ticker": self.data.getTicker(),
            "Shape": {
                    "rows" : shape[0],
                    "columns":shape[1],
                },
            "data_types": dTypes_dict
            }
    
    # Step 2: Identifying missing data
    def getMissingData(self) -> dict:
        dataNulls = self.data.getHistory().isnull().sum().to_dict()
        return {
                "columnsNull":[i for i in dataNulls if dataNulls[i] != 0]
                }
    
    def deleteNulls(self):
        self.data.setHistory(self.data.getHistory().dropna())
    
    # Step 3: Identifying atypical values
    # this function could be deleted, if it's possible to render a dinamic histograms in frontend side
    def create_histograms(self) -> dict:
        try:
            self.data.getHistory().hist(figsize=(14,14), xrot=45)
            plt.savefig(f'images/{self.data.getName()}_histograms.png')
            plt.show()
            return {
                "message":"The histograms has been saved into the server succesfully",
                "status" : True
            }
        except Exception as e:
            return {
                "message":"Error: The histograms couldn't been saved into the server",
                "status" : False
            }
    
    def data_statistics(self):
        return self.data.getHistory().describe()
    
    # this function could be deleted, if it's possible to render a dinamic main plots in frontend side
    def create_DataTickerGraphic(self) -> dict:
        try:
            plt.figure(figsize=(20, 5))
            plt.plot(self.data.getHistory()['Open'], color='red', marker='+', label='Open')
            plt.plot(self.data.getHistory()['Close'], color='blue', marker='+', label='Close')
            plt.xlabel('Fecha')
            plt.ylabel('Precio de las acciones')
            plt.title(f'{self.data.getName()}')
            plt.grid(True)
            plt.legend()
            plt.savefig(f'images/{self.data.getName()}_mainGrafic.png')
            plt.show()
            return {
                "message":"The plot has been saved into the server succesfully",
                "status" : True
            }
        except Exception as e:
            return {
                "message":"Error: The plot couldn't been saved into the server",
                "status" : False
            }
            
    # step 4: Identification of relationships between variable pairs
    def getCorrelations(self) -> np:
        return self.data.getHistory().corr()
    
    # this function could be deleted, if it's possible to render a dinamics heatmaps in frontend side
    def getHeatMap(self) -> dict:
        dataCorr = self.getCorrelations()
        try:
            plt.figure(figsize=(14,7))
            MatrizInf = np.triu(dataCorr)
            sns.heatmap(dataCorr, cmap='RdBu_r', annot=True, mask=MatrizInf)
            plt.savefig(f'images/{self.data.getName()}_heatmapCorrelations.png')
            plt.show()
            return {
                "message":"The heatmap has been saved into the server succesfully",
                "status" : True
            }
        except Exception as e:
            return {
                "message":"Error: The heatmap couldn't been saved into the server",
                "status" : False
            }
    def runProcess(self) -> dict:
        try:
            step1 = self.getDescriptionOfData()
            step2 = self.getMissingData()
            step3 = {
                    "histograms_status": self.create_histograms(),
                    "data_statistics" : self.data_statistics().to_dict(),
                    "graphic_status" : self.create_DataTickerGraphic()
                }
            step4 = {
                    "correlations": self.getCorrelations().to_dict(),
                    "heatmap_status": self.getHeatMap()  
                }
            date = datetime.now()
            return {
                "message":"The process was successful",
                "status": True,
                "time_stamp": date,
                "process":{
                    "step1": step1,
                    "step2": step2,
                    "step3": step3,
                    "step4": step4
                }
            }
        except Exception as e:
            return {
                "message":f"something is wrong, Error: {e}",
                "status": False,
                "time_stamp": date
            }


class PCA_algorithm:
    def __init__(self , data, eda):
        self.data : Data = data
        self.eda : EDA_algorithm = eda
        self.MStandard = None
        self.pca_matrix = None
        self.numberOfPrincipalComponents = 0
        self.df_MStandart = None
        self.componentLoads = None
        
    # step 1: Identify possible correlated variables
    def getCorrelations(self) -> np:
        return self.eda.getCorrelations()
    
    # this function could be deleted, if it's possible to render a dinamic heatmps in frontend side
    def getHeatMap(self):
        return self.eda.getHeatMap()
            
    # step 2: Data standardization
    def standardize(self) -> np:
        stData = StandardScaler()
        self.MStandard = stData.fit_transform(self.data.getHistory())
        self.df_MStandart = pd.DataFrame(self.MStandard, columns=self.data.getHistory().columns)
        return self.df_MStandart
    
    # step 3 y 4: The covariance or correlation matrix is calculated, and the components (eigen-vectors) and the variance (eigen-values) are calculated.
    def covariance_matrix(self) -> np.ndarray:
        self.pca_matrix = PCA(n_components=10)
        self.pca_matrix.fit(self.MStandard)
        return self.pca_matrix.components_
    # step 5: The number of principal components is decided
    def setNumberOfPrincipalComponents(self):
        Varianza = self.pca_matrix.explained_variance_ratio_
        for i in range(len(Varianza)):
            s = sum(Varianza[0:i+1])
            if s >= 0.75 and s <= 0.90:
                self.numberOfPrincipalComponents = i+1
                
    def getNumberOfPrincipalComponents(self) -> int:
        self.setNumberOfPrincipalComponents()
        return self.numberOfPrincipalComponents
    
    # this function could be deleted, if it's possible to render a dinamic heatmps in frontend side
    def cumulativeVariance_components(self) -> dict:
        try:
            plt.plot(np.cumsum(self.pca_matrix.explained_variance_ratio_))
            plt.xlabel('Número de componentes')
            plt.ylabel('Varianza acumulada')
            plt.grid()
            plt.savefig(f'images/{self.data.getName()}_numberOfPrincipalComponents_plot.png')
            plt.show()
            return {
                    "message":"The plot of cumulative variance in components has been saved into the server succesfully",
                    "status" : True
                }
        except Exception as e:
            return {
                "message":"Error: The plot of cumulative variance in components couldn't been saved into the server",
                "status" : False
            }
    
    # step 6: The proportion of relevances is examined, check this
    def getComponentLoads(self):
        return self.componentLoads
    
    def dropLessSignificantColumns(self):
        firstComponents = self.getComponentLoads().head(self.numberOfPrincipalComponents + 1)
        columns = []
        for i in firstComponents:
            if len(list(filter(lambda elem : elem >= 0.50 ,firstComponents[i].values))) > 0:
                columns.append(i)
        self.componentLoads = self.getComponentLoads().filter(items = columns)
        
        return self.getComponentLoads()
    
    # Check this function, we need to convert the dataframes to dictionaries
    def runProcess(self):
        try:
            step1 = self.getCorrelations()
            step2 = self.standardize()
            step3_4 = self.covariance_matrix()
            step5 = self.setNumberOfPrincipalComponents()
            step6 = self.dropLessSignificantColumns()
            date = datetime.now()
            return {
                "message":"The process was successful",
                "status": True,
                "time_stamp": date,
                "process":{
                    "step1": step1,
                    "step2": step2,
                    "step3_4": step3_4,
                    "step5": step5,
                    "step6": step6
                }
            }
        except Exception as e:
            date = datetime.now()
            return {
                "message":f"something is wrong, Error: {e}",
                "status": False,
                "time_stamp": date
            }
            
class Model:
    def __init__(self , data ,eda):
        self.data = data
        self.eda = eda
        self.Mdata = data.getHistory().drop(columns = ['Volume', 'Dividends', 'Stock Splits'])
        self.Mdata = self.Mdata.dropna()
        self.X = np.array(self.MData[['Open',
                    'High',
                    'Low']])
        self.Y = np.array(self.MData[['Close']])
        self.X_train = []
        self.X_test = []
        self.Y_train = []
        self.Y_test = []
        self.model = None
        self.Y_Pronostic = []
        
    def set_trainTest(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test = model_selection.train_test_split(self.X, 
                                                                                                self.Y, 
                                                                                                test_size = 0.2, 
                                                                                                random_state = 0, 
                                                                                                shuffle = True
                                                                                                )
    
    def trainModel(self,model):
        self.model = model
        self.model.fit(self.X_train, self.Y_train)
        self.Y_Pronostic = self.model.predict(self.X_test)
    
    def infoModel(self):
        return {
            "criteria" : self.model.criterion,
            "variables_importance" : self.model.feature_importances_,
            "mae": mean_absolute_error(self.Y_test, self.Y_Pronostic),
            "mse": mean_squared_error(self.Y_test, self.Y_Pronostic),
            "rmse": mean_squared_error(self.Y_test, self.Y_Pronostic,squared=False),
            "score": r2_score(self.Y_test, self.Y_Pronostic)
        }
        
    # this function could be deleted, if it's possible to render a dinamic plot in frontend side
    def plotModel(self):
        try:
            plt.figure(figsize=(20, 5))
            plt.plot(self.Y_test, color='red', marker='+', label='Real')
            plt.plot(self.Y_Pronostico, color='green', marker='+', label='Estimado')
            plt.xlabel('Fecha')
            plt.ylabel('Precio de las acciones')
            plt.title(f'Pronóstico de las acciones de {self.data.getName()}')
            plt.grid(True)
            plt.legend()
            plt.savefig(f'images/{self.data.getName()}_plotModel.png')
            plt.show()
            return {
                    "message":"The plot of model has been saved into the server succesfully",
                    "status" : True
                }
        except Exception as e:
            return {
                "message":"Error: The plot of model couldn't been saved into the server",
                "status" : False
            }
    
    def buildModel(self):
        try:
            self.set_trainTest()
            self.trainModel()
            date = datetime.now()
            return {"message":"The model has been created succesfully",
                    "status": True,
                    "time_stamp": date,
                    "model_info": self.infoModel()
                    }
        except Exception as e:
            date = datetime.now()
            return {"message":f"Error, Something is wrong {e}",
                    "status": False,
                    "time_stamp": date 
                    }
        
    # this function receives a df with columns 'Open': [] , 'High': [], 'Low' : []
    def newPronostic(self,stockMarketSharePrice):
        try:
            newPron = self.model.predict(stockMarketSharePrice)[0]
            date = datetime.now()
            return {
                    "message":"The pronostic has been created succesfully",
                    "status": True,
                    "time_stamp": date,
                    "input":{
                        "Open" : stockMarketSharePrice["Open"], 
                        "High" : stockMarketSharePrice["High"], 
                        "Low" : stockMarketSharePrice["Low"]
                        },
                    "output":{
                        "close": newPron
                    }
                }
        except Exception as e:
            date = datetime.now()
            return {
                    "message":f"something is wrong, Error: {e}",
                    "status": False,
                    "time_stamp": date,
                    "input":stockMarketSharePrice,
                    "output":{
                        "close": None
                    }
                }

class randomForestModel(Model):
    def __init__(self , data, eda):
        super().__init__(self, data, eda)
        
    def trainModel(self):
        self.model = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples_split=4, min_samples_leaf=2, random_state=0)
        self.model.fit(self.X_train, self.Y_train)
        self.Y_Pronostic = self.model.predict(self.X_test)
        

class DtreeModel(Model):
    def __init__(self , data, eda):
        super().__init__(self, data, eda)
    
    def trainModel(self):
        self.model = DecisionTreeRegressor(max_depth=10, min_samples_split=4, min_samples_leaf=2, random_state=0)
        self.model.fit(self.X_train, self.Y_train)
        self.Y_Pronostic = self.model.predict(self.X_test)
        
class randomForestModel_Classifier(randomForestModel):
    def __init__(self , data,eda, X, Y):
        super().__init__(self,data,eda)
        self.X = X
        self.Y = Y

class Hybrid_kmeansRandomForest():
    def __init__(self,data):
        self.data = data
        self.eda = EDA_algorithm(data)
        self.Mdata = data.getHistory().drop(columns = ['Open', 'High','Low', 'Stock Splits']) # we select Close, Volume and Dividends
        self.SMdata = StandardScaler().fit_transform(self.Mdata)
        self.knee = KneeLocator(range(2, 10), [KMeans(n_clusters=i, random_state=0).fit(self.SMdata).inertia_ for i in range(2, 10)], curve="convex", direction="decreasing")
        self.MParticional = KMeans(n_clusters= self.knee.elbow, random_state=0).fit(self.SMdata)
        self.randomForest = None
        self.X = []
        self.Y = []
    def __createLabels(self):
        self.MParticional.predict(self.SMdata)
        self.Mdata['cluster'] = self.MParticional.labels_
    
    def clusterize(self):
        self.__createLabels()
        return self.Mdata

    def classify(self):
        try:
            CMdata = self.clusterize()
            self.X = np.array(CMdata.drop(columns = ['cluster']))
            self.Y = np.array(CMdata['cluster'])
            self.randomForest = randomForestModel_Classifier(self.data, self.X, self.Y)
            self.randomForest.buildModel()
            return True
        except Exception as e:
            return False
    
    # this function receives a df with columns 'Close': [] , 'Volume': [], 'Dividends' : [] 
    def newClassification(self,stockMarketSharePrice):
        try:
            if not self.classify():
                raise Exception()
            newPron = self.randomForest.newPronostic(stockMarketSharePrice)[0]
            date = datetime.now()
            return {
                    "message":"The classification has been created succesfully",
                    "status": True,
                    "time_stamp": date,
                    "input":{
                        "Close" : stockMarketSharePrice["Close"], 
                        "Volume" : stockMarketSharePrice["Volume"], 
                        "Dividends" : stockMarketSharePrice["Dividends"]
                        },
                    "output":{
                        "cluster": newPron
                    }
                }
        except Exception as e:
            date = datetime.now()
            return {
                    "message":f"something is wrong, Error: {e}",
                    "status": False,
                    "time_stamp": date,
                    "input":stockMarketSharePrice,
                    "output":{
                        "cluster": None
                    }
                }
    

class SVM(Model):
    def __init__(self,data,eda,kernel):
        super().__init__(self,data, eda)
        self.kernel = kernel
    def trainModel(self):
        self.model = SVC(kernel = self.kernel)
        self.model.fit(self.X_train, self.Y_train)
        self.Y_Pronostic = self.model.predict(self.X_test)