# Get Email Records

CLI 工具，從 Supabase 查詢 `email_records` 表的信件記錄。支援時間篩選、類型篩選、關鍵字搜尋，輸出 JSON（AI 友好）或表格格式。

## 安裝

需要 [uv](https://docs.astral.sh/uv/) 套件管理工具。

### 方式一：全域安裝（推薦）

安裝為全域指令，可在任何目錄直接執行：

```bash
uv tool install git+https://github.com/vollocare/Get-email-records.git
```

更新版本：

```bash
uv tool upgrade get-email-records
```

移除：

```bash
uv tool uninstall get-email-records
```

### 方式二：本地開發

```bash
git clone https://github.com/vollocare/Get-email-records.git
cd Get-email-records
uv sync
# 使用 uv run 執行
uv run get-email-records [OPTIONS]
```

## 設定

Supabase 連線資訊可透過以下三種方式提供（依優先順序）：

### 1. CLI 參數

```bash
get-email-records --supabase-url "https://xxx.supabase.co" --supabase-key "your_key" --period 24h
```

### 2. 環境變數

```bash
export SUPABASE_URL=https://your-project-id.supabase.co
export SUPABASE_KEY=your_publishable_key
```

可加入 `~/.zshrc` 或 `~/.bashrc` 使其永久生效：

```bash
echo 'export SUPABASE_URL=https://your-project-id.supabase.co' >> ~/.zshrc
echo 'export SUPABASE_KEY=your_publishable_key' >> ~/.zshrc
source ~/.zshrc
```

### 3. 本地開發用 `.env`（僅限方式二）

```bash
cp .env.example .env
# 編輯 .env 填入連線資訊
```

> 注意：全域安裝模式不會讀取 `.env` 檔案，請使用環境變數或 CLI 參數。

## 使用方式

```bash
# 全域安裝後
get-email-records [OPTIONS]

# 或本地開發
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
| `--list-types` | 列出資料庫中所有不重複的 `mail_type` 值 |

### 輸出控制

| 參數 | 說明 |
|------|------|
| `--format {json,table}` | 輸出格式（預設：json） |
| `--limit N` | 最大筆數（預設：100） |

## 範例

```bash
# 查詢最近 24 小時的所有信件（預設）
get-email-records

# 查詢最近 7 天的信件
get-email-records --period 7d

# 篩選特定類型
get-email-records --period 24h --type "橘News"

# 關鍵字搜尋，表格輸出
get-email-records --keyword "測試" --format table

# 自訂時間範圍
get-email-records --from 2026-03-01T00:00:00 --to 2026-03-09T00:00:00

# 限制回傳筆數
get-email-records --period 7d --limit 10

# 列出所有信件類型
get-email-records --list-types
```

## AI Skill

本專案支援 [Skills](https://skills.sh/) 生態系，可讓 AI 助手自動學會使用此 CLI。

### 安裝 Skill

```bash
npx skills add vollocare/Get-email-records
```

安裝後，AI 助手會自動知道如何查詢信件記錄。

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
