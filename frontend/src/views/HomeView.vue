<template>
  <div class="home">
    <!-- ============ Hero 区 ============ -->
    <section class="hero">
      <!-- 背景装饰 -->
      <div class="hero-mountain"></div>
      <div class="hero-grid"></div>

      <div class="hero-content">
        <div class="hero-eyebrow gp-anim-fade-up" style="animation-delay: 0.1s">
          <span class="dot"></span>
          <span>中国研究生乡村振兴科技强农+创新大赛</span>
        </div>

        <h1 class="hero-title gp-anim-fade-up" style="animation-delay: 0.2s">
          <span class="title-line">绿脉兴农</span>
          <span class="title-sub">生态产品价值实现赋能乡村振兴一体化智能系统</span>
        </h1>

        <p class="hero-desc gp-anim-fade-up" style="animation-delay: 0.4s">
          基于 AHP 层次分析 · 熵权法 · 耦合协调度 · 障碍度模型，<br />
          一站式完成 <span class="hl">政策检索 · 数据评估 · AI 模式识别 · 路径优化</span>
        </p>

        <div class="hero-actions gp-anim-fade-up" style="animation-delay: 0.6s">
          <button class="gp-btn-primary gp-btn-gold" @click="$router.push('/analysis')">
            <el-icon><DataAnalysis /></el-icon>
            开始智能评估
          </button>
          <button class="gp-btn-primary gp-btn-outline" @click="$router.push('/case')">
            查看典型案例
          </button>
        </div>

        <div class="hero-stats gp-anim-fade-up" style="animation-delay: 0.8s">
          <div class="stat">
            <div class="stat-num">5</div>
            <div class="stat-label">发展模式</div>
          </div>
          <div class="stat-sep">·</div>
          <div class="stat">
            <div class="stat-num">4</div>
            <div class="stat-label">评估模型</div>
          </div>
          <div class="stat-sep">·</div>
          <div class="stat">
            <div class="stat-num">27</div>
            <div class="stat-label">核心指标</div>
          </div>
          <div class="stat-sep">·</div>
          <div class="stat">
            <div class="stat-num">AI</div>
            <div class="stat-label">路径优化</div>
          </div>
        </div>
      </div>

      <!-- 印章 -->
      <div class="hero-seal">
        <div class="seal-inner">
          <span>绿脉</span>
          <span>兴农</span>
        </div>
      </div>
    </section>

    <!-- ============ 核心方法论 ============ -->
    <section class="page-wrap">
      <div class="gp-anim-fade-up">
        <div class="section-eyebrow">核心方法论 · METHODOLOGY</div>
        <h2 class="section-title">四模型驱动 · AI 智能识别</h2>
        <p class="section-subtitle">
          融合 AHP 层次分析、熵权法、耦合协调度、障碍度四大模型，
          结合 DeepSeek AI 大模型，自动识别五种生态产品价值实现模式并输出差异化路径优化建议。
        </p>
      </div>

      <div class="method-grid">
        <div class="method-card gp-anim-fade-up" style="animation-delay: 0.1s">
          <div class="method-num">01</div>
          <h3>AHP 层次分析</h3>
          <p>构建生态产品价值实现（11项指标）与乡村振兴（15项指标）两级指标体系，通过专家判断矩阵计算组合权重。</p>
        </div>
        <div class="method-card gp-anim-fade-up" style="animation-delay: 0.2s">
          <div class="method-num">02</div>
          <h3>熵权法</h3>
          <p>基于10个区县5年面板数据的信息熵，客观赋权计算生态产品价值实现综合指数与乡村振兴综合指数。</p>
        </div>
        <div class="method-card gp-anim-fade-up" style="animation-delay: 0.3s">
          <div class="method-num">03</div>
          <h3>耦合协调度模型</h3>
          <p>测算生态产品价值实现与乡村振兴两大系统的耦合协调度 D∈[0,1]，划分10个等级判定协调发展水平。</p>
        </div>
        <div class="method-card gp-anim-fade-up" style="animation-delay: 0.4s">
          <div class="method-num">04</div>
          <h3>障碍度模型</h3>
          <p>识别制约生态产品价值实现与乡村振兴协同发展的关键障碍因子，定位改进优先方向。</p>
        </div>
      </div>

      <div class="gp-divider">
        <span class="gp-divider-mark">❖</span>
      </div>
    </section>

    <!-- ============ 四大功能 ============ -->
    <section class="page-wrap">
      <div class="gp-anim-fade-up">
        <div class="section-eyebrow">四大核心功能 · CORE MODULES</div>
        <h2 class="section-title">从政策到落地，一站式赋能</h2>
        <p class="section-subtitle">
          覆盖政策检索、数据评估、AI 路径优化、产品交易、案例学习全链路。
        </p>
      </div>

      <div class="feature-grid">
        <div
          v-for="(f, i) in features"
          :key="f.path"
          class="feature-card gp-anim-fade-up"
          :style="{ animationDelay: 0.1 * (i + 1) + 's' }"
          @click="$router.push(f.path)"
        >
          <div class="feature-icon-wrap" :style="{ background: f.bg }">
            <el-icon :size="32">
              <component :is="f.icon" />
            </el-icon>
          </div>
          <div class="feature-num">0{{ i + 1 }}</div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
          <div class="feature-arrow">
            进入 <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ 五种模式 ============ -->
    <section class="modes-section">
      <div class="page-wrap">
        <div class="gp-anim-fade-up">
          <div class="section-eyebrow">五种发展模式 · FIVE PARADIGMS</div>
          <h2 class="section-title">因地制宜，因势利导</h2>
          <p class="section-subtitle">
            基于层次聚类分析，将10个典型区县划分为五种生态产品价值实现模式。
            AI 智能分析中心根据地区生态、经济、社会指标自动识别所属模式，并输出差异化路径优化建议。
          </p>
        </div>

        <div class="modes-grid">
          <div
            v-for="(m, i) in modes"
            :key="m.name"
            class="mode-card gp-anim-fade-up"
            :style="{ animationDelay: 0.1 * (i + 1) + 's' }"
          >
            <div class="mode-num">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="mode-name">{{ m.name }}</div>
            <div class="mode-tag">{{ m.tag }}</div>
            <p class="mode-desc">{{ m.desc }}</p>
            <div class="mode-criteria">
              <span class="mode-criteria-label">识别阈值：</span>
              <span>{{ m.criteria }}</span>
            </div>
            <div class="mode-path">
              <span class="gp-chip gp-chip-gold">路径优化</span>
              <span class="mode-path-text">{{ m.path }}</span>
            </div>
          </div>
        </div>

        <div class="modes-cta gp-anim-fade-up">
          <button class="gp-btn-primary gp-btn-gold" @click="$router.push('/analysis')">
            <el-icon><DataAnalysis /></el-icon>
            立即体验 AI 模式识别
          </button>
        </div>
      </div>
    </section>

    <!-- ============ 评估流程 ============ -->
    <section class="page-wrap">
      <div class="gp-anim-fade-up">
        <div class="section-eyebrow">智能评估流程 · WORKFLOW</div>
        <h2 class="section-title">五步生成专业评估报告</h2>
      </div>

      <div class="flow-grid">
        <div
          v-for="(step, i) in flowSteps"
          :key="i"
          class="flow-item gp-anim-fade-up"
          :style="{ animationDelay: 0.1 * (i + 1) + 's' }"
        >
          <div class="flow-num">{{ String(i + 1).padStart(2, '0') }}</div>
          <div class="flow-title">{{ step.title }}</div>
          <p class="flow-desc">{{ step.desc }}</p>
          <div class="flow-arrow" v-if="i < flowSteps.length - 1">→</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const features = [
  { title: '政策中心', desc: '汇集国家级 / 省级 / 地市级乡村振兴与生态产品价值实现政策，支持主题、级别、关键词多维检索。', icon: 'Document', path: '/policy', bg: 'linear-gradient(135deg, #f5ead5, #e6c449)' },
  { title: '智能分析', desc: '上传地区数据，自动完成 4 维评估、AI 模式识别、路径优化建议生成与 PDF 报告下载。', icon: 'DataAnalysis', path: '/analysis', bg: 'linear-gradient(135deg, #cad2c5, #52796f)' },
  { title: '农产品商城', desc: '面向农户与合作社的生态农产品展示与交易平台，缩短农户与市场的距离。', icon: 'ShoppingCart', path: '/mall', bg: 'linear-gradient(135deg, #f0ebe0, #c79a00)' },
  { title: '案例中心', desc: '汇集全国 5 种模式的典型生态产品价值实现案例，供学习借鉴。', icon: 'Collection', path: '/case', bg: 'linear-gradient(135deg, #cad2c5, #2d6a4f)' },
]

