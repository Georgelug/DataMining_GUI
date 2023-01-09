<template>
    <div>
        <h1>Models</h1>
        <ul class="list-group list-group-flush">
            <li class="list-group-item">
                <DtreeModel></DtreeModel>
            </li>
            <li class="list-group-item">
                <RandomForestModel></RandomForestModel>
            </li>
            <li class="list-group-item">
                <SVMModel></SVMModel>
            </li>
        </ul>
    </div>
</template>

<script>
import DtreeModel from "./PronosticModels/DtreeModel.vue"
import RandomForestModel from "./PronosticModels/RForestModel.vue"
import  SVMModel from "./PronosticModels/SVMModel.vue"
export default {
    name: 'PronosticModels',
    components:{
        DtreeModel,
        RandomForestModel,
        SVMModel,
    },
    props:{
        tickerData: Boolean,
    },
    data(){
        return {
        
        }
    },
    methods:{
        checkTickerData(){
            return this.tickerData
        },
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>