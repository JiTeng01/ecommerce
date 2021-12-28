<template>
  <v-container fluid class="pl-4 pr-4 container align-top">
    <v-row>
        <v-col cols="12" xs="6" sm="6" md="3" lg="3" xl="3">
            <v-text-field clearable hide-details label="Username" placeholder="" class="dark-blue--text" v-model="filter.username"></v-text-field>
        </v-col>
        <v-col cols="12" xs="6" sm="6" md="3" lg="3" xl="3">
            <v-text-field clearable hide-details label="Full Name" placeholder="" class="dark-blue--text" v-model="filter.full_name"></v-text-field>
        </v-col>
        <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6" class="pt-6">
            <v-btn dark color="success" class="btn" @click="get">Search</v-btn>
            <v-btn @click="reset">Reset</v-btn>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
            <v-btn dark color="success" @click="openAddDialog" v-if="response.permissions.add_admin">Create New Admin Account</v-btn>
        </v-col>
        <v-col cols="12" sm="12">
            <div>
                <div class="mt-4">
                    <v-data-table hide-default-footer class="elevation-1" :items-per-page="50" :loading="loading" :headers="response.headers" :items="response.items" loading-text="Loading... Please wait" no-data-text="There is no data available">
                        <template v-slot:item="{ item, index }">
                            <tr>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="index + 1"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.username"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.full_name"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.email"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center" v-text="item.phone_number"></td>
                                <td class="text-center text-xs-center text-sm-center text-md-center text-lg-center text-xl-center">
                                    <v-menu bottom offset-y v-if="hasMenu(item)">
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-btn icon v-bind="attrs" v-on="on">
                                                <v-icon>mdi-dots-vertical</v-icon>
                                            </v-btn>
                                        </template>
                                        <v-list dense>
                                            <v-list-item @click="openEditDialog(item)" v-if="item.details_url">
                                                <v-list-item-title>Edit Admin Account</v-list-item-title>
                                            </v-list-item>
                                            <v-list-item @click="openDeleteDialog(item)" v-if="item.details_url">
                                                <v-list-item-title>Delete Admin Account</v-list-item-title>
                                            </v-list-item>
                                            <!-- <v-list-item @click="openPasswordModal(item)" v-if="item.password_url">
                                                <v-list-item-title>Change Password</v-list-item-title>
                                            </v-list-item>
                                            <v-list-item :href="item.permission_url" v-if="item.permission_url">
                                                <v-list-item-title>Manage Permissions</v-list-item-title>
                                            </v-list-item> -->
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
    <admin-add-dialog ref="addDialog" :roles="response.roles" @created="get"></admin-add-dialog>
    <admin-edit-dialog ref="editDialog" :permission_list="response.permission_list" @edited="get"></admin-edit-dialog>
    <admin-delete-dialog ref="deleteDialog" @deleted="get"></admin-delete-dialog>
  </v-container> 
</template>

<script>
import { api } from '../../axios-api'
import AdminAddDialog from './AdminAddDialog.vue'
import AdminEditDialog from './AdminEditDialog.vue'
import AdminDeleteDialog from './AdminDeleteDialog.vue'
export default {

    name: "AdminList",

    components: {
        adminAddDialog: AdminAddDialog,
        adminEditDialog: AdminEditDialog,
        adminDeleteDialog: AdminDeleteDialog,
    },

    data() {
        return {
            loading: true,
            filter: {
                username: "",
                full_name: "",
                page: 1
            },
            response: {
                headers: [],
                roles: [],
                items: [],
                permission_list: [],
                pagination: {},
                permissions: {
                    add_admin: false,
                }
            }
        }
    },

    computed: {
        addDialog() {
            return this.$refs.addDialog;
        },
        editDialog() {
            return this.$refs.editDialog;
        },
        deleteDialog(){
            return this.$refs.deleteDialog;
        }
    },

    mounted: function() {
        this.get();
    },

    methods:{
        openAddDialog: function(){
            this.addDialog.open();
        },

        reset: function(){
            this.filter = { username: "", full_name: "", page: 1 };
            this.get();
        },

        get: function() {
           api.get('/api/admin', {
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

        openEditDialog: function(item){
            this.editDialog.object = item;
            this.editDialog.open();
        },

        openDeleteDialog: function(item){
            this.deleteDialog.object = { url: item.details_url };
            this.deleteDialog.open();
        },

        hasMenu: function(item) {
            return item.details_url || item.password_url || item.permission_url;
        }
    },

};
</script>

<style scoped>
.btn {
    margin-right: 10px !important;
}

</style>
