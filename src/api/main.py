"""
FastAPI Backend API for Web UI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random
import os
import uuid
import asyncio
import threading
import time

app = FastAPI(title="AI Browser Automation API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 数据模型
# =============================================================================

class Statistics(BaseModel):
    totalTasks: int
    completedTasks: int
    failedTasks: int
    runningTasks: int
    totalTokens: int
    successRate: float

class TokenTrend(BaseModel):
    date: str
    tokens: int

class DurationDistribution(BaseModel):
    range: str
    count: int

class TaskAnalysis(BaseModel):
    successCount: int
    failedCount: int
    durationDistribution: List[DurationDistribution]

class Task(BaseModel):
    id: str
    name: str
    status: str
    startTime: str
    endTime: Optional[str] = None
    duration: Optional[int] = None
    tokenUsed: Optional[int] = None
    result: Optional[str] = None
    error: Optional[str] = None

class AgentConfig(BaseModel):
    agentType: str = "custom"
    maxSteps: int = 100
    useVision: bool = True
    maxActionsPerStep: int = 10
    toolCallInContent: bool = True

class BrowserConfig(BaseModel):
    headless: bool = False
    disableSecurity: bool = True
    windowWidth: int = 1280
    windowHeight: int = 1100
    saveRecordingPath: Optional[str] = "./tmp/recordings"
    saveTracePath: Optional[str] = "./tmp/traces"

class LLMConfig(BaseModel):
    provider: str = "openai"
    modelName: str = "gpt-4o"
    temperature: float = 1.0
    baseUrl: Optional[str] = None
    apiKey: Optional[str] = None

class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[dict] = None

class AgentRunRequest(BaseModel):
    task: str

# =============================================================================
# 模拟数据存储
# =============================================================================

# 配置存储
_agent_config = AgentConfig()
_browser_config = BrowserConfig()
_llm_config = LLMConfig()

# 任务存储
_tasks: List[Task] = []

def _generate_mock_tasks():
    """生成模拟任务数据"""
    task_names = [
        "搜索GitHub项目", "填写表单并提交", "抓取商品信息",
        "自动登录测试", "数据导出任务", "网页截图任务",
        "表单自动化测试", "数据采集任务", "自动化脚本执行"
    ]
    statuses = ["completed", "failed", "running", "pending", "cancelled"]
    
    tasks = []
    for i in range(50):
        status = statuses[i % 5]
        start_time = datetime.now() - timedelta(hours=random.randint(1, 72))
        duration = random.randint(10, 300) if status in ["completed", "failed"] else None
        
        task = Task(
            id=str(i + 1),
            name=f"{task_names[i % len(task_names)]} #{i + 1}",
            status=status,
            startTime=start_time.strftime("%Y-%m-%d %H:%M:%S"),
            duration=duration,
            tokenUsed=random.randint(100, 5000) if status != "pending" else None,
            error="执行超时" if status == "failed" else None,
            result="任务执行成功" if status == "completed" else None,
        )
        tasks.append(task)
    return tasks

_tasks = _generate_mock_tasks()

# =============================================================================
# API路由
# =============================================================================

@app.get("/api/statistics", response_model=ApiResponse)
async def get_statistics():
    """获取统计数据"""
    completed = len([t for t in _tasks if t.status == "completed"])
    failed = len([t for t in _tasks if t.status == "failed"])
    running = len([t for t in _tasks if t.status == "running"])
    total_tokens = sum(t.tokenUsed or 0 for t in _tasks)
    
    stats = Statistics(
        totalTasks=len(_tasks),
        completedTasks=completed,
        failedTasks=failed,
        runningTasks=running,
        totalTokens=total_tokens,
        successRate=round(completed / len(_tasks) * 100, 1) if _tasks else 0,
    )
    return ApiResponse(data=stats.model_dump())

@app.get("/api/statistics/token-trend", response_model=ApiResponse)
async def get_token_trend(days: int = 7):
    """获取Token消耗趋势"""
    trends = []
    for i in range(days):
        date = datetime.now() - timedelta(days=days - i - 1)
        trends.append(TokenTrend(
            date=date.strftime("%m-%d"),
            tokens=random.randint(30000, 80000),
        ))
    return ApiResponse(data={"trends": [t.model_dump() for t in trends]})

@app.get("/api/statistics/task-analysis", response_model=ApiResponse)
async def get_task_analysis():
    """获取任务分析数据"""
    completed = len([t for t in _tasks if t.status == "completed"])
    failed = len([t for t in _tasks if t.status == "failed"])
    
    analysis = TaskAnalysis(
        successCount=completed,
        failedCount=failed,
        durationDistribution=[
            DurationDistribution(range="0-30s", count=random.randint(50, 150)),
            DurationDistribution(range="30-60s", count=random.randint(100, 200)),
            DurationDistribution(range="1-5min", count=random.randint(80, 150)),
            DurationDistribution(range="5-10min", count=random.randint(30, 80)),
            DurationDistribution(range=">10min", count=random.randint(5, 30)),
        ],
    )
    return ApiResponse(data=analysis.model_dump())

@app.get("/api/tasks", response_model=ApiResponse)
async def get_tasks(page: int = 1, pageSize: int = 10):
    """获取任务列表"""
    start = (page - 1) * pageSize
    end = start + pageSize
    paginated_tasks = _tasks[start:end]
    
    return ApiResponse(data={
        "list": [t.model_dump() for t in paginated_tasks],
        "total": len(_tasks),
        "page": page,
        "pageSize": pageSize,
    })

@app.get("/api/tasks/{task_id}", response_model=ApiResponse)
async def get_task(task_id: str):
    """获取单个任务详情"""
    task = next((t for t in _tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return ApiResponse(data=task.model_dump())

@app.post("/api/tasks/{task_id}/stop", response_model=ApiResponse)
async def stop_task(task_id: str):
    """停止任务"""
    task = next((t for t in _tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "running":
        raise HTTPException(status_code=400, detail="Task is not running")
    task.status = "cancelled"
    return ApiResponse(message="Task stopped successfully")

# =============================================================================
# 配置API
# =============================================================================

@app.get("/api/config/agent", response_model=ApiResponse)
async def get_agent_config():
    """获取Agent配置"""
    return ApiResponse(data=_agent_config.model_dump())

@app.post("/api/config/agent", response_model=ApiResponse)
async def update_agent_config(config: AgentConfig):
    """更新Agent配置"""
    global _agent_config
    _agent_config = config
    return ApiResponse(message="Agent config updated successfully")

@app.get("/api/config/browser", response_model=ApiResponse)
async def get_browser_config():
    """获取Browser配置"""
    return ApiResponse(data=_browser_config.model_dump())

@app.post("/api/config/browser", response_model=ApiResponse)
async def update_browser_config(config: BrowserConfig):
    """更新Browser配置"""
    global _browser_config
    _browser_config = config
    return ApiResponse(message="Browser config updated successfully")

@app.get("/api/config/llm", response_model=ApiResponse)
async def get_llm_config():
    """获取LLM配置"""
    return ApiResponse(data=_llm_config.model_dump())

@app.post("/api/config/llm", response_model=ApiResponse)
async def update_llm_config(config: LLMConfig):
    """更新LLM配置"""
    global _llm_config
    _llm_config = config
    return ApiResponse(message="LLM config updated successfully")

# =============================================================================
# Agent Run - 任务执行API
# =============================================================================

# Agent运行时状态存储
_agent_runs: Dict[str, Dict[str, Any]] = {}

def _simulate_agent_execution(task_id: str, task: str):
    """模拟Agent执行过程（后台线程）"""
    run_state = _agent_runs.get(task_id)
    if not run_state:
        return

    max_steps = random.randint(5, 15)
    run_state["maxSteps"] = max_steps
    start_time = time.time()

    step_messages = [
        "正在分析任务需求...",
        "正在打开浏览器...",
        "正在导航到目标页面...",
        "正在定位页面元素...",
        "正在执行点击操作...",
        "正在输入文本内容...",
        "正在等待页面加载...",
        "正在提取页面数据...",
        "正在处理搜索结果...",
        "正在截取页面快照...",
        "正在验证操作结果...",
        "正在整理输出内容...",
        "正在生成执行报告...",
        "正在保存执行记录...",
        "正在完成最终检查...",
    ]

    for step in range(1, max_steps + 1):
        # 检查停止/暂停信号
        if run_state["status"] == "stopped":
            run_state["chatHistory"].append({
                "role": "system",
                "content": "任务已被用户停止",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            })
            return

        # 暂停等待
        while run_state["status"] == "paused":
            time.sleep(0.5)
            if run_state["status"] == "stopped":
                return

        run_state["currentStep"] = step
        elapsed = time.time() - start_time
        run_state["totalDuration"] = round(elapsed, 2)
        run_state["avgStepDuration"] = round(elapsed / step, 2)

        # 模拟Token消耗
        prompt_add = random.randint(500, 3000)
        completion_add = random.randint(100, 800)
        run_state["promptTokens"] += prompt_add
        run_state["completionTokens"] += completion_add
        run_state["totalTokens"] = run_state["promptTokens"] + run_state["completionTokens"]

        # 模拟重试
        if random.random() < 0.15:
            retry_type = random.choice(["system", "business"])
            if retry_type == "system":
                run_state["systemRetries"] += 1
            else:
                run_state["businessRetries"] += 1
            run_state["totalRetries"] += 1

        # 添加步骤消息
        msg_idx = (step - 1) % len(step_messages)
        step_content = f"**Step {step}/{max_steps}** - {step_messages[msg_idx]}\n"
        step_content += f"Tokens: +{prompt_add} prompt, +{completion_add} completion"
        run_state["chatHistory"].append({
            "role": "assistant",
            "content": step_content,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        })

        time.sleep(random.uniform(1.5, 3.0))

    # 执行完成
    elapsed = time.time() - start_time
    run_state["totalDuration"] = round(elapsed, 2)
    run_state["status"] = "completed"
    run_state["chatHistory"].append({
        "role": "assistant",
        "content": f"**任务完成**\n\n- 总步数: {max_steps}\n- 总耗时: {run_state['totalDuration']}秒\n- 总Token: {run_state['totalTokens']}\n- 任务: {task}",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })


@app.post("/api/agent/run", response_model=ApiResponse)
async def start_agent_run(req: AgentRunRequest):
    """提交Agent执行任务"""
    task_id = str(uuid.uuid4())[:8]

    run_state: Dict[str, Any] = {
        "taskId": task_id,
        "task": req.task,
        "status": "running",
        "currentStep": 0,
        "maxSteps": 0,
        "totalDuration": 0,
        "avgStepDuration": 0,
        "promptTokens": 0,
        "completionTokens": 0,
        "totalTokens": 0,
        "systemRetries": 0,
        "businessRetries": 0,
        "totalRetries": 0,
        "screenshot": None,
        "chatHistory": [
            {
                "role": "user",
                "content": req.task,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            },
            {
                "role": "assistant",
                "content": "收到任务，正在初始化Agent和浏览器环境...",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            },
        ],
    }
    _agent_runs[task_id] = run_state

    # 启动后台模拟线程
    thread = threading.Thread(
        target=_simulate_agent_execution, args=(task_id, req.task), daemon=True
    )
    thread.start()

    return ApiResponse(data={"taskId": task_id})


@app.get("/api/agent/run/{task_id}/status", response_model=ApiResponse)
async def get_agent_run_status(task_id: str):
    """获取Agent执行状态"""
    run_state = _agent_runs.get(task_id)
    if not run_state:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return ApiResponse(data=run_state)


@app.post("/api/agent/run/{task_id}/stop", response_model=ApiResponse)
async def stop_agent_run(task_id: str):
    """停止Agent执行"""
    run_state = _agent_runs.get(task_id)
    if not run_state:
        raise HTTPException(status_code=404, detail="Agent run not found")
    run_state["status"] = "stopped"
    return ApiResponse(message="Stop signal sent")


@app.post("/api/agent/run/{task_id}/pause", response_model=ApiResponse)
async def pause_agent_run(task_id: str):
    """暂停Agent执行"""
    run_state = _agent_runs.get(task_id)
    if not run_state:
        raise HTTPException(status_code=404, detail="Agent run not found")
    run_state["status"] = "paused"
    return ApiResponse(message="Pause signal sent")


@app.post("/api/agent/run/{task_id}/resume", response_model=ApiResponse)
async def resume_agent_run(task_id: str):
    """恢复Agent执行"""
    run_state = _agent_runs.get(task_id)
    if not run_state:
        raise HTTPException(status_code=404, detail="Agent run not found")
    run_state["status"] = "running"
    return ApiResponse(message="Resume signal sent")


# =============================================================================
# 静态文件服务 (生产环境)
# =============================================================================

# 检查是否存在构建后的前端文件
frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """服务React SPA"""
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
