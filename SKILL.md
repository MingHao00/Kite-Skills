---
name: kite-import
description: >-
  将每日学习任务导入 Kite 待办软件。当用户说"把今天的任务加到 Kite"、"导入 Day N 的计划"、
  "帮我写明天的 Kite 日程"、"生成今天的待办并导入"时使用本技能。
  包含 Markdown 文件格式规范、文件命名规则、颜色约定和导入脚本使用说明。
---

# Kite 日程导入技能

将学习计划任务写入 Markdown 文件，由 `import_plan.py` 解析后写入 Kite 数据库。

## 执行约束（必须遵守）

- **每次只处理一天**：每次对话仅生成当天（或用户指定的某一天）的 Markdown 文件，不批量生成多天
- **直接创建文件**：使用文件写入工具直接创建 `YYYY-MM-DD.md`，**禁止通过编写 Python/Shell 脚本间接生成**
- **内容来自对话上下文**：文件内容应基于用户的实际学习进度和当天状态，不得机械复制学习计划原文

## 工作流程

1. 确认前置配置（首次使用）
2. 直接创建并写入 `YYYY-MM-DD.md`
3. 引导用户运行导入命令

---

## 前置配置（仅首次）

向用户确认两项：

**① `.kite_config` 是否已初始化**

若未初始化，需要用户提供 `kite.db` 完整路径（通常在 Kite 安装目录下），然后运行：

```bash
cd "{kite安装目录}"
python scripts/import_plan.py --db "{kite.db路径}" --dir "{Markdown文件目录}"
```

**② Markdown 文件存放目录**

建议与学习计划文档放同一目录（如 `D:\Python\Career\plan\`）。

> Agent 无需自行查询数据库检查重复。脚本运行时会自动检测并交互提示（s 跳过 / d 删除重入 / q 退出）。

---

## Markdown 文件格式

**文件命名**：`YYYY-MM-DD.md`，日期即为 Kite 中显示的日历日期。

**完整模板**：

```markdown
# [今日] Day 2 · Python 异步编程

目标：建立异步编程心智模型。总时长：5小时

## [09:00 · 2h] 精读 asyncio 官方文档

重点章节：协程 / 任务 / 事件循环
参考：https://docs.python.org/zh-cn/3/library/asyncio.html

## [11:00 · 3h] 完成异步编程练习

用 asyncio.gather 并发调用3个模拟 IO 函数

---

# [预习] Day 3 预习 · LLM API 初调用

明日预习，约15分钟。

## [17:00 · 0.5h] 浏览 OpenAI Quickstart

重点：messages 参数结构、role 字段含义
```

**格式规则**：

| 元素 | 规则 |
|---|---|
| H1 | 必须含类型标签：`# [今日] 标题` / `# [预习] 标题` / `# [周末实战] 标题` |
| H2 | 建议含时间：`## [HH:MM · Xh] 标题`（省略时 time 写 None 并警告）|
| 分隔 | 多个父任务块之间用单独一行 `---` 分隔 |
| 层级 | 只用 H1 和 H2，不使用 H3/H4 |
| 日期 | 由文件名提供，文件内无需声明 |
| frontmatter | 禁止使用 YAML frontmatter |

可直接复制的 H2 模板（避免中点字符输入差异）：
```
## [09:00 · 2h] 子任务标题
```

---

## 颜色约定

| H1 类型标签 | Kite 颜色 | 适用场景 |
|---|---|---|
| `[今日]` | 蓝色 | 当天主要学习任务 |
| `[预习]` | 绿色 | 次日内容提前了解（可选）|
| `[周末实战]` | 红色 | 周末项目实战 |

使用表外标签（如 `[复习]`）会导致脚本报错。

---

## 导入命令速查

```bash
# 日常使用：导入指定文件（日期自动从文件名读取）
python scripts/import_plan.py --file "{Markdown文件路径}"

# 首次初始化 + 立即导入（一步完成）
python scripts/import_plan.py --db "{kite.db路径}" --dir "{目录}" --file "{Markdown文件路径}"

# 查看所有文件的导入状态
python scripts/import_plan.py --status
```

## 工具脚本

**`scripts/import_plan.py`**：Markdown 解析 + Kite 数据库写入

```bash
python scripts/import_plan.py --help
```

脚本功能：
- 从文件名解析日期（`YYYY-MM-DD.md` → `YYYYMMDD`）
- 从 H1 标签推断颜色，从 H2 提取时间
- 路径持久化到脚本同目录 `.kite_config`（两行：db路径 / plan目录）
- 重复日期时交互确认（s / d / q）
- `--status` 输出三态状态表（已导入 / 仅有文件 / 仅在DB）
