<template>
    <div>
        <div class="card text-center">
            <div class="card-header">
                <h4>Hybrid model (Kmeans + Random Forest classifier)</h4>
                <div class="col">
                    <button @click='getData' class="btn btn-primary mb-2"> Compute</button>
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
                                        <label> Clusters </label>
                                        <ul>
                                            <li v-for="element in arrCluster" v-bind:key="element">
                                                {{ element }}
                                            </li>
                                        </ul>
                                        <p>{{ info?.criteria }}</p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="card text-black bg-light mb-3" style="max-width: 18rem;">
                            <div class="card-header">Plot</div>
                            <div class="card-body">
                                <PlotModel :yTest="toplot?.yTest" :yPronostic="toplot?.yPronostic" :company="company"></PlotModel>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">
                            <div class="card-header">Classification</div>
                            <div class="card-body">
                                <form class="form-group" @submit="getPronostic"  method="post" action="">
                                    <div class="form-group row">
                                        <label>Close</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.Close" :state="true" placeholder="Open value">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label>Volume</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.Volume" :state="true" placeholder="High value">
                                        </div>
                                    </div>
                                    <div class="form-group row">
                                        <label>Dividends</label>
                                        <div class="col-sm-10">
                                            <input type="number" class="form-control form-control-sm" v-model="posts.Dividends" :state="true" placeholder="Low value">
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
                                            <label>Cluster: </label>
                                            {{ Cluster }}
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
    name: 'HybridModel',
    components:{
        PlotModel
    },
    props:{
        company: String
    },
    data(){
        return {
            res : null,
            info : null,
            toplot : null,
            Cluster: null,
            arrCluster: null,
            posts:{
                Close: '',
                Volume: '',
                Dividends: '',
            },
        }
    },
    methods:{
        getData(e){
            e.preventDefault();
            this.axios.get("http://127.0.0.1:3000/Model/hybrid")
            .then((result) => {
                this.res =  result?.data?.hybridmodel;
                console.log(this.res)
            })
            .catch(error =>{
                console.error(error);
            })
        },
        getPronostic(e){
            
            let aux = {
                Close: [this.posts.Close],
                Volume: [this.posts.Volume],
                Dividends: [this.posts.Dividends],
            }
            
            this.axios.post("http://127.0.0.1:3000/Model/hybrid",aux)
            .then((result)=>{
                console.log(result.data)
                this.Cluster = result?.data?.hybridModel?.output?.cluster
                this.arrCluster = result?.data?.hybridModel?.clusters
                this.toplot = result?.data?.hybridModel?.toPlot
                console.log(this.Cluster);
                console.log(typeof(this.arrCluster));
                console.log(Array.from(this.arrCluster));
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