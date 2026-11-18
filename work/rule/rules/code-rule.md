---
description: Java 编码细则（复杂逻辑、集合处理、Optional、Guava）
---

# 编码规则

## 1. 复杂逻辑优先使用卫语句（Guard Clauses）
- 当方法内存在多层 `if/else`、前置条件较多或分支复杂时，优先使用卫语句提前返回。
- 目标是"先处理异常/边界，再处理主流程"，减少嵌套层级，提升可读性和可维护性。
- 在不影响语义的前提下，避免将主流程包裹在多层条件内部。

简单示例：

```java
// 避免
if (order != null) {
    if (order.isValid()) {
        return handle(order);
    }
}
return null;

// 推荐
if (order == null) {
    return null;
}
if (!order.isValid()) {
    return null;
}
return handle(order);
```

## 2. List 遍历时评估 Map 预处理
- 代码涉及 `List` 遍历时，必须评估是否存在"循环中再查找/再遍历"的场景。
- 若存在多重循环、按 key 频繁匹配或重复查找，优先将数据预处理为 `Map`（如 `Map<K, V>` / `Map<K, List<V>>`）后再处理。
- 目标是降低时间复杂度，避免不必要的嵌套循环和性能损耗。

简单示例：

```java
// 避免：双重循环反复匹配
for (Order order : orderList) {
    for (User user : userList) {
        if (Objects.equals(order.getUserId(), user.getUserId())) {
            order.setUserName(user.getUserName());
        }
    }
}

// 推荐：先转成 Map 再处理
Map<Long, User> userMap = userList.stream()
    .collect(Collectors.toMap(User::getUserId, Function.identity(), (a, b) -> a));
for (Order order : orderList) {
    User user = userMap.get(order.getUserId());
    if (user != null) {
        order.setUserName(user.getUserName());
    }
}
```

## 3. 判空与默认值，链式取值只用 Optional，禁止使用 TripChain 
- 对可能为 `null` 的对象，优先使用 `Optional` 进行表达式化处理，减少样板式判空代码。
- 需要默认值时，优先使用 `orElse` / `orElseGet` 明确兜底逻辑，禁止"判空但无默认策略"的写法。
-  禁止使用 `com.ctrip.soa.cruise.product.tourincomeservice.v1.func.TripChain` 及任何等价工具类，即使项目现有代码里已经在用 —— 视作历史遗留，不要跟随。
- 仅在确有必要时才使用 `isPresent/get` 组合，避免把 `Optional` 用回传统判空风格。

简单示例：

```java
// 避免
String name = user != null ? user.getName() : "";
// 禁止
String mobile = TripChain.of(orderDetailInfo)             
          .chain(GetOrderDetailInfoResponseType::getContactInfo)                                                                                                                 
          .chain(ContactDTO::getContactMobile)                                                                                                                                   
          .get();   

// 推荐
String name = Optional.ofNullable(user)
    .map(User::getName)
    .orElse(StringUtils.EMPTY);
String mobile = Optional.ofNullable(orderDetailInfo)                                                                                                                           
          .map(GetOrderDetailInfoResponseType::getContactInfo)                                                                                                                   
          .map(ContactDTO::getContactMobile)                                                                                                                                     
          .orElse(StringUtils.EMPTY);  
```

## 4. 集合处理优先使用 Guava API
- 对 `List`、`Map`、`Set` 的创建、转换、过滤、分组等操作，优先使用 Guava 提供的 API 与工具类。
- 优先选择语义清晰、可读性高的 Guava 能力（如 `Lists`、`Maps`、`Sets`、`Multimap` 等）来替代重复手写逻辑。
- 在引入 Guava 用法时，保持与项目现有编码风格一致，避免同类场景混用多套实现方式。

简单示例：

```java
// 避免
List<String> nameList = new ArrayList<>();
Map<Long, String> nameMap = new HashMap<>();
Set<Long> idSet = new HashSet<>();

// 推荐
List<String> nameList = Lists.newArrayList();
Map<Long, String> nameMap = Maps.newHashMap();
Set<Long> idSet = Sets.newHashSet();
```

