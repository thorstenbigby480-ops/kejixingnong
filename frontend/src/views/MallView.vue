<template>
  <div class="mall-page">
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">生态农产品商城 · ECO MALL</div>
          <h1 class="page-title">从田间到餐桌，生态直供</h1>
          <p class="page-subtitle">面向农户与合作社的生态农产品展示与交易平台</p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <!-- 分类筛选 -->
      <div class="filter-bar gp-anim-fade-up">
        <div class="category-tabs">
          <button
            v-for="c in categories"
            :key="c"
            class="cat-tab"
            :class="{ active: filters.category === c }"
            @click="setCategory(c)"
          >
            {{ c }}
          </button>
        </div>
        <div class="filter-actions">
          <el-input v-model="filters.keyword" placeholder="搜索商品…" clearable @keyup.enter="load" class="search-input">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-badge :value="cartCount" :hidden="cartCount === 0" class="cart-badge">
            <el-button type="primary" plain @click="cartVisible = true">
              <el-icon><ShoppingCart /></el-icon> 购物车
            </el-button>
          </el-badge>
        </div>
      </div>

      <!-- 商品网格 -->
      <div class="product-grid" v-loading="loading">
        <div
          v-for="(p, idx) in list"
          :key="p.id"
          class="product-card gp-anim-fade-up"
          :style="{ animationDelay: 0.05 * idx + 's' }"
        >
          <div class="product-image">
            <img v-if="p.image_url" :src="p.image_url" :alt="p.name" />
            <div v-else class="img-placeholder">
              <el-icon :size="48"><Picture /></el-icon>
            </div>
            <div class="product-badge" v-if="p.eco_cert">
              <span class="gp-chip gp-chip-forest">{{ p.eco_cert }}</span>
            </div>
          </div>
          <div class="product-body">
            <div class="product-meta">
              <span class="gp-chip gp-chip-gold">{{ p.category }}</span>
              <span class="origin" v-if="p.origin">
                <el-icon><Location /></el-icon> {{ p.origin }}
              </span>
            </div>
            <h3 class="product-name">{{ p.name }}</h3>
            <p class="product-desc" v-if="p.description">{{ p.description }}</p>
            <div class="product-foot">
              <div class="price">
                <span class="symbol">¥</span>
                <span class="amount">{{ p.price }}</span>
                <span class="unit">/份</span>
              </div>
              <span class="stock" :class="{ low: p.stock < 50 }">库存 {{ p.stock }}</span>
            </div>
            <div class="buy-actions">
              <el-input-number v-model="qtyMap[p.id]" :min="1" :max="p.stock" size="small" class="qty-input" />
              <el-button type="primary" class="buy-btn" @click="addToCart(p)">
                <el-icon><ShoppingCart /></el-icon> 加入购物车
              </el-button>
            </div>
          </div>
        </div>

        <div v-if="!loading && list.length === 0" class="empty-state">
          <el-empty description="暂无商品" />
        </div>
      </div>
    </div>

    <!-- 购物车抽屉 -->
    <el-drawer v-model="cartVisible" title="我的购物车" size="480px" :direction="direction">
      <div class="cart-content">
        <div v-if="cart.length === 0" class="cart-empty">
          <el-empty description="购物车空空如也~">
            <el-button type="primary" @click="cartVisible = false">继续选购</el-button>
          </el-empty>
        </div>
        <template v-else>
          <div class="cart-list">
            <div v-for="item in cart" :key="item.product_id" class="cart-item">
              <div class="cart-item-img">
                <img v-if="item.image_url" :src="item.image_url" :alt="item.name" />
                <el-icon v-else :size="32"><Picture /></el-icon>
              </div>
              <div class="cart-item-info">
                <div class="cart-item-name">{{ item.name }}</div>
                <div class="cart-item-meta">
                  <span class="cart-item-price">¥{{ item.price }}</span>
                  ×
                  <el-input-number v-model="item.qty" :min="1" :max="item.maxQty" size="small" class="cart-qty" @change="updateCart" />
                </div>
              </div>
              <div class="cart-item-sub">
                <div class="cart-item-total">¥{{ (item.price * item.qty).toFixed(2) }}</div>
                <el-button link type="danger" size="small" @click="removeFromCart(item.product_id)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>

          <div class="cart-summary">
            <div class="summary-row">
              <span>商品总数</span>
              <span>{{ cartCount }} 件</span>
            </div>
            <div class="summary-row total">
              <span>合计</span>
              <span class="amount">¥{{ cartTotal.toFixed(2) }}</span>
            </div>
          </div>

          <div class="cart-actions">
            <el-button @click="clearCart">清空</el-button>
            <el-button type="primary" @click="goCheckout" :loading="submitting">
              去结算
            </el-button>
          </div>
        </template>
      </div>
    </el-drawer>

    <!-- 结算对话框 -->
    <el-dialog v-model="checkoutVisible" title="确认订单" width="540px">
      <div class="checkout-form" v-if="checkoutItems.length">
        <div class="form-section-title">收货信息</div>
        <el-form :model="checkoutForm" label-width="80px" label-position="left">
          <el-form-item label="收货人">
            <el-input v-model="checkoutForm.consignee" placeholder="请输入收货人姓名" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="checkoutForm.phone" placeholder="请输入手机号" maxlength="11" />
          </el-form-item>
          <el-form-item label="收货地址">
            <el-input v-model="checkoutForm.address" type="textarea" :rows="2" placeholder="请输入详细收货地址" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="checkoutForm.remark" type="textarea" :rows="2" placeholder="选填" />
          </el-form-item>
        </el-form>

        <div class="form-section-title">订单明细</div>
        <div class="checkout-list">
          <div v-for="item in checkoutItems" :key="item.product_id" class="checkout-item">
            <span class="ck-name">{{ item.name }}</span>
            <span class="ck-qty">× {{ item.qty }}</span>
            <span class="ck-price">¥{{ (item.price * item.qty).toFixed(2) }}</span>
          </div>
        </div>

        <div class="checkout-total">
          <span>实付金额</span>
          <span class="amount">¥{{ cartTotal.toFixed(2) }}</span>
        </div>
      </div>

      <template #footer>
        <el-button @click="checkoutVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOrder" :loading="submitting">提交订单</el-button>
      </template>
    </el-dialog>

    <!-- 支付对话框 -->
    <el-dialog v-model="payVisible" title="模拟支付" width="420px">
      <div class="pay-dialog">
        <div class="pay-amount">
          <div class="pay-label">应付金额</div>
          <div class="pay-value">¥{{ payOrder?.total_amount?.toFixed(2) }}</div>
        </div>
        <div class="pay-methods">
          <div class="pay-method active">
            <el-icon :size="28"><Wallet /></el-icon>
            <span>模拟支付</span>
          </div>
        </div>
        <div class="pay-tip">
          <el-icon><InfoFilled /></el-icon>
          演示环境：点击下方按钮直接完成支付。
        </div>
      </div>
      <template #footer>
        <el-button @click="payVisible = false">取消支付</el-button>
        <el-button type="primary" @click="confirmPay" :loading="paying">确认支付 ¥{{ payOrder?.total_amount?.toFixed(2) }}</el-button>
      </template>
    </el-dialog>

    <!-- 订单结果对话框 -->
    <el-dialog v-model="resultVisible" title="订单状态" width="420px">
      <div class="result-dialog" v-if="resultOrder">
        <el-icon :size="56" class="result-icon"><CircleCheckFilled /></el-icon>
        <div class="result-title">{{ resultOrder.message || '订单已创建' }}</div>
        <div class="result-info">
          <div class="info-row"><span>订单号</span><span>#{{ resultOrder.order_id || resultOrder.id }}</span></div>
          <div class="info-row" v-if="resultOrder.total_amount"><span>金额</span><span>¥{{ resultOrder.total_amount.toFixed(2) }}</span></div>
          <div class="info-row" v-if="resultOrder.status"><span>状态</span><span class="status-tag" :class="resultOrder.status">{{ statusLabel(resultOrder.status) }}</span></div>
        </div>
      </div>
      <template #footer>
        <el-button @click="resultVisible = false">关闭</el-button>
        <el-button type="primary" @click="resultVisible = false">好的</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, ShoppingCart, Location, Picture, Delete, Wallet, InfoFilled, CircleCheckFilled } from '@element-plus/icons-vue'
