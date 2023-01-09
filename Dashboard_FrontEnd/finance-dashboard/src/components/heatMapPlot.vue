<template>
    <div>
        {{ this.corr }}
    </div>
</template>

<script>

export default {
    name: 'heatMapPlot',
    props:{
        corr: Array
    },
    components:{
        
    },
    data(){
        return {
            chartData:{
                type: 'line',
                series:[
                    {
                        values: null
                    }
                ]
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