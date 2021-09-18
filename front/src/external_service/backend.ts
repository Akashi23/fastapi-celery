import axios from "axios"

const URL = "http://localhost:8000"

export interface Route{
    Data: Object
}

export async function getCalendarByRoute(routeName: string): Promise<Route> {
    const res = await axios.get(`${URL}/${routeName}`)
    console.log(res.data)
    return res.data
}