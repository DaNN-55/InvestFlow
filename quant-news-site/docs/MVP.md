# MVP 规格（初版）

## 目标

在 `quant-news-site` 内实现一个可日常使用的财经资讯聚合与摘要最小版本：

1. 抓取 2-3 个中英文来源（优先 RSS/API）
2. 保存基础字段（标题、链接、来源、时间、语言）
3. 用 LLM API 生成中文摘要
4. 通过网站页面浏览资讯列表
5. 支持手动触发抓取/摘要任务

## 后端接口（MVP）

- `GET /api/news`：资讯列表
- `GET /api/news/{id}`：单篇详情
- `POST /api/jobs/fetch`：手动抓取
- `POST /api/jobs/summarize`：手动摘要
- `GET /api/sources`：查看已配置来源与启用状态
- `GET /api/meta`：查看服务状态与 LLM 配置状态（不返回密钥）

## 数据字段（MVP）

- `id`
- `title`
- `url`
- `source`
- `published_at`
- `language`
- `summary_cn`
- `created_at`

## 备注

- 当前代码骨架中已提供占位接口与 mock 数据
- 后续可从 SQLite 升级到 PostgreSQL
- 摘要失败时应允许降级显示原标题与来源链接
