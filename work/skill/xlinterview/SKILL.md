---
name: xlinterview
description: Fetch and display interview question content from xiaolincoding.com and xiaolinnote.com. Supports topic lookup (e.g. "LLM engineering", "RAG", "Agent", "MySQL index", "ByteDance"). Renders original text without images. Triggers on: "/xlinterview X", "xlinterview".
---

# 小林面试题拉取

用户请求的专题：**{query}**

---

## 站点与专题目录

### 站点一：xiaolincoding.com（免费，无需 token）

**后端面试真题（大厂/中厂/银行/新能源/通信/手机）**
| 专题 | URL 路径 |
|------|---------|
| 字节跳动 | `/backend_interview/internet_giants/byte_dance.html` |
| 阿里巴巴 | `/backend_interview/internet_giants/aliyun.html` |
| 腾讯 | `/backend_interview/internet_giants/tencent.html` |
| 百度 | `/backend_interview/internet_giants/baidu.html` |
| 美团 | `/backend_interview/internet_giants/meituan.html` |
| 滴滴 | `/backend_interview/internet_giants/didi.html` |
| 快手 | `/backend_interview/internet_giants/kuaishou.html` |
| 京东 | `/backend_interview/internet_giants/jingdong.html` |
| 饿了么 | `/backend_interview/internet_giants/elme.html` |
| 蚂蚁 | `/backend_interview/internet_giants/mayi.html` |
| 米哈游 | `/backend_interview/internet_giants/mihayou.html` |
| QQ音乐 | `/backend_interview/internet_giants/qqmusic.html` |
| Shopee | `/backend_interview/internet_giants/shopee.html` |
| 淘宝 | `/backend_interview/internet_giants/taobao.html` |
| B站 | `/backend_interview/internet_medium/bilibili.html` |
| 小红书 | `/backend_interview/internet_medium/xiaohongshu.html` |
| 携程 | `/backend_interview/internet_medium/xiecheng.html` |
| 科大讯飞 | `/backend_interview/internet_medium/kedaxunfei.html` |
| 华为 | `/backend_interview/telecommunication/huawei.html` |
| 小米 | `/backend_interview/mobile/xiaomi.html` |
| 比亚迪 | `/backend_interview/new_energy/biyadi.html` |
| 理想 | `/backend_interview/new_energy/lixiang.html` |
| 蔚来 | `/backend_interview/new_energy/weilai.html` |
| 招商银行 | `/backend_interview/bank/china_merchants_bank.html` |

**基础八股（深度文章）**
| 专题 | URL 路径 |
|------|---------|
| Java基础 | `/interview/java.html` |
| JVM | `/interview/jvm.html` |
| JUC并发 | `/interview/juc.html` |
| Spring | `/interview/spring.html` |
| MySQL面试 | `/interview/mysql.html` |
| Redis面试 | `/interview/redis.html` |
| 网络面试 | `/interview/network.html` |
| 操作系统面试 | `/interview/os.html` |
| 消息队列MQ | `/interview/mq.html` |
| 系统设计 | `/interview/systemdesign.html` |
| Docker | `/interview/docker.html` |
| 算法 | `/interview/algorithms.html` |
| MySQL索引 | `/mysql/index/index_interview.html` |
| MySQL事务/MVCC | `/mysql/transaction/mvcc.html` |
| MySQL锁 | `/mysql/lock/mysql_lock.html` |
| TCP面试 | `/network/3_tcp/tcp_interview.html` |
| HTTP面试 | `/network/2_http/http_interview.html` |
| Redis数据结构 | `/redis/data_struct/data_struct.html` |
| Redis持久化AOF | `/redis/storage/aof.html` |
| Redis集群 | `/redis/cluster/cluster.html` |

---

### 站点二：xiaolinnote.com（付费，需要 token）