import request from '../api'

const categories = ['全部', '粮食', '果蔬', '茶叶', '特产', '畜禽', '加工品']
const filters = reactive({ category: '全部', keyword: '' })
const list = ref([])
const loading = ref(false)
const qtyMap = reactive({})

// 购物车（localStorage 持久化）
const cart = ref([])
const cartVisible = ref(false)
const direction = 'rtl'

const cartCount = computed(() => cart.value.reduce((s, it) => s + it.qty, 0))
const cartTotal = computed(() => cart.value.reduce((s, it) => s + it.price * it.qty, 0))

// 结算 & 支付
const checkoutVisible = ref(false)
const checkoutItems = ref([])
const checkoutForm = reactive({ consignee: '', phone: '', address: '', remark: '' })
const submitting = ref(false)
const payVisible = ref(false)
const payOrder = ref(null)
const paying = ref(false)
const resultVisible = ref(false)
const resultOrder = ref(null)

async function load() {
  loading.value = true
  try {
    const params = { ...filters }
    if (params.category === '全部') params.category = ''
    const res = await request.get('/mall/products', { params })
    list.value = res.items || []
    list.value.forEach(p => {
      if (!qtyMap[p.id]) qtyMap[p.id] = 1
    })
  } finally {
    loading.value = false
  }
}

