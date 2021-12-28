<template>
    <v-alert dense text type="error" v-show="visible">{{ message }}</v-alert>
</template>


<script>

export default {
    name: "AlertMessage",
    data() {
        return {
            visible: false,
            timeout: 2000,
            message: ""
        }
    },
    methods: {
        show: function(){
            this.visible = true;
            this.hide();
        },
        hide: function(){
            if(this.timeout === -1){
                this.visible = false;
            }else{
                setTimeout(() => {
                    this.visible = false;
                }, this.timeout);
            }
        }
    }
}

</script>