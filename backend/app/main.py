"""FastAPI 入口"""
import os
import bcrypt
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.policy import Policy
from app.models.case import Case
from app.models.product import Product
from app.api import auth, policy, analysis, mall, case, dashboard


def seed_data():
    """应用启动时自动填充种子数据（如果表为空）"""
    db = SessionLocal()
    try:
        # 1. 创建商户用户
        existing_user = db.query(User).filter(User.username == "merchant001").first()
        if not existing_user:
            salt = bcrypt.gensalt()
            hashed_pwd = bcrypt.hashpw("123456".encode("utf-8"), salt).decode("utf-8")
            merchant = User(
                username="merchant001",
                email="merchant@greenpulse.com",
                hashed_password=hashed_pwd,
                phone="13800138000",
                role="merchant",
            )
            db.add(merchant)
            db.commit()
            db.refresh(merchant)
            print("[seed] ✓ 创建商户用户 merchant001")
        else:
            merchant = existing_user
            print("[seed] - 商户用户已存在，跳过")

        # 3. 政策数据（25条：国家级+省级+地市级）
        if db.query(Policy).count() == 0:
            policies = [
                # === 国家级 - 生态产品价值实现（5条）===
                {"title": "关于建立健全生态产品价值实现机制的意见", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2021-02-19", "source": "中共中央办公厅 国务院办公厅", "content": "到2025年，生态产品价值实现的制度框架初步建立，生态产品价值核算、生态产品交易、生态补偿等机制基本形成；到2035年，完善的生态产品价值实现机制全面建立。"},
                {"title": "生态保护补偿条例", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2024-04-10", "source": "国务院", "content": "规范生态保护补偿活动，坚持政府主导、社会参与，统筹生态效益、经济效益和社会效益，建立健全市场化、多元化生态保护补偿机制。"},
                {"title": "关于深化生态保护补偿制度改革的意见", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2021-09-12", "source": "中共中央办公厅 国务院办公厅", "content": "完善生态保护补偿体制机制，加快构建市场化、多元化生态保护补偿制度体系，推动生态保护补偿工作制度化、规范化。"},
                {"title": "关于推行生态产品价值实现机制试点示范工作的通知", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2022-03-28", "source": "国家发展改革委", "content": "在浙江丽水、江西抚州等地区开展生态产品价值实现机制试点，探索形成可复制可推广的经验做法。"},
                {"title": "生态系统生产总值（GEP）核算技术指南", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2020-09-22", "source": "国家发展改革委 国家统计局", "content": "规范生态系统生产总值核算方法，为生态产品价值实现提供技术支撑。GEP包括供给服务、调节服务和文化服务三类。"},
                # === 国家级 - 乡村振兴（5条）===
                {"title": "中华人民共和国乡村振兴促进法", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2021-04-29", "source": "全国人民代表大会常务委员会", "content": "全面实施乡村振兴战略，推进乡村产业振兴、人才振兴、文化振兴、生态振兴、组织振兴，促进城乡融合发展。"},
                {"title": "中共中央 国务院关于做好2023年全面推进乡村振兴重点工作的意见", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2023-01-02", "source": "中共中央 国务院", "content": "提出加快建设农业强国，建设宜居宜业和美乡村，全方位夯实粮食安全根基。"},
                {"title": "全国乡村产业发展规划（2020-2025年）", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2020-07-09", "source": "农业农村部", "content": "推动乡村产业高质量发展，提升农产品加工业、拓展乡村特色产业、优化乡村休闲旅游业、推进乡村新型服务业。"},
                {"title": "关于推动乡村人才振兴的意见", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2021-02-23", "source": "中共中央办公厅 国务院办公厅", "content": "加快培养农业生产经营、农村二三产业发展、乡村公共服务、乡村治理、农业农村科技五类人才。"},
                {"title": "农村人居环境整治提升五年行动方案（2021-2025年）", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2021-12-05", "source": "中共中央办公厅 国务院办公厅", "content": "扎实推进农村厕所革命、生活污水垃圾治理、村容村貌提升，全面提升农村人居环境质量。"},
                # === 省级（5条）===
                {"title": "江苏省乡村振兴促进条例", "category": "乡村振兴", "level": "省级", "region": "江苏省", "publish_date": "2022-09-29", "source": "江苏省人民代表大会常务委员会", "content": "江苏省推进乡村振兴的法治保障，明确产业兴旺、生态宜居、乡风文明、治理有效、生活富裕的总要求。"},
                {"title": "江苏省建立健全生态产品价值实现机制实施方案", "category": "生态产品价值实现", "level": "省级", "region": "江苏省", "publish_date": "2022-06-20", "source": "江苏省人民政府办公厅", "content": "推进生态产品调查监测、价值评价、经营开发、保护补偿、保障机制五大体系建设。"},
                {"title": '浙江省深化"两山"理念推进生态文明建设实施方案', "category": "生态产品价值实现", "level": "省级", "region": "浙江省", "publish_date": "2020-08-15", "source": "浙江省人民政府", "content": '深入践行"绿水青山就是金山银山"理念，建设美丽浙江，示范引领全国生态文明建设。'},
                {"title": "浙江省丽水市生态产品价值实现机制试点方案", "category": "生态产品价值实现", "level": "省级", "region": "浙江省丽水市", "publish_date": "2019-05-12", "source": "浙江省人民政府", "content": "建立生态产品价值核算体系、交易平台、补偿机制，打造全国生态产品价值实现机制试点样板。"},
                {"title": '江苏省"十四五"推进农业农村现代化规划', "category": "乡村振兴", "level": "省级", "region": "江苏省", "publish_date": "2021-12-30", "source": "江苏省人民政府办公厅", "content": "围绕农业高质高效、乡村宜居宜业、农民富裕富足，加快农业农村现代化进程。"},
                # === 地市级（6条）===
                {"title": "南京市乡村振兴战略实施规划（2018-2022年）", "category": "乡村振兴", "level": "地市级", "region": "江苏省南京市", "publish_date": "2018-11-15", "source": "南京市人民政府", "content": "推进南京都市现代农业建设，发展休闲农业、创意农业，建设一批特色田园乡村。"},
                {"title": "溧水区生态产品价值实现机制试点方案", "category": "生态产品价值实现", "level": "地市级", "region": "江苏省南京市溧水区", "publish_date": "2023-03-10", "source": "溧水区人民政府", "content": "在石湫、晶桥、白马等街道镇开展生态产品价值核算与交易试点，建设生态产品交易平台。"},
                {"title": '杭州市淳安县"两山"转化实施方案', "category": "生态产品价值实现", "level": "地市级", "region": "浙江省杭州市淳安县", "publish_date": "2022-04-22", "source": "淳安县人民政府", "content": "依托千岛湖生态资源，发展生态旅游、生态农业，建设绿水青山向金山银山转化示范县。"},
                {"title": "苏州市昆山市特色田园乡村建设实施方案", "category": "乡村振兴", "level": "地市级", "region": "江苏省苏州市昆山市", "publish_date": "2021-06-18", "source": "昆山市人民政府", "content": "推进特色田园乡村建设，培育乡村特色产业，提升乡村人居环境，保护乡村文化。"},
                {"title": "合肥市肥西县农村产业融合发展示范园创建方案", "category": "乡村振兴", "level": "地市级", "region": "安徽省合肥市肥西县", "publish_date": "2022-08-08", "source": "肥西县人民政府", "content": "推进农业与旅游、教育、文化、健康养老等产业深度融合，创建国家农村产业融合发展示范园。"},
                {"title": "广州市从化区生态产品价值实现机制试点方案", "category": "生态产品价值实现", "level": "地市级", "region": "广东省广州市从化区", "publish_date": "2021-10-25", "source": "从化区人民政府", "content": "依托流溪河生态资源，建设生态产品交易中心，打造北部山区生态产品价值实现样板。"},
                # === 其他国家级（4条）===
                {"title": '农业农村部关于实施农产品"三品一标"提升行动的通知', "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2022-09-15", "source": "农业农村部", "content": "推动绿色食品、有机农产品、农产品地理标志和达标合格农产品发展，提升农产品质量安全水平。"},
                {"title": "国家林业和草原局关于推进国家森林城市建设的指导意见", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2023-06-30", "source": "国家林业和草原局", "content": "推进城乡绿化一体化，建设国家森林城市，提供更多优质生态产品，满足人民日益增长的优美生态环境需要。"},
                {"title": "国务院关于落实<乡村振兴促进法>重点工作分工的通知", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2021-06-15", "source": "国务院", "content": "明确国务院各部门在乡村振兴工作中的职责分工，确保法律各项规定落地实施。"},
                {"title": "关于金融支持全面推进乡村振兴的指导意见", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2023-03-20", "source": "中国人民银行 农业农村部", "content": "引导金融机构加大对乡村振兴重点领域和薄弱环节的信贷支持，创新绿色金融产品。"},
            ]
            for p in policies:
                db.add(Policy(**p))
            db.commit()
            print(f"[seed] ✓ 插入{len(policies)}条政策")
        else:
            print("[seed] - 政策已存在，跳过")

        # 4. 案例数据（15个：每模式2-3个）
        if db.query(Case).count() == 0:
            cases = [
                # === 生态康养型（3个）===
                {"title": "浙江丽水：GEP核算开创生态价值转化新路", "region": "浙江省丽水市", "mode_type": "生态康养型", "summary": "丽水率先开展GEP核算，将生态资源转化为经济价值，2022年生态产品价值实现额超500亿元，GEP达5316亿元。", "content": "【背景】丽水市森林覆盖率81.7%，被誉为\"浙江绿谷\"。2019年成为全国首个生态产品价值实现机制试点市。\n【做法】1. 构建GEP核算体系；2. 推进生态产品交易；3. 培育\"丽水山耕\"\"丽水山居\"\"丽水山景\"品牌；4. 完善生态补偿。\n【成效】2019年GEP达5316亿元，农民人均可支配收入从19975元增至29028元。", "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80"},
                {"title": "安徽黄山黟县：徽派古村康养旅游典范", "region": "安徽省黄山市黟县", "mode_type": "生态康养型", "summary": "黟县依托西递、宏村世界文化遗产和森林生态资源，发展徽派古村康养旅游，年接待游客超300万人次。", "content": "【背景】黟县森林覆盖率76%，拥有西递、宏村两处世界文化遗产。\n【做法】1. 古村落保护性开发；2. 发展徽派民宿集群；3. 推出森林康养、徽文化体验产品；4. 建立利益共享机制。\n【成效】年接待游客超300万人次，培育精品民宿200余家，村民人均增收1.5万元。", "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"},
                {"title": "四川成都蒲江县：果园康养融合发展示范", "region": "四川省成都市蒲江县", "mode_type": "生态康养型", "summary": "蒲江县依托柑橘、猕猴桃果园生态资源，发展果园康养、农事体验、生态度假，年综合收入超30亿元。", "content": "【背景】蒲江县森林覆盖率50.8%，是国家级柑橘、猕猴桃生产基地。\n【做法】1. 建设果园康养基地；2. 发展\"农业+康养+文旅\"融合业态；3. 推进有机认证；4. 建立联农带农机制。\n【成效】年综合收入超30亿元，培育有机农产品品牌20余个，带动农户2万户。", "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&q=80"},
                # === 湿地水域型（2个）===
                {"title": "浙江淳安：千岛湖生态产品价值实现样板", "region": "浙江省杭州市淳安县", "mode_type": "湿地水域型", "summary": "淳安依托千岛湖优质水资源，发展生态渔业、生态旅游、水权交易，2022年水产品价值实现额超20亿元。", "content": "【背景】千岛湖是国家级重要水源地，水域面积573平方公里。\n【做法】1. 建立\"保水渔业\"模式；2. 发展巨网捕鱼、水上运动等生态旅游；3. 探索水权交易；4. 完善生态补偿机制。\n【成效】2022年水产品价值实现额超20亿元，年接待游客超千万人次，水质常年保持I类。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                {"title": "福建南平：'生态银行'激活绿色资源", "region": "福建省南平市", "mode_type": "湿地水域型", "summary": "南平创新'生态银行'模式，将碎片化生态资源集中收储、规模化运营，2022年生态产品价值实现额超200亿元。", "content": "【背景】南平市森林覆盖率78.29%，被誉为\"南方林海\"。\n【做法】1. 创新\"生态银行\"模式；2. 整合林权、水权、宅基地使用权；3. 引入企业规模经营；4. 建立利益联结机制。\n【成效】2022年生态产品价值实现额超200亿元，收储林权130万亩，培育\"武夷山水\"品牌。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                # === 农业品牌型（3个）===
                {"title": "江苏苏州昆山：特色田园乡村建设示范", "region": "江苏省苏州市昆山市", "mode_type": "农业品牌型", "summary": "昆山打造计家墩、祝甸等特色田园乡村，发展稻香文化、水乡民宿、阳澄湖大闸蟹品牌，年旅游收入超30亿元。", "content": "【背景】昆山市地处江南水乡，文化底蕴深厚。\n【做法】1. 建设计家墩理想村等特色田园乡村；2. 做强阳澄湖大闸蟹品牌；3. 引入设计师驻村；4. 举办品牌节庆活动。\n【成效】年接待游客超500万人次，阳澄湖大闸蟹品牌价值超600亿元，带动农民人均收入4.8万元。", "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"},
                {"title": "江苏泰州兴化：垛田花海打造农业品牌", "region": "江苏省泰州市兴化市", "mode_type": "农业品牌型", "summary": "兴化依托全球重要农业文化遗产垛田，发展千垛菜花旅游、大闸蟹品牌、生态稻米，年综合收入超15亿元。", "content": "【背景】兴化垛田是全球重要农业文化遗产，是独特的垛形耕地。\n【做法】1. 打造千垛菜花旅游品牌；2. 发展\"垛田大闸蟹\"生态养殖；3. 推进\"垛田米\"品牌建设；4. 农文旅融合发展。\n【成效】年综合收入超15亿元，接待游客超200万人次，培育农产品品牌10余个。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                {"title": "江苏淮安盱眙：小龙虾品牌引领产业振兴", "region": "江苏省淮安市盱眙县", "mode_type": "农业品牌型", "summary": "盱眙以\"盱眙龙虾\"品牌为引领，发展龙虾养殖、加工、餐饮、节庆全产业链，品牌价值超350亿元。", "content": "【背景】盱眙县是\"中国龙虾之都\"，拥有独特的山水湖滩生态资源。\n【做法】1. 建设\"盱眙龙虾\"区域公用品牌；2. 发展稻虾综合种养；3. 举办国际龙虾节；4. 延伸加工产业链。\n【成效】品牌价值超350亿元，养殖面积80万亩，带动20万农户增收，年综合收入超百亿。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                # === 农文旅融合型（4个）===
                {"title": "浙江湖州安吉：'两山'理念发源地乡村振兴样板", "region": "浙江省湖州市安吉县", "mode_type": "农文旅融合型", "summary": "安吉作为'两山'理念发源地，发展竹林生态、白茶产业、美丽乡村，年接待游客超3000万人次，旅游收入超400亿。", "content": "【背景】安吉是\"绿水青山就是金山银山\"理念发源地，森林覆盖率70%。\n【做法】1. 建设美丽乡村全域旅游；2. 做强安吉白茶品牌；3. 发展竹产业全链条；4. 打造\"余村\"乡村振兴样板。\n【成效】年接待游客超3000万人次，旅游收入超400亿元，农民人均收入超4万元。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                {"title": "南京石湫：影视基地带动农文旅融合发展", "region": "江苏省南京市溧水区", "mode_type": "农文旅融合型", "summary": "石湫依托影视基地资源，发展乡村旅游和特色农业，年接待游客超100万人次，带动村民人均增收1.2万元。", "content": "【背景】石湫街道拥有石湫影视基地、西横山生态区、环山河湿地等资源。\n【做法】1. 影视产业带动旅游；2. 农文旅融合；3. 村庄改造民宿；4. 农民技能培训。\n【成效】年接待游客超100万人次，发展影视主题民宿60余家，培育特色农产品品牌15个。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                {"title": "南京高淳：慢城模式打造国际慢城品牌", "region": "江苏省南京市高淳区", "mode_type": "农文旅融合型", "summary": "高淳以桠溪国际慢城为核心，发展慢城旅游、固城湖螃蟹品牌、生态农业，年接待游客超千万人次。", "content": "【背景】高淳是中国首个国际慢城，拥有桠溪慢城、固城湖等生态资源。\n【做法】1. 打造国际慢城品牌；2. 做强固城湖螃蟹品牌；3. 发展慢生活民宿；4. 推进生态农业。\n【成效】年接待游客超千万人次，固城湖螃蟹品牌价值超百亿，带动农民人均收入3.5万元。", "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"},
                {"title": "江苏常州溧阳：'1号公路'串联农文旅融合示范带", "region": "江苏省常州市溧阳市", "mode_type": "农文旅融合型", "summary": "溧阳以365公里'1号公路'串联乡村旅游资源，发展白茶、竹海、温泉度假，年旅游收入超200亿元。", "content": "【背景】溧阳拥有天目湖、南山竹海等5A级景区。\n【做法】1. 建设365公里'1号公路'旅游风景道；2. 发展白茶、休闲农庄、温泉度假；3. 打造民宿集群；4. 培育\"天目湖\"品牌。\n【成效】年旅游收入超200亿元，培育民宿500余家，带动农民人均收入3.8万元。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                # === 城郊消费型（3个）===
                {"title": "四川成都战旗村：集体土地入市改革试点", "region": "四川省成都市郫都区", "mode_type": "城郊消费型", "summary": "战旗村通过集体经营性建设用地入市，探索乡村振兴新路径，村集体收入超600万元，年接待游客80万人次。", "content": "【背景】战旗村是习近平总书记2018年视察地，农村集体经营性建设用地入市首批试点。\n【做法】1. 集体土地入市；2. 发展乡村十八坊；3. 建设第五季妈妈农庄；4. 壮大集体经济。\n【成效】年接待游客超80万人次，村集体收入超600万元，村民人均收入3.8万元。", "image_url": "https://images.unsplash.com/photo-1504788363733-507549153474?w=1200&q=80"},
                {"title": "江苏苏州吴中区：城郊农文旅融合发展典范", "region": "江苏省苏州市吴中区", "mode_type": "城郊消费型", "summary": "吴中区依托太湖生态资源，发展碧螺春茶、枇杷杨梅、洞庭蟹等高端农产品，年旅游收入超百亿。", "content": "【背景】吴中区紧邻苏州中心城区，拥有太湖、洞庭山等生态资源。\n【做法】1. 打造\"碧螺春\"等区域品牌；2. 发展城郊休闲农业；3. 建设民宿集群；4. 推进农文旅融合。\n【成效】年旅游收入超百亿，培育高端农产品品牌10余个，带动农民人均收入4.5万元。", "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"},
                {"title": "江苏盐城大丰：荷兰花海打造城郊消费新业态", "region": "江苏省盐城市大丰区", "mode_type": "城郊消费型", "summary": "大丰以荷兰花海为核心，发展花卉产业、婚庆旅游、生态农业，年接待游客超300万人次。", "content": "【背景】大丰区紧邻盐城市区，拥有黄海湿地世界自然遗产。\n【做法】1. 建设荷兰花海景区；2. 发展花卉产业链；3. 培育婚庆消费业态；4. 推进农业品牌建设。\n【成效】年接待游客超300万人次，综合收入超20亿元，带动农民人均收入3.2万元。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
            ]
            for c in cases:
                db.add(Case(**c))
            db.commit()
            print(f"[seed] ✓ 插入{len(cases)}个案例")
        else:
            print("[seed] - 案例已存在，跳过")

        # 4. 商品数据（10个，使用本地图片 /images/xxx.jpg）
        if db.query(Product).count() == 0:
            products = [
                {"name": "兴化大闸蟹", "category": "水产", "origin": "江苏泰州兴化", "price": 588.0, "stock": 100, "image_url": "/images/兴化大闸蟹.jpg", "eco_cert": "地理标志产品", "description": "兴化垛田大闸蟹，青壳白肚金爪黄毛，公4.5两母3.5两，8只装礼盒。"},
                {"name": "吴中东山枇杷", "category": "果蔬", "origin": "江苏苏州吴中", "price": 128.0, "stock": 200, "image_url": "/images/吴中东山枇杷.jpg", "eco_cert": "地理标志产品", "description": "东山白玉枇杷，果肉细腻多汁，甜度18+，2斤装礼盒。"},
                {"name": "大丰恒北早酥梨", "category": "果蔬", "origin": "江苏盐城大丰", "price": 68.0, "stock": 300, "image_url": "/images/大丰恒北早酥梨.jpg", "eco_cert": "绿色食品认证", "description": "恒北村早酥梨，皮薄肉脆汁多，5斤装。"},
                {"name": "安吉白茶", "category": "茶叶", "origin": "浙江湖州安吉", "price": 458.0, "stock": 60, "image_url": "/images/安吉白茶.jpg", "eco_cert": "地理标志产品", "description": "安吉高山明前采摘，清香甘醇，50g礼盒装。"},
                {"name": "淳安辣酱", "category": "加工品", "origin": "浙江杭州淳安", "price": 38.0, "stock": 500, "image_url": "/images/淳安辣酱.jpg", "eco_cert": "无公害农产品", "description": "千岛湖农家手工辣酱，鲜辣醇香，250g装。"},
                {"name": "溧阳天目湖白茶", "category": "茶叶", "origin": "江苏常州溧阳", "price": 528.0, "stock": 80, "image_url": "/images/溧阳天目湖白茶.png", "eco_cert": "地理标志产品", "description": "天目湖白茶，氨基酸含量高，鲜爽回甘，50g礼盒装。"},
                {"name": "盱眙龙虾", "category": "水产", "origin": "江苏淮安盱眙", "price": 168.0, "stock": 150, "image_url": "/images/盱眙龙虾.jpg", "eco_cert": "地理标志产品", "description": "盱眙十三香小龙虾，活体现发，3斤装（约30只）。"},
                {"name": "蒲江县猕猴桃", "category": "果蔬", "origin": "四川成都蒲江", "price": 88.0, "stock": 200, "image_url": "/images/蒲江县猕猴桃.jpg", "eco_cert": "有机产品认证", "description": "蒲江红心猕猴桃，甜度18+，10枚装礼盒。"},
                {"name": "高淳雨花茶", "category": "茶叶", "origin": "江苏南京高淳", "price": 368.0, "stock": 100, "image_url": "/images/高淳雨花茶.jpg", "eco_cert": "地理标志产品", "description": "高淳雨花茶，条索紧细翠绿，清香高雅，100g礼盒装。"},
                {"name": "黟县香榧", "category": "特产", "origin": "安徽黄山黟县", "price": 158.0, "stock": 120, "image_url": "/images/黟县香榧.jpg", "eco_cert": "地理标志产品", "description": "黟县香榧，香脆可口营养丰富，250g礼盒装。"},
            ]
            for p in products:
                p["merchant_id"] = merchant.id
                p["is_approved"] = True
                db.add(Product(**p))
            db.commit()
            print("[seed] ✓ 插入10个商品")
        else:
            print("[seed] - 商品已存在，跳过")

        print(f"[seed] 数据统计: 政策{db.query(Policy).count()}条, 案例{db.query(Case).count()}个, 商品{db.query(Product).count()}个, 用户{db.query(User).count()}个")
    except Exception as e:
        print(f"[seed] 数据填充出错: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建表 + 填充种子数据
    Base.metadata.create_all(bind=engine)
    seed_data()
    yield


app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version=settings.APP_VERSION,
    description="生态产品价值实现赋能乡村振兴的一体化智能系统",
    lifespan=lifespan,
)

# CORS（开发期放开；生产可通过 CORS_ORIGINS 环境变量限定）
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件（上传目录，自动创建避免部署时报错）
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(policy.router, prefix="/api/policies", tags=["政策中心"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["智能分析"])
app.include_router(mall.router, prefix="/api/mall", tags=["商城"])
app.include_router(case.router, prefix="/api/cases", tags=["案例中心"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["数据大屏"])


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
