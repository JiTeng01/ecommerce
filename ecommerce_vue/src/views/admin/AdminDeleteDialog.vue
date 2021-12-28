<template>
    <v-dialog persistent :max-width="maxWidth" v-model="dialog">
        <v-card>
            <v-card-title class="headline">Delete Admin</v-card-title>
            <v-card-text>
                <v-container fluid class="pa-0">
                    <v-row>
                        <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                            <error-alert-message ref="errorAlertMessage"></error-alert-message>
                            <v-alert type="warning">Are you sure that you want to delete this admin? </v-alert>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions class="pl-6 pr-6">
                <v-spacer></v-spacer>
                <v-btn text @click="close">Close</v-btn>
                <v-btn text color="red" @click="remove">Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>


<script>

import ErrorAlertMessage from '../utilities/ErrorAlertMessage.vue';
import { api } from '../../axios-api';

export default {
    name: "AdminDeleteDialog",
    components: {
        errorAlertMessage: ErrorAlertMessage,
    },
    data() {
        return {
            dialog: false,
            object: {
                url: ""
            }
        }
    },
    computed:{
        breakpointName() {
            return this.$vuetify.breakpoint.name;
        },
        maxWidth() {
            switch(this.breakpointName){
                case 'md':
                case 'lg':
                case 'xl': return window.screen.width * 0.8; break;
                default: return null; break;
            }
        },
        errorAlertMessage() {
            return this.$refs.errorAlertMessage;
        }
    },
    methods: {
        remove: function(){
           api.delete(this.object.url).then((response) => {
                if(response.data.status === 200){
                    this.$emit("deleted");
                    this.close();
                }else{
                    this.errorAlertMessage.message = response.data.message;
                    this.errorAlertMessage.show();
                }
            });
        },
        open: function(){
            this.dialog = true;
        },
        close: function() {
            this.dialog = false;
        }
    }
}

</script>