function setCategory(c) {
  filters.category = c
  load()
}

// ============ 购物车操作 ============
function loadCart() {
  try {
    const raw = localStorage.getItem('gp_cart')
    if (raw) cart.value = JSON.parse(raw)
  } catch (e) {
    cart.value = []
  }
}

function saveCart() {
  localStorage.setItem('gp_cart', JSON.stringify(cart.value))
}

function addToCart(p) {
  const qty = qtyMap[p.id] || 1
  const existing = cart.value.find(i => i.product_id === p.id)
  if (existing) {
    const newQty = existing.qty + qty
    if (newQty > p.stock) {
      ElMessage.warning(`库存不足，最多只能购买 ${p.stock} 件`)
      return
    }
    existing.qty = newQty
    existing.maxQty = p.stock
  } else {
    cart.value.push({
      product_id: p.id,
      name: p.name,
      price: p.price,
      image_url: p.image_url,
      qty: qty,
      maxQty: p.stock,
    })
  }
  saveCart()
  ElMessage.success(`已加入购物车：${p.name}`)
}

function removeFromCart(pid) {
  cart.value = cart.value.filter(i => i.product_id !== pid)
  saveCart()
}

function updateCart() {
  saveCart()
}

function clearCart() {
  ElMessageBox.confirm('确定要清空购物车吗？', '提示', { type: 'warning' })
    .then(() => {
      cart.value = []
      saveCart()
      ElMessage.success('购物车已清空')
    })
    .catch(() => {})
}

// ============ 结算 & 下单 ============
function goCheckout() {
  // 检查登录
  const token = localStorage.getItem('gp_token')
  if (!token) {
    ElMessage.warning('请先登录后再结算')
    return
  }
  checkoutItems.value = cart.value.map(i => ({ ...i }))
  checkoutVisible.value = true
}

