import { defineComponent } from "@vue/runtime-core";
import { reactive } from "@vue/reactivity";
import { Route, getCalendarByRoute } from "./external_service/backend";

export const App = defineComponent({
    async setup() {
        const routeName = await getCalendarByRoute("ALA-NQZ")
        const routeData = reactive<Route>(routeName)
        console.log(routeData)
        return (h: any) => (
            <div>dsa</div>
        )
    },
});