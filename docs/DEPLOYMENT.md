# 正式部署驗證

- 網址：https://qianzai-odyssey.hk6429.workers.dev/
- 日期：2026-10-04
- Cloudflare 版本：fb56060d-d555-4863-a36d-91928bf8ec12
- 發布前 12 項測試全部通過。
- 13 個公開資源 HTTP 200、SHA-256 與本機成品相符，nosniff 正常，MIME 已記錄。_headers 由平台解析，不作公開檔案。
- .env、原始資料、建置腳本與 _headers 皆回傳 404。第一次無自訂 User-Agent 的排除路徑請求曾回傳 403；改以明確驗證標頭取得上列結果。
- 正式站獨立 ?test 存檔完成三題：刻意答錯、關閉、重新載入、保留錯題回饋、重新回答、入帳 3 題／30 XP。
- 窄螢幕檢查宋朝試讀；實際 innerWidth 355、scrollWidth 341，沒有水平溢出。暫時尺寸覆寫已清除。
- 瀏覽器警告與錯誤紀錄為空。
- 已另開無 ?test 的首頁並保留分頁，正式使用者進度顯示 0 題。
- 證據：production-readback.json、screenshots/production-home.png、screenshots/production-mobile.png。
