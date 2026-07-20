<template>
  <div class="policy-page">
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">政策中心 · POLICY HUB</div>
          <h1 class="page-title">乡村振兴政策一站式检索</h1>
          <p class="page-subtitle">汇集国家级、省级、地市级生态产品价值实现与乡村振兴相关政策</p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <!-- 统计 -->
      <div class="stats-row gp-anim-fade-up">
        <div class="gp-stat-card" v-for="s in stats" :key="s.label">
          <div class="stat-label">{{ s.label }}</div>
          <div class="stat-value">{{ s.value }}<span class="stat-unit">{{ s.unit }}</span></div>
        </div>
      </div>

      <!-- 筛选 -->
      <div class="filter-card gp-anim-fade-up">
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">主题</span>
            <div class="filter-chips">
              <button
                v-for="c in categories"
                :key="c"
                class="filter-chip"
                :class="{ active: filters.category === c }"
                @click="toggleFilter('category', c)"
              >{{ c }}</button>
            </div>
          </div>
          <div class="filter-group">
            <span class="filter-label">级别</span>
            <div class="filter-chips">
              <button
                v-for="l in levels"
                :key="l"
                class="filter-chip"
                :class="{ active: filters.level === l }"
                @click="toggleFilter('level', l)"
              >{{ l }}</button>
            </div>
          </div>
        </div>
        <div class="search-row">
          <el-input v-model="filters.keyword" placeholder="搜索政策标题、关键词…" clearable size="large" @keyup.enter="load">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
          <el-button type="primary" size="large" @click="load">
            <el-icon><Search /></el-icon> 查询
          </el-button>
        </div>
      </div>

      <!-- 政策列表（杂志感） -->
      <div class="policy-list" v-loading="loading">
        <div
          v-for="(p, idx) in list"
          :key="p.id"
          class="policy-item gp-anim-fade-up"
          :style="{ animationDelay: 0.05 * idx + 's' }"
        >
          <div class="policy-index">{{ String(idx + 1 + (page - 1) * size).padStart(2, '0') }}</div>
          <div class="policy-main">
            <div class="policy-meta">
              <span class="gp-chip" :class="chipClass(p.category)">{{ p.category }}</span>
              <span class="gp-chip" :class="levelChipClass(p.level)">{{ p.level }}</span>
              <span class="meta-region" v-if="p.region">
                <el-icon><Location /></el-icon> {{ p.region }}
              </span>
              <span class="meta-date" v-if="p.publish_date">
                {{ p.publish_date.substring(0, 10) }}
              </span>
            </div>
            <h3 class="policy-title">
              <a :href="p.url" target="_blank">{{ p.title }}</a>
            </h3>
            <p class="policy-source" v-if="p.source">来源：{{ p.source }}</p>
          </div>
          <div class="policy-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div v-if="!loading && list.length === 0" class="empty-state">
          <el-empty description="未找到相关政策" />
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-row" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="size"
          :total="total"
          layout="prev, pager, next, total, jumper"
          @current-change="load"
          background
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../api'

const categories = ['生态产品价值实现', '乡村振兴']
const levels = ['国家级', '省级', '地市级']
const filters = reactive({ category: '', level: '', keyword: '' })
const list = ref([])
const loading = ref(false)
const page = ref(1)
const size = ref(20)
const total = ref(0)

const stats = ref([
  { label: 'TOTAL POLICIES', value: 0, unit: ' 条' },
  { label: 'NATIONAL LEVEL', value: 0, unit: ' 条' },
  { label: 'PROVINCIAL', value: 0, unit: ' 条' },
  { label: 'MUNICIPAL', value: 0, unit: ' 条' },
])

async function load() {
  loading.value = true
  try {
    const res = await request.get('/policies/', { params: { ...filters, page: page.value, size: size.value } })
    list.value = res.items || []
    total.value = res.total || 0
    // 拉总数统计
    const all = await request.get('/policies/', { params: { size: 1 } })
    stats.value[0].value = all.total || 0
    // 简化：用列表数据估算
    stats.value[1].value = list.value.filter(p => p.level === '国家级').length
    stats.value[2].value = list.value.filter(p => p.level === '省级').length
    stats.value[3].value = list.value.filter(p => p.level === '地市级').length
  } finally {
    loading.value = false
  }
}

function toggleFilter(key, value) {
  filters[key] = filters[key] === value ? '' : value
  page.value = 1
  load()
}

function chipClass(c) {
  if (c === '生态产品价值实现') return 'gp-chip-forest'
  return 'gp-chip-gold'
}

function levelChipClass(l) {
  if (l === '国家级') return 'gp-chip-red'
  if (l === '省级') return 'gp-chip-forest'
  return 'gp-chip'
}

onMounted(load)
</script>

<style scoped>
.policy-page { min-height: 100vh; }

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

/* 统计 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

/* 筛选 */
.filter-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-soft);
}

.filter-row {
  display: flex;
  gap: 32px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px dashed var(--gp-line);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.filter-label {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-ink-3);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  white-space: nowrap;
}

.filter-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-chip {
  padding: 6px 14px;
  font-size: 13px;
  border: 1px solid var(--gp-line);
  background: #fff;
  color: var(--gp-ink-2);
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-sans);
}

.filter-chip:hover {
  border-color: var(--gp-forest-3);
  color: var(--gp-forest);
}

.filter-chip.active {
  background: var(--gp-forest);
  border-color: var(--gp-forest);
  color: #fff;
}

.search-row {
  display: flex;
  gap: 12px;
}

/* 政策列表 */
.policy-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.policy-item {
  display: grid;
  grid-template-columns: 60px 1fr 40px;
  gap: 24px;
  padding: 24px 20px;
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
  transition: all 0.25s;
  align-items: center;
  cursor: pointer;
}

.policy-item:hover {
  border-color: var(--gp-forest-3);
  background: linear-gradient(90deg, #fffdf6 0%, #fff 100%);
  transform: translateX(4px);
  box-shadow: var(--shadow-card);
}

.policy-index {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 600;
  color: var(--gp-gold);
  text-align: center;
  letter-spacing: 0.05em;
}

.policy-main { min-width: 0; }

.policy-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.meta-region, .meta-date {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--gp-ink-3);
  font-family: var(--font-mono);
}

.policy-title {
  font-size: 18px;
  margin: 0 0 6px;
  font-weight: 600;
  line-height: 1.5;
}

.policy-title a {
  color: var(--gp-forest);
  transition: color 0.2s;
}

.policy-title a:hover {
  color: var(--gp-gold);
}

.policy-source {
  font-size: 12px;
  color: var(--gp-ink-3);
  margin: 0;
}

.policy-arrow {
  color: var(--gp-gold);
  font-size: 18px;
  transition: transform 0.2s;
}

.policy-item:hover .policy-arrow {
  transform: translateX(4px);
}

.empty-state {
  padding: 60px 0;
  background: #fff;
  border: 1px dashed var(--gp-line);
  border-radius: var(--radius-md);
}

.pagination-row {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

@media (max-width: 768px) {
  .stats-row { grid-template-columns: 1fr 1fr; }
  .filter-row { flex-direction: column; gap: 16px; }
  .filter-group { flex-direction: column; align-items: flex-start; }
  .policy-item { grid-template-columns: 40px 1fr; }
  .policy-arrow { display: none; }
}
</style>