const modes = [
  {
    name: '生态康养型',
    tag: '森林 / 温泉 / 气候',
    desc: '依托森林、温泉、气候等生态资源，发展康养度假、疗养保健业态。',
    criteria: '森林覆盖率≥65%，城镇化率≤55%，空气优良率≥80%',
    path: '建设森林康养基地、开发气候疗养产品、打造康养小镇品牌',
  },
  {
    name: '湿地水域型',
    tag: '湿地 / 水域 / 滨海',
    desc: '依托湿地、水域生态系统，发展生态旅游、碳汇交易、生态补偿。',
    criteria: '水质达标率≥95%，重要生态保护区面积占比突出',
    path: '建设湿地公园、发展保水渔业、探索水权交易与碳汇交易',
  },
  {
    name: '农业品牌型',
    tag: '区域公用品牌',
    desc: '依托特色农产品区域公用品牌，延伸产业链，提升附加值。',
    criteria: '粮食播种面积≥10万公顷，农产品产出≥90万吨',
    path: '打造区域公用品牌、建设三品一标体系、延伸精深加工产业链',
  },
  {
    name: '农文旅融合型',
    tag: '三产融合',
    desc: '农业、文化、旅游深度融合，发展研学、体验、文创多元业态。',
    criteria: '森林覆盖率≥15%，空气优良率≥80%，文化资源丰富',
    path: '开发研学线路、建设文创工坊、举办乡村节庆、培育特色民宿',
  },
  {
    name: '城郊消费型',
    tag: '近郊 / 城市圈',
    desc: '依托城郊区位，面向城市居民消费需求，发展体验式农业与休闲。',
    criteria: '城镇化率≥70%，GDP≥1000亿元，农村人均收入≥4万元',
    path: '建设都市农园、发展采摘体验、打造城郊休闲综合体、培育周末经济',
  },
]

