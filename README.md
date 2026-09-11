# week03-pytest

用 pytest 调 httpbin 的接口练习：GET / POST、fixture、YAML 数据、`common` 封装。

## 怎么跑

```powershell
git clone https://github.com/JINGTAO101/week03-pytest.git
cd week03-pytest
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests -v

```

期望：`6 passed, 1 skipped, 1 xfailed`。不要提交 `.venv`，本地自己建。

默认读 `config/test.yaml`。换环境（PowerShell）：

```powershell
$env:TEST_ENV="dev"
.\.venv\Scripts\python.exe -m pytest tests -v
```