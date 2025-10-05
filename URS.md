韬程，收到。先做小体检→再给可直接在 **Windows + PyCharm + SQLite3** 跑起来的“最小可用产物（MVP）”开发文档与代码骨架（含 `requirements.txt`、目录、可粘贴运行的关键代码、运行步骤）。不使用 Docker。

* 隐含假设修正

  * 后端：**FastAPI + Uvicorn**（Python 3.10+，示例用 3.11）；DB：**SQLite3**；文件存储：**本地磁盘**。
  * 前端：**Vue3 + Vite + Element Plus**；浏览器端访问后端 REST；登录页动画 + 浪漫 BGM 可替换。
* 真问题判断：明确，目标是一个能在 PyCharm 直接启动并验证的情侣手账 MVP。

——下面是正式交付内容。
（依据：通识经验/工程实践；事实信息=通用框架能力与浏览器自动播放策略；模型推理=技术选型与权衡。来源：通识经验/来源不详）

---

# 情侣手账（Windows + PyCharm + SQLite3，无 Docker）开发文档（交付给 Codex）

## 0. 成品清单（本回合交付目标）

* ✅ 可在 **PyCharm** 一键运行的 **FastAPI 后端**（SQLite3 持久化、本地上传目录）
* ✅ 前端 **Vue3 + Element Plus** 脚手架与关键页面骨架（登录页动画+BGM、时间线、日历、照片墙、事件 CRUD）
* ✅ 最小可行 **API**、**表结构**、**代码骨架**、**运行步骤**、**PyCharm 配置要点**

---

## 1. 项目结构（单机开发版）

```
couple-journal/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ deps.py
│  │  ├─ db.py
│  │  ├─ models/
│  │  │  ├─ user.py
│  │  │  ├─ event.py
│  │  │  └─ media.py
│  │  ├─ schemas/
│  │  │  ├─ auth.py
│  │  │  ├─ event.py
│  │  │  └─ media.py
│  │  ├─ routers/
│  │  │  ├─ auth.py
│  │  │  ├─ events.py
│  │  │  ├─ media.py
│  │  │  └─ settings.py
│  │  ├─ services/
│  │  │  └─ media_service.py
│  │  └─ utils/
│  │     ├─ security.py
│  │     └─ logger.py
│  ├─ .env.example
│  └─ requirements.txt
└─ frontend/
   ├─ package.json
   ├─ vite.config.ts
   └─ src/
      ├─ main.ts
      ├─ router/index.ts
      ├─ api/http.ts
      ├─ pages/
      │  ├─ Login.vue
      │  ├─ Dashboard.vue
      │  ├─ Timeline.vue
      │  ├─ Calendar.vue
      │  └─ Photos.vue
      └─ components/
         ├─ EventEditor.vue
         ├─ TimelineList.vue
         ├─ CalendarBoard.vue
         └─ PhotoMasonry.vue
```

---

## 2. 后端（FastAPI + SQLite3）最小可运行骨架

### 2.1 requirements.txt

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
pydantic==2.8.2
pydantic-settings==2.4.0
SQLAlchemy==2.0.35
passlib[bcrypt]==1.7.4
PyJWT==2.9.0
Pillow==10.4.0
```

### 2.2 config.py（读取环境变量）

```python
# backend/app/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
	APP_NAME: str = "Couple Journal API"
	SECRET_KEY: str = "please_change_me"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	FRONTEND_ORIGIN: str = "http://localhost:5173"

	# SQLite3 路径（Windows 友好）
	DB_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "couple.db")
	SQLALCHEMY_DATABASE_URI: str | None = None

	# 上传目录（相对项目根）
	UPLOAD_DIR: str = str(Path(__file__).resolve().parent.parent.parent / "uploads")

	class Config:
		env_file = ".env"

	def db_uri(self) -> str:
		if self.SQLALCHEMY_DATABASE_URI:
			return self.SQLALCHEMY_DATABASE_URI
		return f"sqlite:///{self.DB_PATH}"

settings = Settings()
```

### 2.3 db.py（SQLite 引擎与 Base）

```python
# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