**大模型面试题（74 道）**
| 专题 | URL 路径 |
|------|---------|
| 大模型工程总览 | `/ai/llm/llm_info.html` |
| 什么是大语言模型 | `/ai/llm/what_is_llm.html` |
| Transformer架构 | `/ai/llm/transformer_architecture.html` |
| MHA/MQA/GQA/Flash Attention | `/ai/llm/mha_mqa_gqa_flash_attention.html` |
| 位置编码RoPE | `/ai/llm/position_encoding.html` |
| 分词器Tokenizer | `/ai/llm/tokenizer.html` |
| 大模型训练流程 | `/ai/llm/llm_training.html` |
| Scaling Law与涌现能力 | `/ai/llm/scaling_law_emergence.html` |
| 大模型微调方案 | `/ai/llm/finetuning.html` |
| LoRA技术 | `/ai/llm/lora.html` |
| Post-Training/RLHF/DPO | `/ai/llm/post_training.html` |
| DPO vs PPO | `/ai/llm/dpo_vs_ppo.html` |
| 解码策略 | `/ai/llm/decoding_strategies.html` |
| 温度/Top-P/Top-K | `/ai/llm/temperature_top_p_top_k.html` |
| KV Cache与Prompt Caching | `/ai/llm/kv_cache_prompt_caching.html` |
| 大模型量化 | `/ai/llm/quantization.html` |
| Prompt工程 | `/ai/llm/prompt_engineering.html` |
| CoT思维链 | `/ai/llm/cot.html` |
| 大模型幻觉 | `/ai/llm/hallucination.html` |
| MoE混合专家模型 | `/ai/llm/moe.html` |
| 部署框架vLLM/TGI | `/ai/llm/deployment_frameworks.html` |
| 评测指标 | `/ai/llm/evaluation_metrics.html` |
| 模型选型 | `/ai/llm/model_selection.html` |
| Agent面试题总览 | `/ai/agent/agent_info.html` |
| 什么是Agent | `/ai/agent/1_whatisagent.html` |
| Agent组件 | `/ai/agent/2_components.html` |
| Workflow与工具 | `/ai/agent/3_workflow_tools.html` |
| Agent设计模式 | `/ai/agent/4_patterns.html` |
| ReAct | `/ai/agent/5_react.html` |
| 三种Agent模式 | `/ai/agent/6_three_patterns.html` |
| 任务拆分 | `/ai/agent/7_tasksplit.html` |
| Agent记忆 | `/ai/agent/8_memory.html` |
| 记忆存储 | `/ai/agent/9_memory_storage.html` |
| 多Agent | `/ai/agent/10_multiagent.html` |
| 单Agent vs 多Agent | `/ai/agent/11_single_multi.html` |
| 记忆压缩 | `/ai/agent/12_memcompress.html` |
| 手写代码Agent | `/ai/agent/13_handcode.html` |
| Planning规划 | `/ai/agent/14_planning.html` |
| 反思Reflection | `/ai/agent/15_reflection.html` |
| 协作模式 | `/ai/agent/16_collab.html` |
| RAG面试题总览 | `/ai/rag/rag_info.html` |
| 什么是RAG | `/ai/rag/1_whatisrag.html` |
| RAG的问题 | `/ai/rag/2_rag_problems.html` |
| RAG vs 微调 | `/ai/rag/3_rag_vs_finetune.html` |
| 文档分块Chunking | `/ai/rag/4_chunking.html` |
| 语义切割 | `/ai/rag/5_semantic_cuts.html` |
| Embedding | `/ai/rag/6_embedding.html` |
| Embedding算法 | `/ai/rag/7_embedding_algos.html` |
| 向量数据库 | `/ai/rag/8_vectordb.html` |
| 向量库实践 | `/ai/rag/9_vectordb_practice.html` |
| 在线工作流 | `/ai/rag/10_online_workflow.html` |
| 检索类型 | `/ai/rag/11_retrieval_types.html` |
| 查询改写 | `/ai/rag/12_query_rewrite.html` |
| 多路检索 | `/ai/rag/13_multi_retrieval.html` |
| 检索优化 | `/ai/rag/14_retrieval_opt.html` |
| 高级RAG范式 | `/ai/rag/15_advanced_paradigms.html` |
| 图数据库 | `/ai/rag/16_graph_db.html` |
| RAG幻觉 | `/ai/rag/17_hallucination.html` |
| RAG评测 | `/ai/rag/18_evaluation.html` |
| 动态更新 | `/ai/rag/19_dynamic_update.html` |
| RAG最难的部分 | `/ai/rag/20_hardest_parts.html` |
| LLM工具调用总览 | `/ai/tools/tools_info.html` |
| Function Calling | `/ai/tools/1_function_calling.html` |
| LLM工具学习 | `/ai/tools/2_llm_tool_learning.html` |
| FC训练 | `/ai/tools/3_fc_training.html` |
| 什么是MCP | `/ai/tools/4_what_is_mcp.html` |
| MCP组件 | `/ai/tools/5_mcp_components.html` |
| MCP vs FC | `/ai/tools/6_mcp_vs_fc.html` |
| FC vs MCP使用场景 | `/ai/tools/7_fc_vs_mcp_usage.html` |
| 推理时不用MCP | `/ai/tools/8_reasoning_no_mcp.html` |
| Skill机制 | `/ai/tools/9_skill.html` |
| MCP vs Skill | `/ai/tools/10_mcp_vs_skill.html` |
| FC/Skill/MCP关系 | `/ai/tools/11_fc_skill_mcp.html` |
| A2A协议 | `/ai/tools/12_a2a_protocol.html` |
| MCP传输层 | `/ai/tools/13_mcp_transport.html` |
| SSE vs WebSocket | `/ai/tools/14_sse_vs_websocket.html` |
| WebRTC vs WS | `/ai/tools/15_webrtc_vs_ws.html` |
| LLM Gateway | `/ai/tools/16_llm_gateway.html` |

