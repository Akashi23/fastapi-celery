<template>
  <div>
    <select v-model="currentRoute">
    <option v-for="(route, index) in routes" :key="index" @click="setRoute(route)">{{route}}</option>
    </select>
    <div v-for="(r, jndex) in routeData[currentRoute]" :key="jndex">{{r}}</div>
    {{currentRoute}}
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getCalendarByRoute } from "./external_service/backend";
// import Calendar from "./Calendar.vue"

export default defineComponent({
  name: "App",
  components: {
    // Calendar
  },
  data() {
    return {
      routeData: undefined,
      routes: [
        "ALA-NQZ",
        "NQZ-ALA",
        "ALA-VKO",
        "VKO-ALA",
        "ALA-CIT",
        "CIT-ALA",
        "NQZ-VKO",
        "VKO-NQZ",
        "NQZ-LED",
        "LED-NQZ"
      ],
      currentRoute: "ALA-NQZ",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    setRoute(){
      this.getData().then((res)=> console.log(res))
    },
    async getData() {
      let routeData = await getCalendarByRoute(this.currentRoute);
      this.routeData = routeData;
      console.log(routeData);
    },
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
