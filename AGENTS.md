# Repository Guidelines

## 项目结构与模块组织

本仓库是个人投资学习工作区，当前主要项目为：

- `quant-news-site/`：主应用（FastAPI 后端 + 静态前端）
- `learning/`：本地学习资料（如 `investment.ipynb`、CSV 示例）

`quant-news-site/` 目录说明：

- `backend/app/`：API、数据模型、存储、RSS 抓取与摘要服务
- `frontend/`：静态页面（`index.html`）
- `scripts/`：手动任务脚本（`fetch_news.py`、`summarize_news.py`）
- `data/`：本地 JSON 数据与自定义源配置（大多不提交）
- `docs/`：项目说明与配置文档

## 构建、测试与开发命令

除特别说明外，在 `quant-news-site/` 下执行。

- `cd backend; python -m venv .venv; .venv\\Scripts\\Activate.ps1; pip install -r requirements.txt`：首次初始化后端环境
- `cd backend; uvicorn app.main:app --reload`：启动本地 API（`http://127.0.0.1:8000`）
- `python .\\scripts\\fetch_news.py`：抓取 RSS 新闻并写入 `data/news.json`
- `python .\\scripts\\summarize_news.py`：生成或更新新闻摘要
- `.\start.ps1` 或 `start.bat`：Windows 一键启动（打开浏览器并运行后端）

## 代码风格与命名规范

- Python 遵循 PEP 8：4 空格缩进，函数/变量/模块使用 `snake_case`。
- 优先添加类型标注（当前后端代码已大量使用）。
- Pydantic 模型/响应模型使用 `PascalCase`，常量使用 `UPPER_SNAKE_CASE`。
- 路由处理函数保持简短；业务逻辑放入 `backend/app/services/`。
- 当前未配置格式化或 Lint 工具；请保持导入分组清晰、代码可读，不提交 `.venv/` 或生成数据文件。

## 测试指南

目前暂无自动化测试。修改后至少进行以下手动验证：

- `GET /health`
- `GET /api/meta`
- `POST /api/jobs/fetch`
- `POST /api/jobs/summarize`

如新增测试，建议放在 `quant-news-site/backend/tests/`，文件命名使用 `test_*.py`。

## 提交与合并请求规范

当前 Git 历史以简短、祈使式提交信息为主（可使用中文）。建议保持一致，例如：

- `backend: 修复摘要数量限制`
- `docs: 更新启动说明`

PR 应包含：

- 变更范围与目的说明
- 受影响路径（如 `backend/app/services/jobs.py`）
- 配置/依赖变更（如 `.env.example`、`requirements.txt`）
- 前端改动截图，或后端接口调用示例
