<template>
  <div class="case-page">
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">案例中心 · CASE STUDIES</div>
          <h1 class="page-title">五种模式的典型案例</h1>
          <p class="page-subtitle">汇集全国生态产品价值实现赋能乡村振兴的典型经验</p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <!-- 模式标签 -->
      <div class="mode-tabs gp-anim-fade-up">
        <button
          v-for="m in modes"
          :key="m"
          class="mode-tab"
          :class="{ active: filters.mode_type === m }"
          @click="setMode(m)"
        >
          {{ m }}
        </button>
      </div>

      <!-- 案例网格 -->
      <div class="case-grid" v-loading="loading">
        <div
          v-for="(c, idx) in list"
          :key="c.id"
          class="case-card gp-anim-fade-up"
          :style="{ animationDelay: 0.1 * idx + 's' }"
          @click="onView(c)"
        >
          <div class="case-image">
            <img v-if="c.image_url" :src="c.image_url" :alt="c.title" />
            <div v-else class="img-ph">
              <el-icon :size="56"><Picture /></el-icon>
            </div>
            <div class="case-mode-tag">
              <span class="gp-chip gp-chip-gold">{{ c.mode_type }}</span>
            </div>
            <div class="case-num">CASE · {{ String(idx + 1).padStart(2, '0') }}</div>
          </div>
          <div class="case-content">
            <div class="case-region" v-if="c.region">
              <el-icon><Location /></el-icon> {{ c.region }}
            </div>
            <h3 class="case-title">{{ c.title }}</h3>
            <p class="case-summary">{{ c.summary }}</p>
            <div class="case-action">
              <span>查看详情</span>
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>

        <div v-if="!loading && list.length === 0" class="empty-state">
          <el-empty description="暂无案例" />
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <el-dialog v-model="dialogVisible" :title="current?.title" width="60%" class="case-dialog">
      <div v-if="current" class="dialog-content">
        <div class="dialog-meta">
          <span class="gp-chip gp-chip-gold">{{ current.mode_type }}</span>
          <span class="meta-item"><el-icon><Location /></el-icon> {{ current.region }}</span>
        </div>
        <div class="dialog-body">{{ current.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../api'

const modes = ['全部', '生态康养型', '湿地水域型', '农业品牌型', '农文旅融合型', '城郊消费型']
const filters = reactive({ mode_type: '' })
const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const current = ref(null)

async function load() {
  loading.value = true
  try {
    const params = { ...filters }
    if (params.mode_type === '全部') params.mode_type = ''
    const res = await request.get('/cases/', { params })
    list.value = res.items || []
  } finally {
    loading.value = false
  }
}

function setMode(m) {
  filters.mode_type = m
  load()
}

function onView(c) {
  current.value = c
  dialogVisible.value = true
}

onMounted(load)
</script>

<style scoped>
.case-page { min-height: 100vh; }

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

.mode-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 32px;
  padding: 12px;
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}

.mode-tab {
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  background: transparent;
  color: var(--gp-ink-2);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-serif);
  font-weight: 500;
}

.mode-tab:hover {
  background: rgba(13, 59, 46, 0.06);
  color: var(--gp-forest);
}

.mode-tab.active {
  background: var(--gp-forest);
  color: #fff;
}

.case-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.case-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.case-card:hover {
  border-color: var(--gp-forest-3);
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}

.case-image {
  position: relative;
  height: 220px;
  background: linear-gradient(135deg, var(--gp-paper-2), var(--gp-cream));
  overflow: hidden;
}

.case-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s;
}

.case-card:hover .case-image img {
  transform: scale(1.06);
}

.img-ph {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gp-moss);
}

.case-mode-tag {
  position: absolute;
  top: 16px;
  left: 16px;
}

.case-num {
  position: absolute;
  bottom: 16px;
  right: 16px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: #fff;
  letter-spacing: 0.2em;
  background: rgba(0, 0, 0, 0.4);
  padding: 4px 10px;
  border-radius: 4px;
  backdrop-filter: blur(4px);
}

.case-content { padding: 24px; }

.case-region {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--gp-ink-3);
  font-family: var(--font-mono);
  margin-bottom: 10px;
}

.case-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--gp-forest);
  margin: 0 0 12px;
  line-height: 1.4;
}

.case-summary {
  font-size: 14px;
  color: var(--gp-ink-2);
  line-height: 1.8;
  margin: 0 0 20px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.case-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--gp-gold);
  letter-spacing: 0.1em;
  transition: gap 0.2s;
}

.case-card:hover .case-action { gap: 12px; }

.empty-state {
  grid-column: 1 / -1;
  padding: 60px 0;
  background: #fff;
  border: 1px dashed var(--gp-line);
  border-radius: var(--radius-md);
}

/* 弹窗 */
.case-dialog :deep(.el-dialog__header) {
  background: linear-gradient(180deg, var(--gp-paper-2) 0%, #fff 100%);
  border-bottom: 1px solid var(--gp-line);
  margin-right: 0;
  padding: 24px;
}

.case-dialog :deep(.el-dialog__title) {
  font-family: var(--font-serif);
  font-size: 22px;
  color: var(--gp-forest);
}

.dialog-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--gp-ink-3);
  font-family: var(--font-mono);
}

.dialog-body {
  white-space: pre-wrap;
  line-height: 2;
  font-size: 14px;
  color: var(--gp-ink);
  padding: 8px 0;
}

@media (max-width: 768px) {
  .case-grid { grid-template-columns: 1fr; }
}
</style>
