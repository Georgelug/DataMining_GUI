<template>
    <div>
        <div class="card text-center">
            <div class="card-header">
                <h4>Random Forest</h4>
                <div class="col">
                    <button @click='getData' class="btn btn-primary mb-2">Compute</button>
                </div>
            </div>
            <div class="card-body" v-if="checkData">
                <ul class="card-deck">
                    <li class="list-group-item">
                        <div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">
                            <div class="card-header">Information</div>
                            <div class="card-body">
                                <ul>
                                    <li>
                                        <label> Criteria</label>
                                        <p>{{ info?.criteria }}</p>
                                    </li>
                                    <li>
                                        <label> Variables importance</label>
                                        <p>{{ info?.variables_importance }}</p>
                                    </li>
                                    <li>
                                        <label>MAE</label>
                                        <p>{{ info?.mae }}</p>
                                    </li>
                                    <li>
                                        <label>MSE</label>
                                        <p>{{ info?.mse }}</p>
                                    </li>
                                    <li>
                                        <label>RMSE</label>
                                        <p>{{ info?.rmse }}</p>
                                    </li>
                                    <li>
                                        <label>Score</label>
                                        <p>{{ info?.score }}</p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="card text-black bg-light mb-3" style="max-width: 18rem;">
                            <div class="card-header">Plot</div>
                            <div class="card-body">
                                <PlotModel :yTest="toplot?.yTest" :yPronostic="toplot?.yPronostic"></PlotModel>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">
                            <div class="card-header">Pronostic</div>
                            <div class="card-body">
                                <form class="form-group" @submit="getPronostic"  method="post" action="">
                                    <div class="form-group row">
                                        <label>Open</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.Open" :state="true" placeholder="Open value">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label>High</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.High" :state="true" placeholder="High value">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label>Low</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.Low" :state="true" placeholder="Low value">
                                        </div>
                                    </div>

                                    <div class="col-auto">
                                        <input  type="reset" class="btn btn-secondary mb-2" value="reset">
                                    </div>
                                    <div class="col-auto">
                                        <input  type="submit" class="btn btn-primary mb-2" value="Calculate">
                                    </div>
                                    <div class="col-auto">
                                        <p v-if="checkPronostic">
                                            <label>Close: </label>
                                            {{ close }}
                                        </p>
                                    </div>
                                    
                                </form>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import PlotModel from "./plotModel.vue"

export default {
    name: 'RandomForestModel',
    components:{
        PlotModel
    },
    data(){
        return {
            res : null,
            info : null,
            toplot : null,
            close: null,
            posts:{
                Open: '',
                High: '',
                Low: '',
            },
        }
    },
    methods:{
        getData(e){
            e.preventDefault();
            this.axios.get("http://127.0.0.1:3000/Model/randomForest")
            .then((result) => {
                this.res =  result?.data?.randomForest;
                this.info = this.res?.model_info;
                this.toplot = this.res?.toPlot;
                console.log(typeof(this.res))
                console.log(this.info)
            })
            .catch(error =>{
                console.error(error);
            })
        },
        getPronostic(e){
            
            let aux = {
                Open: [this.posts.Open],
                High: [this.posts.High],
                Low: [this.posts.Low],
            }
            
            this.axios.post("http://127.0.0.1:3000/Model/randomForest",aux)
            .then((result)=>{
                this.close = result?.data?.dTree?.output?.close
                console.log(this.close);
            }).catch(error => {
                console.log(error);
            });
            e.preventDefault();
        },
        checkData(){
            return this.res ? true : false;
        },
        checkPronostic(){
            return this.close ? true : false;
        },
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>