const flowSteps = [
  { title: '上传数据', desc: '按指标模板录入地区生态、经济、社会数据。' },
  { title: '模型评估', desc: '加权综合评分 + 耦合协调度 + 障碍度模型计算。' },
  { title: 'AI 模式识别', desc: 'DeepSeek 智能判定五种发展模式之一。' },
  { title: '路径优化', desc: '生成 500-800 字差异化路径优化建议。' },
  { title: 'PDF 报告', desc: '一键导出专业评估报告，便于汇报与归档。' },
]
</script>

<style scoped>
/* ============ Hero ============ */
.hero {
  position: relative;
  min-height: 88vh;
  padding: 120px 32px 80px;
  background: linear-gradient(180deg, var(--gp-paper) 0%, var(--gp-paper-2) 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-mountain {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%;
  background:
    linear-gradient(180deg, transparent 0%, rgba(13, 59, 46, 0.04) 100%),
    url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 400' xmlns='http://www.w3.org/2000/svg' preserveAspectRatio='none'%3E%3Cpath d='M0,400 L0,250 Q150,150 300,200 T600,180 Q750,100 900,170 T1200,150 L1200,400 Z' fill='%230d3b2e' fill-opacity='0.06'/%3E%3Cpath d='M0,400 L0,320 Q200,250 400,290 T800,280 Q1000,220 1200,260 L1200,400 Z' fill='%232d6a4f' fill-opacity='0.06'/%3E%3C/svg%3E") no-repeat bottom / cover;
  pointer-events: none;
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(199, 154, 0, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(199, 154, 0, 0.04) 1px, transparent 1px);
  background-size: 80px 80px;
  pointer-events: none;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1100px;
  text-align: center;
}

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 18px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--gp-line);
  border-radius: 100px;
  font-size: 12px;
  color: var(--gp-ink-2);
  letter-spacing: 0.1em;
  backdrop-filter: blur(4px);
  margin-bottom: 32px;
}

