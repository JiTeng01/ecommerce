<template>
    <v-dialog persistent :max-width="maxWidth" v-model="dialog">
        <v-card>
            <v-card-title class="headline">Create New Product</v-card-title>
            <v-card-text>
                <v-form lazy-validation ref="form" v-model="valid">
                    <v-container fluid class="pa-0">
                        <v-row>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Code" type="text" :rules="rules.code" :error-messages="errors.code" v-model="object.code"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field required label="Name" type="text" :rules="rules.name" :error-messages="errors.name" v-model="object.name"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                                <v-textarea label="Description" name="description" :error-messages="errors.description" v-model="object.description"></v-textarea>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                                <v-file-input clearable label="Image" name="image" :rules="rules.image" :error-message="errors.image" accept="image/*" v-model="object.cover"></v-file-input>
                            </v-col>
                             <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field label="Price" type="text" :rules="rules.price" :error-messages="errors.price" v-model="object.price"></v-text-field>
                            </v-col>
                            <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                                <v-text-field label="Discount" type="number" :rules="rules.discount" :error-messages="errors.discount" v-model="object.discount"></v-text-field>
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
    name: "ProductAddDialog",
    data() {
        return {
            dialog: false,
            valid: true,
            object: {},
            errors: {},
            rules: {
                name: [
                    (value) => {
                        if(!value){
                            return "Name is required";
                        }

                        if(value.length < 5 || value.length > 3030){
                            return "Name length must between 5 and 3030";
                        }

                        return true;
                    }
                ],
                code: [
                    (value) => {
                        if(!value){
                            return "Code is required";
                        }

                        if(value.length < 3 || value.length > 100){
                            return "Code length must between 3 and 100";
                        }

                        return true;
                    }
                ],
                description: [
                    (value) => !!value || 'Description is required',
                ],
                price: [
                    (value) => !!value || 'Price is required',
                ],
                image: [
                    (value) => !!value || 'Image is required'
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
        create: function(){
            if(this.form.validate()){
                this.getImageBase64URL();
                setTimeout(() => {
                    var object = {"code": this.object.code, "name": this.object.name,
                               "image": this.object.image, "description": this.object.description,
                               "price": this.object.price, "discount": this.object.discount};
                    api.post('/api/product/', object).then((response) => {
                    if(response.data.status === 200) {
                        this.form.reset();
                        this.$emit("created");
                        this.close();
                    }
                    else {
                        this.errors = response.data.errors;
                    }
                });
                }, 1000);
            }
        },
        getImageBase64URL: function(){
            var reader = new FileReader();
            reader.readAsDataURL(this.object.cover);
            reader.addEventListener('load', (readerEvent) => {
                var image = new Image();
                image.addEventListener('load', () => {
                    var canvas = document.createElement('canvas'),
                        width = image.width * 0.6,
                        height = image.height * 0.6;

                    canvas.width = width;
                    canvas.height = height;
                    canvas.getContext('2d').drawImage(image, 0, 0, width, height);
                    this.object.image = canvas.toDataURL('image/jpeg');
                });
                image.src = readerEvent.target.result;
            })

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