async function submitOrder() {
  if (!checkoutForm.consignee || !checkoutForm.phone || !checkoutForm.address) {
    ElMessage.warning('请填写完整的收货信息')
    return
  }
  if (!/^1\d{10}$/.test(checkoutForm.phone)) {
    ElMessage.warning('手机号格式不正确')
    return
  }
  submitting.value = true
  try {
    const res = await request.post('/mall/orders', {
      items: checkoutItems.value.map(i => ({
        product_id: i.product_id,
        name: i.name,
        price: i.price,
        qty: i.qty,
        image_url: i.image_url,
      })),
      address: `${checkoutForm.consignee} | ${checkoutForm.phone} | ${checkoutForm.address}`,
      phone: checkoutForm.phone,
      remark: checkoutForm.remark,
    })
    checkoutVisible.value = false
    // 清空购物车
    cart.value = []
    saveCart()
    // 刷新商品库存
    load()
    // 弹支付
    payOrder.value = res
    payVisible.value = true
  } catch (e) {
    // 错误已被拦截器提示
  } finally {
    submitting.value = false
  }
}

async function confirmPay() {
  paying.value = true
  try {
    const res = await request.post(`/mall/orders/${payOrder.value.id}/pay`)
    payVisible.value = false
    resultOrder.value = { ...res, total_amount: payOrder.value.total_amount }
    resultVisible.value = true
  } catch (e) {
    // 错误已被拦截器提示
  } finally {
    paying.value = false
  }
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
  loadCart()
  load()
})
</script>

<style scoped>
.mall-page { min-height: 100vh; }

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

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  margin-top: 32px;
}

.category-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.cat-tab {
  padding: 8px 18px;
  font-size: 14px;
  border: 1px solid var(--gp-line);
  background: #fff;
  color: var(--gp-ink-2);
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-sans);
}

.cat-tab:hover {
  border-color: var(--gp-forest-3);
  color: var(--gp-forest);
}

.cat-tab.active {
  background: var(--gp-forest);
  border-color: var(--gp-forest);
  color: #fff;
}

.filter-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input { width: 240px; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.product-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  border-color: var(--gp-forest-3);
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}

.product-image {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, var(--gp-paper-2), var(--gp-cream));
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.product-card:hover .product-image img {
  transform: scale(1.08);
}

.img-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gp-moss);
}

.product-badge {
  position: absolute;
  top: 12px;
  left: 12px;
}

.product-body {
  padding: 18px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.product-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  gap: 8px;
}

.origin {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--gp-ink-3);
  font-family: var(--font-mono);
}

.product-name {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--gp-forest);
  margin: 0 0 8px;
}

.product-desc {
  font-size: 12px;
  color: var(--gp-ink-3);
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-foot {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 14px;
}

.price {
  color: var(--gp-red);
}

.price .symbol {
  font-size: 14px;
  font-weight: 600;
}

.price .amount {
  font-family: var(--font-mono);
  font-size: 26px;
  font-weight: 700;
  margin-left: 2px;
}

.price .unit {
  font-size: 12px;
  color: var(--gp-ink-3);
  margin-left: 4px;
}

.stock {
  font-size: 12px;
  color: var(--gp-ink-3);
  font-family: var(--font-mono);
}

.stock.low {
  color: var(--gp-red);
}

.buy-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: auto;
}

.qty-input {
  width: 110px;
}

.buy-btn {
  flex: 1;
}

.empty-state {
  grid-column: 1 / -1;
  padding: 60px 0;
  background: #fff;
  border: 1px dashed var(--gp-line);
  border-radius: var(--radius-md);
}

/* ============ 购物车抽屉 ============ */
.cart-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0 4px;
}

.cart-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px solid var(--gp-line);
}

.cart-item-img {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--gp-paper-2);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-item-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cart-item-info {
  flex: 1;
  min-width: 0;
}

.cart-item-name {
  font-size: 14px;
  color: var(--gp-ink-1);
  font-weight: 500;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cart-item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--gp-ink-3);
}

.cart-item-price {
  color: var(--gp-red);
  font-family: var(--font-mono);
  font-weight: 600;
}

