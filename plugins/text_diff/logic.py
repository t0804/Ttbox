def lcs_opcodes(a, b):
    """
    基于 LCS 的 diff，返回 opcodes 列表。
    每个元素为 (tag, i1, i2, j1, j2)，tag 为 equal/delete/insert/replace。
    零依赖，可被桌面版和 Web 版复用。
    """
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        ai = a[i]
        row, nxt = dp[i], dp[i + 1]
        for j in range(m - 1, -1, -1):
            row[j] = nxt[j + 1] + 1 if ai == b[j] else max(nxt[j], row[j + 1])
    raw = []
    i = j = 0
    while i < n and j < m:
        if a[i] == b[j]:
            raw.append(("equal", i, i + 1, j, j + 1)); i += 1; j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            raw.append(("delete", i, i + 1, j, j)); i += 1
        else:
            raw.append(("insert", i, i, j, j + 1)); j += 1
    while i < n:
        raw.append(("delete", i, i + 1, j, j)); i += 1
    while j < m:
        raw.append(("insert", i, i, j, j + 1)); j += 1
    out = []
    for tag, i1, i2, j1, j2 in raw:
        if out and out[-1][0] == tag:
            p = out[-1]
            out[-1] = (tag, p[1], i2, p[3], j2)
        else:
            out.append((tag, i1, i2, j1, j2))
    return out
