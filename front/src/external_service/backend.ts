import axios from "axios"

const URL = "http://localhost:8000"

export interface Route{
    Data: Object
}

export async function getCalendarByRoute(routeName: string): Promise<any> {
    const res = await axios.get(`${URL}/${routeName}`)
    return res.data
}