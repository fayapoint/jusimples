import sys, importlib.util, json
from pathlib import Path

# Ensure backend on path
sys.path.insert(0, r"c:\juximplex\jusimplesBeta-master\backend")

spec = importlib.util.spec_from_file_location("appmod", r"c:\juximplex\jusimplesBeta-master\backend\app.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

client = mod.app.test_client()
paths = ["/health", "/ready", "/api/health", "/api/status", "/"]

results = []
for p in paths:
    try:
        r = client.get(p)
        body = r.data.decode('utf-8', 'ignore')
        results.append({"path": p, "status": r.status_code, "body": body[:1000]})
    except Exception as e:
        results.append({"path": p, "error": str(e)})

out_path = Path(r"c:\juximplex\jusimplesBeta-master\health_check_output.json")
out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(str(out_path))
