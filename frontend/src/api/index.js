import axios from 'axios'
import { ElMessage } from 'element-plus'

// 支持环境变量配置 API baseURL，方便本地/生产环境切换
// 本地开发：默认 http://localhost:8000/api
// 生产部署：在 Vercel 配置 VITE_API_BASE 环境变量指向 Railway 后端
const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

const request = axios.create({
  baseURL,
  timeout: 60000,
})

// 请求拦截：带 token
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('gp_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：统一错误处理
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const msg = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default request