.hero-eyebrow .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--gp-gold);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.hero-title {
  margin: 0 0 32px;
}

.title-line {
  display: block;
  font-family: var(--font-serif);
  font-size: 96px;
  font-weight: 900;
  letter-spacing: 0.2em;
  background: linear-gradient(135deg, var(--gp-forest) 0%, var(--gp-forest-3) 50%, var(--gp-gold) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
  margin-left: 0.2em;
}

.title-sub {
  display: block;
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 500;
  color: var(--gp-ink-2);
  letter-spacing: 0.15em;
  margin-top: 12px;
}

.hero-desc {
  font-size: 16px;
  line-height: 2;
  color: var(--gp-ink-2);
  margin: 0 auto 40px;
  max-width: 720px;
}

.hero-desc .hl {
  color: var(--gp-forest);
  font-weight: 600;
  border-bottom: 1.5px dashed var(--gp-gold);
  padding-bottom: 2px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 60px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 32px;
  justify-content: center;
  padding: 24px 40px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  backdrop-filter: blur(8px);
  max-width: 720px;
  margin: 0 auto;
}

.stat-num {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 600;
  color: var(--gp-forest);
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: var(--gp-ink-3);
  letter-spacing: 0.15em;
  margin-top: 6px;
}

.stat-sep {
  color: var(--gp-gold);
  font-size: 20px;
}

.hero-seal {
  position: absolute;
  top: 15%;
  right: 8%;
  width: 100px;
  height: 100px;
  background: var(--gp-red);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotate(-8deg);
  box-shadow: 0 8px 32px rgba(139, 30, 63, 0.3);
  opacity: 0.95;
}

.seal-inner {
  width: 86px;
  height: 86px;
  border: 2px solid #fff;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.1em;
  line-height: 1.4;
}

/* ============ 核心方法论 ============ */
.method-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 32px;
}

.method-card {
  position: relative;
  padding: 32px 24px;
  border-radius: var(--radius-md);
  background: #fff;
  border: 1px solid var(--gp-line);
  box-shadow: var(--shadow-soft);
  transition: all 0.4s ease;
  overflow: hidden;
}

.method-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--gp-forest) 0%, var(--gp-gold) 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.method-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
  border-color: var(--gp-gold);
}

.method-card:hover::before { transform: scaleX(1); }

.method-num {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 700;
  color: var(--gp-gold);
  letter-spacing: 0.1em;
  opacity: 0.5;
  line-height: 1;
  margin-bottom: 16px;
}

.method-card h3 {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  color: var(--gp-forest);
  margin: 0 0 12px;
}

.method-card p {
  color: var(--gp-ink-2);
  line-height: 1.8;
  font-size: 13px;
  margin: 0;
}

/* ============ 功能卡片 ============ */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 32px;
}

.feature-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 32px 24px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  border-color: var(--gp-forest-3);
  transform: translateY(-6px);
  box-shadow: var(--shadow-hover);
}

.feature-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gp-forest);
  margin-bottom: 20px;
}

.feature-num {
  position: absolute;
  top: 20px;
  right: 24px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--gp-ink-3);
  letter-spacing: 0.2em;
}

.feature-card h3 {
  font-size: 22px;
  margin: 0 0 12px;
  color: var(--gp-forest);
}

