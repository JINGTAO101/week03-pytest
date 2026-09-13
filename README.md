# week03-pytest

[![ci](https://github.com/JINGTAO101/week03-pytest/actions/workflows/ci.yml/badge.svg)](https://github.com/JINGTAO101/week03-pytest/actions/workflows/ci.yml)

pytest 接口练习：httpbin、本地 FastAPI（注册 / 登录 / 查询 / 下单）、MySQL 对账、Allure 报告、Docker Compose、GitHub Actions。

不要提交 `.venv`、`allure-results/`、`allure-report/`，本地自己建。

## 怎么安装

```powershell
git clone https://github.com/JINGTAO101/week03-pytest.git
cd week03-pytest
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

看 Allure 网页还需要本机有 **JRE** 和 **Allure 命令行**，并且 `java`、`allure` 能在新开的终端里直接用。

## 怎么配环境

默认读 `config/test.yaml`（`base_url` 是 httpbin，`timeout: 10`）。换环境（PowerShell）：

```powershell
$env:TEST_ENV="dev"
```

本地 FastAPI 地址写在用例里，是 `http://127.0.0.1:8000`，不走这份 YAML。

两套 MySQL，不要混端口：

- 本机服务（`test_mysql_devices.py`）连 `127.0.0.1:3306`，库名 `qa_practice`。
- Docker Compose 里的 MySQL 映射到宿主机 **3307**。订单对账 `test_orders.py` 走 3307。容器内部应用连的是主机名 `mysql`、端口 `3306`。

练习密码在 `common/db.py` 里，只给本机和练习 CI 用。

## 怎么跑

只跑 httpbin（要能访问外网）：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_httpbin_get.py tests/test_httpbin_post.py tests/test_httpbin_auth.py tests/test_httpbin_get_params.py tests/test_marks.py -v
```

跑本地注册 / 登录 / `/me` 之前，另开一个窗口先起被测服务：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

再跑：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_app_auth.py -v
```

跑本机设备表对账之前，本机 MySQL 要在、且有库 `qa_practice` 和表 `devices`：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_mysql_devices.py -v
```

跑下单 / 查单 / 非法数量 / 库表对账之前，用 Compose 起 MySQL + 应用（不要和本机 uvicorn 同时占 8000）。容器起来不等于库就绪，先等到 `/db-ping` 返回 JSON，再跑用例：

```powershell
docker compose up -d --build
curl.exe http://127.0.0.1:8000/db-ping
.\.venv\Scripts\python.exe -m pytest tests/test_orders.py -v
docker compose down
```

`/db-ping` 若是 `Internal Server Error`，隔几秒再 curl，直到出现 `{"ok":1}`。

全部一起跑（httpbin + 本地服务 + MySQL 都就绪时）：

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

当前大约：`17 passed, 1 skipped, 1 xfailed`。httpbin 偶发超时或 502，重跑即可。

## 报告在哪看

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v --alluredir=allure-results
```

新开终端（PATH 里要有 `java` 和 `allure`）：

```powershell
allure serve allure-results
```

浏览器会打开 Allure。点套件里的某条用例，**Attachments** 里有 `request` 和 `response`。`serve` 占着窗口，看完 Ctrl+C。

本仓库作者本机：JRE 在 `D:\JRE`，Allure 在 `D:\Allure`。旧终端若找不到命令，用完整路径或新开窗口。

## CI

`push` 到 `master` 后，GitHub Actions 会在 Ubuntu 上：安装依赖 → 跑 `test_marks.py` → `docker compose up` 起 MySQL 和应用 → 等到 `/db-ping` 通 → 跑登录三条 → 跑订单四条（含库表对账）→ 上传 `allure-results`。

徽章绿只说明这次 workflow 过了。订单有没有测到，要看 job 里有没有 `Wait for db` 和 `Pytest orders`。

看红绿：仓库页 **Actions**，或点标题下的徽章。失败点进 job 看是哪一步红了。

下载产物：打开那次运行的 Summary，Artifacts 里有 `allure-results`。解压后本机：

```powershell
allure serve 解压出来的目录
```

GitHub 网页打不开 Allure，必须本机 `serve`。

本地用容器起整套栈（不要和本机 uvicorn 同时占 8000）：

```powershell
docker compose up -d --build
curl.exe http://127.0.0.1:8000/db-ping
.\.venv\Scripts\python.exe -m pytest tests/test_app_auth.py tests/test_orders.py -v
docker compose down
```
