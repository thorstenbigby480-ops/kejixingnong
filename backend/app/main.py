"""FastAPI 入口"""
import os
import bcrypt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.policy import Policy
from app.models.case import Case
from app.models.product import Product
from app.api import auth, policy, analysis, mall, case

# 启动时创建表
Base.metadata.create_all(bind=engine)


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

        # 2. 政策数据（简化版，只填5条核心政策）
        if db.query(Policy).count() == 0:
            policies = [
                {"title": "关于建立健全生态产品价值实现机制的意见", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2021-02-19", "source": "中共中央办公厅 国务院办公厅", "content": "到2025年，生态产品价值实现的制度框架初步建立。"},
                {"title": "生态保护补偿条例", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2024-04-10", "source": "国务院", "content": "规范生态保护补偿活动，建立健全市场化、多元化生态保护补偿机制。"},
                {"title": "乡村振兴促进法", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2021-04-29", "source": "全国人大常委会", "content": "全面实施乡村振兴战略，促进农业全面升级、农村全面进步、农民全面发展。"},
                {"title": "关于深化生态保护补偿制度改革的意见", "category": "生态产品价值实现", "level": "国家级", "region": "全国", "publish_date": "2021-09-01", "source": "中共中央办公厅 国务院办公厅", "content": "加快推进生态保护补偿制度改革，推动生态文明建设迈上新台阶。"},
                {"title": "国家乡村振兴战略规划（2018-2022年）", "category": "乡村振兴", "level": "国家级", "region": "全国", "publish_date": "2018-09-26", "source": "中共中央 国务院", "content": "部署重大工程、重大计划、重大行动，确保乡村振兴战略落地见效。"},
            ]
            for p in policies:
                db.add(Policy(**p))
            db.commit()
            print("[seed] ✓ 插入5条政策")
        else:
            print("[seed] - 政策已存在，跳过")

        # 3. 案例数据（5个）
        if db.query(Case).count() == 0:
            cases = [
                {"title": "浙江丽水：GEP核算开创生态价值转化新路", "region": "浙江省丽水市", "mode_type": "生态康养型", "summary": "丽水率先开展GEP核算，将生态资源转化为经济价值，2022年生态产品价值实现额超500亿元。", "content": "丽水通过建立GEP核算体系，将生态资源资产化，打通生态价值转化通道。", "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80"},
                {"title": "南京石湫：影视基地带动农文旅融合发展", "region": "江苏省南京市溧水区", "mode_type": "农文旅融合型", "summary": "石湫依托影视基地资源，发展乡村旅游和特色农业，年接待游客超100万人次。", "content": "石湫影视基地带动周边乡村发展民宿、农产品加工、文化体验等产业。", "image_url": "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80"},
                {"title": "江苏苏州昆山：特色田园乡村建设示范", "region": "江苏省苏州市昆山市", "mode_type": "农业品牌型", "summary": "昆山打造特色田园乡村，发展稻香文化、水乡民宿、阳澄湖大闸蟹品牌，年旅游收入超30亿元。", "content": "昆山以文化为魂、以农业为基、以旅游为媒，实现农业、文化、旅游深度融合。", "image_url": "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80"},
                {"title": "福建南平：'生态银行'激活绿色资源", "region": "福建省南平市", "mode_type": "湿地水域型", "summary": "南平市创新'生态银行'模式，将碎片化生态资源集中收储、规模化运营，2022年生态产品价值实现额超200亿元。", "content": "南平通过'生态银行'模式破解资源碎片化难题，实现生态资源规模化经营。", "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&q=80"},
                {"title": "四川成都战旗村：集体土地入市改革试点", "region": "四川省成都市郫都区", "mode_type": "城郊消费型", "summary": "战旗村通过集体经营性建设用地入市，探索乡村振兴新路径，村集体收入超千万元。", "content": "战旗村盘活集体资产，发展乡村旅游、农产品加工、文化创意等产业。", "image_url": "https://images.unsplash.com/photo-1504788363733-507549153474?w=1200&q=80"},
            ]
            for c in cases:
                db.add(Case(**c))
            db.commit()
            print("[seed] ✓ 插入5个案例")
        else:
            print("[seed] - 案例已存在，跳过")

        # 4. 商品数据（10个）
        if db.query(Product).count() == 0:
            products = [
                {"name": "溧水蓝莓礼盒", "category": "果蔬", "origin": "江苏南京溧水", "price": 128.0, "stock": 200, "image_url": "https://images.unsplash.com/photo-1583511655826-05700d52f4d9?w=800&q=80", "eco_cert": "有机产品认证", "description": "溧水白马镇蓝莓，果大汁甜富含花青素，500g礼盒装。"},
                {"name": "石湫大米", "category": "粮油", "origin": "江苏南京溧水石湫", "price": 68.0, "stock": 500, "image_url": "https://images.unsplash.com/photo-1586201375761-83865074da31?w=800&q=80", "eco_cert": "绿色食品认证", "description": "石湫优质稻花香米，软糯香甜，5kg真空包装。"},
                {"name": "阳澄湖大闸蟹礼券", "category": "水产", "origin": "江苏苏州昆山", "price": 588.0, "stock": 100, "image_url": "https://images.unsplash.com/photo-1518977676601-b53b0c12c0c0?w=800&q=80", "eco_cert": "地理标志产品", "description": "阳澄湖核心产区大闸蟹，公4.5两母3.5两，8只装礼券。"},
                {"name": "丽水香菇干货", "category": "食用菌", "origin": "浙江丽水庆元", "price": 58.0, "stock": 300, "image_url": "https://images.unsplash.com/photo-1544200179-ca6e80c8d2de?w=800&q=80", "eco_cert": "有机产品认证", "description": "庆元香菇，肉厚味鲜，250g装。"},
                {"name": "武夷岩茶大红袍", "category": "茶叶", "origin": "福建南平武夷山", "price": 368.0, "stock": 80, "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=80", "eco_cert": "地理标志产品", "description": "武夷山大红袍，岩韵悠长，100g礼盒装。"},
                {"name": "安吉白茶", "category": "茶叶", "origin": "浙江湖州安吉", "price": 458.0, "stock": 60, "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9c4a6?w=800&q=80", "eco_cert": "有机产品认证", "description": "安吉高山明前采摘，清香甘醇，50g装。"},
                {"name": "战旗村手工豆瓣", "category": "加工品", "origin": "四川成都郫都战旗村", "price": 38.0, "stock": 500, "image_url": "https://images.unsplash.com/photo-1607301405964-d50e65c8c3e5?w=800&q=80", "eco_cert": "地理标志产品", "description": "战旗村百年老坊手工酿造，500g装。"},
                {"name": "淳安千岛湖有机鱼头", "category": "畜禽", "origin": "浙江杭州淳安千岛湖", "price": 128.0, "stock": 150, "image_url": "https://images.unsplash.com/photo-1535140728325-a4d3707eee95?w=800&q=80", "eco_cert": "有机产品认证", "description": "千岛湖野生放养鳙鱼鱼头，3斤装。"},
                {"name": "巴城阳光玫瑰葡萄", "category": "果蔬", "origin": "江苏苏州昆山巴城", "price": 98.0, "stock": 200, "image_url": "https://images.unsplash.com/photo-1599477173151-9f4b9c8c8e1d?w=800&q=80", "eco_cert": "绿色食品认证", "description": "巴城阳光玫瑰葡萄，玫瑰香气甜度20+，2斤装。"},
                {"name": "肥西老母鸡礼盒", "category": "畜禽", "origin": "安徽合肥肥西", "price": 188.0, "stock": 100, "image_url": "https://images.unsplash.com/photo-1605195999683-88f3e3c9c28a?w=800&q=80", "eco_cert": "无公害农产品", "description": "肥西散养300天老母鸡，2只装礼盒。"},
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


# 启动时自动填充种子数据
seed_data()

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version=settings.APP_VERSION,
    description="生态产品价值实现赋能乡村振兴的一体化智能系统",
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
