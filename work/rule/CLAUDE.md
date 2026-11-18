# 全局指令

## 硬规则（必须遵守）

**严禁**在查找 jar / 依赖 / 第三方源码时使用全盘 `find /` 或 `mdfind`。本地 Maven 仓库固定在 `/Users/xuxinyu/repository`。

## 开局必读

每个新会话开始时，先 Read 以下三个文件以加载规则索引：

1. `~/.claude/memory/user_profile.md` — 用户偏好（称呼、沟通风格等），每次必读
2. `~/.claude/memory/global-rules.md` — 五个规则文件（code/biz/test/git/workflow）的导航表
3. `~/.claude/memory/maven_repository.md` — 本地 Maven 仓库路径与用法

读完按其中的场景描述，按需 Read `~/.claude/rules/` 下对应的具体规则文件。