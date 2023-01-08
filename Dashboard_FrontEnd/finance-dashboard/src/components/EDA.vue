<template>
    <div class="mt-5" v-if="checkTickerData">
        <h1>EDA</h1>
        <div class="col-auto">
            <button @click='getData' class="btn btn-secondary mb-2">Compute EDA</button>
        </div>

        <div class="row" v-if="checkEDAData">
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
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Step 3</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Outlier detection</h6>
                    <!-- <p v-if="this.nulls === null">There's no nulls in data</p>
                    <ul v-if="this.nulls">
                        <li v-for=" item in this.res?.process?.step1?.data_types" v-bind:key="item" >
                            {{ item }} 
                        </li>
                    </ul> -->
                    data_statistics
                    graphic_status
                    histograms_status
                </div>
            </div>
                <h3>{{this.res?.process?.step3}}</h3>
                <h3>{{this.res?.process?.step4}}</h3>
            </div>

    </div>
</template>

<script>
export default {
    name: 'EDA',
    props:{
        tickerData: Boolean
    },
    components:{
    },
    data(){
        return {
            res : null,
            datatypes: this.res?.process?.step1?.data_types,
            nulls: this.res?.process?.step2?.columnsNull.length > 0 ? this.res?.process?.step2?.columnsNull.length : null
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
                console.table(this.res)
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
        }
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>