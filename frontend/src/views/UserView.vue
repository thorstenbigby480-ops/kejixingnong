<template>
  <div class="user-page">
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">用户中心 · ACCOUNT</div>
          <h1 class="page-title">个人面板</h1>
          <p class="page-subtitle">注册 / 登录后可查看评估记录、收藏政策、管理订单</p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <!-- 未登录：登录注册卡片 -->
      <div v-if="!user" class="auth-layout">
        <div class="auth-card gp-anim-fade-up">
          <div class="auth-side">
            <div class="auth-bg"></div>
            <div class="auth-content">
              <div class="auth-eyebrow">WELCOME</div>
              <h2>绿脉兴农</h2>
              <p>生态产品价值实现赋能乡村振兴一体化智能系统</p>
              <ul class="auth-features">
                <li><el-icon><Check /></el-icon> 智能评估 + AI 路径优化</li>
                <li><el-icon><Check /></el-icon> 政策收藏 + 案例学习</li>
                <li><el-icon><Check /></el-icon> 农产品上架与交易</li>
              </ul>
            </div>
          </div>

          <div class="auth-form">
            <el-tabs v-model="activeTab" class="auth-tabs">
              <el-tab-pane label="登录" name="login">
                <el-form :model="loginForm" label-position="top">
                  <el-form-item label="用户名">
                    <el-input v-model="loginForm.username" placeholder="请输入用户名" size="large">
                      <template #prefix><el-icon><User /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="密码">
                    <el-input v-model="loginForm.password" type="password" show-password placeholder="请输入密码" size="large">
                      <template #prefix><el-icon><Lock /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-button type="primary" size="large" @click="onLogin" class="auth-submit">登录</el-button>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="注册" name="register">
                <el-form :model="regForm" label-position="top">
                  <el-form-item label="用户名">
                    <el-input v-model="regForm.username" size="large">
                      <template #prefix><el-icon><User /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="邮箱">
                    <el-input v-model="regForm.email" size="large">
                      <template #prefix><el-icon><Message /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="密码">
                    <el-input v-model="regForm.password" type="password" show-password size="large">
                      <template #prefix><el-icon><Lock /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="手机">
                    <el-input v-model="regForm.phone" size="large">
                      <template #prefix><el-icon><Phone /></el-icon></template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="角色">
                    <el-radio-group v-model="regForm.role">
                      <el-radio value="user">普通用户</el-radio>
                      <el-radio value="merchant">商家</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-button type="primary" size="large" @click="onRegister" class="auth-submit">注册</el-button>
                </el-form>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </div>

      <!-- 已登录：个人面板 -->
      <div v-else>
        <!-- 用户信息卡 -->
        <div class="profile-card gp-anim-fade-up">
          <div class="profile-bg"></div>
          <div class="profile-content">
            <div class="profile-avatar">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
            <div class="profile-info">
              <div class="profile-eyebrow">已登录</div>
              <h2 class="profile-name">{{ user.username }}</h2>
              <div class="profile-meta">
                <span class="gp-chip gp-chip-forest">{{ roleText }}</span>
                <span class="meta-item"><el-icon><Message /></el-icon> {{ user.email }}</span>
                <span class="meta-item" v-if="user.phone"><el-icon><Phone /></el-icon> {{ user.phone }}</span>
              </div>
            </div>
            <el-button type="danger" plain @click="onLogout">退出登录</el-button>
          </div>
        </div>

        <!-- 评估记录 -->
        <div class="records-card gp-anim-fade-up">
          <div class="records-header">
            <div>
              <div class="card-eyebrow">MY ASSESSMENTS</div>
              <h3 class="records-title">我的评估记录</h3>
            </div>
            <el-button type="primary" @click="$router.push('/analysis')">
              <el-icon><Plus /></el-icon> 新建评估
            </el-button>
          </div>

          <el-table :data="assessments" stripe v-loading="loadingRecords">
            <el-table-column prop="region_name" label="地区" min-width="180" />
            <el-table-column prop="year" label="年份" width="80" />
            <el-table-column prop="eco_score" label="生态得分" width="100">
              <template #default="{ row }">
                <span class="score-text">{{ row.eco_score }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="rural_score" label="振兴得分" width="100">
              <template #default="{ row }">
                <span class="score-text gold">{{ row.rural_score }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="coupling_d" label="D 值" width="80">
              <template #default="{ row }">
                <span class="d-value">{{ row.coupling_d }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="mode_type" label="模式" width="130">
              <template #default="{ row }">
                <span class="gp-chip gp-chip-gold">{{ row.mode_type }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="评估时间" width="180">
              <template #default="{ row }">
                {{ row.created_at?.substring(0, 19).replace('T', ' ') }}
              </template>
            </el-table-column>
          </el-table>

          <div v-if="!loadingRecords && assessments.length === 0" class="empty-records">
            <el-empty description="暂无评估记录，去新建一个评估吧" />
          </div>
        </div>

        <!-- 我的订单 -->
        <div class="records-card gp-anim-fade-up" style="margin-top:24px">
          <div class="records-header">
            <div>
              <div class="card-eyebrow">MY ORDERS</div>
              <h3 class="records-title">我的订单</h3>
            </div>
            <el-button type="primary" @click="$router.push('/mall')">
              <el-icon><ShoppingCart /></el-icon> 去购物
            </el-button>
          </div>

          <el-table :data="orders" stripe v-loading="loadingOrders">
            <el-table-column prop="id" label="订单号" width="80">
              <template #default="{ row }">#{{ row.id }}</template>
            </el-table-column>
            <el-table-column label="商品" min-width="280">
              <template #default="{ row }">
                <div class="order-items">
                  <span v-for="(it, i) in row.items" :key="i" class="order-item-tag">
                    {{ it.name }} × {{ it.qty }}
                  </span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="total_amount" label="金额" width="120">
              <template #default="{ row }">
                <span class="order-amount">¥{{ row.total_amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <span class="status-tag" :class="row.status">{{ statusLabel(row.status) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="下单时间" width="180">
              <template #default="{ row }">
                {{ row.created_at?.substring(0, 19).replace('T', ' ') }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="140">
              <template #default="{ row }">
                <el-button v-if="row.status === 'pending'" type="primary" size="small" @click="payOrder(row)">立即支付</el-button>
                <el-button v-if="row.status === 'pending'" type="danger" size="small" plain @click="cancelOrder(row)">取消</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="!loadingOrders && orders.length === 0" class="empty-records">
            <el-empty description="暂无订单，去商城看看吧" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, Message, Phone, Check, Plus, ShoppingCart } from '@element-plus/icons-vue'
import request from '../api'

const activeTab = ref('login')
const loginForm = reactive({ username: '', password: '' })
const regForm = reactive({ username: '', email: '', password: '', phone: '', role: 'user' })
const user = ref(null)
const assessments = ref([])
const loadingRecords = ref(false)
const orders = ref([])
const loadingOrders = ref(false)

const roleText = computed(() => {
  const map = { user: '普通用户', merchant: '商家', admin: '管理员' }
  return map[user.value?.role] || ''
})

function loadUser() {
  const raw = localStorage.getItem('gp_user')
  if (raw) user.value = JSON.parse(raw)
}

async function onLogin() {
  if (!loginForm.username || !loginForm.password) {
    return ElMessage.error('请输入用户名和密码')
  }
  const res = await request.post('/auth/login', loginForm)
  localStorage.setItem('gp_token', res.access_token)
  localStorage.setItem('gp_user', JSON.stringify(res.user))
  user.value = res.user
  ElMessage.success('登录成功')
  loadAssessments()
  loadOrders()
}

async function onRegister() {
  if (!regForm.username || !regForm.password || !regForm.email) {
    return ElMessage.error('请填写用户名、邮箱和密码')
  }
  await request.post('/auth/register', regForm)
  ElMessage.success('注册成功，请登录')
  activeTab.value = 'login'
  loginForm.username = regForm.username
  loginForm.password = regForm.password
}

function onLogout() {
  localStorage.removeItem('gp_token')
  localStorage.removeItem('gp_user')
  user.value = null
  assessments.value = []
  orders.value = []
  ElMessage.info('已退出')
}

async function loadAssessments() {
  loadingRecords.value = true
  try {
    const res = await request.get('/analysis/history')
    assessments.value = res.items || []
  } finally {
    loadingRecords.value = false
  }
}

async function loadOrders() {
  loadingOrders.value = true
  try {
    const res = await request.get('/mall/orders')
    orders.value = res.items || []
  } catch (e) {
    // 错误已被拦截器提示
  } finally {
    loadingOrders.value = false
  }
}

async function payOrder(row) {
  try {
    await request.post(`/mall/orders/${row.id}/pay`)
    ElMessage.success('支付成功')
    loadOrders()
  } catch (e) {}
}

async function cancelOrder(row) {
  ElMessageBox.confirm(`确认取消订单 #${row.id}？取消后库存会自动恢复。`, '取消订单', { type: 'warning' })
    .then(async () => {
      try {
        await request.post(`/mall/orders/${row.id}/cancel`)
        ElMessage.success('订单已取消')
        loadOrders()
      } catch (e) {}
    })
    .catch(() => {})
}

function statusLabel(s) {
  const m = {
    pending: '待支付',
    paid: '已支付',
    shipped: '已发货',
    done: '已完成',
    cancelled: '已取消',
  }
  return m[s] || s
}

onMounted(() => {
  loadUser()
  if (user.value) {
    loadAssessments()
    loadOrders()
  }
})
</script>

<style scoped>
.user-page { min-height: 100vh; }

.page-header {
  background: linear-gradient(180deg, var(--gp-paper-2) 0%, transparent 100%);
  padding: 48px 0 24px;
  border-bottom: 1px solid var(--gp-line);
}

.page-title {
  font-family: var(--font-serif);
  font-size: 42px;
  font-weight: 700;
  color: var(--gp-forest);
  margin: 0 0 8px;
  letter-spacing: 0.04em;
}

.page-subtitle {
  color: var(--gp-ink-2);
  font-size: 15px;
  margin: 0;
}

/* === 登录注册卡 === */
.auth-layout {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.auth-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 880px;
  width: 100%;
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  min-height: 540px;
}

.auth-side {
  position: relative;
  background: linear-gradient(135deg, var(--gp-forest) 0%, var(--gp-forest-3) 100%);
  color: #fff;
  padding: 48px 36px;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.auth-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 80% 20%, rgba(199, 154, 0, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 40%);
  pointer-events: none;
}

.auth-content { position: relative; z-index: 2; }

.auth-eyebrow {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.3em;
  color: var(--gp-gold-light);
  margin-bottom: 12px;
}

.auth-side h2 {
  font-family: var(--font-serif);
  font-size: 38px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 12px;
  letter-spacing: 0.1em;
}

.auth-content > p {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  margin: 0 0 32px;
}

.auth-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.auth-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.auth-features .el-icon {
  color: var(--gp-gold-light);
}

.auth-form {
  padding: 48px 40px;
  display: flex;
  align-items: center;
}

.auth-tabs { width: 100%; }

.auth-tabs :deep(.el-tabs__item) {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  height: 48px;
}

.auth-submit {
  width: 100%;
  margin-top: 16px;
}

/* === 已登录：个人面板 === */
.profile-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  margin-bottom: 32px;
  overflow: hidden;
  position: relative;
}

.profile-bg {
  height: 100px;
  background:
    linear-gradient(135deg, var(--gp-forest) 0%, var(--gp-forest-3) 100%);
  position: relative;
  overflow: hidden;
}

.profile-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 80% 30%, rgba(199, 154, 0, 0.3) 0%, transparent 50%);
}

.profile-content {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 32px 24px;
  position: relative;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--gp-gold);
  color: #fff;
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #fff;
  margin-top: -32px;
  box-shadow: var(--shadow-card);
}

.profile-info { flex: 1; }

.profile-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-gold);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.profile-name {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 700;
  color: var(--gp-forest);
  margin: 4px 0 8px;
}

.profile-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--gp-ink-2);
  font-family: var(--font-mono);
}

/* === 评估记录 === */
.records-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 24px 28px;
  box-shadow: var(--shadow-soft);
}

