import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/auth/LoginPage.vue';

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/wallet', name: 'wallet', component: () => import('../views/user/Wallet') },
  { path: '/home', name: 'home', component: () => import('../views/Home') },
  { path: '/profile', name: 'profile', component: () => import('../views/user/Profile') },
  { path: '/resource', name: 'resource', component: () => import('../views/user/MyResources') },
  { path: '/course', name: 'course', component: () => import('../views/course/course') },
  { path: '/admin', name: 'admin', component: () => import('../views/admin/admin.vue') },
  { path: '/questiondetail/:id', name: 'questiondetail', component: () => import('../views/question/Detail') },
  { path: '/coursedetail/:id', name: 'coursedetail', component: () => import('../views/course/coursedetail') },
  { path: '/register', name: 'register', component: () => import('../views/auth/Register') },
  { path: '/forgot-password', name: 'ForgotPassword', component: () => import('@/views/auth/ForgotPassword.vue')},
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
