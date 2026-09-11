# week03-pytest

用 pytest 调 httpbin 的接口练习：GET / POST、fixture、YAML 数据、`common` 封装。

## 怎么跑

```powershell
git clone https://github.com/JINGTAO101/week03-pytest.git
cd week03-pytest
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests -v