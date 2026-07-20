"""种子数据脚本：填充25条政策、5个案例、10个农产品

用法：python seed_data.py
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.policy import Policy
from app.models.case import Case
from app.models.product import Product
import bcrypt


def hash_password(plain: str) -> str:
    """直接用 bcrypt 模块生成密码哈希（passlib 在新版 bcrypt 上有兼容性问题）"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")

# ============= 政策数据（25条）=============
POLICIES = [
    # 国家级 - 生态产品价值实现
    {
        "title": "关于建立健全生态产品价值实现机制的意见",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2021-02-19",
        "source": "中共中央办公厅 国务院办公厅",
        "url": "https://www.gov.cn/zhengce/2021-02/24/content_5588535.htm",
        "content": "到2025年，生态产品价值实现的制度框架初步建立，生态产品价值核算、生态产品交易、生态补偿等机制基本形成；到2035年，完善的生态产品价值实现机制全面建立。"
    },
    {
        "title": "生态保护补偿条例",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2024-04-10",
        "source": "国务院",
        "url": "https://www.gov.cn/zhengce/content/202405/content_6953611.htm",
        "content": "规范生态保护补偿活动，坚持政府主导、社会参与，统筹生态效益、经济效益和社会效益，建立健全市场化、多元化生态保护补偿机制。"
    },
    {
        "title": "关于深化生态保护补偿制度改革的意见",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2021-09-12",
        "source": "中共中央办公厅 国务院办公厅",
        "url": "https://www.gov.cn/zhengce/2021-09/13/content_5632304.htm",
        "content": "完善生态保护补偿体制机制，加快构建市场化、多元化生态保护补偿制度体系，推动生态保护补偿工作制度化、规范化。"
    },
    {
        "title": "关于推行生态产品价值实现机制试点示范工作的通知",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2022-03-28",
        "source": "国家发展改革委",
        "url": "https://www.ndrc.gov.cn/",
        "content": "在浙江丽水、江西抚州等地区开展生态产品价值实现机制试点，探索形成可复制可推广的经验做法。"
    },
    {
        "title": "生态系统生产总值（GEP）核算技术指南",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2020-09-22",
        "source": "国家发展改革委 国家统计局",
        "url": "https://www.ndrc.gov.cn/",
        "content": "规范生态系统生产总值核算方法，为生态产品价值实现提供技术支撑。GEP包括供给服务、调节服务和文化服务三类。"
    },
    # 国家级 - 乡村振兴
    {
        "title": "中华人民共和国乡村振兴促进法",
        "category": "乡村振兴",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2021-04-29",
        "source": "全国人民代表大会常务委员会",
        "url": "https://www.gov.cn/xinwen/2021-04/30/content_5654363.htm",
        "content": "全面实施乡村振兴战略，推进乡村产业振兴、人才振兴、文化振兴、生态振兴、组织振兴，促进城乡融合发展。"
    },
    {
        "title": "中共中央 国务院关于做好2023年全面推进乡村振兴重点工作的意见",
        "category": "乡村振兴",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2023-01-02",
        "source": "中共中央 国务院",
        "url": "https://www.gov.cn/zhengce/2023-02/13/content_5742160.htm",
        "content": "提出加快建设农业强国，建设宜居宜业和美乡村，全方位夯实粮食安全根基。"
    },
    {
        "title": "全国乡村产业发展规划（2020-2025年）",
        "category": "乡村振兴",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2020-07-09",
        "source": "农业农村部",
        "url": "http://www.moa.gov.cn/",
        "content": "推动乡村产业高质量发展，提升农产品加工业、拓展乡村特色产业、优化乡村休闲旅游业、推进乡村新型服务业。"
    },
    {
        "title": "关于推动乡村人才振兴的意见",
        "category": "乡村振兴",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2021-02-23",
        "source": "中共中央办公厅 国务院办公厅",
        "url": "https://www.gov.cn/zhengce/2021-02/24/content_5588545.htm",
        "content": "加快培养农业生产经营、农村二三产业发展、乡村公共服务、乡村治理、农业农村科技五类人才。"
    },
    {
        "title": "农村人居环境整治提升五年行动方案（2021-2025年）",
        "category": "乡村振兴",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2021-12-05",
        "source": "中共中央办公厅 国务院办公厅",
        "url": "https://www.gov.cn/zhengce/2021-12/05/content_5655776.htm",
        "content": "扎实推进农村厕所革命、生活污水垃圾治理、村容村貌提升，全面提升农村人居环境质量。"
    },
    # 省级 - 江苏/浙江/福建
    {
        "title": "江苏省乡村振兴促进条例",
        "category": "乡村振兴",
        "level": "省级",
        "region": "江苏省",
        "publish_date": "2022-09-29",
        "source": "江苏省人民代表大会常务委员会",
        "url": "https://www.jsrd.gov.cn/",
        "content": "江苏省推进乡村振兴的法治保障，明确产业兴旺、生态宜居、乡风文明、治理有效、生活富裕的总要求。"
    },
    {
        "title": "江苏省建立健全生态产品价值实现机制实施方案",
        "category": "生态产品价值实现",
        "level": "省级",
        "region": "江苏省",
        "publish_date": "2022-06-20",
        "source": "江苏省人民政府办公厅",
        "url": "https://www.jiangsu.gov.cn/",
        "content": "推进生态产品调查监测、价值评价、经营开发、保护补偿、保障机制五大体系建设。"
    },
    {
        "title": '浙江省深化"两山"理念推进生态文明建设实施方案',
        "category": "生态产品价值实现",
        "level": "省级",
        "region": "浙江省",
        "publish_date": "2020-08-15",
        "source": "浙江省人民政府",
        "url": "https://www.zj.gov.cn/",
        "content": '深入践行"绿水青山就是金山银山"理念，建设美丽浙江，示范引领全国生态文明建设。'
    },
    {
        "title": "浙江省丽水市生态产品价值实现机制试点方案",
        "category": "生态产品价值实现",
        "level": "省级",
        "region": "浙江省丽水市",
        "publish_date": "2019-05-12",
        "source": "浙江省人民政府",
        "url": "https://www.zj.gov.cn/",
        "content": "建立生态产品价值核算体系、交易平台、补偿机制，打造全国生态产品价值实现机制试点样板。"
    },
    {
        "title": "福建省生态产品价值实现机制试点方案",
        "category": "生态产品价值实现",
        "level": "省级",
        "region": "福建省南平市",
        "publish_date": "2020-11-10",
        "source": "福建省人民政府",
        "url": "https://www.fujian.gov.cn/",
        "content": "探索生态银行、生态产品价值核算、生态产品交易等模式，将生态优势转化为经济优势。"
    },
    {
        "title": '江苏省"十四五"推进农业农村现代化规划',
        "category": "乡村振兴",
        "level": "省级",
        "region": "江苏省",
        "publish_date": "2021-12-30",
        "source": "江苏省人民政府办公厅",
        "url": "https://www.jiangsu.gov.cn/",
        "content": "围绕农业高质高效、乡村宜居宜业、农民富裕富足，加快农业农村现代化进程。"
    },
    # 地市级
    {
        "title": "南京市乡村振兴战略实施规划（2018-2022年）",
        "category": "乡村振兴",
        "level": "地市级",
        "region": "江苏省南京市",
        "publish_date": "2018-11-15",
        "source": "南京市人民政府",
        "url": "https://www.nanjing.gov.cn/",
        "content": "推进南京都市现代农业建设，发展休闲农业、创意农业，建设一批特色田园乡村。"
    },
    {
        "title": '溧水区生态产品价值实现机制试点方案',
        "category": "生态产品价值实现",
        "level": "地市级",
        "region": "江苏省南京市溧水区",
        "publish_date": "2023-03-10",
        "source": "溧水区人民政府",
        "url": "https://www.njls.gov.cn/",
        "content": "在石湫、晶桥、白马等街道镇开展生态产品价值核算与交易试点，建设生态产品交易平台。"
    },
    {
        "title": '杭州市淳安县"两山"转化实施方案',
        "category": "生态产品价值实现",
        "level": "地市级",
        "region": "浙江省杭州市淳安县",
        "publish_date": "2022-04-22",
        "source": "淳安县人民政府",
        "url": "http://www.qiandao.gov.cn/",
        "content": "依托千岛湖生态资源，发展生态旅游、生态农业，建设绿水青山向金山银山转化示范县。"
    },
    {
        "title": '苏州市昆山市特色田园乡村建设实施方案',
        "category": "乡村振兴",
        "level": "地市级",
        "region": "江苏省苏州市昆山市",
        "publish_date": "2021-06-18",
        "source": "昆山市人民政府",
        "url": "https://www.ks.gov.cn/",
        "content": "推进特色田园乡村建设，培育乡村特色产业，提升乡村人居环境，保护乡村文化。"
    },
    {
        "title": "合肥市肥西县农村产业融合发展示范园创建方案",
        "category": "乡村振兴",
        "level": "地市级",
        "region": "安徽省合肥市肥西县",
        "publish_date": "2022-08-08",
        "source": "肥西县人民政府",
        "url": "https://www.ahfeixi.gov.cn/",
        "content": "推进农业与旅游、教育、文化、健康养老等产业深度融合，创建国家农村产业融合发展示范园。"
    },
    {
        "title": "广州市从化区生态产品价值实现机制试点方案",
        "category": "生态产品价值实现",
        "level": "地市级",
        "region": "广东省广州市从化区",
        "publish_date": "2021-10-25",
        "source": "从化区人民政府",
        "url": "http://www.conghua.gov.cn/",
        "content": "依托流溪河生态资源，建设生态产品交易中心，打造北部山区生态产品价值实现样板。"
    },
    {
        "title": "成都市郫都区战旗村乡村振兴示范案例",
        "category": "乡村振兴",
        "level": "地市级",
        "region": "四川省成都市郫都区",
        "publish_date": "2023-01-15",
        "source": "郫都区人民政府",
        "url": "http://www.pidu.gov.cn/",
        "content": "以战旗村为样板，推进农村集体经营性建设用地入市，发展乡村旅游和特色农产品。"
    },
    {
        "title": '农业农村部关于实施农产品"三品一标"提升行动的通知',
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2022-09-15",
        "source": "农业农村部",
        "url": "http://www.moa.gov.cn/",
        "content": "推动绿色食品、有机农产品、农产品地理标志和达标合格农产品发展，提升农产品质量安全水平。"
    },
    {
        "title": "国家林业和草原局关于推进国家森林城市建设的指导意见",
        "category": "生态产品价值实现",
        "level": "国家级",
        "region": "全国",
        "publish_date": "2023-06-30",
        "source": "国家林业和草原局",
        "url": "https://www.forestry.gov.cn/",
        "content": "推进城乡绿化一体化，建设国家森林城市，提供更多优质生态产品，满足人民日益增长的优美生态环境需要。"
    },
]

# ============= 案例数据（5个）=============
CASES = [
    {
        "title": '浙江丽水：生态产品价值实现"丽水样板"',
        "region": "浙江省丽水市",
        "mode_type": "生态康养型",
        "summary": "丽水市作为全国首个生态产品价值实现机制试点市，建立GEP核算体系，发展生态农业、生态旅游、生态康养产业，2019年GEP达5316亿元。",
        "content": """【背景】丽水市森林覆盖率81.7%，被誉为"浙江绿谷"。2019年成为全国首个生态产品价值实现机制试点市。

【做法】
1. 构建GEP核算体系：出台《丽水市生态产品价值核算技术规范》，建立市、县、乡三级GEP核算体系。
2. 推进生态产品交易：建立生态产品交易平台，开展水权、林权、碳汇交易。
3. 发展生态产业：培育"丽水山耕"生态农产品品牌、"丽水山居"民宿品牌、"丽水山景"旅游景区。
4. 完善生态补偿：建立市域内生态补偿机制，对生态保护区进行转移支付。

【成效】
- 2019年丽水GEP达5316亿元，GDP达1477亿元，GEP/GDP比值3.6
- 农民人均可支配收入从2018年19975元增长到2023年29028元
- 培育"丽水山耕"品牌农产品400余个
- "丽水山居"民宿农家乐超过3000家

【启示】通过GEP核算让"绿水青山"有价可依，通过品牌化运营让生态产品有市可循，实现生态价值向经济价值转化。""",
        "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80"
    },
    {
        "title": '江苏南京石湫：影视基地+生态康养融合发展',
        "region": "江苏省南京市溧水区石湫街道",
        "mode_type": "农文旅融合型",
        "summary": '石湫街道依托影视基地和生态资源，打造"影视+文旅+康养"融合发展模式，年接待游客超100万人次，带动村民人均增收1.2万元。',
        "content": """【背景】石湫街道位于南京市溧水区南部，拥有石湫影视基地、西横山生态区、环山河湿地等资源。

【做法】
1. 影视产业带动：以石湫影视基地为核心，承接影视拍摄，带动旅游消费。
2. 农文旅融合：发展环山河湿地观光、西横山森林康养、生态农业采摘体验。
3. 村庄改造：将周边村庄改造为影视主题民宿、文创商店、特色餐饮。
4. 农民培训：开展群众演员、民宿管家、农产品电商等技能培训。

【成效】
- 年接待游客超100万人次
- 带动周边8个村农户增收，村民人均增收1.2万元
- 发展影视主题民宿60余家
- 培育地方特色农产品品牌15个

【启示】发挥区域特色资源优势，通过"影视+"模式打通农业、文化、旅游产业链，激活乡村经济新动能。""",
        "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"
    },
    {
        "title": '江苏苏州昆山：特色田园乡村建设示范',
        "region": "江苏省苏州市昆山市",
        "mode_type": "农业品牌型",
        "summary": "昆山打造计家墩、祝甸等特色田园乡村，发展稻香文化、水乡民宿、阳澄湖大闸蟹品牌，年旅游收入超30亿元。",
        "content": """【背景】昆山市地处江南水乡，文化底蕴深厚，水网密布，农业资源丰富。

【做法】
1. 特色田园乡村打造：建设计家墩理想村、祝甸砖窑文化村、朱浜村等特色田园乡村。
2. 品牌农业培育：做强阳澄湖大闸蟹、巴城葡萄、淀山湖大米等品牌。
3. 文创+民宿：引入设计师驻村，将老宅改造为文创空间和精品民宿。
4. 节庆活动：举办大闸蟹开捕节、稻田艺术节、乡村音乐节等品牌活动。

【成效】
- 年接待游客超500万人次
- 阳澄湖大闸蟹品牌价值超600亿元
- 培育特色田园乡村20余个
- 带动农民人均可支配收入达4.8万元

【启示】以文化为魂、以农业为基、以旅游为媒，实现农业、文化、旅游深度融合，打造可复制可推广的水乡振兴样板。""",
        "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"
    },
    {
        "title": '福建南平："生态银行"激活绿色资源',
        "region": "福建省南平市",
        "mode_type": "湿地水域型",
        "summary": '南平市创新"生态银行"模式，将碎片化生态资源集中收储、规模化运营，2022年生态产品价值实现额超200亿元。',
        "content": """【背景】南平市森林覆盖率78.29%，被誉为"南方林海"，但生态资源分散、规模化经营难。

【做法】
1. "生态银行"模式：借鉴商业银行"分散输入、集中输出"理念，将碎片化生态资源集中收储。
2. 资源整合：整合林权、水权、宅基地使用权等，形成可规模经营的项目包。
3. 产业导入：引入企业进行规模化经营，发展生态林业、生态旅游、生态农业。
4. 利益共享：建立"公司+合作社+农户"利益联结机制，保障农民收益。

【成效】
- 2022年生态产品价值实现额超200亿元
- 收储林权130万亩，发展林下经济60万亩
- 培育"武夷山水"区域公共品牌
- 带动农民人均增收2.5万元

【启示】通过"生态银行"模式破解资源碎片化难题，实现生态资源规模化、集约化经营，是生态产品价值实现的有效路径。""",
        "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&q=80"
    },
    {
        "title": '四川成都战旗村：集体经营性建设用地入市样板',
        "region": "四川省成都市郫都区战旗村",
        "mode_type": "城郊消费型",
        "summary": "战旗村作为全国首批农村集体经营性建设用地入市改革试点，发展乡村旅游和特色农产品，年接待游客超80万人次，村集体经济收入超600万元。",
        "content": """【背景】战旗村位于成都市郫都区，是习近平总书记2018年视察地，也是农村集体经营性建设用地入市改革首批试点。

【做法】
1. 集体土地入市：2015年敲响全国农村集体经营性建设用地入市"第一槌"，每亩52.5万元成交。
2. 乡村十八坊：发展豆瓣、酱油、豆腐等传统手工作坊，打造乡村体验式消费场景。
3. 第五季妈妈农庄：建设现代农业观光园，发展亲子研学、农事体验。
4. 集体经济壮大：组建村集体资产管理公司，实现村民变股民。

【成效】
- 年接待游客超80万人次
- 村集体经济收入超600万元
- 村民人均可支配收入达3.8万元
- 培育"战旗豆瓣""战旗米"等特色品牌

【启示】通过土地制度改革激活农村资源要素，通过场景营造打造消费新业态，实现集体经济壮大与农民增收双赢。""",
        "image_url": "https://images.unsplash.com/photo-1504788363733-507549153474?w=1200&q=80"
    },
]

