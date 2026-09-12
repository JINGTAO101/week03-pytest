# week03-pytest

pytest 接口练习：httpbin、本地 FastAPI（注册 / 登录 / 查询）、MySQL 对账、Allure 报告。

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

本地 FastAPI 地址写在 `tests/test_app_auth.py` 里，是 `http://127.0.0.1:8000`，不走这份 YAML。

MySQL 用例连 `127.0.0.1:3306`，库名 `qa_practice`，账号 `root`。练习密码在 `common/db.py` 里，只给本机用。

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

跑 MySQL 对账之前，本机 MySQL 要在、且有库 `qa_practice` 和表 `devices` / `orders`：

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_mysql_devices.py -v
```

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
