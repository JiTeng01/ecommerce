<template>
    <v-dialog persistent :max-width="maxWidth" v-model="dialog">
        <v-card>
            <v-card-title class="headline">Create New Admin Account</v-card-title>
            <v-card-text>
                <v-form lazy-validation ref="form" v-model="valid">
                    <v-container fluid class="pa-0">
                        <v-row>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Username" type="text" :rules="rules.username" :error-messages="errors.username" v-model="object.username"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Email" type="email" :rules="rules.email" :error-messages="errors.email" v-model="object.email"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Password" type="password" :rules="rules.password" :error-messages="errors.password" v-model="object.password"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Repeat Password" type="password" :rules="rules.repeat_password" :error-messages="errors.repeat_password" v-model="object.repeat_password"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Full Name" type="text" :rules="rules.full_name" :error-messages="errors.full_name" v-model="object.full_name"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Phone Number" type="text" :rules="rules.phone_number" :error-messages="errors.phone_number" v-model="object.phone_number"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-select required label="Role" :items="roles" :rules="rules.role" :error-messages="errors.role" v-model="object.role"></v-select>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-form>
            </v-card-text>
            <v-card-actions class="pl-6 pr-6">
                <v-spacer></v-spacer>
                <v-btn text @click="close">Close</v-btn>
                <v-btn text color="dark-blue" @click="create">Create</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>


<script>

import { Base64 } from 'js-base64';
import { api } from '../../axios-api';
export default {
    name: "AdminAddDialog",
    props: {
        roles: {
            type: Array,
            required: true,
            default: () => {}
        }
    },
    data() {
        return {
            dialog: false,
            valid: true,
            object: {},
            errors: {},
            rules: {
                username: [
                    (value) => {
                        if(!value){
                            return "Username is required";
                        }

                        if(value.length < 5 || value.length > 30){
                            return "Username length must between 5 and 30";
                        }

                        var specialCharacters = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
                        if(specialCharacters.test(value)){
                            return "Special characters are not allowed: !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?";
                        }

                        return true;
                    }
                ],
                email: [
                    (value) => {
                        if(value && /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(String(value).toLowerCase())){
                            return true;
                        }

                        return 'Email format is invalid';
                    }
                ],
                password: [
                    (value) => !!value || 'Password is required',
                    (value) => value && value.length >= 6 && value.length <= 20 || 'Password must be between 6 and 20 characters'
                ],
                repeat_password: [
                    (value) => {
                        if(!value){
                            return 'Repeat Password is required';
                        }

                        if(value.length < 6 || value.length > 20){
                            return "Password must be between 6 and 20 characters";
                        }

                        if(this.object.password && this.object.password !== value){
                            return "Password does not match";
                        }

                        return true;
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
                role: [
                    (value) => !!value || 'Role is required',
                ]
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
        create: function(){
            if(this.form.validate()){
                var object = { "username": this.object.username, "password" : Base64.encode(this.object.password),
                               "repeat_password": Base64.encode(this.object.repeat_password), "email": this.object.email,
                               "full_name": this.object.full_name, "phone_number": this.object.phone_number,
                               "role": this.object.role };

                api.post('/api/admin/', object).then((response) => {
                    if(response.data.status === 200) {
                        this.form.reset();
                        this.form.resetValidation();
                        this.$emit("created");
                        this.close();
                    }
                    else {
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