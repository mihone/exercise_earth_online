---
name: 全局编码规则
description: 七个全局规则文件，plan-rule 优先级最高；其余为 code-rule（一般编码）、biz-rule（业务逻辑）、test-rule（单元测试）、git-rule（git 操作）、workflow-rule（Claude 自身操作规范）、review-rule（review 阶段跨点一致性自查）
type: reference
---

已设置全局规则文件在 `~/.claude/rules/` 目录，按场景使用。

> **优先级说明**：`plan-rule.md` 是最高优先级规则。只要进入 plan 模式，必须先加载并严格遵守，不得以其他规则或便利性为由降级。

## 规则文件位置

| 规则文件 | 路径 | 应用场景 |
|---------|------|---------|
| **plan-rule.md** ⭐ | `~/.claude/rules/plan-rule.md` | **最高优先级**。进入 plan 模式时必读：plan 文件末尾维护 `## Prompt 历史` 段，首次写入含触发 prompt，后续每次修改 plan 前先 append 新 prompt |
| **code-rule.md** | `~/.claude/rules/code-rule.md` | 写一般代码时必须参照：卫语句、Map预处理、Optional、Guava、StringUtils、优先复用禁止复制代码 |
| **biz-rule.md** | `~/.claude/rules/biz-rule.md` | 写业务逻辑时必须参照：区分防御编程vs业务语义、消除歧义、拿不准输出TODO |
| **test-rule.md** | `~/.claude/rules/test-rule.md` | 写单元测试时必须参照：JUnit4+PowerMock、命名规范、Mock配置、断言方式 |
| **git-rule.md** | `~/.claude/rules/git-rule.md` | 执行 git/PR 操作时必须参照：commit/PR 不带模型署名、禁止危险操作、显式 add |
| **workflow-rule.md** | `~/.claude/rules/workflow-rule.md` | Claude 自身操作规范：查依赖前先查 memory、Maven 增量编译判读、Explore prompt 聚焦 |
| **review-rule.md** | `~/.claude/rules/review-rule.md` | 只要进入 code review（自查 diff / 正式 review / /code-review skill / review PR），常规 review 体系之外都要额外过一遍本规则的检查项清单。目标是抓"每处单独看都对、合起来矛盾"的隐蔽 bug。清单会持续追加，当前含：阈值比较运算符一致性、写入值域 vs 读取分支、成对判断互补性、特殊值跨点语义 |

## 使用方式

### 场景1（最高优先级）：Plan 模式
参照 **plan-rule.md**
- 进入 plan 模式（`EnterPlanMode`）后立即读取，优先级高于所有其他规则
- plan 文件末尾维护 `## Prompt 历史` 段，首次写入必须包含触发 plan 的 user prompt 原文
- 后续每次修改 plan 前，先 append 触发本次修改的 prompt
- `ExitPlanMode` 前确认 Prompt 历史段存在且至少 1 条

### 场景2：一般Java代码编写
参照 **code-rule.md**
- 卫语句处理复杂逻辑
- List/Map性能评估
- Optional处理判空
- Guava集合工具
- StringUtils字符串处理

### 场景3：业务逻辑编写
同时参照 **code-rule.md** 和 **biz-rule.md**
- 先用 code-rule 规范编码风格
- 再用 biz-rule 区分防御编程vs业务语义
- 防止机械删除有业务含义的判空逻辑
- 拿不准时输出TODO由用户判断

### 场景4：单元测试编写
参照 **test-rule.md**
- 使用 JUnit4 + PowerMock 框架
- 遵循命名规范和结构规范
- Mock配置、断言方式
- 测试覆盖场景

### 场景5：操作流程（Claude 自身行为）
参照 **workflow-rule.md**
- 查找依赖 / jar / 仓库路径之前，先读 `~/.claude/memory/MEMORY.md`
- `mvn compile` 看到 "Nothing to compile" 不要重跑，改看 `target/classes/` 是否有新 .class
- Explore agent prompt 聚焦、简短；多主题用并发多 agent 而非一个长 prompt

### 场景6：Code Review（自查 diff 或 review 他人 PR）
参照 **review-rule.md**
- 触发：只要进入 review 阶段，就要在常规 review 体系之外额外过一遍本规则清单
- 通用动作：把所有引用点摘录并排、代入临界值跑真值表、发现矛盾停下
- 当前清单：阈值比较运算符一致性、写入值域 vs 读取分支、成对判断互补性、特殊值跨点语义（清单会持续追加）
- 单个小节若明确与本次改动无关可空转跳过，但不整体跳过
- 拿不准是否真矛盾，按 biz-rule 第 4 条列 TODO 交给用户

## 自动应用承诺
- **进入 plan 模式时，必须优先自动参照 plan-rule**（plan 文件 Prompt 历史段维护，最高优先级）
- 当写一般 Java 代码时，自动参照 code-rule
- 当写业务逻辑相关代码时，自动参照 biz-rule（可识别业务概念、领域对象、状态判断等）
- 当写单元测试时，自动参照 test-rule
- 当执行 git / PR 操作时，自动参照 git-rule（commit message 不带模型署名等）
- 当涉及查依赖 / 编译判读 / 子 agent 调度等工作流动作时，自动参照 workflow-rule
- 当进入 review 阶段（自查 diff、正式 code review、requesting-code-review skill）时，自动参照 review-rule