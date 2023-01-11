<template>
    <img :src="histogramlink" class="img-fluid" alt="Responsive image"/>
</template>

<script>

export default {
    name: 'histogramPlot',
    components:{
    },
    props:{
        corr: Object,
        company: String,
    },
    data(){
        return{

        }
    },
    methods:{
        getImage(e){
            e.preventDefault();
            this.axios.get(`http://127.0.0.1:3000/get_histogram/${this.company}`)
            .then((result) => {
                this.res =  result?.data
                console.log(this.res)
            })
            .catch(error =>{
                console.error(error);
            })
        }
    },
    computed:{
        histogramlink(){
            console.log(`http://127.0.0.1:3000/get_histogram/${this.company}`)
            return `http://127.0.0.1:3000/get_histogram/${this.company}`
        }
    }
}
</script>

<style>
    /* .graph{
        margin: 0 auto;
        background-color: center;
    }
    .tooltip{
        background-color: center;
        border: 1px solid black;
        width: 100px;
        opacity: 0;
        color: black;
        position: absolute;
    } */
</style>