# ============= 商品数据（10个，含图片URL）=============
PRODUCTS = [
    {
        "name": "溧水白马蓝莓",
        "category": "果蔬",
        "origin": "江苏南京溧水白马镇",
        "price": 88.0,
        "stock": 200,
        "image_url": "https://images.unsplash.com/photo-1583511655826-05700d52f4d9?w=800&q=80",
        "eco_cert": "绿色食品认证",
        "description": "溧水白马镇蓝莓基地直供，个大味甜，富含花青素，0农残绿色认证。"
    },
    {
        "name": "石湫生态大米",
        "category": "粮食",
        "origin": "江苏南京溧水石湫",
        "price": 49.9,
        "stock": 500,
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865074da31?w=800&q=80",
        "eco_cert": "有机产品认证",
        "description": "西横山生态种植，不打农药不施化肥，米香浓郁口感软糯，5kg装。"
    },
    {
        "name": "阳澄湖大闸蟹礼盒",
        "category": "畜禽",
        "origin": "江苏苏州昆山阳澄湖",
        "price": 588.0,
        "stock": 80,
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53b0c12c0c0?w=800&q=80",
        "eco_cert": "地理标志产品",
        "description": "阳澄湖正宗大闸蟹，青壳白肚金爪黄毛，母蟹2.5两+公蟹3.5两，4对8只装。"
    },
    {
        "name": "丽水山耕香菇",
        "category": "特产",
        "origin": "浙江丽水",
        "price": 68.0,
        "stock": 300,
        "image_url": "https://images.unsplash.com/photo-1544200179-ca6e80c8d2de?w=800&q=80",
        "eco_cert": "森林食品认证",
        "description": "丽水深山椴木香菇，自然生长晒干，肉质厚实香味浓郁，250g装。"
    },
    {
        "name": "武夷山岩茶大红袍",
        "category": "茶叶",
        "origin": "福建南平武夷山",
        "price": 328.0,
        "stock": 100,
        "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=80",
        "eco_cert": "地理标志产品",
        "description": "武夷山核心产区岩茶，传统炭焙工艺，岩韵浓郁回甘持久，100g礼罐装。"
    },
    {
        "name": "安吉白茶明前特级",
        "category": "茶叶",
        "origin": "浙江湖州安吉",
        "price": 458.0,
        "stock": 60,
        "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9c4a6?w=800&q=80",
        "eco_cert": "有机产品认证",
        "description": "安吉高山明前采摘，外形挺直披毫，汤色嫩绿明亮，清香甘醇，50g装。"
    },
    {
        "name": "战旗村手工豆瓣",
        "category": "加工品",
        "origin": "四川成都郫都战旗村",
        "price": 38.0,
        "stock": 500,
        "image_url": "https://images.unsplash.com/photo-1607301405964-d50e65c8c3e5?w=800&q=80",
        "eco_cert": "地理标志产品",
        "description": "战旗村百年老坊手工酿造，蚕豆+二荆条辣椒，日光晒露1年以上，500g装。"
    },
    {
        "name": "淳安千岛湖有机鱼头",
        "category": "畜禽",
        "origin": "浙江杭州淳安千岛湖",
        "price": 128.0,
        "stock": 150,
        "image_url": "https://images.unsplash.com/photo-1535140728325-a4d3707eee95?w=800&q=80",
        "eco_cert": "有机产品认证",
        "description": "千岛湖野生放养鳙鱼鱼头，肉质紧实无泥腥味，3斤装，冷链直达。"
    },
    {
        "name": "巴城阳光玫瑰葡萄",
        "category": "果蔬",
        "origin": "江苏苏州昆山巴城",
        "price": 98.0,
        "stock": 200,
        "image_url": "https://images.unsplash.com/photo-1599477173151-9f4b9c8c8e1d?w=800&q=80",
        "eco_cert": "绿色食品认证",
        "description": "巴城阳光玫瑰葡萄，果穗大果粒匀，浓郁玫瑰香气甜度20+，2斤装。"
    },
    {
        "name": "肥西老母鸡礼盒",
        "category": "畜禽",
        "origin": "安徽合肥肥西",
        "price": 188.0,
        "stock": 100,
        "image_url": "https://images.unsplash.com/photo-1605195999683-88f3e3c9c28a?w=800&q=80",
        "eco_cert": "无公害农产品",
        "description": "肥西散养300天老母鸡，谷物喂养，肉质紧实适合炖汤，2只装礼盒。"
    },
]


