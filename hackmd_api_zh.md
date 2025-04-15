# HackMD API 使用指南

## API 驗證

### Bearer 身份驗證
Bearer 身份驗證（又稱令牌驗證）是一種 HTTP 驗證方案，使用稱為 Bearer 令牌的安全令牌。"Bearer 身份驗證"可以理解為"授予此令牌持有者訪問權限"。Bearer 令牌是一個加密字符串，通常由服務器響應登錄請求而生成。客戶端在請求受保護資源時，必須在 Authorization 標頭中發送此令牌：

```
Header: Authorization: Bearer <token>
```

`<token>` 可以在您的設置中創建，請參閱"如何發行 API 令牌"。

### 響應標頭

```
X-HackMD-API-Version: 1.0.0
```

### 測試驗證
獲取訪問令牌後，您可以請求"Me API 端點" https://api.hackmd.io/v1/me 來測試身份驗證是否有效：

```bash
curl "https://api.hackmd.io/v1/me" -H "Authorization: Bearer <token>"
```

## 用戶信息

### 獲取用戶信息
`GET /me`

**成功響應**
- 狀態碼: 200
- 返回體:
```json
{
    "id": "00c437e8-9d79-4200-997f-8e9384415a76",
    "name": "James",
    "email": null,
    "userPath": "AMQ36J15QgCZf46ThEFadg",
    "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
    "teams": [
        {
            "id": "e9ed1dcd-830f-435c-9fe2-d53d5f191666",
            "ownerId": "00c437e8-9d79-4200-997f-8e9384415a76",
            "path": "CAT",
            "name": "API client testing team",
            "logo": "data:image/svg+xml;base64,...",
            "description": "This is for testing client API",
            "visibility": "public",
            "createdAt": 1644371278721
        }
    ]
}
```

## 用戶筆記 API

### 獲取用戶工作區中的筆記列表
`GET /notes`

**成功響應**
- 狀態碼: 200
- 返回體:
```json
[
   {
      "id": "ehgwc6a8RXSmcSaRwIQ2jw",
      "title": "Personal note title",
      "tags": ["personal", "test"],
      "createdAt": 1643270371245,
      "publishType": "view",
      "publishedAt": null,
      "permalink": null,
      "shortId": "SysJb0yAY",
      "lastChangedAt": 1643270452413,
      "lastChangeUser": {
          "name": "James",
          "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
          "biography": null,
          "userPath": "AMQ36J15QgCZf46ThEFadg"
      },
      "userPath": "AMQ36J15QgCZf46ThEFadg",
      "teamPath": null,
      "readPermission": "guest",
      "writePermission": "signed_in",
      "publishLink": "https://hackmd.io/@username/permalink"
    }
 ]
```

### 獲取單個筆記
`GET /notes/:noteId`

**URL 參數**:
- noteId: string

**成功響應**
- 狀態碼: 200
- 返回體:
```json
{
    "id": "ehgwc6a8RXSmcSaRwIQ2jw",
    "title": "Personal note title",
    "tags": [
        "Personal",
        "test"
    ],
    "createdAt": 1643270371245,
    "publishType": "view",
    "publishedAt": null,
    "permalink": null,
    "shortId": "SysJb0yAY",
    "content": "# Personal note title\n###### tags: `Personal` `test`",
    "lastChangedAt": 1644461594806,
    "lastChangeUser": {
        "name": "James",
        "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
        "biography": null,
        "userPath": "AMQ36J15QgCZf46ThEFadg"
    },
    "userPath": "AMQ36J15QgCZf46ThEFadg",
    "teamPath": null,
    "readPermission": "guest",
    "writePermission": "signed_in",
    "publishLink": "https://hackmd.io/@username/permalink"                
}
```

### 創建筆記
`POST /notes`

**數據參數**
- 主體 (可選) [application/json]

```json
{
    "title": "New note",
    "content": "",
    "readPermission": "owner",
    "writePermission": "owner",
    "commentPermission": "everyone"
}
```

| 字段 | 類型 | 值 |
|------|------|-----|
| title | string | |
| content | string | |
| readPermission | string | owner, signed_in, guest |
| writePermission | string | owner, signed_in, guest |
| commentPermission | string | disabled, forbidden, owners, signed_in_users, everyone |
| permalink | string | |

