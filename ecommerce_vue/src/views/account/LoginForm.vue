<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Login form</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-form lazy-validation method="post" ref="form" v-model="valid">
                           <v-text-field :rules="rules.username" :error-messages="errors.username" prepend-icon="mdi-account-circle" name="login" label="Login" v-model="object.username" type="text"></v-text-field>
                           <v-text-field :rules="rules.password" :error-messages="errors.password" id="password" prepend-icon="mdi-lock" name="password" label="Password" v-model="object.password" type="password"></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary"  @click="submit">Login</v-btn>
                     </v-card-actions>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
import { Base64 } from 'js-base64';
import { api } from '../../axios-api'
export default {
    name: 'LoginForm',
    data() {
        return {
            valid: true,
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
                password: [
                    (value) => !!value || 'Password is required',
                    (value) => value && value.length >= 6 && value.length <= 20 || 'Password must be between 6 and 20 characters'
                ]
            },
            object: {
                username: 'superadmin',
                password: '123123'
            },
            errors: {}
        }
    },

    methods: {
        submit: function() {
            if (this.$refs.form.validate()) {
                var object = { "password" : Base64.encode(this.object.password), "username": this.object.username };
                api.post('/api/login/', object).then((response) => {
                    if(response.data.status === 200){
                        this.$router.push({name: 'admins'})
                    }else{
                        console.log(response)
                        this.errors = response.data.errors;
                    }
                });
            }
        }
    }
};
</script>

<style>
.flex{
    max-width: 30% !important;
}
</style>
