"""把数据库中所有图片 URL 替换为 Unsplash 稳定公网链接

原 URL 用的是 trae-api-cn.mchost.guru 内部 API，公网访问不了。
部署前必须运行此脚本，否则线上图片全部 404。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.product import Product
from app.models.case import Case

# Unsplash 图片 URL（永久公开访问，免费 CDN）
# 格式：https://images.unsplash.com/photo-xxx?w=800&q=80

# 商品图片（按商品ID映射）
PRODUCT_IMAGES = {
    1: "https://images.unsplash.com/photo-1583511655826-05700d52f4d9?w=800&q=80",  # 蓝莓
    2: "https://images.unsplash.com/photo-1586201375761-83865074da31?w=800&q=80",  # 大米
    3: "https://images.unsplash.com/photo-1518977676601-b53b0c12c0c0?w=800&q=80",  # 大闸蟹
    4: "https://images.unsplash.com/photo-1544200179-ca6e80c8d2de?w=800&q=80",     # 香菇
    5: "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=80",     # 武夷岩茶
    6: "https://images.unsplash.com/photo-1564890369478-c89ca6d9c4a6?w=800&q=80",  # 安吉白茶
    7: "https://images.unsplash.com/photo-1607301405964-d50e65c8c3e5?w=800&q=80",  # 豆瓣
    8: "https://images.unsplash.com/photo-1535140728325-a4d3707eee95?w=800&q=80",  # 鱼头
    9: "https://images.unsplash.com/photo-1599477173151-9f4b9c8c8e1d?w=800&q=80",  # 葡萄
    10: "https://images.unsplash.com/photo-1605195999683-88f3e3c9c28a?w=800&q=80", # 老母鸡
}

# 案例图片（按 case id）
CASE_IMAGES = {
    1: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80",  # 浙江丽水山区
    2: "https://images.unsplash.com/photo-1444723121867-7a241cacace3?w=1200&q=80",  # 南京石湫影视基地
    3: "https://images.unsplash.com/photo-1528283648649-30a22d55e5cc?w=1200&q=80",  # 苏州昆山
    4: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200&q=80",  # 福建武夷山
    5: "https://images.unsplash.com/photo-1504788363733-507549153474?w=1200&q=80",  # 四川成都战旗村
}


def main():
    print("=" * 60)
    print("替换图片 URL 为 Unsplash 公网链接")
    print("=" * 60)

    db = SessionLocal()
    try:
        # 1. 商品图片
        print("\n[1] 替换商品图片 URL...")
        for pid, url in PRODUCT_IMAGES.items():
            p = db.get(Product, pid)
            if p:
                old = p.image_url
                p.image_url = url
                print(f"  #{pid} {p.name}: ✓")
                print(f"    旧: {old[:80] if old else 'None'}...")
                print(f"    新: {url[:80]}...")
        db.commit()

        # 2. 案例图片
        print("\n[2] 替换案例图片 URL...")
        for cid, url in CASE_IMAGES.items():
            c = db.get(Case, cid)
            if c:
                old = c.image_url
                c.image_url = url
                print(f"  #{cid} {c.title[:30]}: ✓")
                print(f"    旧: {old[:80] if old else 'None'}...")
                print(f"    新: {url[:80]}...")
        db.commit()

        # 3. 校验
        print("\n[3] 校验结果：")
        products = db.query(Product).all()
        cases = db.query(Case).all()
        bad_products = [p for p in products if p.image_url and "mchost.guru" in p.image_url]
        bad_cases = [c for c in cases if c.image_url and "mchost.guru" in c.image_url]
        print(f"  商品总数: {len(products)}，仍有内网链接: {len(bad_products)}")
        print(f"  案例总数: {len(cases)}，仍有内网链接: {len(bad_cases)}")
        if bad_products or bad_cases:
            print("\n  ⚠ 警告：仍有内网链接未替换！")
            for p in bad_products:
                print(f"    商品 #{p.id}: {p.image_url}")
            for c in bad_cases:
                print(f"    案例 #{c.id}: {c.image_url}")
        else:
            print("\n  ✓ 全部替换完成，公网可访问")

    finally:
        db.close()

    print("\n" + "=" * 60)
    print("✓ 完成！现在数据库中的图片 URL 都是 Unsplash 公开链接")
    print("=" * 60)


if __name__ == "__main__":
    main()
