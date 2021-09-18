<template>
  <div class="container">
    <select v-model="currentRoute" @change="setRoute()">
      <option v-for="(route, index) in routes" :key="index">{{ route }}</option>
    </select>
    <div class="card-body d-flex justify-content-around">
        <span>Дата</span>
        <span>Цена</span>
      </div>
    <div class="card" v-for="(r, jndex) in routeData" :key="jndex">
      <div class="card-body row">
        <span class="col-sm">{{ r.date }}</span>
        <span class="col-sm">{{ r.minPrice || "Не объявлено" }} Тенге</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getCalendarByRoute } from "./external_service/backend";

export default defineComponent({
  name: "App",
  data() {
    return {
      routeData: [],
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
        "LED-NQZ",
      ],
      currentRoute: "ALA-NQZ",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    setRoute() {
      this.getData().then((res) => console.log(res));
    },
    async getData() {
      this.routeData = await getCalendarByRoute(this.currentRoute);
      console.log(this.routeData);
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
