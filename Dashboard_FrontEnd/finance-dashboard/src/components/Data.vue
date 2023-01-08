<template>
    <!-- <div v-html="plot"></div> -->
    <div class="mt-5">
        <div class="col-lg8 offset-lg-3">
            <div class="table-responsive">
                <DataTable :data="hist" :columns="columns" :options="{responsive:true, autoWidth:false, dom:'Bfrtip', buttons:btns}" class="table table-striped table-bordered display">
                    <thead>
                        <tr>
                            <th>index</th>
                            <th>Open</th>
                            <th>High</th>
                            <th>Low</th>
                            <th>Close</th>
                            <th>Volume</th>
                            <th>Dividends</th>
                            <th>Stock splits</th>
                        </tr>
                    </thead>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script>
    import {DataFrame} from "danfojs";
    import DataTable from "datatables.net-vue3";
    import DataTablelib from "datatables.net-bs5";
    // import Buttons from "datatables.net-buttons-bs5";
    import ButtonsHtml5 from "datatables.net-buttons/js/buttons.html5";
    // import print from "datatables.net-buttons/js/buttons.print";
    import pdfmake from 'pdfmake';
    import pdfFonts from 'pdfmake/build/vfs_fonts';
    pdfmake.vfs = pdfFonts.pdfMake.vfs;
    import "datatables.net-responsive-bs5";
    import JsZip from "jszip";
    window.JSZip = JsZip;
    DataTable.use(DataTablelib);
    DataTable.use(pdfmake);
    DataTable.use(ButtonsHtml5);
    export default {
        name: 'DataFrameTable',
        props: {
            df: DataFrame,
            hist: null
        },
        components:{
            DataTable
        },
        data(){
            return {
                data:this.hist,
                columns: [
                    {
                        data:null,
                        render: function(data,type,row,meta){
                            return `${meta.row+1}`
                        }
                    },
                    {data: 'Open'},
                    {data: 'High'},
                    {data: 'Low'},
                    {data: 'Close'},
                    {data: 'Volume'},
                    {data: 'Dividends'},
                    {data: 'Stock Splits'},
                ],
                btns: [
                    {
                        title: 'finance report',
                        extend: 'excelHtml5',
                        text: '<i class="fa-solid fa-file-excel"></i> Excel',
                        className: 'btn btn-success',
                    },
                    {
                        title: 'finance report',
                        extend: 'pdfHtml5',
                        text: '<i class="fa-solid fa-file-pdf"></i> PDF',
                        className: 'btn btn-danger',
                    },
                    {
                        title: 'finance report',
                        extend: 'copy',
                        text: '<i class="fa-solid fa-copy"></i> Copy',
                        className: 'btn btn-light',
                    },
                ]
            }
        },
    }
</script>

<style>
    @import 'datatables.net-bs5';
</style>