.feature-card p {
  color: var(--gp-ink-2);
  line-height: 1.8;
  font-size: 13px;
  margin: 0 0 20px;
}

.feature-arrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--gp-gold);
  letter-spacing: 0.1em;
  transition: gap 0.3s;
}

.feature-card:hover .feature-arrow { gap: 12px; }

/* ============ 五种模式 ============ */
.modes-section {
  background: linear-gradient(180deg, var(--gp-paper-2) 0%, var(--gp-paper) 100%);
  padding: 48px 0;
}

.modes-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-top: 32px;
}

.mode-card {
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 28px 20px;
  text-align: left;
  position: relative;
  transition: all 0.3s;
  cursor: default;
}

.mode-card:hover {
  border-color: var(--gp-gold);
  background: linear-gradient(135deg, #fffdf6 0%, #fff 100%);
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

.mode-num {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--gp-gold);
  letter-spacing: 0.2em;
  margin-bottom: 12px;
}

.mode-name {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  color: var(--gp-forest);
  margin-bottom: 6px;
}

.mode-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--gp-ink-3);
  letter-spacing: 0.1em;
  margin-bottom: 12px;
}

.mode-desc {
  font-size: 12px;
  line-height: 1.7;
  color: var(--gp-ink-2);
  margin: 0 0 14px;
}

.mode-criteria {
  padding: 10px 12px;
  background: rgba(13, 59, 46, 0.04);
  border-left: 2px solid var(--gp-forest-3);
  border-radius: 4px;
  font-size: 11px;
  line-height: 1.6;
  color: var(--gp-ink-2);
  margin-bottom: 12px;
}

.mode-criteria-label {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--gp-forest);
  letter-spacing: 0.05em;
}

.mode-path {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px dashed var(--gp-line);
}

.mode-path-text {
  font-size: 11px;
  line-height: 1.6;
  color: var(--gp-ink-2);
  flex: 1;
}

.modes-cta {
  text-align: center;
  margin-top: 40px;
}

/* ============ 流程 ============ */
.flow-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-top: 32px;
  position: relative;
}

.flow-item {
  position: relative;
  background: #fff;
  border: 1px solid var(--gp-line);
  border-radius: var(--radius-md);
  padding: 24px;
  text-align: center;
  transition: all 0.3s;
}

.flow-item:hover {
  border-color: var(--gp-forest-3);
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

.flow-num {
  display: inline-flex;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--gp-forest);
  color: #fff;
  font-family: var(--font-mono);
  font-weight: 600;
  margin-bottom: 16px;
}

.flow-title {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  color: var(--gp-forest);
  margin-bottom: 8px;
}

.flow-desc {
  font-size: 12px;
  color: var(--gp-ink-2);
  line-height: 1.7;
  margin: 0;
}

.flow-arrow {
  position: absolute;
  right: -16px;
  top: 40%;
  color: var(--gp-gold);
  font-size: 24px;
  font-weight: 300;
  z-index: 2;
}

/* ============ 响应式 ============ */
@media (max-width: 1024px) {
  .method-grid { grid-template-columns: repeat(2, 1fr); }
  .feature-grid { grid-template-columns: repeat(2, 1fr); }
  .modes-grid { grid-template-columns: repeat(2, 1fr); }
  .flow-grid { grid-template-columns: repeat(2, 1fr); }
  .flow-arrow { display: none; }
  .title-line { font-size: 64px; }
  .hero-seal { display: none; }
}

@media (max-width: 768px) {
  .hero { padding: 80px 16px 60px; }
  .title-line { font-size: 44px; }
  .title-sub { font-size: 14px; }
  .hero-stats { flex-wrap: wrap; gap: 16px; padding: 16px; }
  .stat-sep { display: none; }
  .feature-grid { grid-template-columns: 1fr; }
  .modes-grid { grid-template-columns: 1fr; }
  .flow-grid { grid-template-columns: 1fr; }
}
</style>
