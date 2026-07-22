<template>
  <div class="dashboard-page">
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">数据大屏 · DATA INSIGHT</div>
          <h1 class="page-title">10 区县 5 年生态振兴数据透视</h1>
          <p class="page-subtitle">基于层次聚类分析的五种模式横向对比与时间序列演化</p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <!-- 控制面板 -->
      <div class="controls gp-anim-fade-up">
        <div class="control-group">
          <label>对比指标：</label>
          <el-select v-model="metric" @change="loadCompare">
            <el-option label="生态产品价值实现成效" value="eco_score" />
            <el-option label="乡村振兴水平" value="rural_score" />
            <el-option label="耦合协调度 D" value="d_value" />
            <el-option label="森林覆盖率(%)" value="forest" />
            <el-option label="农村人均收入(元)" value="income" />
            <el-option label="GDP(万元)" value="gdp" />
          </el-select>
        </div>
        <div class="control-group">
          <label>年份：</label>
          <el-select v-model="year" @change="loadCompare">
            <el-option v-for="y in [2020, 2021, 2022, 2023, 2024]" :key="y" :label="y" :value="y" />
          </el-select>
        </div>
      </div>

      <!-- 统计卡 -->
      <div class="stat-cards gp-anim-fade-up">
        <div class="stat-card">
          <div class="stat-label">样本区县</div>
          <div class="stat-value">10</div>
          <div class="stat-sub">覆盖苏浙皖川</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">观察年份</div>
          <div class="stat-value">5 年</div>
          <div class="stat-sub">2020-2024</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">聚类模式</div>
          <div class="stat-value">5 类</div>
          <div class="stat-sub">层次聚类结果</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ year }}年最高{{ metricLabel }}</div>
          <div class="stat-value highlight">{{ topRegion?.value ?? '-' }}</div>
          <div class="stat-sub">{{ topRegion?.name?.replace(/省|市|区|县/g, '') }}</div>
        </div>
      </div>

      <!-- 横向对比柱状图 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">横向对比 · {{ metricLabel }}（{{ year }}年）</h3>
          <span class="chart-subtitle">按模式分色 · 降序排列</span>
        </div>
        <div ref="barChartRef" class="chart-box"></div>
      </div>

      <!-- 时间序列折线图 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">时间演化 · 5年趋势（{{ metricLabel }}）</h3>
          <div class="legend-tags">
            <span v-for="(c, i) in modeColors" :key="i" class="legend-tag" :style="{background: c.color}">
              {{ c.mode }}
            </span>
          </div>
        </div>
        <div ref="lineChartRef" class="chart-box"></div>
      </div>

      <!-- 雷达图：5种模式综合对比 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">模式综合对比 · 雷达图（{{ year }}年）</h3>
          <span class="chart-subtitle">各模式代表区县五维得分</span>
        </div>
        <div ref="radarChartRef" class="chart-box"></div>
      </div>

      <!-- 散点图：生态 vs 振兴 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">耦合协调散点图 · 生态得分 vs 振兴得分（{{ year }}年）</h3>
          <span class="chart-subtitle">对角线为 D=1（完全协调），距线越远越失调</span>
        </div>
        <div ref="scatterChartRef" class="chart-box"></div>
      </div>

      <!-- AHP权重可视化 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">AHP层次分析法组合权重分布</h3>
          <span class="chart-subtitle">两个指标体系 · 按准则层分色</span>
        </div>
        <div ref="weightsChartRef" class="chart-box chart-box-tall"></div>
      </div>

      <!-- 聚类散点图：主成分降维 -->
      <div class="chart-card gp-anim-fade-up">
        <div class="chart-header">
          <h3 class="chart-title">层次聚类分析结果（主成分降维散点图）</h3>
          <span class="chart-subtitle">按模式分色 · X=PC1, Y=PC2</span>
        </div>
        <div ref="clusterChartRef" class="chart-box"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import request from '../api'

const metric = ref('eco_score')
const year = ref(2024)
const compareData = ref([])
const overviewData = ref([])
const weightsData = ref({})
const clusterData = ref([])

const barChartRef = ref(null)
const lineChartRef = ref(null)
const radarChartRef = ref(null)
const scatterChartRef = ref(null)
const weightsChartRef = ref(null)
const clusterChartRef = ref(null)

