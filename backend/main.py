from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pypinyin import lazy_pinyin, Style
from snownlp import SnowNLP
import json
from datetime import datetime
from pathlib import Path



# 用 __file__ 定位，不依赖进程的工作目录：
# 从 backend/ 启动和从项目根用 --app-dir 启动，都会落到同一个文件上。
HISTORY_FILE = Path(__file__).with_name("history.json")

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_record(record):
    records = load_history()
    records.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


profile = {
    "heroTitle": "关于我",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
    "featuredWork": {
        "kicker": "作品",
        "title": "文字实验室",
        "copy": "拼音和情绪，挖掘中文里的细节",
        "linkLabel": "打开作品",
    },
    "identity": {
        "motto": "已识乾坤大，尤怜草木青",
        "learning": "零到全栈",
    },
}


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/api/profile")
def get_profile():
    return profile


def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text
    score = round(SnowNLP(text).sentiments, 2)
    result = {
        "text": text,
        "score": score,
        "label": score_label(score),
        "pinyin": " ".join(lazy_pinyin(text, style=Style.TONE)),
        # astimezone() 带上本机时区，存成 2026-11-18T22:15:00+08:00 这种形式；
        # 原来是 UTC，前端直接显示会差 8 小时。
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    save_record(result)                                                          # ← 存档到文件
    return result

@app.get("/api/history")
def history():
    records = load_history()
    records.reverse()          # 倒过来：新的排前面
    return records[:10]        # 只返回最近 10 条

