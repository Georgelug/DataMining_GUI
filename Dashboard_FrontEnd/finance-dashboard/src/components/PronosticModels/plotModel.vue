<template>
    <Line :data="data" :options="options" />
    
</template>

<script>

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'
// import * as chartConfig from './chartConfig.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'PlotModel',
    components:{
        Line
    },
    props:{
        yTest : Array, 
        yPronostic : Array, 
    },
    data(){
        return{
            data : {
                labels: this.yTest,
                datasets: [
                {
                    label: 'Data One',
                    backgroundColor: '#f87979',
                    data: this.yPronostic
                }
                ]
            },
            options : {
                responsive: true,
                maintainAspectRatio: true
            }
        }
    },
    methods:{
        
    },
    computed:{
        
    }
}
</script>

<style>
    
</style>