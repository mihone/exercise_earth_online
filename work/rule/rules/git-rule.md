# Git 操作规则

## 1. commit message 不要带模型署名
- 生成 `git commit` 消息时，**不要**追加任何与 AI/模型相关的署名，包括但不限于：
  - `Co-Authored-By: Claude ... <noreply@anthropic.com>`
  - `🤖 Generated with [Claude Code](...)`
- 只保留业务描述本身（中文短句优先），空行与署名行都不要。
- 如果默认模板/HEREDOC 示例中带有上述内容，必须主动删除后再提交。

## 2. PR body 同样不要带模型署名
- `gh pr create` 的 body 中，不要带 `🤖 Generated with Claude Code` 之类的标记行。
- 保留 `## Summary` / `## Test plan` 等正文内容即可。

## 3. 不要擅自执行危险 / 不可逆 git 操作
- 未经用户明确同意，不得执行：`push --force`、`reset --hard`、`branch -D`、`checkout .`、`clean -f`、`commit --amend`（除非用户要求 amend）、`--no-verify` / `--no-gpg-sign`。
- 遇到 pre-commit hook 失败：修复后新建一次 commit，不要 `--amend`，也不要加 `--no-verify` 绕过。

## 4. 提交前确认范围
- `git add` 优先按文件名显式添加，避免 `git add .` / `git add -A` 把无关文件（`.cursor/`、`.vscode/`、临时脚本、密钥文件等）也纳入提交。
- 未跟踪文件如果不属于当前任务，保持 untracked 状态，不要主动纳入。