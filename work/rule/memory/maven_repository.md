---
name: 本地 Maven 仓库位置
description: 检索本地 Maven 仓库（查找 jar、POM、依赖源码）时使用的路径
type: reference
---

本地 Maven 仓库路径：`/Users/xuxinyu/repository`

**如何使用：** 当需要查找某个依赖的 jar 包、解压查看 class 文件、确认依赖版本或查看第三方源码时，从 `/Users/xuxinyu/repository` 开始检索，而不是默认的 `~/.m2/repository`。

例如：
- 查找 daas-client-soa：`find /Users/xuxinyu/repository -name "daas-client-soa*.jar"`
- 查找某个 groupId 的 artifact：`ls /Users/xuxinyu/repository/com/ctrip/sysdev/`