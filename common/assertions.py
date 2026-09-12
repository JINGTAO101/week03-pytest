def assert_status(response, expected=200):
    assert response.status_code == expected, (
        f"url={response.url} status={response.status_code} body={response.text}"
    )

def assert_json(body, path, expected):
    cur = body
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            cur = None
            break
        cur = cur[key]
    assert cur == expected, f"{path} expected {expected!r} got {cur!r}"

def assert_len(body, path, expected):
    cur = body
    for key in path.split("."):
        cur = cur[key]
    assert len(cur) == expected, f"{path} expected {expected} got {len(cur)}"
