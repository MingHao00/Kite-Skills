# Kite-Skills

> 一个 Cursor Agent Skill，协助 AI 将学习计划以 Markdown 形式批量导入 [Kite](https://kiteapp.ai) 待办软件。

---

## 功能概览

- **内容与逻辑解耦**：Agent 按规范编写 `YYYY-MM-DD.md`，脚本负责解析和写库
- **文件名即日期**：无需 frontmatter，日期直接从文件名读取
- **H1 标签即颜色**：`[今日]` 蓝 / `[预习]` 绿 / `[周末实战]` 红
- **路径持久化**：首次配置后自动记住 `kite.db` 路径和 plan 目录，后续免参数
- **安全重复处理**：检测到日期已有数据时交互询问（跳过 / 删除重入 / 退出）
- **状态可视化**：`--status` 输出三态对比表（已导入 / 仅有文件 / 仅在DB）

---

## 快速开始

### 1. 安装 Skill

将本仓库克隆到你的 Cursor 项目的 `.cursor/skills/` 目录下：

```bash
cd your-project/.cursor/skills
git clone https://github.com/MingHao00/Kite-Skills.git kite-import
```

或手动复制 `SKILL.md` 和 `scripts/` 文件夹到 `.cursor/skills/kite-import/`。

### 2. 部署导入脚本

将 `scripts/import_plan.py` 复制到 Kite 安装目录（`kite.db` 所在位置）：

```bash
# Windows 示例
copy scripts\import_plan.py "C:\Users\<你的用户名>\AppData\Local\kite\"
```

### 3. 首次初始化配置

```bash
cd "{kite安装目录}"
python import_plan.py --db "{kite.db完整路径}" --dir "{Markdown文件目录}"
```

示例：

```bash
cd "C:\Users\MingH\AppData\Local\kite"
python import_plan.py --db "C:\Users\MingH\AppData\Local\kite\kite.db" --dir "D:\Python\Career\plan"
```

配置自动写入脚本同目录的 `.kite_config`，后续运行无需再次指定。

---

## Markdown 文件格式

每天一个文件，**文件名即日期**：`YYYY-MM-DD.md`

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

### 格式规则

| 元素 | 规则 |
|---|---|
| H1 | 必须含类型标签：`[今日]` / `[预习]` / `[周末实战]` |
| H2 | 建议含时间标签：`[HH:MM · Xh]`，省略时 `time` 写 `None` 并警告 |
| 分隔 | 多个父任务块之间用单独一行 `---` 分隔 |
| 层级 | 只使用 H1 和 H2，不支持 H3/H4 |
| frontmatter | 禁止使用 YAML frontmatter |

### 颜色约定

| H1 类型标签 | Kite 颜色 | 适用场景 |
|---|---|---|
| `[今日]` | 🔵 蓝色 | 当天主要学习任务 |
| `[预习]` | 🟢 绿色 | 次日内容提前了解（可选）|
| `[周末实战]` | 🔴 红色 | 周末项目实战 |

---

## 导入脚本用法

```bash
# 导入指定文件（日常使用）
python import_plan.py --file "D:\plan\2026-07-10.md"

# 首次初始化 + 立即导入（一步完成）
python import_plan.py --db "...\kite.db" --dir "D:\plan" --file "D:\plan\2026-07-10.md"

# 查看所有文件的导入状态
python import_plan.py --status

# 查看帮助
python import_plan.py --help
```

### `--status` 输出示例

```
日期         状态         任务数   文件
------------------------------------------------------------
2026-07-09   [仅在DB]     5        （无文件）
2026-07-10   [已导入]     5        2026-07-10.md
2026-07-11   [仅有文件]   0        2026-07-11.md

汇总：已导入 1 天，仅有文件 1 天，仅在DB 1 天
```

---

## 文件结构

```
Kite-Skills/
├── README.md
├── SKILL.md               # Cursor Skill 主文件（Agent 读取此文件）
└── scripts/
    └── import_plan.py     # Markdown 解析 + Kite 数据库写入脚本
```

### `.kite_config` 格式（自动生成）

脚本首次运行后在其同目录自动创建，两行纯文本：

```
C:\Users\MingH\AppData\Local\kite\kite.db
D:\Python\Career\plan
```

---

## 环境要求

- Python 3.10+（使用了 `str | None` 类型注解）
- 标准库即可，无需安装第三方包

---

## 与 Cursor Agent 配合使用

将本 Skill 注册后，对 Agent 说：

> "帮我把今天的学习任务加到 Kite"

Agent 会自动读取 `SKILL.md`，询问必要信息，按规范生成 `YYYY-MM-DD.md`，并引导你运行导入命令。