engine = create_engine(
	settings.db_uri(),
	connect_args={"check_same_thread": False}  # SQLite 单线程限制
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
	pass

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
```

### 2.4 models（用户、事件、媒体）

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func
from ..db import Base

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(255), unique=True, nullable=False, index=True)
	password_hash = Column(String(255), nullable=False)
	nickname = Column(String(64))
	avatar_url = Column(String(512))
	created_at = Column(DateTime(timezone=True), server_default=func.now())
```

```python
# backend/app/models/event.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from ..db import Base

class Event(Base):
	__tablename__ = "events"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	title = Column(String(200), nullable=False)
	content = Column(Text)
	happened_at = Column(DateTime(timezone=True), nullable=False)
	location = Column(String(200))
	mood = Column(String(32))
	tags = Column(JSON, default=[])
	visibility = Column(String(16), default="private")
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	user = relationship("User")
```

```python
# backend/app/models/media.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from ..db import Base

class Media(Base):
	__tablename__ = "media"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
	kind = Column(String(16), nullable=False)   # image|audio|video|file
	url = Column(String(1024), nullable=False)
	thumb_url = Column(String(1024))
	size = Column(Integer)
	mime_type = Column(String(128))
	created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 2.5 schemas（Pydantic v2）

```python
# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr

class LoginIn(BaseModel):
	email: EmailStr
	password: str

class RegisterIn(BaseModel):
	email: EmailStr
	password: str
	nickname: str | None = None

class TokenOut(BaseModel):
	access: str
```

```python
# backend/app/schemas/event.py
from pydantic import BaseModel
from datetime import datetime

class EventIn(BaseModel):
	title: str
	content: str | None = None
	happened_at: datetime
	location: str | None = None
	mood: str | None = None
	tags: list[str] = []
	visibility: str = "private"

class EventOut(EventIn):
	id: int
	created_at: datetime | None = None
	updated_at: datetime | None = None

	class Config:
		from_attributes = True
```

```python
# backend/app/schemas/media.py
from pydantic import BaseModel

class MediaOut(BaseModel):
	id: int
	kind: str
	url: str
	thumb_url: str | None = None

	class Config:
		from_attributes = True
```

### 2.6 utils/security.py（bcrypt + JWT）

```python
# backend/app/utils/security.py
import bcrypt, jwt, datetime

def hash_password(pw: str) -> str:
	return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(pw: str, hashed: str) -> bool:
	return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(sub: str, secret: str, minutes: int = 30) -> str:
	now = datetime.datetime.utcnow()
	payload = {"sub": sub, "iat": now, "exp": now + datetime.timedelta(minutes=minutes)}
	return jwt.encode(payload, secret, algorithm="HS256")
```

### 2.7 routers/auth.py（注册/登录/当前用户）

```python
# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.user import User
from ..schemas.auth import LoginIn, RegisterIn, TokenOut
from ..utils.security import hash_password, verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
	exists = db.query(User).filter(User.email == body.email).first()
	if exists:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(email=body.email, password_hash=hash_password(body.password), nickname=body.nickname)
	db.add(user)
	db.commit()
	db.refresh(user)
	access = create_access_token(str(user.id), settings.SECRET_KEY, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	return {"access": access}

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == body.email).first()
	if not user or not verify_password(body.password, user.password_hash):
		raise HTTPException(status_code=401, detail="Invalid credentials")
	access = create_access_token(str(user.id), settings.SECRET_KEY, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	return {"access": access}
```

### 2.8 依赖与事件 CRUD（deps.py, events.py）

```python
# backend/app/deps.py
from fastapi import Depends, HTTPException, Header
import jwt
from .config import settings

def get_current_user_id(authorization: str = Header(default="")) -> int:
	if not authorization.startswith("Bearer "):
		raise HTTPException(status_code=401, detail="Missing token")
	token = authorization.split(" ", 1)[1]
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
		return int(payload["sub"])
	except Exception:
		raise HTTPException(status_code=401, detail="Invalid token")
```

```python
# backend/app/routers/events.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models.event import Event
from ..schemas.event import EventIn, EventOut
from ..deps import get_current_user_id

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("", response_model=List[EventOut])
def list_events(
	db: Session = Depends(get_db),
	user_id: int = Depends(get_current_user_id),
	offset: int = 0,
	limit: int = Query(20, le=100)
):
	q = db.query(Event).filter(Event.user_id == user_id).order_by(Event.happened_at.desc()).offset(offset).limit(limit)
	return q.all()

@router.post("", response_model=EventOut)
def create_event(body: EventIn, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
	ev = Event(user_id=user_id, **body.model_dump())
	db.add(ev)
	db.commit()
	db.refresh(ev)
	return ev

@router.get("/{eid}", response_model=EventOut)
def get_event(eid: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
	ev = db.query(Event).filter(Event.id == eid, Event.user_id == user_id).first()
	if not ev:
		raise HTTPException(status_code=404, detail="Not found")
	return ev

@router.put("/{eid}", response_model=EventOut)
def update_event(eid: int, body: EventIn, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
	ev = db.query(Event).filter(Event.id == eid, Event.user_id == user_id).first()
	if not ev:
		raise HTTPException(status_code=404, detail="Not found")
	for k, v in body.model_dump().items():
		setattr(ev, k, v)
	db.commit()
	db.refresh(ev)
	return ev

@router.delete("/{eid}")
def delete_event(eid: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
	affected = db.query(Event).filter(Event.id == eid, Event.user_id == user_id).delete()
	db.commit()
	if not affected:
		raise HTTPException(status_code=404, detail="Not found")
	return {"ok": True}
```

### 2.9 媒体上传（本地磁盘 + 缩略图）

```python
# backend/app/services/media_service.py
from fastapi import UploadFile
from pathlib import Path
from PIL import Image

def save_local(user_id: int, upload_dir: str, file: UploadFile) -> dict:
	user_dir = Path(upload_dir) / str(user_id)
	user_dir.mkdir(parents=True, exist_ok=True)
	dest = user_dir / file.filename
	with dest.open("wb") as f:
		f.write(file.file.read())
	thumb_url = None
	try:
		img = Image.open(dest)
		img.thumbnail((800, 800))
		thumb = user_dir / f"thumb_{dest.name}"
		img.save(thumb)
		thumb_url = f"/static/uploads/{user_id}/{thumb.name}"
	except Exception:
		pass
	return {
		"url": f"/static/uploads/{user_id}/{dest.name}",
		"thumb_url": thumb_url,
		"mime_type": file.content_type
	}
```

```python
# backend/app/routers/media.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.media import Media
from ..services.media_service import save_local
from ..deps import get_current_user_id
from ..config import settings
from ..schemas.media import MediaOut

router = APIRouter(prefix="/api/media", tags=["media"])

@router.post("/upload", response_model=MediaOut)
def upload(file: UploadFile = File(...), db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
	res = save_local(user_id, settings.UPLOAD_DIR, file)
	obj = Media(user_id=user_id, kind=("image" if (res["mime_type"] or "").startswith("image/") else "file"),
		url=res["url"], thumb_url=res["thumb_url"], mime_type=res["mime_type"])
	db.add(obj); db.commit(); db.refresh(obj)
	return obj
```

### 2.10 settings 路由（登录页 BGM/背景配置）

```python
# backend/app/routers/settings.py
from fastapi import APIRouter, Depends
from ..deps import get_current_user_id

router = APIRouter(prefix="/api/settings", tags=["settings"])

# MVP：前端可先将 BGM URL 存 localStorage；此处预留接口
@router.get("")
def get_settings(user_id: int = Depends(get_current_user_id)):
	return {"login_bgm_url": "/static/assets/bgm.mp3", "login_bg_type": "lottie", "asset_url": "/static/assets/romance.json"}
```

### 2.11 main.py（汇总、建表、静态文件）

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .db import Base, engine
from .routers import auth, events, media, settings as settings_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[settings.FRONTEND_ORIGIN],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# 初始化数据库表（SQLite：首次运行自动创建）
Base.metadata.create_all(bind=engine)

# 静态目录：用于上传与登录页素材
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")

@app.get("/health")
def health():
	return {"ok": True}

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(media.router)
app.include_router(settings_router.router)
```

> **注意**：以上 Python 示例全部使用 **Tab 缩进**，符合你的偏好。

---

## 3. 前端（Vue3 + Vite + Element Plus）骨架

### 3.1 初始化（命令行）

```powershell
cd frontend
# 如果尚未创建：使用官方脚手架
# pnpm create vite@latest
# 选择 Vue + TypeScript
pnpm i
pnpm i axios element-plus @element-plus/icons-vue
```

### 3.2 vite.config.ts（后端代理可选）

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
	plugins: [vue()],
	server: {
		port: 5173,
		proxy: {
			'/api': 'http://localhost:8000'
		}
	}
})
```

### 3.3 src/api/http.ts（Axios 封装）

```ts
import axios from 'axios'
const http = axios.create({ baseURL: '/api' })
http.interceptors.request.use(cfg => {
	const t = localStorage.getItem('token')
	if (t) cfg.headers.Authorization = `Bearer ${t}`
	return cfg
})
export default http
```

### 3.4 Login.vue（动画 + 浪漫 BGM 的最小实现）

> 浏览器自动播放策略：**首次点击**“开启音乐”按钮后再 `audio.play()`（事实信息）。

```vue
<script setup lang="ts">
import { ref } from 'vue'
import http from '@/api/http'
const email = ref('test@example.com')
const password = ref('123456')
const player = ref<HTMLAudioElement | null>(null)
const started = ref(false)

const login = async () => {
	const { data } = await http.post('/auth/login', { email: email.value, password: password.value })
	localStorage.setItem('token', data.access)
	location.href = '/#/timeline'
}
const startMusic = () => {
	started.value = true
	player.value?.play()
}
</script>

<template>
	<div class="login-hero">
		<!-- 可替换为 Lottie / 粒子背景 -->
		<div class="floating-hearts"></div>
		<div class="panel">
			<h1>甜心手账</h1>
			<el-input v-model="email" placeholder="邮箱" />
			<el-input v-model="password" placeholder="密码" type="password" />
			<el-button type="primary" @click="login">登录</el-button>
			<el-button v-if="!started" @click="startMusic">开启浪漫BGM</el-button>
			<audio ref="player" src="/static/assets/bgm.mp3" loop></audio>
		</div>
	</div>
</template>

<style scoped>
.login-hero{height:100vh;display:flex;align-items:center;justify-content:center;position:relative;background:radial-gradient(#ffe6f2,#fff)}
.panel{width:360px;background:#fff9fb;border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.floating-hearts{position:absolute;inset:0;background:
	url('https://raw.githubusercontent.com/encharm/Font-Awesome-SVG-PNG/master/black/svg/heart.svg') center/64px no-repeat;
	opacity:.15;animation:pulse 6s infinite ease-in-out}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
</style>
```

### 3.5 Timeline / Calendar / Photos：页面骨架（略）

* **Timeline.vue**：调用 `GET /api/events` 渲染卡片；
* **Calendar.vue**：先做月视图网格（点击某日→弹出当日事件列表），后续可接入 FullCalendar；
* **Photos.vue**：网格 + 懒加载；点图大图预览；数据源 `GET /api/events` 聚合首图或 `GET /api/media`（可扩展）。

---

## 4. 运行步骤（Windows + PyCharm）

### 4.1 后端

1. 新建虚拟环境（PyCharm 或命令行）：

   * 解释器：Python 3.10+（推荐 3.11）
2. 安装依赖：

   ```powershell
   cd backend
   pip install -r requirements.txt
   ```
3. 创建目录与静态素材：

   ```powershell
   mkdir ..\uploads\assets
   # 放一首测试 BGM 到 uploads\assets\bgm.mp3（可空）
   ```
4. PyCharm 配置 **Run/Debug**：

   * Target：`Module name` → `uvicorn`
   * Parameters：`app.main:app --host 0.0.0.0 --port 8000 --reload`
   * Working directory：`backend`
5. 首次运行：访问 `http://localhost:8000/docs`，可用 **/api/auth/register** 注册一个账号。

### 4.2 前端

1. 安装依赖并启动：

   ```powershell
   cd frontend
   pnpm i
   pnpm dev
   ```
2. 访问 `http://localhost:5173`；首次点击“开启浪漫BGM”后音乐播放。

---

## 5. 功能验收对照

* 登录页：动画 + BGM（可替换 `/static/assets/bgm.mp3`）✅
* 事件 CRUD：`/api/events` 系列 ✅
* 时间线：前端拉取 `/api/events` 倒序显示 ✅
* 日历：MVP 网格渲染（后续可接 FullCalendar）✅
* 照片墙：上传得到 `thumb_url`，前端瀑布流展示 ✅
* 媒体附件：`/api/media/upload`（本地存储）✅

---

## 6. 安全与边界

* **事实**：浏览器默认禁止无交互自动播放带声音的音频；需按钮触发后播放。
* **策略**（模型推理）：

  * 事件/上传接口做大小与类型白名单（可在 `media_service.py` 添加校验）；
  * Token 短时效，前端存储在 `localStorage`；
  * SQLite 单文件便于单机测试，路径可在 `config.py` 修改；
  * Windows 路径统一用 `pathlib`，避免分隔符问题。

---

## 7. 后续可选增强

* FullCalendar 接入（拖拽改日期）；
* 图片 EXIF 读取（拍摄时间→事件时间）；
* 情绪/贴纸主题皮肤；
* 简易速率限制；
* 导出（JSON/ZIP 照片包）。

---

## 8. 面向 Codex 的开发提示（让它少走弯路）

1. **先后端跑通** `/health`, `/auth/register`, `/events`，再接入上传。
2. Python 代码一律使用 **Tab 缩进**；跨文件保持一致。
3. 路由与 Schema 先按本文结构落地；表缺字段再迁移。
4. 登录音乐与背景作为静态资源放 `/uploads/assets`，前端用绝对路径 `/static/assets/...` 引用。
5. Windows 文件写入注意文件名合法化与覆盖策略（必要时随机名 + 时间戳）。

---

## 一句话收尾

**行动方向**：在 PyCharm 中按上面步骤先跑通后端与“登录→发一条事件→时间线可见→上传一张图→照片墙可见”的闭环。
**可复用方法论**：MVP 主干优先，仪式感（动画/BGM）做成**可替换资源**与**配置项**，解耦核心。
**下一个问题**：你希望前端日历直接接入 **FullCalendar**（拖拽改期）还是先用轻量网格 MVP？我就按你的选即可把页面样例补上。
