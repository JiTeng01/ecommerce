<template>
  <v-container fluid class="pl-4 pr-4 container align-top">
    <v-row>
        <v-col cols="12" xs="6" sm="6" md="3" lg="3" xl="3">
            <v-text-field clearable hide-details label="Code" placeholder="" class="dark-blue--text" v-model="filter.code"></v-text-field>
        </v-col>
        <v-col cols="12" xs="6" sm="6" md="3" lg="3" xl="3">
            <v-text-field clearable hide-details label="Name" placeholder="" class="dark-blue--text" v-model="filter.name"></v-text-field>
        </v-col>
        <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6" class="pt-6">
            <v-btn dark color="success" class="btn" @click="get">Search</v-btn>
            <v-btn @click="reset">Reset</v-btn>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
            <v-btn dark color="success" @click="openAddDialog">Create New Product</v-btn>
        </v-col>
        <v-col cols="12" sm="12">
            <div>
                <div class="mt-4">
                    <v-data-table hide-default-footer class="elevation-1" :items-per-page="50" :loading="loading" :headers="response.headers" :items="response.items" loading-text="Loading... Please wait" no-data-text="There is no data available">
                        <template v-slot:item="{ item, index }">
                            <tr>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="index + 1"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.code"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.name"></td>
                                <td>
                                    <v-img :src="item.image" class="image-center image-pointer" width="70" @click="openImageDialog(item)"></v-img>
                                </td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.price"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center">
                                    <v-menu bottom offset-y>
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-btn icon v-bind="attrs" v-on="on">
                                                <v-icon>mdi-dots-vertical</v-icon>
                                            </v-btn>
                                        </template>
                                        <v-list dense>
                                            <v-list-item :to="getEditUrl(item.id)">
                                                <v-list-item-title>Edit Product</v-list-item-title>
                                            </v-list-item>
                                        </v-list>
                                    </v-menu>
                                </td>
                            </tr>
                        </template>
                    </v-data-table>
                </div>
            </div>
        </v-col>
    </v-row>
    <product-add-dialog ref="addDialog" @created="get"></product-add-dialog>
    <image-dialog ref="dialog"></image-dialog>
    <!-- <admin-edit-dialog ref="editDialog" :permission_list="response.permission_list" @edited="get"></admin-edit-dialog>
    <admin-delete-dialog ref="deleteDialog" @deleted="get"></admin-delete-dialog> -->
  </v-container> 
</template>

<script>
import { api } from '../../axios-api'
import ProductAddDialog from './ProductAddDialog.vue'
import ImageDialog from '../utilities/ImageDialog.vue';
export default {

    name: "ProductList",

    components: {
       imageDialog: ImageDialog,
       productAddDialog: ProductAddDialog,
    },

    data() {
        return {
            loading: true,
            filter: {
                code: "",
                name: "",
                page: 1
            },
            response: {
                headers: [],
                items: [],
                pagination: {},
            }
        }
    },

    computed: {
        dialog() {
            return this.$refs.dialog;
        },
        addDialog() {
            return this.$refs.addDialog;
        },
    },

    mounted: function() {
        this.get();
    },

    methods:{
        openAddDialog: function(){
            this.addDialog.open();
        },

        reset: function(){
            this.filter = { code: "", name: "", page: 1 };
            this.get();
        },

        get: function() {
           api.get('/api/product', {
               params: this.filter
           })
            .then(response => {
                this.response = response.data;
                this.loading = false;
            })
            .catch(err => {
                console.log(err)
            })
        },
        openImageDialog: function(item){
            this.dialog.imageUrl = item.image;
            this.dialog.open();
        },

        openEditDialog: function(item){
            this.editDialog.object = item;
            this.editDialog.open();
        },

        getEditUrl: function(id) {
            return 'products/' + id + '/edit'
        }
    },

};
</script>

<style scoped>
.btn {
    margin-right: 10px !important;
}

.image-center {
    margin: 0 auto !important;
}

.image-pointer {
    cursor: pointer !important;
}

</style>
