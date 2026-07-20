"""耦合协调度模型 CCD Model
D = sqrt(C * T)
C = 2*sqrt(U1*U2) / (U1 + U2)
T = alpha*U1 + beta*U2
"""
import math

COORDINATION_LEVELS = [
    (0.1, "极度失调"),
    (0.2, "严重失调"),
    (0.3, "中度失调"),
    (0.4, "轻度失调"),
    (0.5, "濒临失调"),
    (0.6, "勉强协调"),
    (0.7, "初级协调"),
    (0.8, "中级协调"),
    (0.9, "良好协调"),
    (1.01, "优质协调"),
]


def compute_coupling_coordination(u1: float, u2: float, alpha: float = 0.5, beta: float = 0.5):
    """u1, u2 可传入 0-100 分或 0-1 分"""
    if u1 > 1 or u2 > 1:
        u1, u2 = u1 / 100, u2 / 100
    s = u1 + u2
    if s == 0:
        return 0.0, 0.0, "极度失调"
    c = (2 * math.sqrt(u1 * u2)) / s
    t = alpha * u1 + beta * u2
    d = math.sqrt(c * t)
    level = "优质协调"
    for bound, name in COORDINATION_LEVELS:
        if d < bound:
            level = name
            break
    return round(c, 4), round(d, 4), level
