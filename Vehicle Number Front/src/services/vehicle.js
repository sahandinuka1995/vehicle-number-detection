/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 17/12/2021 - 8:43 PM
 */
import api from './apiHandler'

export async function addVehicle(data) {
    let apiConfig = {}
    apiConfig.url = `vehicle`
    apiConfig.type = 'POST'
    apiConfig.body = data
    return await api(apiConfig)
}

export async function getAllVehicles() {
    let apiConfig = {}
    apiConfig.url = `vehicle`
    apiConfig.type = 'GET'
    apiConfig.body = null
    return await api(apiConfig)
}
