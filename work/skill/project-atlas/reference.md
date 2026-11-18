# project-atlas 参考模板

SKILL.md 只讲流程，本文件承载所有具体模板、清单、规范。

---

## Explore prompt 模板

### 项目级 Explore prompt

```
探索本项目根目录，仅限本仓库内，不做全盘搜索。产出以下内容，每项给 file:line：

1. 构建配置：读根 pom.xml / settings.gradle，判断是否多模块，列出模块名与依赖关系。
2. 各模块顶层包结构：每个 module 的 src/main/java 下顶层包一句话职责。
3. 对外入口注解全清单（按类型分类）：
   - HTTP：@RestController、@Controller、@RequestMapping、@GetMapping、@PostMapping
   - SOA/RPC：@SofaService、@DubboService、@ThriftService、@Service（如项目内有自定义）
   - MQ 消费：@QMQConsumer、@RocketMQMessageListener、@KafkaListener、@RabbitListener
   - 定时任务：@Scheduled、@QSchedule、@JobHandler、@XxlJob
   - 事件监听：@EventListener、ApplicationListener 实现类
   - 配置变更：@ApolloConfigChangeListener
   - AOP 切面：@Aspect（每个切面要读 pointcut 表达式和实现体，说明"在切什么、干什么"）
   - 拦截器/Filter：HandlerInterceptor、@ControllerAdvice、Filter、RequestFilter
     **每个 Filter/Interceptor 类必须打开源码看 doFilter / preHandle 的实现，具体写清"做了什么"**，不允许只写"请求增强"这类抽象描述。
4. 根 README.md / CLAUDE.md 中的业务背景摘要（若存在）。
5. 顶层核心 Service 类的类头 javadoc（若有），用于抓关键设计约束。

输出控制在 800 字以内，重点信息前置，不写套话。
```

### 功能级 Explore prompt（Phase 2 深挖）

```
以 <入口类#方法> (file:line) 为起点，追调用链和隐藏关联。产出：

1. 主流程调用链：跨类跨模块递归，追到"外部边界"停（详见深度控制清单）。
   输出为分层缩进列表，每一行 `ClassName#method (file:line) — 一句话作用`。
2. 关键分支：列出主流程中影响业务走向的 if/switch，标注条件和差异。
3. 隐藏关联扫描（对以下每一类做专门检索，别只依赖调用链）：
   [见 reference.md「隐藏关联完整清单」]
4. 数据面清单：读/写表、发/收 MQ、调外部接口、用到的 Apollo key、缓存 key。

输出严格用 file:line 标注，不写"大致位置"。
```

---

## L2 归纳规则

**核心原则**：一条 L2 = 用户/业务方能一句话描述的一个动作。

### 归纳粒度

| 场景 | 处理 |
|---|---|
| 一个 Controller 有 20 个 method | 按业务动词聚合（如 create/cancel/query），每个动词一条 L2；纯 CRUD 的读接口可合并"XX 查询" |
| SOA 服务类有 30 个方法 | 同上，按业务动词聚合 |
| 一个业务由多个入口触发 | HTTP + MQ Consumer + Job 同触发"订单创建"，归为**一条** L2，主入口写多个 |
| 同一个入口方法做了多件事 | 拆成多条 L2（例如一个方法同时处理创建和更新，拆成"订单创建 / 订单更新"） |

### 命名策略

- ✅ 用业务领域动词：`订单创建`、`发送出行通知`、`退款审核`
- ❌ 别用类名/方法名：`OrderController`、`sendMessage`
- ✅ 中文首选，因为老人和 AI 查找时都会用中文关键字

### 无法归类的兜底

识别不清或语义模糊的入口，放到 project.md 末尾的 `## L2.杂项待归类` 章节，附原始入口列表（file:line），交给用户确认后再归入正式清单。

---

## 关键设计约束怎么识别

**列 3-8 条**会真正影响改动的约束。**识别到几条列几条，别硬凑够 3 条，也别为了控制在 5 条以内漏掉重要约束**。识别信号：

1. **README/CLAUDE.md 明说的**：项目里有明确文档说的规则。
2. **反复出现的封装模式**：例如所有对外接口都套了同一个 `Optional` 兜底、所有 DAO 都走同一个基类、所有 MQ 消费都过同一个幂等组件——说明这是项目的强约束。
3. **有 AOP / 拦截器强制的**：全局 AOP 在做什么，就是全局约束（尤其是"审计切面 / 变更 changelog 切面 / 权限切面"这类必须独立列一条）。
4. **顶层核心 Service 类头 javadoc 里提到的**：老代码作者留下的设计说明。
5. **跨业务的事务边界约定**：哪些 Bo 方法是 `@Transactional` 的、传播规则、跨 DB 的事务怎么处理。
6. **消息幂等约定**：MQ 消费者怎么防重复消费（Redis token / DB 唯一键 / 分布式锁），是不是有统一封装。
7. **异常兜底约定**：项目层面对外接口是否统一"不主动抛异常给上游"、错误码规则、降级默认值策略。
8. **分布式锁 / 并发控制约定**：哪些写操作必须加锁、锁粒度怎么选、锁 key 命名模板。

