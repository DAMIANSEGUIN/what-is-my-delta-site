import csv, hashlib, os, json
from typing import List, Dict

REQUIRED_COLS = ["prompt","completion","tag"]
REGISTRY_FILE = "data/prompts_registry.json"

def sha256_file(path: str)->str:
    h=hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""): h.update(chunk)
    return h.hexdigest()

def load_csv(path: str)->List[Dict[str,str]]:
    with open(path, newline='', encoding="utf-8") as f:
        reader=csv.DictReader(f)
        cols=set(reader.fieldnames or [])
        missing=[c for c in REQUIRED_COLS if c not in cols]
        if missing: raise ValueError(f"Missing columns: {missing}")
        rows=[r for r in reader]
    if not rows: raise ValueError("CSV is empty")
    return rows

def read_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"active": None, "versions": []}
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"active": None, "versions": []}
            data.setdefault("active", None)
            data.setdefault("versions", [])
            return data
    except Exception:
        # corrupted or unreadable registry; return empty structure
        return {"active": None, "versions": []}

def write_registry(reg):
    with open(REGISTRY_FILE,"w",encoding="utf-8") as f: json.dump(reg, f, indent=2)

def ingest_prompts(csv_path: str):
    digest=sha256_file(csv_path)
    reg=read_registry()
    if any(v["sha256"]==digest for v in reg["versions"]):
        return {"status":"skipped", "reason":"already_ingested", "sha256":digest}
    data=load_csv(csv_path)
    out=f"data/prompts_{digest[:12]}.json"
    with open(out,"w",encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)
    reg["versions"].append({"sha256":digest, "file":out})
    reg["active"]=digest
    write_registry(reg)
    return {"status":"ok","active":digest,"file":out}

def get_active():
    reg = read_registry()
    return {"active": reg.get("active")}
