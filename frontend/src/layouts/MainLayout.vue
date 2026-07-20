<template>
  <el-container class="main-layout">
    <!-- 顶部导航 -->
    <el-header class="header">
      <div class="header-bg"></div>
      <div class="header-inner">
        <!-- 左：品牌 -->
        <div class="brand" @click="$router.push('/')">
          <div class="brand-seal">绿</div>
          <div class="brand-text">
            <div class="brand-name">绿脉兴农</div>
            <div class="brand-sub">LVMAI · 生态产品价值实现赋能平台</div>
          </div>
        </div>

        <!-- 中：导航 -->
        <nav class="nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: $route.path === item.path }"
          >
            <span class="nav-cn">{{ item.cn }}</span>
            <span class="nav-en">{{ item.en }}</span>
          </router-link>
        </nav>

        <!-- 右：用户 -->
        <div class="header-right">
          <el-button text class="login-btn" @click="$router.push('/user')">
            <el-icon><User /></el-icon>
            <span>{{ user ? user.username : '登录' }}</span>
          </el-button>
        </div>
      </div>
    </el-header>

    <!-- 主内容 -->
    <el-main class="main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <div class="footer-brand">
            <span class="footer-mark">绿脉兴农</span>
            <span class="footer-sub">生态产品价值实现赋能乡村振兴一体化智能系统</span>
          </div>
          <p class="footer-tag">让"绿水青山"看得见、算得清、走得通</p>
        </div>
        <div class="footer-col">
          <div class="footer-title">三色融合理论</div>
          <p class="footer-line"><span class="dot red"></span>党建红 · 核心 · 引领方向</p>
          <p class="footer-line"><span class="dot gold"></span>产业金 · 载体 · 创造价值</p>
          <p class="footer-line"><span class="dot green"></span>生态绿 · 支撑 · 保障可持续</p>
        </div>
        <div class="footer-col">
          <div class="footer-title">参赛信息</div>
          <p class="footer-line">中国研究生乡村振兴科技强农+创新大赛</p>
          <p class="footer-line">南京师范大学 · 三色绘三农实践团队</p>
          <p class="footer-line">作品编号：2024S01</p>
        </div>
        <div class="footer-col">
          <div class="footer-title">技术架构</div>
          <p class="footer-line">Vue 3 + Element Plus</p>
          <p class="footer-line">FastAPI + SQLAlchemy</p>
          <p class="footer-line">DeepSeek AI + ECharts</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 绿脉兴农 · ALL RIGHTS RESERVED</span>
        <span class="footer-mono">v0.1.0 · BUILT FOR RURAL REVITALIZATION</span>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'

const navItems = [
  { path: '/', cn: '首页', en: 'HOME' },
  { path: '/policy', cn: '政策中心', en: 'POLICY' },
  { path: '/analysis', cn: '智能分析', en: 'ANALYSIS' },
  { path: '/mall', cn: '农产品商城', en: 'MALL' },
  { path: '/case', cn: '案例中心', en: 'CASE' },
]

const user = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('gp_user'))
  } catch {
    return null
  }
})
</script>

<style scoped>
.main-layout { min-height: 100vh; background: transparent; }

/* ============ Header ============ */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 80px !important;
  padding: 0 !important;
  border-bottom: 1px solid var(--gp-line);
  background: rgba(250, 247, 240, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.header-bg {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent 0%, rgba(199, 154, 0, 0.04) 50%, transparent 100%);
  pointer-events: none;
}

.header-inner {
  position: relative;
  max-width: 1400px;
  height: 100%;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* === 品牌 === */
.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
}

.brand-seal {
  width: 44px;
  height: 44px;
  background: var(--gp-forest);
  color: var(--gp-gold);
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  position: relative;
  box-shadow: 0 4px 12px rgba(13, 59, 46, 0.25);
}

.brand-seal::after {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px solid var(--gp-gold);
  border-radius: 2px;
}

.brand-text { line-height: 1.2; }
.brand-name {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  color: var(--gp-forest);
  letter-spacing: 0.1em;
}
.brand-sub {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--gp-ink-3);
  letter-spacing: 0.15em;
  margin-top: 2px;
}

/* === 导航 === */
.nav {
  display: flex;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 18px;
  border-radius: 6px;
  position: relative;
  transition: all 0.25s;
  color: var(--gp-ink-2);
}

.nav-item:hover {
  background: rgba(13, 59, 46, 0.06);
  color: var(--gp-forest);
}

.nav-item.active {
  color: var(--gp-forest);
  background: rgba(13, 59, 46, 0.08);
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 2px;
  background: var(--gp-gold);
  border-radius: 1px;
}

.nav-cn {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.nav-en {
  font-family: var(--font-mono);
  font-size: 9px;
  letter-spacing: 0.2em;
  color: var(--gp-ink-3);
  margin-top: 2px;
}

.header-right .login-btn {
  color: var(--gp-forest);
  font-family: var(--font-sans);
}

/* ============ Main ============ */
.main {
  padding: 0 !important;
  min-height: calc(100vh - 80px - 320px);
}

/* ============ 页面切换动画 ============ */
.page-enter-active {
  transition: all 0.4s ease-out;
}
.page-leave-active {
  transition: all 0.2s ease-in;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ============ Footer ============ */
.footer {
  height: auto !important;
  padding: 0 !important;
  background: var(--gp-forest);
  color: rgba(255, 255, 255, 0.85);
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg,
    var(--gp-red) 0%,
    var(--gp-red) 33%,
    var(--gp-gold) 33%,
    var(--gp-gold) 66%,
    var(--gp-forest-3) 66%,
    var(--gp-forest-3) 100%);
}

.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 56px 32px 32px;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 40px;
}

.footer-brand { margin-bottom: 16px; }

.footer-mark {
  font-family: var(--font-serif);
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.1em;
}

.footer-sub {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 6px;
  line-height: 1.5;
}

.footer-tag {
  font-family: var(--font-serif);
  font-size: 14px;
  color: var(--gp-gold-light);
  margin: 16px 0 0;
  font-style: italic;
}

.footer-title {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--gp-gold);
  letter-spacing: 0.25em;
  margin-bottom: 14px;
  text-transform: uppercase;
}

.footer-line {
  font-size: 13px;
  margin: 6px 0;
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.dot.red { background: var(--gp-red); }
.dot.gold { background: var(--gp-gold); }
.dot.green { background: var(--gp-forest-3); }

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  font-family: var(--font-mono);
  letter-spacing: 0.1em;
}

@media (max-width: 1024px) {
  .nav-en { display: none; }
  .header-inner { padding: 0 16px; }
  .footer-inner { grid-template-columns: 1fr 1fr; gap: 32px; }
}

@media (max-width: 768px) {
  .brand-sub { display: none; }
  .nav { gap: 0; }
  .nav-item { padding: 6px 10px; }
  .footer-inner { grid-template-columns: 1fr; }
}
</style>