.cart-qty {
  width: 90px;
}

.cart-item-sub {
  text-align: right;
  flex-shrink: 0;
}

.cart-item-total {
  color: var(--gp-red);
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 4px;
}

.cart-summary {
  border-top: 2px solid var(--gp-forest);
  padding: 16px 8px;
  background: var(--gp-paper-2);
  border-radius: 0 0 var(--radius-sm) var(--radius-sm);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  font-size: 14px;
  color: var(--gp-ink-2);
}

.summary-row.total {
  padding-top: 12px;
  border-top: 1px dashed var(--gp-line);
  font-size: 16px;
  font-weight: 600;
  color: var(--gp-forest);
  margin-top: 6px;
}

.summary-row.total .amount {
  color: var(--gp-red);
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
}

.cart-actions {
  display: flex;
  gap: 12px;
  padding: 16px 8px;
}

.cart-actions .el-button {
  flex: 1;
}

/* ============ 结算对话框 ============ */
.checkout-form {
  padding: 0 4px;
}

.form-section-title {
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 600;
  color: var(--gp-forest);
  margin: 16px 0 12px;
  padding-left: 10px;
  border-left: 3px solid var(--gp-gold);
}

.checkout-list {
  background: var(--gp-paper-2);
  border-radius: var(--radius-sm);
  padding: 8px 14px;
  margin-bottom: 16px;
}

.checkout-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed var(--gp-line);
  font-size: 14px;
}

.checkout-item:last-child {
  border-bottom: none;
}

.ck-name {
  flex: 1;
  color: var(--gp-ink-1);
}

.ck-qty {
  width: 80px;
  text-align: center;
  color: var(--gp-ink-3);
}

.ck-price {
  width: 100px;
  text-align: right;
  color: var(--gp-red);
  font-family: var(--font-mono);
  font-weight: 600;
}

.checkout-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 12px;
  background: var(--gp-forest);
  color: #fff;
  border-radius: var(--radius-sm);
}

.checkout-total .amount {
  font-family: var(--font-mono);
  font-size: 24px;
  font-weight: 700;
}

/* ============ 支付对话框 ============ */
.pay-dialog {
  padding: 0 4px;
}

.pay-amount {
  text-align: center;
  padding: 24px 0;
  background: linear-gradient(135deg, var(--gp-forest), var(--gp-forest-2));
  color: #fff;
  border-radius: var(--radius-md);
  margin-bottom: 20px;
}

.pay-label {
  font-size: 13px;
  opacity: 0.85;
  margin-bottom: 6px;
}

.pay-value {
  font-family: var(--font-mono);
  font-size: 36px;
  font-weight: 700;
}

.pay-methods {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.pay-method {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px;
  border: 2px solid var(--gp-line);
  border-radius: var(--radius-sm);
  color: var(--gp-ink-2);
  font-size: 13px;
}

.pay-method.active {
  border-color: var(--gp-forest);
  background: var(--gp-paper-2);
  color: var(--gp-forest);
  font-weight: 600;
}

.pay-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  background: #fff8e1;
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: #b8860b;
}

/* ============ 结果对话框 ============ */
.result-dialog {
  text-align: center;
  padding: 16px 0;
}

.result-icon {
  color: var(--gp-forest);
  margin-bottom: 12px;
}

.result-title {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 600;
  color: var(--gp-forest);
  margin-bottom: 16px;
}

.result-info {
  background: var(--gp-paper-2);
  border-radius: var(--radius-sm);
  padding: 14px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 14px;
}

.info-row span:first-child {
  color: var(--gp-ink-3);
}

.info-row span:last-child {
  color: var(--gp-ink-1);
  font-family: var(--font-mono);
  font-weight: 500;
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

@media (max-width: 1100px) {
  .product-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); }
  .filter-bar { flex-direction: column; align-items: stretch; }
  .filter-actions { width: 100%; }
  .search-input { flex: 1; }
}
</style>
