from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/example-log")
async def get_example_log():
    log_path = "c:/Users/myuan/projects/trae-report-summary/tests/data/log1.txt"
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "示例日志文件未找到"

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_log(request: Request, log_content: str = Form(...)):
    # 提取工具调用
    tool_pattern = r'```\s*toolName: (\w+)\s*\n\s*status: (\w+)\s*```'
    matches = re.findall(tool_pattern, log_content, re.DOTALL)
    
    # 统计
    total_calls = len(matches)
    success_calls = sum(1 for _, status in matches if status == 'success')
    
    tool_counts = {}
    for tool, status in matches:
        if tool not in tool_counts:
            tool_counts[tool] = 0
        tool_counts[tool] += 1
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_calls": total_calls,
        "success_calls": success_calls,
        "tool_counts": tool_counts,
        "log_content": log_content
    })
