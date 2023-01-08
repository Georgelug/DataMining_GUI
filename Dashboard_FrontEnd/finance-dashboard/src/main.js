import * as Vue from 'vue' // in Vue 3
// import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import * as dfd from "danfojs"
import DataTable from 'datatables.net-vue3'
import DataTablesLib from 'datatables.net';
// import {DataFrame} from "danfojs"
// import {Series} from "danfojs"

const app = Vue.createApp(App)
app.mount('#app')
app.use(VueAxios, axios)
DataTable.use(DataTablesLib);
app.use(dfd)
// app.use(DataFrame)
// app.use(Series)
