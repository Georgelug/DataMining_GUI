<template>
    <div>
        <h5>put here the plot</h5>
        {{ yTest }}
        {{ yPronostic }}
    </div>
</template>

<script>
export default {
    name: 'PlotModel',
    components:{
        
    },
    props:{
        yTest : Array, 
        yPronostic : Array, 
    },
    data(){
        return {
        
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