### 每条约束的写法（问题→解法→约束）

```markdown
### 约束 N：<名字>
- **为什么这么设计**：一句话动机（历史事故 / 性能 / 合规 / 一致性）
- **改的时候要遵守什么**：具体规则，最好带正反例
- **相关代码**：file:line
```

---

## 深度控制清单

| 场景 | 处理 |
|---|---|
| 同 repo 内跨类跨模块的直接调用 | ✅ 追 |
| 调 `common` / `util` 依赖模块 | 一般追（按模块名判断，工具类不追） |
| 调外部 SOA / HTTP / RPC | ❌ 标注但不追（写 `→ SOA: XxxService#yyy` 即可） |
| DAO / Mapper / Repository 层 | ❌ 标注但不追（写 `→ DB: t_xxx (read/write)` 即可） |
| 接口有多个实现类 | 全部列出，标注 `@Primary` 或按注解匹配；若明显是策略模式，列全部实现 |
| **同一接口/同名方法有多个平行实现（如旧/新/ERP 三分支这类）** | **不强追**每个实现内部到底（省 token），**但必须**：<br>1. 在文档里显式声明"存在多个实现，逻辑有差异"，别写成"三条 Bo 方法结构相似"这类模糊断言<br>2. 列 **1-2 个具体差异点**（哪个 QConfig 开关、哪张表、哪个 SOA 方法不同）作为警戒线，读者看到就知道要各自看代码<br>3. 修改指引里明确标注"改 A 是否需要同步改 B/C" |
| 循环依赖 / 递归调用 | 显式标注 `↻ recursive` 并终止 |
| 已访问过的方法 | 标注 `[见上文]` 并终止 |
| `StringUtils.isNotBlank` / DTO getter / setter | ❌ 永远不追 |
| Lambda / 匿名内部类内部 | 只追一层，别层层展开 |

### 输出长度约束

- 单条 L3 md 文件建议控制在 500 行以内
- 主流程调用链层级超过 5 层时，把深层折叠为"→ 详见 <ClassName>"链接
- 关键分支只列 top 5，其余归入"其他分支"一行带过

---

## 隐藏关联完整清单

对以下**每一类**做专门检索，不能只依赖调用链发现。

| 类别 | 检索关键字/注解 | 为什么关键 |
|---|---|---|
| **AOP 切面** | `@Aspect` + `@Around/@Before/@After`，匹配主流程类/方法的 pointcut 表达式 | 会短路主流程、修改参数、事务嵌套 |
| **事件监听** | 主流程中所有 `publishEvent` / `ApplicationEventPublisher` 发布点，反向找 `@EventListener` | 异步 side effect 容易漏 |
| **MQ 影响（双向）** | 主流程发的 topic 被谁消费；主流程消费的 topic 被谁发送 | 跨仓库影响面 |
| **定时任务 / 异步** | `@Scheduled` / `@Async` / `CompletableFuture` / 自定义 `ExecutorService`，是否修改了主流程涉及的数据/状态 | 数据一致性风险 |
| **配置驱动分支** | `@Value` / `@ApolloConfig` / `Apollo.getProperty` / 开关字段（`enable`/`switch`/`toggle`） | 生产开关一变行为就变 |
| **Apollo 变更监听** | `@ApolloConfigChangeListener` | 配置热更新时的动态行为 |
| **拦截器 / Filter** | `HandlerInterceptor` / `Filter` / `@ControllerAdvice`，匹配 HTTP 入口路径 | 前置参数校验、鉴权、异常包装 |
| **重试 / 熔断** | `@Retryable` / `@SentinelResource` / `Hystrix` | 失败路径行为改变 |
| **SPI / Strategy 注册** | `@Component` 被 `BeanPostProcessor` / `ApplicationContextAware` 收集实现 | 新增实现类会被自动接入 |
| **Feign / SOA / Dubbo 消费** | `@FeignClient` / `@DubboReference` / SOA 客户端 bean | 外部调用点，改接口会连带影响调用方 |
| **DAAS / 分库分表** | DAAS 路由规则文件、分片键字段 | 命中特定表会走别的路径 |

