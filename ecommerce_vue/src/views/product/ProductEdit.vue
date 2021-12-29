<template>
    <v-container fluid class="pl-4 pr-4 container">
        <v-form lazy-validation ref="form" v-model="valid">
            <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                <success-alert-message ref="successAlertMessage"></success-alert-message>
                <error-alert-message ref="errorAlertMessage"></error-alert-message>
            </v-col>
            <v-row>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                    <v-img :src="object.image_url" class="image-center image-pointer" width="100"></v-img>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                    <v-text-field readonly label="Code" v-model="object.code"></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                    <v-text-field label="Name" v-model="object.name"></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                    <v-textarea label="Description" :error-messages="errors.description" v-model="object.description"></v-textarea>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                    <v-text-field label="price" :rules="rules.price" :error-messages="errors.price" v-model="object.price"></v-text-field>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                    <v-file-input label="Image" name="image" :rules="rules.image" :error-message="errors.image" accept="image/*" v-model="object.cover"></v-file-input>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12">
                    <v-text-field label="Discount" type="number" :error-messages="errors.discount" v-model="object.discount"></v-text-field>
                </v-col>
            </v-row>
        </v-form>
        <v-row>
            <v-col cols="12" xs="12" sm="12" md="12" lg="12" xl="12" class="text-right">
                <v-btn class="mr-2" @click="back">Back</v-btn>
                <v-btn  dark color="success" class="btn" @click="save">Save Changes</v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>

import ErrorAlertMessage from '../utilities/ErrorAlertMessage.vue'
import SuccessAlertMessage from '../utilities/SuccessAlertMessage.vue'
import { api } from '../../axios-api';
export default {
    name: "ProductEdit",
    components: {
        errorAlertMessage: ErrorAlertMessage,
        successAlertMessage: SuccessAlertMessage
    },
    data() {
        return {
            isUpdating: false,
            valid: true,
            errors: {},
            rules: {
                description: [
                    (value) => !!value || 'Description is required',
                ],
                price: [
                   (value) => !!value || 'Price is required'
                ],
                name: [
                    (value) => !!value || 'Name is required'
                ],
            },
            object: {
                forbidden_period: {
                    start_time: "",
                    end_time: "",
                    message:""
                }
            },
            tags: []
        }
    },
    mounted: function(){
        this.get();
    },
    computed: {
        form() {
            return this.$refs.form;
        },
        successAlertMessage() {
            return this.$refs.successAlertMessage;
        },
        errorAlertMessage() {
            return this.$refs.errorAlertMessage;
        }
    },
    methods: {
        get: function() {
           api.get('/api/product/'+ this.$route.params.id)
            .then(response => {
                this.object = response.data.object;
                this.loading = false;
            })
            .catch(err => {
                console.log(err)
            })
        },
        save: function(){
            if(this.form.validate()){
                this.isUpdating = true;
                if(this.object.cover){
                    this.getImageBase64URL();
                }
                setTimeout(() => {
                   var object = {"name": this.object.name, "image": this.object.image, "description": this.object.description,
                                "price": this.object.price, "discount": this.object.discount};
                   api.put('/api/product/'+ this.$route.params.id +'/', object).then((response) => {
                        if(response.data.status === 200){
                            this.successAlertMessage.message = response.data.message;
                            this.successAlertMessage.show();
                            this.get();
                        }else{
                            this.errors = response.data.errors;
                            this.errorAlertMessage.message = response.data.message;
                            this.errors = response.data.errors;
                        }
                    });
                }, 2000);

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
        back: function() {
            history.back();
        }
        
    }
}

</script>

<style scoped>

.image-center {
    margin: 0 auto !important;
}

.image-pointer {
    cursor: pointer !important;
}

.mr-2 {
    margin-right: 2%;
}

</style>