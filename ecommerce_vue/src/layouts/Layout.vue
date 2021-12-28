<template>
  <v-app id="inspire">
    <Header v-model="expandOnHover" v-if="this.$router.currentRoute.name !== 'login'"></Header>
    <Sidebar :expand-on-hover.sync="expandOnHover" v-if="this.$router.currentRoute.name !== 'login'"></Sidebar>
    <v-main>
      <v-container class="" fluid>
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
import Header from "./header/Header";
import Sidebar from "./sidebar/Sidebar";
import { mapState, mapMutations } from "vuex";
export default {
  name: "Layout",

  components: {
    Header,
    Sidebar,
  },

  props: {
    source: String
  },
  data: () => ({
    expandOnHover: false
  }),
  computed: {
    ...mapState(["Customizer_drawer"])
  },

  methods: {
    ...mapMutations({
      setCustomizerDrawer: "SET_CUSTOMIZER_DRAWER"
    })
  }
};
</script>