**兜底**：如果项目内还有其他领域特定注解（如公司自研框架），扫描时按上述模式补充分类。

---

## project.md 模板

```markdown
# <项目名> · Project Atlas

> 用于改需求前定位改动范围、理解模块职责与设计约束。
> 生成时间：<YYYY-MM-DD>

## 项目画像
<一段话：这个项目干什么 + 在系统里的角色 + 关键技术栈>

## 模块分层结构

<ASCII 分层图，展示模块间依赖方向>

| 模块 / 顶层包 | 职责 | 依赖 |
|---|---|---|
| `xxx-service` | <一句话> | `xxx-bo`, `xxx-common` |
| `xxx-bo`      | <一句话> | `xxx-dao` |
| ... | ... | ... |

## 关键设计约束

> 3-5 条真正影响改动的约束。改需求前必读。

### 约束 1：<名字>
- **为什么这么设计**：<一句话>
- **改的时候要遵守什么**：<规则 + 正反例>
- **相关代码**：`XxxAspect.java:20`

### 约束 2：...

## 对外入口清单

### HTTP
- `XxxController#foo()` (`XxxController.java:42`) — <干什么>
- ...

### SOA / RPC
- `YyyServiceImpl#bar()` (`YyyServiceImpl.java:33`) — <干什么>
- ...

### MQ 消费
- 主题 `xxx.topic` → `ZzzConsumer#onMessage()` (`ZzzConsumer.java:15`) — <干什么>

### 定时任务
- `AaaJob#run()` (`AaaJob.java:20`, cron: `0 0 * * *`) — <干什么>

### 事件监听
- ...

### AOP 切面
- ...

## L2 功能清单

### 模块 `xxx-service`

| 功能名 | 一句话 | 主入口 | → L3 |
|---|---|---|---|
| 订单创建 | 用户下单，写库并发消息通知下游 | `OrderController#create` + `OrderCreateConsumer` | `features/订单创建.md` |
| 订单取消 | 处理用户/超时取消，回收库存 | `OrderCancelConsumer` + `OrderController#cancel` | `features/订单取消.md` |

### 模块 `yyy-service`

| ... | ... | ... | ... |

## 业务链路图（跨功能异步调用链）

> L2 是单个动作，本章展示动作之间的**跨功能异步调用链**。老人改需求最需要看这层，判断"改 A 会不会连带影响 B"。
> 只画**跨功能且异步**的链路（同步调用在主流程调用链里已经能看到）。项目内没有跨功能异步链路时，本章显式写「无」。

示例：

```
预算审批  ──[QMQ createtour]──▶  建团  ──[Binlog INSERT]──▶  关联订单
                                          │
                                          └─[Binlog UPDATE]──▶  自动上传财务

支付审批  ──[QMQ payment.upload]──▶  财务上传  ──[QMQ payment.status]──▶  支付状态回调
```

每条链路配一段说明：

- **触发点**：`XxxService#approvePayment` (`file:line`) 发 `payment.upload`
- **消费点**：`UploadFinanceListener#onUploadFinanceMessage` (`file:line`)
- **链路上的关键失败/降级**：QConfig `upload_finance_switch` 关掉整条链路会静默跳过

## L2.杂项待归类

（如有无法归类的入口，放这里，附 file:line，交用户确认）

---

> 想进一步下钻某个功能，执行 `/project-atlas <功能名>`
```

---

## features md 模板

```markdown
# 功能：<功能名>

> 改这个功能前需要知道的所有依赖 / 隐藏关联 / 分支
> 生成时间：<YYYY-MM-DD>

## TL;DR（30 秒定位）

- **主入口**：X 处（HTTP N / MQ M / Job K）
- **关键分支**：Y 处
- **隐藏影响**：Z 个（AOP N / 事件 M / 异步 K）
- **数据面**：写 A 张表 / 发 B 个 MQ / 调 C 个外部接口
- **⚠ 改这里最容易踩的 3 个坑**：
  1. <一行结论> — `file:line`
  2. <一行结论> — `file:line`
  3. <一行结论> — `file:line`

## 主流程调用链

- `XxxController#create` — HTTP 入口 (`XxxController.java:42`)
  - `OrderCreateService#create` (`OrderCreateService.java:33`)
    - `OrderValidator#validate` — 校验 (`OrderValidator.java:15`)
    - `OrderBo#buildOrder` — 组装订单实体 (`OrderBo.java:88`)
      - // 为什么：这里用了 Builder 模式而非直接 setter，见约束 2
    - `OrderRepository#save` — 写库 (`OrderRepository.java:20`) → DB: `t_order` (write)
    - `MessageProducer#send` — 发 MQ (`MessageProducer.java:55`) → MQ: `order.created`
  - 返回响应

