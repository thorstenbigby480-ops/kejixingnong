<template>
  <div class="analysis-page">
    <!-- 头部 -->
    <div class="page-header">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">智能分析中心 · INTELLIGENT ANALYSIS</div>
          <h1 class="page-title">生态产品价值实现评估</h1>
          <p class="page-subtitle">
            上传地区数据 → 4 维模型评估 → AI 模式识别 → 路径优化建议 → PDF 报告导出
          </p>
        </div>
      </div>
    </div>

    <div class="page-wrap">
      <div class="analysis-layout">
        <!-- 左侧：表单 -->
        <div class="form-side gp-anim-fade-up">
          <div class="form-card">
            <div class="card-header">
              <div class="card-title">
                <span class="card-num">01</span>
                数据录入
              </div>
              <el-button link type="primary" @click="loadTemplate">
                <el-icon><Download /></el-icon> 加载模板
              </el-button>
            </div>

            <el-form label-position="top" class="gp-form">
              <div class="form-section">
                <div class="form-section-title">基础信息</div>
                <el-form-item label="地区名称">
                  <el-input v-model="form.region_name" placeholder="如：江苏省南京市溧水区石湫镇">
                    <template #prefix><el-icon><Location /></el-icon></template>
                  </el-input>
                </el-form-item>
                <el-form-item label="评估年份">
                  <el-input v-model.number="form.year" placeholder="2024">
                    <template #prefix><el-icon><Calendar /></el-icon></template>
                  </el-input>
                </el-form-item>
              </div>

              <div class="form-section">
                <div class="form-section-title">
                  <span class="dot green"></span>
                  生态产品价值实现成效指标
                  <span class="form-section-tag">{{ ecoKeys.length }} 项</span>
                </div>
                <div v-for="k in ecoKeys" :key="k" class="form-item">
                  <label class="form-label">{{ k }}</label>
                  <el-input-number v-model="form.data[k]" :controls="false" placeholder="0" />
                </div>
              </div>

              <div class="form-section">
                <div class="form-section-title">
                  <span class="dot gold"></span>
                  乡村振兴水平指标
                  <span class="form-section-tag">{{ ruralKeys.length }} 项</span>
                </div>
                <div v-for="k in ruralKeys" :key="k" class="form-item">
                  <label class="form-label">{{ k }}</label>
                  <el-input-number v-model="form.data[k]" :controls="false" placeholder="0" />
                </div>
              </div>

              <div class="form-actions">
                <el-button type="primary" size="large" :loading="loading" @click="onSubmit">
                  <el-icon><DataLine /></el-icon>
                  开始智能评估
                </el-button>
                <el-button size="large" @click="onReset">重置</el-button>
              </div>
            </el-form>
          </div>
        </div>

        <!-- 右侧：结果 -->
        <div class="result-side">
          <!-- 空状态 -->
          <div v-if="!result" class="empty-card gp-anim-fade-in">
            <div class="empty-icon">
              <el-icon :size="64"><DataAnalysis /></el-icon>
            </div>
            <h3>等待评估</h3>
            <p>请填写左侧数据后点击「开始智能评估」</p>
            <p class="empty-hint">系统将自动计算 4 维指标并调用 DeepSeek 生成路径建议</p>
          </div>

          <!-- 结果展示 -->
          <div v-else class="result-content gp-anim-fade-up">
            <!-- 综合得分卡 -->
            <div class="score-hero">
              <div class="score-header">
                <div>
                  <div class="score-eyebrow">综合评估结果</div>
                  <div class="score-region">{{ result.region_name }} · {{ result.year }}</div>
                </div>
                <el-button type="primary" @click="downloadReport">
                  <el-icon><Download /></el-icon> 下载 PDF
                </el-button>
              </div>

              <div class="score-main">
                <div class="score-card eco">
                  <div class="score-label">生态产品价值实现</div>
                  <div class="score-value">
                    <span class="num">{{ result.eco_score }}</span>
                    <span class="unit">/100</span>
                  </div>
                  <div class="score-bar">
                    <div class="bar-fill" :style="{ width: result.eco_score + '%' }"></div>
                  </div>
                </div>

                <div class="score-card rural">
                  <div class="score-label">乡村振兴水平</div>
                  <div class="score-value">
                    <span class="num">{{ result.rural_score }}</span>
                    <span class="unit">/100</span>
                  </div>
                  <div class="score-bar">
                    <div class="bar-fill gold" :style="{ width: result.rural_score + '%' }"></div>
                  </div>
                </div>
              </div>

              <div class="ccd-box">
                <div class="ccd-left">
                  <div class="ccd-label">耦合协调度 D 值</div>
                  <div class="ccd-value">{{ result.coupling_d }}</div>
                </div>
                <div class="ccd-right">
                  <div class="ccd-label">协调等级</div>
                  <div class="ccd-tag" :class="levelClass(result.coordination_level)">
                    {{ result.coordination_level }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 模式判定 -->
            <div class="mode-banner">
              <div class="mode-banner-bg"></div>
              <div class="mode-banner-content">
                <div class="mode-banner-eyebrow">AI 模式识别结果</div>
                <div class="mode-banner-title">{{ result.mode_type }}</div>
                <div class="mode-banner-reason">{{ result.mode_reason }}</div>
              </div>
              <div class="mode-banner-seal">AI</div>
            </div>

            <!-- 雷达图 + 障碍图 -->
            <div class="charts-grid">
              <div class="chart-card">
                <div class="chart-title">维度评分雷达</div>
                <div ref="radarChartRef" class="chart-box"></div>
              </div>
              <div class="chart-card">
                <div class="chart-title">主要障碍因子 Top 5</div>
                <div ref="obstacleChartRef" class="chart-box"></div>
              </div>
            </div>

            <!-- AI 建议 -->
            <div class="advice-card">
              <div class="advice-header">
                <div>
                  <div class="advice-eyebrow">路径优化建议 · DEEPSEEK AI</div>
                  <div class="advice-title">差异化发展策略</div>
                </div>
                <span class="gp-chip gp-chip-gold">AI 生成</span>
              </div>
              <div class="advice-body">{{ result.advice }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import request from '../api'

const ecoKeys = ref([])
const ruralKeys = ref([])
const form = reactive({ region_name: '', year: 2024, data: {} })
const loading = ref(false)
const result = ref(null)
const radarChartRef = ref(null)
const obstacleChartRef = ref(null)
let radarChart = null
let obstacleChart = null

async function loadTemplate() {
  const res = await request.get('/analysis/template')
  ecoKeys.value = res.eco_indicators || []
  ruralKeys.value = res.rural_indicators || []
  for (const k of [...ecoKeys.value, ...ruralKeys.value]) {
    if (form.data[k] === undefined) form.data[k] = null
  }
  ElMessage.success('指标模板已加载')
}

async function onSubmit() {
  if (!form.region_name) return ElMessage.error('请填写地区名称')
  loading.value = true
  try {
    const data = {}
    for (const [k, v] of Object.entries(form.data)) {
      if (v !== null && v !== undefined && v !== '') data[k] = v
    }
    const fd = new FormData()
    fd.append('region_name', form.region_name)
    fd.append('year', form.year || '')
    fd.append('data', JSON.stringify(data))
    result.value = await request.post('/analysis/assess', fd)
    await nextTick()
    renderRadarChart()
    renderObstacleChart()
    ElMessage.success('评估完成')
  } finally {
    loading.value = false
  }
}

function onReset() {
  for (const k of Object.keys(form.data)) form.data[k] = null
  result.value = null
}

function levelClass(level) {
  if (!level) return ''
  if (level.includes('失调')) return 'level-bad'
  if (level.includes('协调')) return 'level-good'
  return 'level-mid'
}

function renderRadarChart() {
  if (!radarChartRef.value || !result.value) return
  const ecoDim = result.value.eco_dim_scores || {}
  const ruralDim = result.value.rural_dim_scores || {}
  const allDims = Array.from(new Set([...Object.keys(ecoDim), ...Object.keys(ruralDim)]))
  if (radarChart) radarChart.dispose()
  radarChart = echarts.init(radarChartRef.value)
  radarChart.setOption({
    tooltip: {},
    legend: { data: ['生态产品', '乡村振兴'], bottom: 0, textStyle: { fontSize: 11 } },
    radar: {
      indicator: allDims.map(d => ({ name: d.length > 4 ? d.slice(0, 4) + '..' : d, max: 100 })),
      axisName: { color: '#4a4a4a', fontSize: 11 },
      splitArea: { areaStyle: { color: ['rgba(13,59,46,0.02)', 'rgba(13,59,46,0.05)'] } },
      splitLine: { lineStyle: { color: '#d8d2c4' } },
    },
    series: [{
      type: 'radar',
      data: [
        { value: allDims.map(d => ecoDim[d] || 0), name: '生态产品', areaStyle: { color: 'rgba(13,59,46,0.2)' }, lineStyle: { color: '#0d3b2e' } },
        { value: allDims.map(d => ruralDim[d] || 0), name: '乡村振兴', areaStyle: { color: 'rgba(199,154,0,0.2)' }, lineStyle: { color: '#c79a00' } },
      ],
    }],
  })
}

function renderObstacleChart() {
  if (!obstacleChartRef.value || !result.value) return
  const items = Object.entries(result.value.obstacles || {}).slice(0, 5).reverse()
  if (obstacleChart) obstacleChart.dispose()
  obstacleChart = echarts.init(obstacleChartRef.value)
  obstacleChart.setOption({
    grid: { left: '40%', right: 40, top: 10, bottom: 20 },
    xAxis: { type: 'value', max: 1, axisLabel: { fontSize: 10 } },
    yAxis: {
      type: 'category',
      data: items.map(([k]) => k.length > 10 ? k.slice(0, 10) + '..' : k),
      axisLabel: { fontSize: 11, color: '#4a4a4a' },
    },
    series: [{
      type: 'bar',
      data: items.map(([, v]) => v),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#c79a00' },
          { offset: 1, color: '#8b1e3f' },
        ]),
      },
      label: { show: true, position: 'right', formatter: '{c}', fontSize: 11 },
    }],
  })
}

