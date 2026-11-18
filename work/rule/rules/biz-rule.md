---
description: 业务代码编写规则（边界判断、歧义识别、TODO升级）
---

# 业务代码规则

## 1. 写业务代码时必须启用本规则
- 当需求涉及业务语义、业务判断、领域对象状态、默认值含义时，必须同时参考本规则。

## 2. 边界判断不能一律视为防御性编程
- 进行 `null`、空值、缺省值、状态值判断时，必须先区分：这是单纯防御性编程，还是业务语义的一部分。
- 如果某个"空值/缺省值"在业务上有明确含义，则该判断属于业务规则，不能机械简化、删除，或替换成通用判空逻辑。

## 3. 需要结合上下文消除歧义
- 如果上下文存在类似方法、同类字段、历史逻辑、默认约定，必须综合判断，避免只看局部代码就下结论。
- 尤其要关注"默认值代表什么""字段缺失是否等价于某种业务状态""旧逻辑是否已经约定了兜底语义"。

## 4. 拿不准时输出 TODO，由用户判断
- 如果无法确认某个边界判断到底是防御性编程还是业务语义，不要擅自修改结论。
- 必须明确列出 `TODO`，说明歧义点、候选理解和可能影响，由用户最终判断。

## 5. 成对状态动作必须闭环（写之前先画镜像表）
- 业务里常有一对相反动作：成团/不成团、上线/下线、开/关、加/删、启用/停用。写其中一边时，**默认假设"另一边必须在同样的场景里能反向清掉"**。
- 动手前先做一次闭环检查：列出"正向动作会在哪些条件组合下落下状态"，再逐格确认"反向动作能否在**同一条件组合**下清掉"。用一张条件矩阵最直观：

| | 条件 A 成立 | 条件 A 不成立 |
|---|---|---|
| 正向动作 | 写状态 | 写状态 ← 落下了状态 |
| 反向动作 | 清状态 | **清状态？← 必须镜像，不能空** |

- 判断标准很机械：**清理/回滚逻辑如果只用到了入参的一个子集（比如只需要 `productId + departureDate`，用不到 `tourId`），那它就是"分支无关"的，必须抽成独立方法，让所有分支都能调**，不能把它埋在"只有某个前置条件成立才进得了"的分支里。
- 典型反例（本次漏洞）：成团消息在"无团"时也会写一条 `group_status`，但不成团的删除逻辑被挂在 `handleFailedNotice`（只在"有团"分支才调用）下面，于是"无团 + 不成团"这一格空了，删除触发不了。而删除动作其实只依赖 `productId + departureDate`，根本不依赖"是否有团"。

示例：

```java
// 避免：删除逻辑被埋在"有团才能进"的方法里，导致"无团 + 不成团"删不掉
private void handleFailedNotice(Long tourId, Long productId, Timestamp departureDate) {
    // ... 只有 items 非空才会调到这里
    deleteGroupStatus(productId, departureDate);  // 无团分支够不着
}

// 推荐：把"分支无关"的清理下沉为独立方法，有团/无团两个分支都能调
private void deleteGroupStatus(Long productId, Timestamp departureDate) {
    // 只用 productId + departureDate，不依赖 tourId
}
```

示例：

```java
private boolean isSingleSettlement(ResourceSalePriceAndInventoryInfoResponseDto response) {
    if (response == null || response.getResourcePriceKind() == null) {
        return true;
    }
    Integer priceKind = response.getResourcePriceKind().getPriceKind();
    return priceKind == null || priceKind != 2;
}
```

说明：
- 这个方法不是单纯"防御性判空"。
- 这里的 `null` 具有业务含义：资源默认是单结，所以 `priceKind == null` 也应判定为单结。
- 因此，看到类似代码时，不能只因为存在判空就将其归类为可随意收缩的防御性编程。