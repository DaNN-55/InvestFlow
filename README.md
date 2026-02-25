# Investment Workspace

个人学习与信息收集工作区。

## 目录说明

- `1-investment.ipynb`：学习笔记（Jupyter）
- `etf.csv`：示例数据文件
- `quant-news-site/`：个人资讯阅读台（财经资讯抓取 + 摘要 + 浏览）

## 个人资讯阅读台（`quant-news-site`）

这是一个本地运行的网页应用，用于：

- 抓取中英文资讯来源（RSS）
- 生成中文摘要（通过千问 API）
- 在浏览器中筛选、搜索、浏览资讯
- 自定义订阅来源

## 首次准备（只需一次）

### 1. 创建虚拟环境并安装依赖

```powershell
cd d:\Programs\Investment\quant-news-site\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt --proxy=""
```

### 2. 配置千问 API（在 `quant-news-site/.env`）

参考 `quant-news-site/.env` ：

```env
LLM_API_KEY=你的千问API_Key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
LLM_TIMEOUT_SECONDS=30
```

建议加入性能参数（可选）：

```env
FETCH_MAX_ITEMS_PER_SOURCE=10
FETCH_MAX_TOTAL_ITEMS_PER_RUN=50
SUMMARIZE_MAX_ITEMS_PER_RUN=20
FETCH_HTTP_TIMEOUT_SECONDS=12
FETCH_ARTICLE_BODY=1
```

## 日常使用（推荐）

### 一键启动

双击运行：

- `quant-news-site/start.bat`

它会自动：

- 启动后端服务（FastAPI）
- 打开浏览器到 `http://127.0.0.1:8000/`

### 网页中操作顺序

1. 点击 `抓取资讯`
2. 点击 `生成摘要`
3. 点击 `刷新列表`

## 常用说明

### 控制速度（页面左侧）

- `抓取总上限`：建议 `10~20`
- `摘要上限`：建议 `5~10`

这样可以明显减少单次等待时间。

### 添加自定义来源

在左侧 `订阅来源（自定义）` 中填写：

- 来源名称
- RSS 地址
- 语言（中文/英文）
- 是否启用
- 是否抓取正文（更全但更慢）

保存后再执行 `抓取资讯`。

## 如果一键启动失败（手动方式）

```powershell
cd d:\Programs\Investment\quant-news-site\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

然后在浏览器打开：

- `http://127.0.0.1:8000/`

## 常见问题

### 页面提示“连接失败”

- 确认后端终端仍在运行
- 访问 `http://127.0.0.1:8000/health` 检查是否返回 `{"status":"ok"}`

### 英文内容显示“中文翻译未完成”

- 说明 LLM 未配置成功或调用失败
- 检查 `quant-news-site/.env` 中的千问配置
- 修改后重启后端，再执行 `生成摘要`