async function downloadReport() {
  if (!result.value?.id) return
  // 先触发后端生成报告
  await request.get(`/analysis/${result.value.id}/report`)
  // 通过 baseURL 拼接 PDF 路径，避免硬编码 localhost
  const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
  const apiOrigin = baseURL.replace(/\/api$/, '')
  window.open(`${apiOrigin}/uploads/report_${result.value.id}.pdf`, '_blank')
}

onMounted(loadTemplate)
</script>

<style scoped>
.analysis-page { min-height: 100vh; }

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
  line-height: 1.8;
}

.analysis-layout {
  display: grid;
  grid-template-columns: 480px 1fr;
  gap: 32px;
  align-items: start;
}

/* === 表单 === */
.form-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  position: sticky;
  top: 100px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(180deg, #fffdf6 0%, #fff 100%);
  border-bottom: 1px solid var(--gp-line);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--gp-forest);
}

.card-num {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  color: var(--gp-gold);
  letter-spacing: 0.15em;
  background: var(--gp-cream);
  padding: 4px 8px;
  border-radius: 4px;
}

.gp-form { padding: 20px 24px; }

.form-section { margin-bottom: 24px; }

.form-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 600;
  color: var(--gp-forest);
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px dashed var(--gp-line);
}

.form-section-tag {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-ink-3);
  font-weight: normal;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.dot.green { background: var(--gp-forest); }
