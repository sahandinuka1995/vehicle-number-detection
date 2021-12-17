/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 17/12/2021 - 8:37 PM
 */
import axios from "axios";
import {endpoint} from './apiconfig'

export default async function api(apiConfig) {
    let result = ""
    await axios({
        method: apiConfig.type,
        url: `${endpoint.host}/${apiConfig.url}`,
        // data: apiConfig.body
    }).then(async (res) => {
        result = await res
    });

    return result
}