.records-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--gp-line);
}

.card-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-gold);
  letter-spacing: 0.2em;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.records-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--gp-forest);
  margin: 0;
}

.score-text {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--gp-forest);
}

.score-text.gold { color: var(--gp-clay); }

.d-value {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--gp-gold);
}

.empty-records {
  padding: 40px 0;
}

/* === 订单 === */
.order-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.order-item-tag {
  display: inline-block;
  padding: 2px 8px;
  font-size: 12px;
  background: var(--gp-paper-2);
  color: var(--gp-ink-2);
  border-radius: 4px;
  border: 1px solid var(--gp-line);
}

.order-amount {
  color: var(--gp-red);
  font-family: var(--font-mono);
  font-weight: 600;
}

.status-tag {
  padding: 2px 10px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}

.status-tag.paid {
  background: #e6f4ea;
  color: #1e7e34;
}

.status-tag.pending {
  background: #fff8e1;
  color: #b8860b;
}

.status-tag.cancelled {
  background: #fee;
  color: #c00;
}

.status-tag.shipped {
  background: #e3f2fd;
  color: #1565c0;
}

.status-tag.done {
  background: #f3e5f5;
  color: #6a1b9a;
}

@media (max-width: 768px) {
  .auth-card { grid-template-columns: 1fr; }
  .auth-side { padding: 32px 24px; }
  .auth-form { padding: 32px 24px; }
  .profile-content { flex-direction: column; align-items: flex-start; }
}
</style>
