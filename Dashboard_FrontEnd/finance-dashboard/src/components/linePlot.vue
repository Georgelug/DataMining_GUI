<template>
    <div>
        {{ this.history }}
    </div>
</template>

<script>

export default {
    name: 'linePlot',
    props:{
        history: Object
    },
    components:{
        
    },
    data(){
        return {
            chartData:{
                type: 'line',
                series:[
                    {
                        values: this.history.map(e => e.Open)
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