**成功響應**
- 狀態碼: 201
- 返回體:
```json
{
   "id": "ppZ6pJ9iRFa7RHHUegcLiQ",
   "title": "New note",
   "tags": null,
   "createdAt": 1644461842833,
   "publishType": "view",
   "publishedAt": null,
   "permalink": null,
   "shortId": "HyiMJWMk9",
   "content": "test",
   "lastChangedAt": 1644461842832,
   "lastChangeUser": {
       "name": "James",
       "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
       "biography": null,
       "userPath": "AMQ36J15QgCZf46ThEFadg"
   },
   "userPath": "AMQ36J15QgCZf46ThEFadg",
   "teamPath": null,
   "readPermission": "owner",
   "writePermission": "owner",
   "publishLink": "https://hackmd.io/@username/permalink"                    
}
```

**關於標題字段的注意事項**
目前，筆記的標題是從內容中派生的，因此"title"字段的行為可能需要進一步解釋。

1. 如果在"content"字段中有 H1 標題，則將其用作要創建筆記的標題。
2. 如果在"content"字段中沒有 H1 標題，但在 YAML 元數據部分中分配了標題（---\ntitle: abc\n---），則它將成為筆記的標題。
3. 如果未包含"content"字段，則尋找"title"字段，或者在該字段不存在時創建標題為"Untitled"的筆記。

**關於權限字段的注意事項**
- 創建或更新筆記權限時，必須同時提供 readPermission 和 writePermission 字段。
- writePermission 必須比 readPermission 字段更嚴格。例如，對於 signed_in 用戶可讀的筆記，您可以設置 owner 或 signed_in 可寫權限，但不能為該筆記設置 guest 可寫權限。

### 更新筆記
`PATCH /notes/:noteId`

**URL 參數**:
- noteId: string

**數據參數**:
- 主體 (可選) [application/json]
```json
{
  "content": "# Updated personal note",
  "readPermission": "signed_in",
  "writePermission": "owner",
  "permalink": "note-permalink"
}
```

| 字段 | 類型 | 值 |
|------|------|-----|
| content | string | |
| readPermission | string | owner, signed_in, guest |
| writePermission | string | owner, signed_in, guest |
| permalink | string | |

**成功響應**
- 狀態碼: 202
- 返回體: Accepted

### 刪除筆記
`DELETE /notes/:noteId`

**URL 參數**:
- noteId: string

**成功響應**
- 狀態碼: 204

### 獲取已讀筆記的歷史記錄
`GET /history`

**成功響應**
- 狀態碼: 200
- 返回體:
```json
[
  {
    "id": "0jJVr2b3T2eSkBnMib-inA",
    "title": "Team notes",
    "tags": [],
    "createdAt": 1644371283239,
    "publishType": "view",
    "publishedAt": 1644371283239,
    "permalink": null,
    "shortId": "SysUa9xJc",
    "lastChangedAt": 1644461300662,
    "lastChangeUser": {
        "name": "James",
        "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
        "biography": null,
        "userPath": "AMQ36J15QgCZf46ThEFadg"
    },
    "userPath": null,
    "teamPath": "CAT",
    "readPermission": "guest",
    "writePermission": "signed_in",
    "publishLink": "https://hackmd.io/@username/permalink"                  
},
{
    "id": "QpS6V2TCSbeKmNIS1LOrNQ",
    "title": "Untitled",
    "tags": null,
    "createdAt": 1644393142405,
    "publishType": "view",
    "publishedAt": null,
    "permalink": null,
    "shortId": "HJAnGgZyq",
    "lastChangedAt": 1644393142403,
    "lastChangeUser": {
        "name": "Ming-Hsiu Tsai",
        "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
        "biography": null,
        "userPath": "AMQ36J15QgCZf46ThEFadg"
    },
    "userPath": "AMQ36J15QgCZf46ThEFadg",
    "teamPath": null,
    "readPermission": "owner",
    "writePermission": "owner",
    "publishLink": "https://hackmd.io/@username/permalink"                
  }
]
```

### 上傳附件到筆記（即將推出）
`POST /notes/:noteId/upload`
- file: xxx

## 團隊 API

### 獲取用戶有權限的團隊列表
`GET /teams`