.dot.gold { background: var(--gp-gold); }

.form-item { margin-bottom: 12px; }
.form-label {
  display: block;
  font-size: 12px;
  color: var(--gp-ink-2);
  margin-bottom: 4px;
  line-height: 1.4;
}

.form-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--gp-line);
}

/* === 结果区 === */
.result-side { min-height: 600px; }

.empty-card {
  background: #fff;
  border: 1px dashed var(--gp-line);
  border-radius: var(--radius-md);
  padding: 80px 32px;
  text-align: center;
}

.empty-icon { color: var(--gp-moss); margin-bottom: 20px; }
.empty-card h3 { color: var(--gp-ink-2); margin: 0 0 8px; }
.empty-card p { color: var(--gp-ink-3); margin: 0 0 8px; }
.empty-hint { font-size: 13px !important; }

/* === 综合得分 === */
.score-hero {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
  padding: 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}

.score-hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--gp-forest) 0%, var(--gp-gold) 100%);
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.score-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-gold);
  letter-spacing: 0.2em;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.score-region {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--gp-forest);
}

.score-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.score-card {
  padding: 20px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, rgba(13, 59, 46, 0.04) 0%, rgba(13, 59, 46, 0.02) 100%);
}

.score-card.rural {
  background: linear-gradient(135deg, rgba(199, 154, 0, 0.06) 0%, rgba(199, 154, 0, 0.02) 100%);
}