let barChart, lineChart, radarChart, scatterChart, weightsChart, clusterChart

const metricMap = {
  eco_score: '生态得分',
  rural_score: '振兴得分',
  d_value: '耦合协调度',
  forest: '森林覆盖率',
  income: '农村人均收入',
  gdp: 'GDP',
}

const metricLabel = computed(() => metricMap[metric.value] || metric.value)

const topRegion = computed(() => {
  if (!compareData.value?.length) return null
  return compareData.value[0]
})

const modeColors = [
  { mode: '生态康养型', color: '#1b5e20' },
  { mode: '湿地水域型', color: '#0277bd' },
  { mode: '农业品牌型', color: '#c79a00' },
  { mode: '农文旅融合型', color: '#8b1e3f' },
  { mode: '城郊消费型', color: '#6a1b9a' },
]

function getModeColor(mode) {
  return modeColors.find(m => m.mode === mode)?.color || '#666'
}

// AHP 准则层配色（生态产品价值实现 3 层 + 乡村振兴 5 层）
const criteriaColors = {
  '生态效益': '#1b5e20',
  '经济效益': '#c79a00',
  '社会效益': '#0277bd',
  '产业兴旺': '#6a1b9a',
  '生态宜居': '#00838f',
  '乡风文明': '#8b1e3f',
  '治理有效': '#e65100',
  '生活富裕': '#5d4037',
}

function getCriteriaColor(name) {
  return criteriaColors[name] || '#666'
}

async function loadCompare() {
  const res = await request.get('/dashboard/compare', { params: { metric: metric.value, year: year.value } })
  compareData.value = res.items || []
  await nextTick()
  renderBar()
  renderScatter()
}

async function loadOverview() {
  const res = await request.get('/dashboard/overview', { params: { year: year.value } })
  overviewData.value = res.items || []
  await nextTick()
  renderRadar()
}

async function loadTimeline() {
  // 拉取所有区县的5年趋势
  const res = await request.get('/dashboard/regions')
  const regions = res.regions || []
  const years = [2020, 2021, 2022, 2023, 2024]
  const series = []
  for (const r of regions) {
    try {
      const tl = await request.get('/dashboard/timeline', { params: { region: r.name, metric: metric.value } })
      series.push({
        name: r.name.replace(/省|市|区|县/g, m => m === '省' || m === '市' ? '' : m).slice(0, 6),
        type: 'line',
        smooth: true,
        data: tl.values,
        itemStyle: { color: r.color },
        lineStyle: { color: r.color, width: 2 },
        symbol: 'circle',
        symbolSize: 6,
      })
    } catch (e) {}
  }
  await nextTick()
  renderLine(years, series)
}

async function loadWeights() {
  try {
    const res = await request.get('/dashboard/weights')
    weightsData.value = res || {}
    await nextTick()
    renderWeights()
  } catch (e) {}
}

async function loadCluster() {
  try {
    const res = await request.get('/dashboard/cluster')
    clusterData.value = res.items || []
    await nextTick()
    renderCluster()
  } catch (e) {}
}

function renderBar() {
  if (!barChart) barChart = echarts.init(barChartRef.value)
  const names = compareData.value.map(d => d.name.replace(/省|市|区|县/g, '').slice(0, 10))
  const values = compareData.value.map(d => d.value)
  const colors = compareData.value.map(d => d.color)

  barChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: names, axisLabel: { rotate: 30, fontSize: 11 } },
    yAxis: { type: 'value', name: metricLabel.value },
    series: [{
      type: 'bar',
      data: values.map((v, i) => ({ value: v, itemStyle: { color: colors[i] } })),
      label: { show: true, position: 'top', formatter: '{c}', fontSize: 11 },
      barWidth: '50%',
    }],
  })
}

function renderLine(years, series) {
  if (!lineChart) lineChart = echarts.init(lineChartRef.value)
  lineChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { type: 'scroll', bottom: 0, textStyle: { fontSize: 11 } },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: { type: 'category', data: years.map(String) },
    yAxis: { type: 'value', name: metricLabel.value },
    series,
  }, true)
}