> 行内 `// 为什么：...` 只在设计非直觉时加，别每行都写。

## 隐藏关联

> 三段式：问题 → 解法 → 影响面。前两段解释为什么这么设计，第三段是改动风险。

### AOP：幂等切面
- **问题**：用户重复点击下单会创建多个订单
- **解法**：`OrderCreateAspect#around` (`OrderCreateAspect.java:20`) 用 request token 做幂等，命中直接返回上次结果
- **影响面**：⚠ 改主流程入参结构会让 token 计算失效，导致幂等失败

### 事件监听：下单成功后的 side effect
- **问题**：主流程要保持轻，积分/风控这类不影响下单成功的逻辑不应该同步做
- **解法**：`OrderCreateService` 发布 `OrderCreatedEvent`，被以下监听：
  - `PointRewardListener` (`PointRewardListener.java:18`) — 加积分
  - `RiskCheckListener` (`RiskCheckListener.java:30`) — 风控异步检查
- **影响面**：⚠ 改 `OrderCreatedEvent` 字段结构要同步改所有 Listener

### MQ 影响（双向）
- **发送**：`order.created` → 被 `xxx-notify-service` 消费（不在本仓库）
- **消费**：无
- **影响面**：⚠ 改 MQ 消息体结构要通知下游服务同步升级

### 配置驱动分支
- `Apollo key: order.create.enable-v2`
  - **解法**：为 true 走 `OrderCreateServiceV2`，否则走旧逻辑
  - **影响面**：⚠ 改动只在旧逻辑生效时，生产开关切换会瞬间失效

### 拦截器 / Filter
- ...

### 其他类别（AOP/事件/MQ/定时/配置/Apollo 监听/拦截器/重试/SPI/Feign/DAAS）
- 逐类过一遍，无则显式写「无」，别省略章节。

## 关键分支与条件

| 位置 | 条件 | 走 A | 走 B |
|---|---|---|---|
| `OrderCreateService.java:50` | `user.isVip()` | 免运费 + 优先库存 | 正常流程 |
| ... | ... | ... | ... |

（只列 top 5，其余归入"其他分支"一行）

## 数据与外部依赖

- **表**：`t_order`（写）、`t_user`（读）
- **外部接口**：
  - SOA `UserService#getUserInfo`
  - HTTP `POST /coupon/deduct`
- **MQ**：
  - 发送：`order.created`
  - 消费：无
- **配置 (Apollo)**：`order.create.enable-v2`、`order.create.timeout-ms`
- **缓存**：`Redis: order:idempotent:{userId}:{token}`

## 修改指引

> 老人/AI 视角：常见需求 → 应该改哪里 + 会有哪些连带影响。

| 需求类型 | 主改动点 | 需要同步改 | 相关隐藏关联 |
|---|---|---|---|
| 新增下单校验规则 | `OrderValidator#validate` (`:15`) | 无 | — |
| 修改订单字段 | `OrderBo#buildOrder` (`:88`) + `t_order` DDL | `OrderCreatedEvent` 字段 + 所有 Listener + MQ 消息体 | AOP 幂等切面 + 事件监听 + MQ |
| 加一个下单成功后的 side effect | 新增 `@EventListener` | 无（不影响主流程） | 事件监听 |
| 切换到 V2 流程 | Apollo `order.create.enable-v2` | 无 | 配置驱动分支 |

## 备注

