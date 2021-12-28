<template>
    <v-dialog persistent :max-width="maxWidth" v-model="dialog">
        <v-card>
            <v-card-title class="headline">Edit Admin Account</v-card-title>
            <v-card-text>
                <v-form lazy-validation ref="form" v-model="valid">
                    <v-container fluid class="pa-0">
                        <v-row>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field readonly label="Username" type="text" v-model="object.username"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Email" type="email" :rules="rules.email" :error-messages="errors.email" v-model="object.email"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Full Name" type="text" :rules="rules.full_name" :error-messages="errors.full_name" v-model="object.full_name"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Phone Number" type="text" :rules="rules.phone_number" :error-messages="errors.phone_number" v-model="object.phone_number"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                                <v-autocomplete clearable chips multiple label="Permissions" :rules="rules.permission" :errors="errors.permission" :items="permission_list" v-model="object.permissions"></v-autocomplete>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-form>
            </v-card-text>
            <v-card-actions class="pl-6 pr-6">
                <v-spacer></v-spacer>
                <v-btn text @click="close">Close</v-btn>
                <v-btn text color="dark-blue" @click="save">Save Changes</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>


<script>
import { api } from '../../axios-api'

export default {
    name: "AdminEditDialog",
    props: {
        permission_list: {
            type: Array,
            required: true,
            default: []
        },
    },
    data() {
        return {
            dialog: false,
            valid: true,
            object: {},
            errors: {},
            rules: {
                email: [
                    (value) => {
                        if(value && /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(String(value).toLowerCase())){
                            return true;
                        }

                        return 'Email format is invalid';
                    }
                ],
                full_name: [
                    (value) => {
                        if(!value){
                            return "Full Name is required";
                        }

                        if(value.length < 3 || value.length > 100){
                            return "Full Name length must between 3 and 100";
                        }

                        return true;
                    }
                ],
                phone_number: [
                    (value) => !!value || 'Phone Number is required',
                ],
                permission: [
                    (value) => {
                        if(value.length <= 0){
                            return "Permission is required";
                        }
                        return true;
                    }
                ],
            }
        }
    },
    computed:{
        form() {
            return this.$refs.form;
        },
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
        }
    },
    methods: {
        save: function(){
            if(this.form.validate()){
                var object = { "email": this.object.email, "full_name": this.object.full_name,
                               "phone_number": this.object.phone_number, "permissions": JSON.stringify(this.object.permissions) };

                api.put(this.object.details_url, object).then((response) => {
                    if(response.data.status === 200){
                        this.form.reset();
                        this.form.resetValidation();
                        this.$emit("edited");
                        this.close();
                    }else{
                        this.errors = response.data.errors;
                    }
                });
            }
        },
        open: function(){
            this.dialog = true;
        },
        close: function() {
            this.dialog = false;
        },
        reset: function(){
            this.form.reset();
        }
    }
}

</script>