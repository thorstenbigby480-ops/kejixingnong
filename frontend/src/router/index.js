import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', name: 'home', component: () => import('../views/HomeView.vue') },
      { path: 'policy', name: 'policy', component: () => import('../views/PolicyView.vue') },
      { path: 'analysis', name: 'analysis', component: () => import('../views/AnalysisView.vue') },
      { path: 'mall', name: 'mall', component: () => import('../views/MallView.vue') },
      { path: 'case', name: 'case', component: () => import('../views/CaseView.vue') },
      { path: 'dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
      { path: 'user', name: 'user', component: () => import('../views/UserView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
