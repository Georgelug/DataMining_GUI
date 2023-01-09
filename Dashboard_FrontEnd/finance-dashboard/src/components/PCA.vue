<template>
    <div class="mt-5" v-if="checkTickerData">
        <div class="row justify-content-md-center">
            <div class="col col-lg-2">
                <h1>PCA</h1>
            </div>
            <div class="col">
                <button @click='getData' class="btn btn-secondary mb-2">Compute</button>
            </div>
        </div>
    </div>
    <div class="row justify-content-md-center" v-if="checkPCAData">
        <div class="card w-50" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Step 1</h5>
                <h6 class="card-subtitle mb-2 text-muted">Evidence of possibly correlated variables</h6>
                <ul>
                    <li>
                            <h6>Correlations</h6>
                            <div class="table-responsive">
                                <table class="table table-striped table-hover table-sm">
                                    <thead class="thead-dark">
                                        <tr>
                                            <th scope="col">Open</th>
                                            <th scope="col">High</th>
                                            <th scope="col">Low</th>
                                            <th scope="col">Close</th>
                                            <th scope="col">Volume</th>
                                            <th scope="col">Dividens</th>
                                            <th scope="col">Stock Splits</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="element in this.step1" v-bind:key="element">
                                            <td>
                                                {{ element.Open }}
                                            </td>
                                            <td>
                                                {{ element.High }}
                                            </td>
                                            <td>
                                                {{ element.Low }}
                                            </td>
                                            <td>
                                                {{ element.Close }}
                                            </td>
                                            <td>
                                                {{ element.Volume }}
                                            </td>
                                            <td>
                                                {{ element.Dividends }}
                                            </td>
                                            <td>
                                                {{ element["Stock Splits"] }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                    </li>
                    <li>
                        <h6>Heatmap</h6>
                        <heatMapPlot :corr="step1"></heatMapPlot>
                    </li>
                </ul>
            </div>
        </div>
        <div class="card w-50" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Step 2</h5>
                <h6 class="card-subtitle mb-2 text-muted">Data standardization.</h6>
                <ul>
                    <li>
                        <h6>Standardized data</h6> 
                        <div class="table-responsive">
                            <table class="table table-striped table-hover table-sm">
                                <thead class="thead-dark">
                                    <tr>
                                        <th scope="col">Open</th>
                                        <th scope="col">High</th>
                                        <th scope="col">Low</th>
                                        <th scope="col">Close</th>
                                        <th scope="col">Volume</th>
                                        <th scope="col">Dividens</th>
                                        <th scope="col">Stock Splits</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="element in this.step2" v-bind:key="element">
                                        <td>
                                            {{ element.Open }}
                                        </td>
                                        <td>
                                            {{ element.High }}
                                        </td>
                                        <td>
                                            {{ element.Low }}
                                        </td>
                                        <td>
                                            {{ element.Close }}
                                        </td>
                                        <td>
                                            {{ element.Volume }}
                                        </td>
                                        <td>
                                            {{ element.Dividends }}
                                        </td>
                                        <td>
                                            {{ element["Stock Splits"] }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <div class="card w-50" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Step 3 and 4</h5>
                <h6 class="card-subtitle mb-2 text-muted">The covariance or correlation matrix is calculated, and the components (eigen-vectors) and the variance (eigen-values) are calculated.</h6>
                <ul>
                    <li>
                        <h6>Covariance matrix</h6>
                        <div class="table-responsive">
                            <table class="table table-striped table-hover table-sm">
                                <thead class="thead-dark">
                                    <tr>
                                        <th scope="col">Open</th>
                                        <th scope="col">High</th>
                                        <th scope="col">Low</th>
                                        <th scope="col">Close</th>
                                        <th scope="col">Volume</th>
                                        <th scope="col">Dividens</th>
                                        <th scope="col">Stock Splits</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="element in this.step3_4" v-bind:key="element">
                                        <td v-for="item in element" v-bind:key="item">
                                            {{ item }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Step 5</h5>
                <h6 class="card-subtitle mb-2 text-muted">The number of principal components is decided</h6>
                <ul>
                    <li>
                        <h6>Number of principal components: {{ step5 }}</h6> 
                    </li>
                </ul>
            </div>
        </div>
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Step 6</h5>
                <h6 class="card-subtitle mb-2 text-muted">The proportion of relevances –loads– is examined</h6>
                <ul>
                    <li>
                        <h6>Component loads</h6> 
                        <div class="table-responsive">
                            <table class="table table-striped table-hover table-sm">
                                <thead class="thead-dark">
                                    <tr>
                                        <th scope="col">index</th>
                                        <th scope="col">Volume</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(element , key) in this.step6" v-bind:key="element">
                                        <td>
                                            {{ key }}
                                        </td>
                                        <td>
                                            {{ element.Volume }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import heatMapPlot from './heatMapPlot.vue'
export default {
    name: 'PCA',
    props:{
        tickerData: Boolean,
        hist: Object,
        corrs : Object
    },
    components:{
        heatMapPlot
        
    },
    data(){
        return {
            res : null,
            step1 : null,
            step2 : null,
            step3_4 : null,
            step5 : null,
            step6 : null,
        }
    },
    methods:{
        getData(e){
            e.preventDefault();
            this.axios.get("http://127.0.0.1:3000/PCA")
            .then((result) => {
                this.res =  result?.data?.pca?.process;
                console.log(typeof(this.res))
                console.table(this.res)
                this.step1= JSON.parse(this.res.step1.correlations)
                this.step2= JSON.parse(this.res.step2.standardized_dataFrame)
                this.step3_4= this.res.step3_4.covariance_matrix
                this.step5= this.res.step5.n_PrincipalComponents
                this.step6= JSON.parse(this.res.step6.componentLoads)
                console.log(this.step6)
                console.table(this.step6)

            })
            .catch(error =>{
                console.error(error);
            })
        },
        checkTickerData(){
            return this.tickerData
        },
        checkPCAData(){
            return this.res ? true : false;
        },
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>