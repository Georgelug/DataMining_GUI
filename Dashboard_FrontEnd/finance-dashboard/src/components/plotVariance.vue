<template>
    <div class="col">
        <!-- <button @click='getImage' class="btn btn-secondary mb-2">get image</button> -->
        <img :src="variancelink" class="img-fluid" alt="Responsive image"/>
    </div>
</template>

<script>

export default {
    name: 'variancePlot',
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
        // getImage(e){
        //     e.preventDefault();
        //     this.axios.get(`http://127.0.0.1:3000/get_histogram/${this.company}`)
        //     .then((result) => {
        //         this.res =  result?.data
        //         console.log(this.res)
        //     })
        //     .catch(error =>{
        //         console.error(error);
        //     })
        // }
    },
    computed:{
        variancelink(){
            return `http://127.0.0.1:3000/get_plotVariance/${this.company}`
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