def main():
    """填充种子数据"""
    print("=" * 60)
    print("绿脉兴农 · 种子数据填充")
    print("=" * 60)

    # 先测试数据库连接，连不上就优雅退出（构建阶段数据库不可用）
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[seed] ✓ 数据库连接正常")
    except Exception as e:
        print(f"[seed] 数据库暂不可用（构建阶段正常），跳过数据填充: {e}")
        return  # exit code 0，不阻塞构建

    # 创建表
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. 创建一个商户账号
        print("\n[1/4] 创建商户账号...")
        merchant = db.query(User).filter(User.username == "merchant001").first()
        if not merchant:
            merchant = User(
                username="merchant001",
                email="merchant@greenpulse.cn",
                phone="13800138001",
                role="merchant",
                hashed_password=hash_password("123456"),
            )
            db.add(merchant)
            db.commit()
            db.refresh(merchant)
            print(f"  ✓ 商户账号: merchant001 / 123456 (id={merchant.id})")
        else:
            print(f"  - 商户已存在: merchant001 (id={merchant.id})")

        # 2. 填充政策
        print(f"\n[2/4] 填充政策数据（共 {len(POLICIES)} 条）...")
        existing_policies = db.query(Policy).count()
        if existing_policies == 0:
            for p in POLICIES:
                db.add(Policy(
                    title=p["title"],
                    category=p["category"],
                    level=p["level"],
                    region=p["region"],
                    publish_date=datetime.fromisoformat(p["publish_date"]),
                    source=p["source"],
                    url=p["url"],
                    content=p["content"],
                ))
            db.commit()
            print(f"  ✓ 已插入 {len(POLICIES)} 条政策")
        else:
            print(f"  - 政策已存在 {existing_policies} 条，跳过")

        # 3. 填充案例
        print(f"\n[3/4] 填充案例数据（共 {len(CASES)} 个）...")
        existing_cases = db.query(Case).count()
        if existing_cases == 0:
            for c in CASES:
                db.add(Case(
                    title=c["title"],
                    region=c["region"],
                    mode_type=c["mode_type"],
                    summary=c["summary"],
                    content=c["content"],
                    image_url=c["image_url"],
                ))
            db.commit()
            print(f"  ✓ 已插入 {len(CASES)} 个案例")
        else:
            print(f"  - 案例已存在 {existing_cases} 个，跳过")

        # 4. 填充商品
        print(f"\n[4/4] 填充商品数据（共 {len(PRODUCTS)} 个）...")
        existing_products = db.query(Product).count()
        if existing_products == 0:
            for p in PRODUCTS:
                db.add(Product(
                    name=p["name"],
                    category=p["category"],
                    origin=p["origin"],
                    price=p["price"],
                    stock=p["stock"],
                    image_url=p["image_url"],
                    eco_cert=p["eco_cert"],
                    description=p["description"],
                    merchant_id=merchant.id,
                    is_approved=True,
                ))
            db.commit()
            print(f"  ✓ 已插入 {len(PRODUCTS)} 个商品")
        else:
            print(f"  - 商品已存在 {existing_products} 个，跳过")

        # 总结
        print("\n" + "=" * 60)
        print("数据填充完成！统计：")
        print(f"  政策: {db.query(Policy).count()} 条")
        print(f"  案例: {db.query(Case).count()} 个")
        print(f"  商品: {db.query(Product).count()} 个")
        print(f"  用户: {db.query(User).count()} 个")
        print("=" * 60)

    except Exception as e:
        # 即使数据初始化失败，也不要阻塞部署
        import traceback
        print(f"\n[seed] 数据填充出错（不阻塞部署）: {e}")
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
