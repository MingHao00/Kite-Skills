"""
import_plan.py — Kite 任务批量导入工具（Markdown 驱动版）

用法：
  # 首次初始化
  python import_plan.py --db "<kite.db路径>" --dir "<Markdown目录>"

  # 日常导入
  python import_plan.py --file "<YYYY-MM-DD.md路径>"

  # 查看状态
  python import_plan.py --status
"""

import argparse
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────── 常量 ────────────────────────────────────────────

TAG_COLOR: dict[str, str] = {
    "今日": "blue",
    "预习": "green",
    "周末实战": "red",
}

TAG_RE = re.compile(r'^#\s+\[(.+?)\]\s+(.+)')
H2_RE = re.compile(r'^##\s+(.+)')
TIME_RE = re.compile(r'\[(\d{2}:\d{2})')

# 脚本启动时固定时间戳前缀，避免跨秒边界产生 ID 碰撞
_ID_PREFIX = datetime.now().strftime('%y%m%d%H%M%S')
_seq_counter = 0

CONFIG_FILE = Path(__file__).parent / ".kite_config"


# ─────────────────────────── ID 生成 ─────────────────────────────────────────

def make_id() -> str:
    global _seq_counter
    _seq_counter += 1
    return f"{_ID_PREFIX}{_seq_counter:03d}"


# ─────────────────────────── 配置文件读写 ────────────────────────────────────

def load_config() -> tuple[str, str]:
    """返回 (db_path, plan_dir)，缺失时返回空字符串。"""
    if not CONFIG_FILE.exists():
        return "", ""
    lines = CONFIG_FILE.read_text(encoding="utf-8").splitlines()
    db_path = lines[0].strip() if len(lines) > 0 else ""
    plan_dir = lines[1].strip() if len(lines) > 1 else ""
    return db_path, plan_dir


def save_config(db_path: str = None, plan_dir: str = None) -> None:
    """更新配置，只覆盖传入的非空字段，保留另一字段的原有值。"""
    old_db, old_plan = load_config()
    new_db = db_path.strip() if db_path else old_db
    new_plan = plan_dir.strip() if plan_dir else old_plan
    CONFIG_FILE.write_text(f"{new_db}\n{new_plan}", encoding="utf-8")


def require_db() -> str:
    db, _ = load_config()
    if not db:
        raise SystemExit(
            "未配置 kite.db 路径，请先运行：\n"
            "  python import_plan.py --db \"<kite.db完整路径>\""
        )
    return db


def require_plan_dir() -> Path:
    _, plan = load_config()
    if not plan:
        raise SystemExit(
            "未配置 Markdown 文件目录，请先运行：\n"
            "  python import_plan.py --dir \"<Markdown文件目录>\""
        )
    return Path(plan)


# ─────────────────────────── 数据库连接 ──────────────────────────────────────

def connect_db(db_path: str) -> sqlite3.Connection:
    """连接前验证路径存在，防止 SQLite 静默创建空库。"""
    if not Path(db_path).exists():
        raise SystemExit(
            f"数据库文件不存在：{db_path}\n"
            "请检查路径是否正确，或重新运行 --db 指定正确路径。"
        )
    return sqlite3.connect(db_path)


# ─────────────────────────── 日期解析 ────────────────────────────────────────

def parse_date_from_filename(filepath) -> int:
    """从 YYYY-MM-DD.md 文件名中解析日期，返回整数 YYYYMMDD。"""
    stem = Path(filepath).stem
    dt = datetime.strptime(stem, "%Y-%m-%d")
    return int(dt.strftime("%Y%m%d"))


# ─────────────────────────── 颜色解析 ────────────────────────────────────────

def resolve_color(tag: str) -> str:
    if tag not in TAG_COLOR:
        raise SystemExit(
            f"未知标签 [{tag}]，支持的标签：{list(TAG_COLOR.keys())}\n"
            "请修正 Markdown 文件后重新运行。"
        )
    return TAG_COLOR[tag]


# ─────────────────────────── content 清理 ────────────────────────────────────