**成功響應**
- 狀態碼: 200
- 返回體:
```json
[
  {
    "id": "e9ed1dcd-830f-435c-9fe2-d53d5f191666",
    "ownerId": "00c437e8-9d79-4200-997f-8e9384415a76",
    "path": "CAT",
    "name": "API client testing team",
    "logo": "data:image/svg+xml;base64,...",
    "description": "This is for testing client API",
    "visibility": "public",
    "createdAt": "2022-02-09T01:47:58.721Z"
  }
]
```

## 團隊筆記 API

### 獲取團隊工作區中的筆記列表
`GET /teams/:teamPath/notes`

**URL 參數**
- teamPath: string

**成功響應**
- 狀態碼: 200
- 返回體:
```json
[
  {
    "id": "0jJVr2b3T2eSkBnMib-inA",
    "title": "Team notes",
    "tags": [],
    "createdAt": 1644371283239,
    "publishType": "view",
    "publishedAt": 1644371283239,
    "permalink": null,
    "shortId": "SysUa9xJc",
    "lastChangedAt": 1644461300662,
    "lastChangeUser": null,
    "userPath": null,
    "teamPath": "CAT",
    "readPermission": "guest",
    "writePermission": "signed_in",
    "publishLink": "https://hackmd.io/@username/permalink"                
  }
]
```

請使用"獲取單個筆記" `GET /notes/:noteId` 的 API 來檢索筆記內容。

### 在團隊工作區中創建筆記
`POST /teams/:teamPath/notes`

**URL 參數**
- teamPath: string

**數據參數**
- 主體 (可選)[application/json]
```json
{
    "title": "New note",
    "content": "",
    "readPermission": "owner",
    "writePermission": "owner",
    "commentPermission": "everyone"
}
```

| 字段 | 類型 | 值 |
|------|------|-----|
| title | string | |
| content | string | |
| readPermission | string | owner, sign_in, guest |
| writePermission | string | owner, sign_in, guest |
| commentPermission | string | disabled, forbidden, owners, signed_in_users, everyone |
| permalink | string | |

**成功響應**
- 狀態碼: 201
- 返回體:
```json
{
    "id": "CNf4ZHB-RW-U-ZpR2LRiYA",
    "title": "New team note",
    "tags": null,
    "createdAt": 1644462537700,
    "publishType": "view",
    "publishedAt": null,
    "permalink": null,
    "shortId": "r1GCZbzy9",
    "lastChangedAt": 1644462537700,
    "lastChangeUser": {
        "name": "Ming-Hsiu Tsai",
        "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
        "biography": null,
        "userPath": "AMQ36J15QgCZf46ThEFadg"
    },
    "userPath": null,
    "teamPath": "CAT",
    "readPermission": "owner",
    "writePermission": "owner",
    "publishLink": "https://hackmd.io/@username/permalink"
}
```

### 更新團隊工作區中的筆記
`PATCH /teams/:teamPath/notes/:noteId`

**URL 參數**:
- teamPath: string
- noteId: string

**數據參數**:
- 主體 (可選) [application/json]
```json
{
  "content": "# Updated a team note",
  "readPermission": "signed_in",
  "permalink": "note-permalink"
}
```

| 字段 | 類型 | 值 |
|------|------|-----|
| content | string | |
| readPermission | string | owner, signed_in, guest |
| writePermission | string | owner, signed_in, guest |
| permalink | string | |

**成功響應**
- 狀態碼: 202
- 返回體: Accepted

### 刪除團隊工作區中的筆記
`DELETE /teams/:teamPath/notes/:noteId`

**URL 參數**:
- teamPath: string
- noteId: string

**成功響應**
- 狀態碼: 204

## 附件 API

### 上傳圖片到筆記
即將推出

### 下載附件
`GET https://hackmd.io/_uploads/:filename`

**URL 參數**:
- filename: string

**授權**:
使用授權標頭

**成功響應**
觸發下載

**示例用法**
```bash
# -L 選項開啟跟隨重定向
curl -H "Authorization: Bearer TOKEN" https://hackmd.io/_uploads/By9HvYLR6.png -L > output.png
```

**注意**
- 在 REST 客戶端中開啟"跟隨重定向"選項。
- 您必須使用 hackmd.io 域名而不是常規 API 中的 api.hackmd.io 域名。
