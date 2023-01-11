<template>
    <h2 class="display-4">Finance dashboard</h2>
    <p class="lead">
        To search for a company listed on the stock market, please fill out all the fields requested
    </p>
    <form class="form-group" @submit="postData"  method="post" action="">
        <div class="form-group row">
            <label class="col-sm-2 col-form-label col-form-label-sm">Name</label>
            <div class="col-sm-10">
                <input type="search" class="form-control form-control-sm" v-model="posts.name" :state="true" placeholder="Company name">
            </div>
        </div>
        <div class="form-group row">
            <label class="col-sm-2 col-form-label col-form-label-sm">Ticker</label>
            <div class="col-sm-10">
                <input type="search" class="form-control form-control-sm" v-model="posts.ticker" :state="true" placeholder="Ticker company">
            </div>
        </div>
        <div class="form-group row">
            <label class="col-sm-2 col-form-label col-form-label-sm">Initial date</label>
            <div class="col-sm-10">
                <input type="date" class="form-control form-control-sm" v-model="posts.date_start" :state="checkDate" name="begin" placeholder="dd-mm-yyyy"  min="1997-01-01" :max="today">
            </div>
        </div>
        <div class="form-group row">
            <label class="col-sm-2 col-form-label col-form-label-sm">Final date</label>
            <div class="col-sm-10">
                <input type="date" class="form-control form-control-sm" v-model="posts.date_end" :state="checkDate" name="end" placeholder="dd-mm-yyyy"  min="1997-01-01" :max="today">
                <small  class="alert alert-danger" role="alert" v-if="checkDate">The initial date has to be smaller than the final date</small>
            </div>
        </div>
        
        <div class="col-auto">
            <input  type="reset" class="btn btn-secondary mb-2" value="reset">
        </div>
        <div class="col-auto">
            <input  type="submit" class="btn btn-primary mb-2" value="search">
        </div>
        
    </form>
    
    <div class="mt-5" v-if="checkData">
        <div class="d-flex justify-content-center" >
            <div class="card text-center" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ posts.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ posts.ticker }}</h6>
                    <ul>
                        <li>Initial date: {{ posts.date_start }}</li>
                        <li>Final date: {{ posts.date_end}}</li>
                    </ul>
                    <div class="col-auto">
                            <button @click='resetData' class="btn btn-danger mb-2">get another ticker data</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <mainPlot :company="company"> </mainPlot>
        </div>
        <div class="card">
            <DataFrameTable :hist=history :company = posts.name></DataFrameTable>
        </div>
        <div class="card">
            <EDA :tickerData="true" :hist=history :company=company></EDA>
        </div>
        <div class="card">
            <PCA :tickerData="true" :company=company></PCA>
        </div>
        <div class="card">
            <PronosticModels :tickerData="true" :company=company></PronosticModels>
        </div>
        <div class="card">
            <HybridModel :tickerData="true" :company=company></HybridModel> 
        </div>

    </div>


</template>
    
<script>
import mainPlot from "./mainPlot.vue"
import {DataFrame} from "danfojs";
import DataFrameTable from './Data.vue'
import EDA from './EDA.vue'
import PCA from './PCA.vue'
import PronosticModels from './Models.vue'
import HybridModel from './PronosticModels/HybridModel.vue'

// import {Series} from 'danfojs/dist/core/series';

export default {
    name: 'TickerFinance',
    components:{
        DataFrameTable,
        EDA,
        PCA,
        PronosticModels,
        HybridModel,
        mainPlot,
    },
    props: {
    },
    data(){
        return {
            posts:{
                ticker: '',
                name: '',
                date_start: '',
                date_end: '',
            },
            res: null,
            history: null,
            dfHistory: null,
            theresData: false,
            company: null
        }
    },
    methods:{
        postData(e){
            this.axios.post("http://127.0.0.1:3000/getData",this.posts)
            .then((result)=>{
                this.res = result?.data?.Data
                this.history = JSON.parse(this.res?.history)
                this.company = this.res?.name;
                console.table(this.company);
                this.dfHistory = new DataFrame(this.history)
                // this.dfHistory.print()
            }).catch(error => {
                console.log(error);
            });
            e.preventDefault();
            // console.table(this.posts);
        },
        resetData(e){
            e.preventDefault();
            this.res = null;
            this.history = null;
        },
        
        // emitResult(){
        //     this.$emit('output', this.res)
        // },
    },
    computed:{
        checkData(){
            return this.res ? true : false
        },
        checkDate(){
            return this.posts.date_start >= this.posts.date_end
        },
        today(){ return new Date().toJSON().slice(0, 10)},
        getHist(){
            return this.history
        }
    }
}

</script>

