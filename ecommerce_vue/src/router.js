import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
var VueCookie = require('vue-cookie')
export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            component: () => import('@/layouts/Layout'),
            children: [
                // Components
                {
                    name: 'login',
                    path: '',
                    component: () => import('@/views/account/LoginForm')
                },
                {
                    name: 'admins',
                    path: 'admins',
                    component: () => import('@/views/admin/AdminList'),
                    beforeEnter: (to, form, next) => {
                        if(!VueCookie.get('accesstoken')){
                            next("/")
                        }
                        else{
                            next()
                        }
                    },
                    meta: { auth: true, page_title: 'Admin Managment' },
                },
                {
                    name: 'products',
                    path: 'products',
                    component: () => import('@/views/product/ProductList'),
                    beforeEnter: (to, form, next) => {
                        if(!VueCookie.get('accesstoken')){
                            next("/")
                        }
                        else{
                            next()
                        }
                    },
                    meta: { auth: true, page_title: 'Product Managment' },
                },
                {
                    name: 'product information',
                    path: 'products/:id/edit',
                    component: () => import('@/views/product/ProductEdit'),
                    beforeEnter: (to, form, next) => {
                        if(!VueCookie.get('accesstoken')){
                            next("/")
                        }
                        else{
                            next()
                        }
                    },
                    meta: { auth: true, page_title: 'Product Edit' },
                }
               
            ]
        },
        
    ],
})