function renderRadar() {
  if (!radarChart) radarChart = echarts.init(radarChartRef.value)
  // 每种模式选1个代表区县（按 eco_score + rural_score 最高）
  const byMode = {}
  for (const r of overviewData.value) {
    const total = (r.eco_score || 0) + (r.rural_score || 0)
    if (!byMode[r.cluster] || total > byMode[r.cluster].total) {
      byMode[r.cluster] = { ...r, total }
    }
  }
  const indicators = [
    { name: '生态得分', max: 100 },
    { name: '振兴得分', max: 100 },
    { name: '耦合协调度', max: 1 },
    { name: '森林率(归一)', max: 100 },
    { name: '收入(归一)', max: 50000 },
  ]
  const series = [{
    type: 'radar',
    data: Object.values(byMode).map(r => ({
      value: [
        r.eco_score,
        r.rural_score,
        r.d_value,
        r.forest,
        r.income,
      ],
      name: r.cluster,
      itemStyle: { color: getModeColor(r.cluster) },
      areaStyle: { opacity: 0.1 },
    })),
  }]
  radarChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, textStyle: { fontSize: 11 } },
    radar: { indicator: indicators, radius: '65%' },
    series,
  }, true)
}

function renderScatter() {
  if (!scatterChart) scatterChart = echarts.init(scatterChartRef.value)
  const data = overviewData.value.map(r => ({
    name: r.name.replace(/省|市|区|县/g, '').slice(0, 8),
    value: [r.eco_score, r.rural_score, r.d_value, r.cluster],
    itemStyle: { color: getModeColor(r.cluster) },
  }))
  scatterChart.setOption({
    tooltip: {
      formatter: p => `${p.data.name}<br/>生态: ${p.value[0]}<br/>振兴: ${p.value[1]}<br/>D: ${p.value[2]}<br/>模式: ${p.value[3]}`,
    },
    xAxis: { type: 'value', name: '生态产品价值实现得分', min: 30, max: 100 },
    yAxis: { type: 'value', name: '乡村振兴水平得分', min: 30, max: 100 },
    series: [{
      type: 'scatter',
      data,
      symbolSize: 18,
      label: {
        show: true,
        position: 'right',
        formatter: p => p.data.name,
        fontSize: 10,
      },
    }],
  }, true)
}

function renderWeights() {
  if (!weightsChart) weightsChart = echarts.init(weightsChartRef.value)
  const data = weightsData.value
  // 按体系顺序收集所有指标，保持准则层分组顺序
  const systems = ['生态产品价值实现', '乡村振兴']
  const allItems = []
  for (const sys of systems) {
    if (!data[sys]) continue
    for (const criteria of Object.keys(data[sys])) {
      for (const item of (data[sys][criteria] || [])) {
        allItems.push({
          name: item.indicator,
          system: sys,
          criteria,
          weight: item.weight,
          attribute: item.attribute,
        })
      }
    }
  }
  // Y 轴标签（先收集，再反转用于自上而下展示）
  const yLabels = allItems.map(it => it.name)
  // 准则层去重，保留出现顺序
  const criteriaSet = []
  for (const it of allItems) {
    if (!criteriaSet.includes(it.criteria)) criteriaSet.push(it.criteria)
  }
  // 每个准则层一个 series，便于图例切换与配色
  const series = criteriaSet.map(criteria => ({
    name: criteria,
    type: 'bar',
    stack: 'ahp',
    // 反转数据，使第一个指标显示在顶部
    data: allItems.slice().reverse().map(it =>
      it.criteria === criteria ? Number(it.weight) : null
    ),
    itemStyle: { color: getCriteriaColor(criteria) },
    label: {
      show: true,
      position: 'right',
      formatter: p => (p.value != null ? Number(p.value).toFixed(4) : ''),
      fontSize: 10,
    },
  }))
  weightsChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: params => {
        const p = params.find(p => p.value != null)
        if (!p) return ''
        const idx = allItems.length - 1 - p.dataIndex
        const it = allItems[idx]
        if (!it) return ''
        const attr = it.attribute === '+' ? '正向(+)效益' : (it.attribute === '-' ? '负向(-)效益' : `属性: ${it.attribute}`)
        return `${it.name}<br/>指标体系: ${it.system}<br/>准则层: ${it.criteria}<br/>${attr}<br/>组合权重: ${Number(it.weight).toFixed(4)}`
      },
    },
    legend: { bottom: 0, textStyle: { fontSize: 11 } },
    grid: { left: '3%', right: '8%', bottom: '12%', containLabel: true },
    xAxis: {
      type: 'value',
      name: '组合权重',
      axisLabel: { fontSize: 11 },
    },
    yAxis: {
      type: 'category',
      data: yLabels.slice().reverse(),
      axisLabel: { fontSize: 11 },
    },
    series,
  }, true)
}