## 6. 优先复用，禁止复制代码

- 新增任何方法、类、处理器时，若核心逻辑与已有代码相同或高度相似，**禁止直接复制粘贴**。
- 正确做法：识别差异部分（入参来源、前置过滤、协议解析等）和公共部分（业务逻辑主干），将公共部分提取为独立方法，差异部分各自保留。
- 判断标准：如果修改一处业务逻辑需要同时改多个地方，说明抽象不够，必须重构。
- 抽象的粒度以"最小差异"为准，不要为了复用而过度参数化，导致方法签名臃肿。

## 5. 字符串判空与默认值统一使用 StringUtils
- 判断字符串是否为空、空白字符串时，优先使用 Apache Common 包下的 `StringUtils.isNotBlank()` 或对应方法，避免手写 `null`、`trim()`、`length()` 组合判断。
- 需要使用默认空字符串时，统一使用 `StringUtils.EMPTY`，不要直接写 `""`。
- 目标是统一字符串处理风格，减少重复判空逻辑，提升代码可读性与一致性。

简单示例：

```java
// 避免
if (name != null && name.trim().length() > 0) {
    return name;
}
return "";

// 推荐
if (StringUtils.isNotBlank(name)) {
    return name;
}
return StringUtils.EMPTY;
```

## 7. 任何可能为 null 的字段或返回值必须显式处理
- 只要字段、方法返回值、入参在业务上可能为 `null`（包括外部接口返回、entity 字段、Map.get、链式取值等），使用前必须显式判空或用 `Optional` 兜底。
- 兜底方式二选一：卫语句提前 `return` / `continue` / 抛业务异常；或 `Optional.ofNullable(...).map(...).orElse(默认值)`，默认值要符合业务语义。具体写法见规则 1（卫语句）和规则 3（Optional）。
- 禁止"裸用"可能为 null 的值（直接 `.getXxx()`、直接做算术 / 比较 / 放入集合 key），也禁止用空 catch NPE 兜底。
- 不确定某字段是否会为 null 时，按"可能为 null"处理，宁可多一次判空。

## 8. 新增方法的入参校验失败必须有明确兜底返回
- 新增方法时，如果对入参（或方法内部产生的中间结果，如 DAO 查询后的集合）做了校验（判空、格式、业务前置条件等），校验不通过的分支**必须有明确的兜底返回**，不能校验完却没写返回，或返回值语义模糊导致调用方裸用后出错。
- 兜底返回值的语义要让调用方能安全处理：集合类返回空集合（`Lists.newArrayList()` 等）而不是 `null`；boolean 类语义返回 `false`/`true` 而不是抛异常打断主流程；确实需要中断时按业务语义抛异常。
- 设计校验分支时要同时确认：方法内部后续逻辑（比如拼 SQL `IN` 条件的批量查询/更新）是否本身就不接受空输入——如果是，校验必须挡在调用之前，不能指望被调用的下游方法（DAO/RPC）自己兜底空参数。
- 结合规则 1（卫语句）一起用：卫语句提前 `return` 的同时，返回值必须符合上面的语义要求。

简单示例：

```java
// 避免：校验了却没有明确兜底，调用方可能拿到 null 或走到非法 SQL
public List<TourTourorder> getOrdersByIds(List<Long> orderIds) {
    // 缺少判空，orderIds 为空集合时拼出 IN () 直接 SQL 报错
    return tourTourorderDao.queryByIds(orderIds);
}

// 推荐：校验失败时返回值语义明确，调用方可安全处理
public List<TourTourorder> getOrdersByIds(List<Long> orderIds) {
    if (CollectionUtils.isEmpty(orderIds)) {
        return Lists.newArrayList();
    }
    return tourTourorderDao.queryByIds(orderIds);
}
```