.score-label {
  font-size: 12px;
  color: var(--gp-ink-3);
  margin-bottom: 8px;
  letter-spacing: 0.05em;
}

.score-value { margin-bottom: 12px; }
.score-value .num {
  font-family: var(--font-mono);
  font-size: 42px;
  font-weight: 600;
  color: var(--gp-forest);
}
.score-card.rural .num { color: var(--gp-clay); }
.score-value .unit {
  font-size: 14px;
  color: var(--gp-ink-3);
}

.score-bar {
  height: 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gp-forest) 0%, var(--gp-forest-3) 100%);
  transition: width 1s ease;
}
.bar-fill.gold {
  background: linear-gradient(90deg, var(--gp-gold) 0%, var(--gp-gold-light) 100%);
}

.ccd-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  padding: 20px;
  background: var(--gp-paper);
  border-radius: var(--radius-sm);
}

.ccd-label {
  font-size: 11px;
  color: var(--gp-ink-3);
  margin-bottom: 8px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.ccd-value {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 600;
  color: var(--gp-forest);
}

.ccd-tag {
  display: inline-block;
  padding: 6px 14px;
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 600;
  border-radius: 4px;
  border: 1px solid;
}
.ccd-tag.level-good { background: rgba(45, 106, 79, 0.08); color: var(--gp-forest-3); border-color: var(--gp-forest-3); }
.ccd-tag.level-bad { background: rgba(139, 30, 63, 0.08); color: var(--gp-red); border-color: var(--gp-red); }
.ccd-tag.level-mid { background: rgba(199, 154, 0, 0.08); color: var(--gp-clay); border-color: var(--gp-gold); }

/* === 模式横幅 === */
.mode-banner {
  position: relative;
  background: linear-gradient(135deg, var(--gp-forest) 0%, var(--gp-forest-3) 100%);
  border-radius: var(--radius-md);
  padding: 32px;
  margin-bottom: 24px;
  overflow: hidden;
  color: #fff;
}

.mode-banner-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 80% 30%, rgba(199, 154, 0, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 40%);
  pointer-events: none;
}

.mode-banner-content { position: relative; z-index: 2; }

.mode-banner-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.3em;
  color: var(--gp-gold-light);
  margin-bottom: 8px;
  text-transform: uppercase;
}

.mode-banner-title {
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: 0.05em;
}

.mode-banner-reason {
  font-size: 13px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.85);
  max-width: 80%;
}

.mode-banner-seal {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 60px;
  height: 60px;
  background: var(--gp-red);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.05em;
  transform: rotate(-8deg);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

/* === 图表 === */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.chart-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-soft);
}

.chart-title {
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 600;
  color: var(--gp-forest);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px dashed var(--gp-line);
}

.chart-box {
  width: 100%;
  height: 280px;
}

/* === AI 建议 === */
.advice-card {
  background: linear-gradient(135deg, #fffdf6 0%, #fdf8e8 100%);
  border: 1px solid var(--gp-gold-light);
  border-radius: var(--radius-md);
  padding: 28px;
  box-shadow: var(--shadow-gold);
  position: relative;
}

.advice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--gp-gold);
}

.advice-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-clay);
  letter-spacing: 0.2em;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.advice-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--gp-forest);
}

.advice-body {
  white-space: pre-wrap;
  line-height: 2;
  color: var(--gp-ink);
  font-size: 14px;
}

@media (max-width: 1100px) {
  .analysis-layout { grid-template-columns: 1fr; }
  .form-card { position: static; }
  .charts-grid { grid-template-columns: 1fr; }
  .score-main { grid-template-columns: 1fr; }
  .ccd-box { grid-template-columns: 1fr; }
}
</style>