<!-- manual -->
（这里放用户手动补充的内容，重新生成时会保留）
<!-- /manual -->
```

---

## Phase 4 自检清单

### 内容准确性
- [ ] 所有 `file:line` 都能跳转，都是亲自确认过的（grep 或 Read 验证过）
- [ ] **没有"附近 / 大致 / 大概位置"等禁用词**（找不到具体行号就标 `TODO 待定位`）
- [ ] 类/方法名与真实代码一致
- [ ] 没有编造调用关系
- [ ] 所有代码引用来自真实文件
- [ ] 每个 Filter/Interceptor 都写清了 doFilter/preHandle 实际做的事，没有"请求增强"这类抽象描述
- [ ] 遇到"多个平行实现"（旧/新/ERP 分支这类）：显式声明存在差异，列了 1-2 个具体差异点

### 层级完整性
- [ ] project.md 里列的每个模块，L2 都有功能覆盖（除非明确是纯基础设施模块）
- [ ] L2 每条功能的入口方法能在源码里找到
- [ ] 若跑了 L3，L3 的入口和 L2 描述一致
- [ ] 关键设计约束覆盖了 AOP 全局切面（审计/权限/变更 changelog 类切面必须独立列一条）
- [ ] 业务链路图章节：跨功能异步链路都画到了，或显式写了「无」

### 隐藏关联完整性（老人视角核心 KPI）
- [ ] reference.md「隐藏关联完整清单」里的每一类都过了一遍，无则显式写「无」
- [ ] **每条隐藏关联都给出了明确的"影响面"**，不是仅存在性描述
- [ ] TL;DR 里的"最容易踩的 3 个坑"能对应到具体的隐藏关联条目

### 修改指引可用性（老人视角核心 KPI）
- [ ] 随便挑一条"修改指引"里的需求类型，跟着指引能找到所有要改的地方
- [ ] 修改指引的"需要同步改"栏关联到了隐藏关联章节

### 可读性
- [ ] project.md 顶部有 `>` 目标引用块
- [ ] 每个 L3 顶部有 TL;DR
- [ ] 用了 ASCII 图或表格辅助理解
- [ ] 领域缩写首次出现有展开（TDZT / IES / DAAS / QMQ 等）
- [ ] 结论前置，别写"综上"、"如上所述"

---

## 写作禁忌

- **不允许**：`file:line` 给"大致位置"（例如 `OrderService.java 附近`）—— 详见下方「禁用词红灯」
- **不允许**：编造类/方法名，未验证的调用关系
- **不允许**：隐藏关联只写"存在这个切面"，不写影响面
- **不允许**：写"综上"、"如上所述"、"值得注意的是"这类零信息量套话
- **不允许**：领域缩写不展开（TDZT / IES / DAAS / QMQ 首次出现要展开）
- **不允许**：多段散文式描述——每条 bullet 应该单行结论 + 一行影响
- **不推荐**：过度类比。类比只在概念真的生疏时用一次，用完就切回代码语言

### 禁用词红灯

以下词一旦出现在 file:line 语境里，**直接判定为违规**，必须重写：

- "附近" / "大致" / "大概位置" / "大约在"
- "类似 XXX 的地方" / "XXX 那一块" / "XXX 一带"
- "大致较长" / "行号大约在"

**核心原则**：给出的每一个 file:line **必须是亲自确认过的准确值**。信心不足不是加模糊词的理由，而是应该先做确认动作。

**确认动作清单**（信心不足时按顺序做，做完再落笔）：
1. `grep -n "public.*方法名\|public.*ClassName"` 定位方法/类签名的具体行
2. Read 该行的上下文（前后 5-10 行）确认这就是你要标的位置
3. 若定位不到（例如动态生成、反射、DAL 生成代码），显式标 `TODO 待定位`

**常见借口 → 现实**

| 借口 | 现实 |
|---|---|
| "这方法太长，起点行号不确定" | 起点=方法签名行，grep 就能拿到确切行号，5 秒 |
| "读者能猜到大致位置" | 读者装了 IDE 会直接点 file:line 跳转，写错就跳不过去 |
| "行号我读到的是方法体内部某行，不是签名" | 你读到的那行是准确的就用那行；要标签名就补一次 grep |
| "写具体行号信心不足" | 信心不足的正确做法是补一次 grep 或 Read，不是加"附近"打模糊 |
| "反正差不了几行" | 差 1 行就是错的。宁可 `TODO 待定位`，不写"附近" |

---

## 表达手段清单

| 场景 | 首选手段 |
|---|---|
| 层级 / 流程 | ASCII 图 |
| 多个功能对比 | 表格 |
| 分支差异 / 反模式 | ❌ vs ✅ 对比块 |
| 调用链 | 分层缩进列表 |
| "改哪里" 定位 | 需求类型 → 改动点 的映射表 |
| 生疏的领域概念 | 类比生活场景，只用一次，之后切回代码语言 |

---

## 功能名匹配策略

Phase 1 收到 `{query}` 后：

1. **精确匹配**：与 L2 功能名字符串完全一致。命中即用。
2. **子串匹配**：`{query}` 是 L2 某功能名的子串或反之。1 条命中即用；2+ 条命中，列出所有候选让用户选。
3. **语义模糊匹配**：使用同义/近义词（如"结算" ↔ "收款" ↔ "支付"）扫 L2 和源码。多命中同 #2。
4. **兜底源码搜索**：中文关键字 + 领域实体 + 动作 + MQ 主题 + Apollo key 五路搜索。多命中列候选。
5. **全部失败**：明确告诉用户"没找到匹配项，能否换个说法或给具体入口方法名"，别硬猜。