function renderCluster() {
  if (!clusterChart) clusterChart = echarts.init(clusterChartRef.value)
  const items = clusterData.value || []
  // 按 mode_type 分组
  const byMode = {}
  for (const it of items) {
    const mode = it.mode_type || `簇${it.cluster}`
    if (!byMode[mode]) byMode[mode] = []
    byMode[mode].push([
      Number(it.pc1),
      Number(it.pc2),
      it.region,
      it.cluster,
      it.mode_type,
    ])
  }
  const series = Object.entries(byMode).map(([mode, arr]) => ({
    name: mode,
    type: 'scatter',
    data: arr,
    symbolSize: 16,
    itemStyle: { color: getModeColor(mode) },
    label: {
      show: true,
      position: 'right',
      formatter: p => String(p.data[2] || '').replace(/省|市|区|县/g, '').slice(0, 6),
      fontSize: 10,
    },
  }))
  clusterChart.setOption({
    tooltip: {
      formatter: p => {
        const d = p.data
        return `${d[2]}<br/>模式: ${d[4] || p.seriesName}<br/>聚类簇: ${d[3]}<br/>PC1: ${Number(d[0]).toFixed(3)}<br/>PC2: ${Number(d[1]).toFixed(3)}`
      },
    },
    legend: { bottom: 0, textStyle: { fontSize: 11 } },
    grid: { left: '3%', right: '8%', bottom: '15%', containLabel: true },
    xAxis: { type: 'value', name: 'PC1', axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value', name: 'PC2', axisLabel: { fontSize: 11 } },
    series,
  }, true)
}

function handleResize() {
  barChart?.resize()
  lineChart?.resize()
  radarChart?.resize()
  scatterChart?.resize()
  weightsChart?.resize()
  clusterChart?.resize()
}

onMounted(async () => {
  await loadCompare()
  await loadOverview()
  await loadTimeline()
  await loadWeights()
  await loadCluster()
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-page { min-height: 100vh; }

.page-header {
  background: linear-gradient(180deg, var(--gp-paper-2) 0%, transparent 100%);
  padding: 48px 0 24px;
  border-bottom: 1px solid var(--gp-line);
}

.page-title {
  font-family: var(--font-serif);
  font-size: 36px;
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

.controls {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  margin: 24px 0;
  display: flex;
  gap: 32px;
  align-items: center;
  box-shadow: var(--shadow-soft);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-group label {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--gp-ink-2);
  letter-spacing: 0.05em;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 18px 22px;
  box-shadow: var(--shadow-soft);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
  background: var(--gp-forest);
}

.stat-label {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-gold);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.stat-value {
  font-family: var(--font-serif);
  font-size: 32px;
  font-weight: 700;
  color: var(--gp-forest);
  line-height: 1.1;
}

.stat-value.highlight {
  color: var(--gp-clay);
}

.stat-sub {
  font-size: 12px;
  color: var(--gp-ink-2);
  margin-top: 4px;
}

.chart-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-soft);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed var(--gp-line);
}

.chart-title {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--gp-forest);
  margin: 0;
}

.chart-subtitle {
  font-size: 12px;
  color: var(--gp-ink-2);
}

.legend-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.legend-tag {
  padding: 2px 10px;
  font-size: 11px;
  color: #fff;
  border-radius: 100px;
  font-weight: 600;
}

.chart-box {
  width: 100%;
  height: 420px;
}

.chart-box-tall {
  height: 640px;
}

@media (max-width: 768px) {
  .controls { flex-direction: column; align-items: stretch; gap: 12px; }
  .stat-cards { grid-template-columns: repeat(2, 1fr); }
  .chart-box { height: 320px; }
  .chart-box-tall { height: 480px; }
}
</style>