def clean_content(text: str) -> str | None:
    """去除首尾空白，压缩连续空行为单个换行，空内容返回 None。"""
    text = text.strip()
    if not text:
        return None
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


# ─────────────────────────── Markdown 解析 ───────────────────────────────────

def parse_markdown(filepath: str) -> list[dict]:
    """
    解析 YYYY-MM-DD.md，返回任务列表。
    每项格式：
      {
        "title": str,
        "color": str | None,   # 父任务有值，子任务为 None
        "time":  str | None,   # 子任务有值，父任务为 None
        "content": str | None,
        "is_parent": bool,
        "parent_idx": int | None,  # 子任务指向父任务在列表中的索引
        "sort_order": int,
      }
    """
    raw = Path(filepath).read_text(encoding="utf-8")

    # 将文件按行处理，构建结构化任务树
    lines = raw.splitlines()
    tasks: list[dict] = []

    current_parent: dict | None = None
    parent_content_lines: list[str] = []
    child_content_lines: list[str] = []
    current_child: dict | None = None
    parent_sort = 0

    def flush_child():
        """将当前子任务的 content 存入并重置。"""
        nonlocal current_child, child_content_lines
        if current_child is not None:
            current_child["content"] = clean_content("\n".join(child_content_lines))
            tasks.append(current_child)
        current_child = None
        child_content_lines = []

    def flush_parent():
        """将当前父任务（含 content）存入并重置。"""
        nonlocal current_parent, parent_content_lines
        if current_parent is not None:
            current_parent["content"] = clean_content("\n".join(parent_content_lines))
            tasks.append(current_parent)
        current_parent = None
        parent_content_lines = []

    for line in lines:
        # H1 行：开启新父任务块
        m1 = TAG_RE.match(line)
        if m1:
            flush_child()
            flush_parent()
            tag, title = m1.group(1), m1.group(2).strip()
            color = resolve_color(tag)
            parent_sort += 1
            current_parent = {
                "title": title,
                "color": color,
                "time": None,
                "content": None,
                "is_parent": True,
                "parent_idx": None,
                "sort_order": parent_sort,
            }
            parent_content_lines = []
            continue

        # 分隔符 ---：结束当前块（flush 在下一 H1 时已处理，此处保持兼容）
        if re.match(r'^---\s*$', line):
            flush_child()
            flush_parent()
            continue

        # H2 行：开启子任务
        m2 = H2_RE.match(line)
        if m2:
            if current_parent is None:
                print(f"警告：H2 '{line.strip()}' 出现在 H1 之前，已跳过。")
                continue
            flush_child()
            h2_title = m2.group(1).strip()
            # 提取时间
            tm = TIME_RE.search(h2_title)
            task_time = tm.group(1) if tm else None
            if task_time is None:
                print(f"警告：H2 标题 '{h2_title}' 无时间标签，time 将写入 None。")
            # 子任务的 sort_order：在该父任务内独立计数
            parent_task = tasks[-1] if (current_parent is None and tasks) else current_parent
            # 统计当前父任务已有多少子任务
            parent_ref_idx = len(tasks)  # 父任务尚未 append，先记录其将来的索引
            child_sort = sum(
                1 for t in tasks
                if not t["is_parent"] and t.get("_parent_ref") == id(current_parent)
            ) + 1
            current_child = {
                "title": h2_title,
                "color": None,
                "time": task_time,
                "content": None,
                "is_parent": False,
                "_parent_ref": id(current_parent),
                "parent_idx": None,  # 解析完成后填充
                "sort_order": child_sort,
            }
            child_content_lines = []
            continue

        # 普通文本行
        if current_child is not None:
            child_content_lines.append(line)
        elif current_parent is not None:
            parent_content_lines.append(line)

    # 文件结束时 flush
    flush_child()
    flush_parent()

    return tasks


