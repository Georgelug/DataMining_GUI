<template>
    <div class="mt-5" v-if="checkTickerData">
        <div class="row justify-content-md-center">
            <div class="col col-lg-2">
                <h1>EDA</h1>
            </div>
            <div class="col">
                <button @click='getData' class="btn btn-secondary mb-2">Compute</button>
            </div>
        </div>

        <div class="row justify-content-md-center" v-if="checkEDAData">
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Step 1</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Description of the data structure</h6>
                    <ul>
                        <!-- <li>Initial date: {{ posts.date_start }}</li>
                        <li>Final date: {{ posts.date_end}}</li> -->
                        <li>Company: {{ this.res?.process?.step1?.Company }}</li>
                        <li>Ticker: {{ this.res?.process?.step1?.Ticker }}</li>
                        <li>Shape
                            <ul>
                                <li>Columns: {{this.res?.process?.step1?.Shape.columns}}</li>
                                <li>Rows: {{this.res?.process?.step1?.Shape.rows}}</li>
                            </ul>
                        </li>
                        <li>Data types 
                            <ul>
                                <li v-for=" (item,key) in this.res?.process?.step1?.data_types" v-bind:item="item" v-bind:key="key">
                                    {{ key }}: {{ item }} 
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Step 2</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Identification of missing data</h6>
                    <p v-if="this.nulls === null">There's no nulls in data</p>
                    <ul v-if="this.nulls">
                        <li v-for=" item in this.nulls" v-bind:key="item" >
                            {{ item }} 
                        </li>
                    </ul>
                </div>
            </div>
            <div class="card w-50" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Step 3</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Outlier detection</h6>
                    <ul>
                        <li>
                            <h6>Data statistics</h6>
                            <div class="table-responsive">
                                <table class="table table-striped table-hover table-sm">
                                    <thead class="thead-dark">
                                        <tr>
                                            <th scope="col">Name</th>
                                            <th scope="col">25%</th>
                                            <th scope="col">50%</th>
                                            <th scope="col">75%</th>
                                            <th scope="col">count</th>
                                            <th scope="col">max</th>
                                            <th scope="col">mean</th>
                                            <th scope="col">min</th>
                                            <th scope="col">std</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(key, item) in this.res?.process?.step3?.data_statistics" v-bind:item="item" v-bind:key="key">
                                            {{item}}
                                            <td v-for="element in key" v-bind:key="element">
                                                {{ element }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </li>
                        <li>
                            <h6>Line plot</h6>
                            <linePlot :history="hist"></linePlot>
                        </li>
                        <li>
                            <h6>Histogram plot</h6>
                            <histogramPlot :history="hist"></histogramPlot>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="card w-50" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Step 4</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Identification of relationships between variable pairs</h6>
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
                                        <tr v-for="element in this.corrs" v-bind:key="element">
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
                            <heatMapPlot :corr="corrs"></heatMapPlot>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import linePlot from './linePlot.vue'
import histogramPlot from './histogramPlot.vue'
import heatMapPlot from './heatMapPlot.vue'
export default {
    name: 'EDA',
    props:{
        tickerData: Boolean,
        hist: Object,
    },
    components:{
        linePlot,
        histogramPlot,
        heatMapPlot
    },
    data(){
        return {
            res : null,
            datatypes: this.res?.process?.step1?.data_types,
            nulls: this.res?.process?.step2?.columnsNull.length > 0 ? this.res?.process?.step2?.columnsNull.length : null,
            corrs : null
        }
    },
    methods:{
        getData(e){
            e.preventDefault();
            this.axios.get("http://127.0.0.1:3000/EDA")
            .then((result) => {
                // this.res =  JSON.parse(result?.data);
                console.log(result.data.eda)
                this.res =  result?.data?.eda;
                this.corrs = JSON.parse(this.res?.process?.step4?.correlations)
                console.log()
            })
            .catch(error =>{
                console.error(error);
            })
        },
        checkTickerData(){
            return this.tickerData
        },
        checkEDAData(){
            return this.res ? true : false;
        },
        getDataTypes(){
            return this.res?.process?.step1?.data_types
        },
        checkCorrelationsAllNotNull(){
            return this.res?.process?.step4?.correlations.map(e => !(e.Open && e.High && e.Low && e.Close && e.Volume && e.Dividends && e["Stock Splits"])).length === 0;
        }
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>