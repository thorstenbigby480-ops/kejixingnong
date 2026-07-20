"""重置商品库存"""
from app.database import SessionLocal
from app.models.product import Product

ORIG_STOCK = {
    1: 200,  # 蓝莓
    2: 500,  # 大米
    3: 80,   # 大闸蟹
    4: 300,  # 香菇
    5: 100,  # 大红袍
    6: 60,   # 安吉白茶
    7: 500,  # 豆瓣
    8: 150,  # 千岛湖鱼
    9: 200,  # 葡萄
    10: 100, # 老母鸡
}

db = SessionLocal()
for pid, stock in ORIG_STOCK.items():
    p = db.get(Product, pid)
    if p:
        p.stock = stock
        print(f"  #{pid} {p.name}: 库存重置为 {stock}")
db.commit()
print("✓ 库存已重置")
db.close()