def build_rows(tasks: list[dict], date_int: int) -> list[tuple]:
    """
    将解析后的任务列表转换为数据库行元组列表。
    同时处理 parent_id 赋值（父先于子）。

    返回：(id, title, completed, date, sort_order, content, color, time, parent_id) 元组列表
    """
    rows = []
    # 按出现顺序处理：父任务先行，子任务其后
    # 由于 parse_markdown 已按父→子顺序排列，直接顺序处理即可
    # 构建 parent_ref → parent_id 映射
    parent_ref_to_id: dict[int, str] = {}

    # 两遍处理：先分配父任务 ID，再分配子任务 ID
    parent_tasks = [t for t in tasks if t["is_parent"]]
    child_tasks = [t for t in tasks if not t["is_parent"]]

    # 为父任务分配 ID
    parent_id_map: dict[int, str] = {}
    for t in parent_tasks:
        pid = make_id()
        parent_id_map[id(t)] = pid

    # 第二轮：为子任务分配 ID，并找到对应父任务
    # 需要知道每个子任务属于哪个父任务
    # parse_markdown 使用 _parent_ref = id(current_parent) 但父任务已 flush 出 tasks
    # 需要重建映射：子任务的 _parent_ref 对应哪个父任务对象
    # 由于父任务对象被 flush 到 tasks 列表中，此时对象仍存活，id() 仍有效
    for t in parent_tasks:
        pid = parent_id_map[id(t)]
        rows.append((
            pid,
            t["title"],
            0,
            date_int,
            t["sort_order"],
            t["content"],
            t["color"],
            t["time"],
            None,  # parent_id = None for parent tasks
        ))

    for t in child_tasks:
        cid = make_id()
        parent_ref = t.get("_parent_ref")
        par_id = None
        # 根据 _parent_ref 找对应父任务
        for pt in parent_tasks:
            if id(pt) == parent_ref:
                par_id = parent_id_map[id(pt)]
                break
        rows.append((
            cid,
            t["title"],
            0,
            date_int,
            t["sort_order"],
            t["content"],
            t["color"],
            t["time"],
            par_id,
        ))

    return rows


# ─────────────────────────── 导入操作 ────────────────────────────────────────

def do_import(filepath: str, conn: sqlite3.Connection) -> None:
    """解析 Markdown 文件并导入到数据库。"""
    # 解析文件名中的日期
    try:
        date_int = parse_date_from_filename(filepath)
    except ValueError:
        raise SystemExit(
            f"文件名格式错误：{Path(filepath).name}\n"
            "文件名须为 YYYY-MM-DD.md 格式（例：2026-07-10.md）"
        )

    cur = conn.cursor()

    # 检查重复
    cur.execute("SELECT COUNT(*) FROM todos WHERE date = ?", (date_int,))
    existing = cur.fetchone()[0]

    if existing > 0:
        print(f"[!] 日期 {date_int} 已有 {existing} 条记录。")
        print("    请选择：s=跳过  d=删除后重新导入  q=退出", end="  ")
        choice = input().strip().lower()
        if choice == "s":
            print("已跳过。")
            return
        elif choice == "q":
            print("已退出。")
            sys.exit(0)
        elif choice == "d":
            print(f"将删除 {date_int} 的原有数据并重新导入...")
        else:
            print(f"无效选项 '{choice}'，已退出。")
            sys.exit(1)

    # 解析 Markdown
    tasks = parse_markdown(filepath)
    if not tasks:
        print(f"警告：文件 {Path(filepath).name} 未解析到任何任务。")
        return

    rows = build_rows(tasks, date_int)

    # 事务：DELETE（如需）+ INSERT
    with conn:
        if existing > 0:
            conn.execute("DELETE FROM todos WHERE date = ?", (date_int,))
        conn.executemany(
            "INSERT INTO todos "
            "(id, title, completed, date, sort_order, content, color, time, parent_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows
        )

    # 汇总输出
    date_str = f"{str(date_int)[:4]}-{str(date_int)[4:6]}-{str(date_int)[6:]}"
    parent_count = sum(1 for t in tasks if t["is_parent"])
    child_count = sum(1 for t in tasks if not t["is_parent"])
    print(f"\n[OK] 导入完成：日期 {date_str}，共插入 {len(rows)} 条记录")
    print(f"     父任务 {parent_count} 条，子任务 {child_count} 条")
    print("     请重启 Kite 以刷新显示。")


