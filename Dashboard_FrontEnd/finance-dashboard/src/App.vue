<template>
  <img  src="./assets/logo2.jpg"  class="img-fluid" alt="Responsive image">
  <TickerFinance></TickerFinance>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import TickerFinance from './components/Ticker.vue'


export default {
  name: 'App',
  components: {
    TickerFinance,
  },
  data(){
    return {
      theresData: false
    }
  },
  methods:{
    checkTickerData(value){
            console.log(value);
            this.theresData = value;
    }
  },
  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