---

## 执行步骤

### Step 1：识别专题，确定 URL

根据用户输入的 `{query}`，从上面目录中匹配最相关的专题 URL：
- 模糊匹配：如"大模型"→ 大模型工程总览；"RAG分块"→ 文档分块Chunking；"字节"→ 字节跳动
- 可以同时返回多个相关页面（如用户说"RAG全套"则返回所有 `/ai/rag/` 下的页面）
- 站点一 URL 前缀：`https://www.xiaolincoding.com`
- 站点二 URL 前缀：`https://xiaolinnote.com`

### Step 2：读取 token（仅站点二需要）

读取文件 `~/.claude/xlinterview_token.txt`，提取 `readmore_token_84217-9121498685057-715=` 后面的值作为 cookie。

**token 过期处理：**
若读取失败，或 curl 返回内容明显是登录页/空内容（关键词：`请登录`、`付费`、内容 < 5KB），则：
1. 告知用户 token 已过期
2. 引导用户提供新 token，支持两种方式：
   - **方式 A（直接 token）**：用户粘贴 `readmore_token_84217-9121498685057-715=eyJ...` 这一行
   - **方式 B（curl 命令）**：用户粘贴完整 curl 命令，从 `-b '...'` 参数中解析出 `readmore_token_84217-9121498685057-715=eyJ...`
3. 将新 token 写入 `~/.claude/xlinterview_token.txt`（覆盖旧值），格式保持不变

### Step 3：拉取页面内容

**站点一（无 token）：**
```bash
curl -s "https://www.xiaolincoding.com{path}" \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
```

**站点二（带 token）：**
```bash
curl -s "https://xiaolinnote.com{path}" \
  -b 'readmore_token_84217-9121498685057-715={token值}' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
```

### Step 4：提取正文并输出

从 HTML 中提取正文，规则：
1. 去掉所有 `<img>` 标签（不含图）
2. 保留 `<h1>`~`<h4>` 标题结构
3. 保留 `<p>`、`<ul>`、`<ol>`、`<li>`、`<code>`、`<pre>`、`<table>` 等内容标签的文字
4. 去掉导航栏、页脚、广告、侧边栏等噪音（通常在 `<nav>`、`<footer>`、`<aside>` 里）
5. 用 pandoc 或 sed/grep 转为可读文本，Bash 命令参考：
```bash
# 提取正文文本（去图片、去标签、保留结构）
cat /tmp/page.html \
  | sed 's/<img[^>]*>//g' \
  | grep -oE '<(h[1-4]|p|li|code|pre|td|th)[^>]*>.*?</(h[1-4]|p|li|code|pre|td|th)>' \
  | sed 's/<[^>]*>//g' \
  | grep -v '^[[:space:]]*$'
```
或者保存到临时文件后用 pandoc：
```bash
curl -s "{url}" ... -o /tmp/xl_page.html
pandoc -f html -t markdown --wrap=none /tmp/xl_page.html 2>/dev/null \
  | grep -v '!\[' \
  | sed '/^[[:space:]]*$/d'
```

### Step 5：格式化呈现

输出格式：
```
## {专题名称}
> 来源：{完整 URL}

{正文内容，保留标题层级和代码块}
```

多个专题时依次输出，每个之间加分隔线 `---`。

---

## 特殊指令支持

- `/xlinterview 目录` 或 `/xlinterview list` — 列出所有专题目录（不拉取内容）
- `/xlinterview token <值>` — 直接更新 token，写入文件
- `/xlinterview token` — 显示当前 token 文件内容（脱敏：只显示前20字符）
