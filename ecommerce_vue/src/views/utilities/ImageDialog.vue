<template>
    <v-dialog persistent :max-width="maxWidth" v-model="dialog">
        <v-card class="mx-auto">
            <v-img contain class="white--text align-end image-center" :width="maxWidth" :src="imageUrl"></v-img>
            <v-card-actions class="pl-4 pr-4">
                <v-spacer></v-spacer>
                <v-btn text @click="close">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>


<script>

export default {
    name: "SuccessUploadDialog",
    data() {
        return {
            dialog: false,
            imageUrl: ""
        }
    },
    computed:{
        breakpointName() {
            return this.$vuetify.breakpoint.name;
        },
        height() {
            switch(this.breakpointName){
                case 'xs':
                case 'sm': return window.screen.height * 0.6; break;
                default: return null; break;
            }
        },
        maxWidth() {
            switch(this.breakpointName){
                case 'md':
                case 'lg':
                case 'xl': return (window.screen.width * 0.8) / 2; break;
                default: return null; break;
            }
        }
    },
    methods: {
        open: function() {
            this.dialog = true;
        },
        close: function() {
            this.dialog = false;
        }
    }
}

</script>


<style scoped>

.image-center {
    margin: 0 auth !important;
}

</style>