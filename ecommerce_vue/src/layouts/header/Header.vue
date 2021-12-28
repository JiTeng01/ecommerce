<template>
  <v-app-bar app clipped-left clipped-right color="primary" dark>
    <v-toolbar-title class="align-center d-flex">
      <span class="logo-icon">
        <img src="../../assets/logo-light-icon.png" />
      </span>
      <span class="logo-text ml-2">
        <span>Vue Ecommerce</span>
      </span>
    </v-toolbar-title>
    <v-app-bar-nav-icon
      class="d-block d-md-none"
      @click="$vuetify.breakpoint.smAndDown ? setSidebarDrawer(!Sidebar_drawer) : $emit('input', !value)"
    />
    <v-spacer />
    <!---right part -->
    <v-btn dark color="success" href="https://www.wrappixel.com/templates/materialpro-vuetify-admin/">Upgrade to Pro</v-btn>
    <v-menu bottom left transition="scale-transition">
      <template v-slot:activator="{ on }">
        <v-btn dark icon v-on="on">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item v-for="(item, i) in userprofile" :key="i" @click="href">
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
         <v-list-item @click="logout">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>
<script>
// Utilities
import { mapState, mapMutations } from "vuex";

export default {
  name: "Header",

  components: {},

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    userprofile: [
      { title: "My Profile" },
      { title: "My Balance" },
      { title: "Inbox" },
      { title: "Account Setting" },
    ],
    href() {
      return undefined;
    }
  }),

  computed: {
    ...mapState(["Sidebar_drawer"])
  },

  methods: {
    logout: function(){
      var VueCookie = require('vue-cookie')
      VueCookie.delete('accesstoken')
      this.$router.push({name:'login'})
    },
    ...mapMutations({
      setSidebarDrawer: "SET_SIDEBAR_DRAWER"
    })
  }
};
</script>