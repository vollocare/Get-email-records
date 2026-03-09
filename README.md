# Get Email Records

CLI 工具，從 Supabase 查詢 `email_records` 表的信件記錄。支援時間篩選、類型篩選、關鍵字搜尋，輸出 JSON（AI 友好）或表格格式。

## 安裝

需要 [uv](https://docs.astral.sh/uv/) 套件管理工具。

```bash
# 安裝依賴
uv sync
```

## 設定

複製 `.env.example` 為 `.env`，填入你的 Supabase 連線資訊：

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_publishable_key
```

也可以透過 CLI 參數 `--supabase-url` 和 `--supabase-key` 傳入。

## 使用方式

```bash
uv run get-email-records [OPTIONS]
```

### 時間篩選（互斥）

| 參數 | 說明 |
|------|------|
| `--period {1h,4h,12h,24h,7d}` | 預設時間區間 |
| `--from DATETIME` | 自訂起始時間（ISO 8601 格式） |
| `--to DATETIME` | 自訂結束時間（預設：現在） |

未指定時間參數時，預設查詢最近 24 小時。

### 內容篩選

| 參數 | 說明 |
|------|------|
| `--type TYPE` | 依 `mail_type` 精確篩選 |
| `--keyword TEXT` | 搜尋 `subject` 和 `content_summary`（伺服器端模糊比對） |

### 輸出控制

| 參數 | 說明 |
|------|------|
| `--format {json,table}` | 輸出格式（預設：json） |
| `--limit N` | 最大筆數（預設：100） |

## 範例

```bash
# 查詢最近 24 小時的所有信件（預設）
uv run get-email-records

# 查詢最近 7 天的信件
uv run get-email-records --period 7d

# 篩選特定類型
uv run get-email-records --period 24h --type "橘News"

# 關鍵字搜尋，表格輸出
uv run get-email-records --keyword "測試" --format table

# 自訂時間範圍
uv run get-email-records --from 2026-03-01T00:00:00 --to 2026-03-09T00:00:00

# 限制回傳筆數
uv run get-email-records --period 7d --limit 10
```

## JSON 輸出結構

```json
{
  "query": {
    "period": "24h",
    "type": null,
    "keyword": null,
    "from": "2026-03-08T15:00:00+00:00",
    "to": "2026-03-09T15:00:00+00:00"
  },
  "count": 3,
  "records": [...]
}
```
