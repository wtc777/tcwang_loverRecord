import { createRouter, createWebHistory } from 'vue-router'

const routes = [
	{
		path: '/',
		name: 'login',
		component: () => import('../pages/Login.vue')
	},
        {
                path: '/register',
                name: 'register',
                component: () => import('../pages/Register.vue')
        },
        {
                path: '/dashboard',
                component: () => import('../pages/Dashboard.vue'),
                children: [
			{
				path: '',
				name: 'timeline',
				component: () => import('../pages/Timeline.vue')
			},
			{
				path: 'calendar',
				name: 'calendar',
				component: () => import('../pages/Calendar.vue')
			},
			{
				path: 'photos',
				name: 'photos',
				component: () => import('../pages/Photos.vue')
			}
		]
	}
]

const router = createRouter({
        history: createWebHistory(),
        routes
})

export default router
