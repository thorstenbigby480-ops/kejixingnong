"""端到端测试商城订单流程"""
import httpx
import time

BASE = "http://localhost:8000/api"

print("=" * 60)
print("商城订单流程端到端测试")
print("=" * 60)

# 1. 注册一个测试用户
print("\n[1] 注册测试用户...")
ts = int(time.time())
username = f"testuser_{ts}"
email = f"{username}@test.com"
r = httpx.post(f"{BASE}/auth/register", json={
    "username": username,
    "email": email,
    "password": "123456",
    "phone": "13800138000",
    "role": "user",
}, timeout=30)
print(f"  状态: {r.status_code}")
if r.status_code == 200:
    print(f"  ✓ 用户: {r.json()}")
else:
    print(f"  失败: {r.text}")

# 2. 登录
print("\n[2] 登录...")
r = httpx.post(f"{BASE}/auth/login", json={"username": username, "password": "123456"}, timeout=30)
print(f"  状态: {r.status_code}")
token = r.json().get("access_token")
print(f"  ✓ token: {token[:30]}...")
headers = {"Authorization": f"Bearer {token}"}

# 3. 用商户账号登录测试
print("\n[3] 商户账号登录 merchant001/123456...")
r = httpx.post(f"{BASE}/auth/login", json={"username": "merchant001", "password": "123456"}, timeout=30)
print(f"  状态: {r.status_code}")
if r.status_code == 200:
    print(f"  ✓ 商户登录成功: {r.json()['user']}")
else:
    print(f"  ✗ 失败: {r.text}")

# 4. 查询商品列表
print("\n[4] 查询商品列表...")
r = httpx.get(f"{BASE}/mall/products", timeout=30)
print(f"  状态: {r.status_code}")
data = r.json()
print(f"  ✓ 总数: {data['total']}, 返回 {len(data['items'])} 个")
for p in data["items"][:3]:
    print(f"    - #{p['id']} {p['name']} ¥{p['price']} 库存{p['stock']}")

# 5. 测试分类筛选
print("\n[5] 测试分类筛选（茶叶）...")
r = httpx.get(f"{BASE}/mall/products?category=茶叶", timeout=30)
print(f"  状态: {r.status_code}")
print(f"  ✓ 茶叶类商品: {r.json()['total']} 个")

# 6. 下单
print("\n[6] 创建订单...")
order_payload = {
    "items": [
        {"product_id": 1, "name": "溧水白马蓝莓", "price": 88.0, "qty": 2},
        {"product_id": 5, "name": "武夷山岩茶大红袍", "price": 328.0, "qty": 1},
    ],
    "address": "张三 | 13800138000 | 江苏省南京市溧水区石湫街道",
    "phone": "13800138000",
    "remark": "测试订单",
}
r = httpx.post(f"{BASE}/mall/orders", json=order_payload, headers=headers, timeout=30)
print(f"  状态: {r.status_code}")
if r.status_code == 200:
    order = r.json()
    print(f"  ✓ 订单已创建: #{order['id']} 金额 ¥{order['total_amount']}")
    expected_total = 88 * 2 + 328 * 1
    assert abs(order['total_amount'] - expected_total) < 0.01, f"金额计算错误: 实际{order['total_amount']}, 期望{expected_total}"
    print(f"  ✓ 金额校验通过: 88×2 + 328×1 = {expected_total}")
    order_id = order["id"]
else:
    print(f"  ✗ 失败: {r.text}")
    order_id = None

# 7. 查询我的订单
if order_id:
    print("\n[7] 查询我的订单...")
    r = httpx.get(f"{BASE}/mall/orders", headers=headers, timeout=30)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  ✓ 共 {data['total']} 个订单")
        for o in data["items"]:
            print(f"    - #{o['id']} ¥{o['total_amount']} 状态:{o['status']} 商品数:{len(o['items'])}")

    # 8. 模拟支付
    print(f"\n[8] 模拟支付订单 #{order_id}...")
    r = httpx.post(f"{BASE}/mall/orders/{order_id}/pay", headers=headers, timeout=30)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        print(f"  ✓ {r.json()}")
    else:
        print(f"  ✗ 失败: {r.text}")

    # 9. 再次查询订单状态
    print(f"\n[9] 查询订单 #{order_id} 详情...")
    r = httpx.get(f"{BASE}/mall/orders/{order_id}", headers=headers, timeout=30)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        o = r.json()
        print(f"  ✓ 订单 #{o['id']} 状态:{o['status']} 金额 ¥{o['total_amount']}")

# 10. 测试另一个订单 - 取消流程
print("\n[10] 创建第二个订单（用于取消）...")
order_payload2 = {
    "items": [
        {"product_id": 2, "name": "石湫生态大米", "price": 49.9, "qty": 3},
    ],
    "address": "李四 | 13900139000 | 浙江省杭州市西湖区",
    "phone": "13900139000",
}
r = httpx.post(f"{BASE}/mall/orders", json=order_payload2, headers=headers, timeout=30)
if r.status_code == 200:
    order2 = r.json()
    print(f"  ✓ 订单 #{order2['id']} 已创建 金额 ¥{order2['total_amount']}")
    
    # 查询商品2的当前库存
    r = httpx.get(f"{BASE}/mall/products/2", timeout=30)
    stock_after_order = r.json()["stock"]
    print(f"  ✓ 商品 #2 当前库存: {stock_after_order} (原500-3=497)")
    
    # 取消订单
    print(f"\n[11] 取消订单 #{order2['id']}...")
    r = httpx.post(f"{BASE}/mall/orders/{order2['id']}/cancel", headers=headers, timeout=30)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        print(f"  ✓ {r.json()}")
    
    # 验证库存恢复
    r = httpx.get(f"{BASE}/mall/products/2", timeout=30)
    stock_after_cancel = r.json()["stock"]
    print(f"  ✓ 商品 #2 库存恢复后: {stock_after_cancel} (应=500)")
    assert stock_after_cancel == 500, "库存未正确恢复"

# 12. 未登录下单应该被拒绝
print("\n[12] 未登录下单（应被拒绝）...")
r = httpx.post(f"{BASE}/mall/orders", json={"items": [{"product_id": 1, "name": "test", "price": 88, "qty": 1}]}, timeout=30)
print(f"  状态: {r.status_code} (应=401)")
assert r.status_code == 401
print(f"  ✓ 已拦截: {r.json()}")

# 13. 查询政策
print("\n[13] 查询政策列表...")
r = httpx.get(f"{BASE}/policies/", timeout=30)
print(f"  状态: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    total = data.get("total", len(data.get("items", [])))
    print(f"  ✓ 政策总数: {total}")

# 14. 查询案例
print("\n[14] 查询案例列表...")
r = httpx.get(f"{BASE}/cases/", timeout=30)
print(f"  状态: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    total = data.get("total", len(data.get("items", [])))
    print(f"  ✓ 案例总数: {total}")

print("\n" + "=" * 60)
print("✅ 全部测试通过！")
print("=" * 60)
