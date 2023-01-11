<template>
    <div v-if="tickerData">
        <h1>Models</h1>
        <ul class="list-group list-group-flush">
            <li class="list-group-item">
                <DtreeModel :company=company></DtreeModel>
            </li>
            <li class="list-group-item">
                <RandomForestModel :company=company></RandomForestModel>
            </li>
            <li class="list-group-item">
                <SVMModel :company=company></SVMModel>
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
        company: String
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