# ─────────────────────────── 状态视图 ────────────────────────────────────────

def do_status(plan_dir: Path, conn: sqlite3.Connection) -> None:
    """扫描目录与数据库，输出三态状态表。"""
    # 扫描目录中合法的 YYYY-MM-DD.md 文件
    md_dates: dict[int, Path] = {}
    for f in sorted(plan_dir.glob("????-??-??.md")):
        try:
            d = parse_date_from_filename(f)
            md_dates[d] = f
        except ValueError:
            print(f"警告：跳过非法文件名 {f.name}")

    # 查询数据库中已有记录的日期
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT date, COUNT(*) FROM todos GROUP BY date")
    db_dates: dict[int, int] = {row[0]: row[1] for row in cur.fetchall()}

    all_dates = sorted(set(md_dates.keys()) | set(db_dates.keys()))

    if not all_dates:
        print("（目录和数据库中均无数据）")
        return

    print(f"\n{'日期':<12} {'状态':<12} {'任务数':<8} {'文件'}")
    print("-" * 60)

    for d in all_dates:
        d_str = f"{str(d)[:4]}-{str(d)[4:6]}-{str(d)[6:]}"
        has_file = d in md_dates
        has_db = d in db_dates
        count = db_dates.get(d, 0)
        fname = md_dates[d].name if has_file else "（无文件）"

        if has_file and has_db:
            status = "[已导入]"
        elif has_file and not has_db:
            status = "[仅有文件]"
        else:
            status = "[仅在DB]"

        print(f"{d_str:<12} {status:<12} {count:<8} {fname}")

    print()
    imported = sum(1 for d in all_dates if d in md_dates and d in db_dates)
    file_only = sum(1 for d in all_dates if d in md_dates and d not in db_dates)
    db_only = sum(1 for d in all_dates if d not in md_dates and d in db_dates)
    print(f"汇总：已导入 {imported} 天，仅有文件 {file_only} 天，仅在DB {db_only} 天")


# ─────────────────────────── CLI 入口 ────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kite 任务导入工具（Markdown 驱动版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 首次初始化配置
  python import_plan.py --db "E:\\kite\\kite.db" --dir "D:\\plan"

  # 导入指定文件（日期自动从文件名读取）
  python import_plan.py --file "D:\\plan\\2026-07-10.md"

  # 首次初始化 + 立即导入
  python import_plan.py --db "E:\\kite\\kite.db" --dir "D:\\plan" --file "D:\\plan\\2026-07-10.md"

  # 查看所有文件的导入状态
  python import_plan.py --status
        """
    )
    parser.add_argument("--db", metavar="PATH", help="kite.db 的完整路径（首次使用时指定，自动记住）")
    parser.add_argument("--dir", metavar="DIR", help="Markdown 文件所在目录（首次使用时指定，自动记住）")
    parser.add_argument("--file", metavar="FILE", help="要导入的 Markdown 文件路径（YYYY-MM-DD.md）")
    parser.add_argument("--status", action="store_true", help="显示目录中所有 Markdown 文件的导入状态")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # 无参数时打印帮助
    if not any([args.db, args.dir, args.file, args.status]):
        import subprocess
        subprocess.run([sys.executable, __file__, "--help"])
        return

    # 持久化 --db / --dir（若提供）
    if args.db or args.dir:
        save_config(db_path=args.db, plan_dir=args.dir)

    # 获取 db 路径
    db_path = require_db()
    conn = connect_db(db_path)

    try:
        if args.file:
            do_import(args.file, conn)

        if args.status:
            plan_dir = require_plan_dir()
            do_status(plan_dir, conn)

        # 若只传了 --db / --dir 而未指定操作，打印配置确认
        if not args.file and not args.status:
            db_cfg, dir_cfg = load_config()
            print(f"[OK] 配置已保存：")
            print(f"     kite.db  = {db_cfg}")
            print(f"     plan目录 = {dir_cfg}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
