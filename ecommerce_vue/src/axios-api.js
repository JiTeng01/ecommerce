import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"

var VueCookie = require('vue-cookie')
const api = axios.create({
    baseURL: '/',
    headers: {
        // "Content-Type": "application/x-www-form-urlencoded",
        "Access-Control-Allow-Origin": "*",
        "Authorization": "Token " + VueCookie.get('accesstoken')
    }
})

export { api }