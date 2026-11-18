---
name: code-stem
description: Fetch and display a LeetCode problem statement. Use when the user provides a problem number (e.g. "72", "#72") or a name fragment (e.g. "edit distance", "两数之和"). Triggers on phrases like "查一下leetcode X", "leetcode题目 X", "/leetcode X", "找一下X的题干". Outputs ONLY the complete problem statement — no analysis, no hints, no solution discussion.
---

# LeetCode 题目获取 Prompt

用户请求的题目标识：**{query}**（可能是题号、中文名片段或英文名片段）

---

## 执行步骤

### Step 1：从训练数据直接输出（优先）

根据题号或题名，直接从训练数据中检索题目内容并输出。训练数据覆盖绝大多数 LeetCode 题目（截止 2025/08），优先使用此方式，**无需任何网络请求**。

直接按 Step 2 的格式输出即可。

### Step 2：训练数据中找不到时，改用网络抓取

仅当训练数据确实无法确认题目内容时，才走网络抓取流程：

1. 确定英文 slug（如 `two-sum`、`edit-distance`）；若不确定，先用 WebSearch：
   - 搜索词：`leetcode {query} problem statement`
2. 用 WebFetch 抓取：
   ```
   https://leetcode.com/problems/{slug}/description/
   ```
3. 若 WebFetch 返回 403，改用 WebSearch 获取摘要内容。

### Step 3：格式化输出

按以下格式严格输出，**不添加任何分析、解释、提示或注释**：

```
## {题号}. {题目名称}

**难度**：Easy / Medium / Hard

**题目描述**
{题目正文，保留原文的换行和段落}

**示例**
{所有示例，保留输入/输出/解释原文}

**提示**
{Constraints 原文，若有}
```

---

## 输出约束

- 只输出题目内容，不得包含任何分析、思路、解法提示。
- 不得在题目内容之外加任何引导语，如"这道题考察了……""你可以考虑……"。
- 若同时有中英文题目名，两个都输出。
- 若训练数据和网络抓取都失败，说明原因，不要自行编造题目内容。
