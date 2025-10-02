import csv, glob, hashlib, os, json
from typing import List, Dict, Optional

REQUIRED_COLS = ["prompt","completion","tag"]
REGISTRY_FILE = "data/prompts_registry.json"
FALLBACK_CSV_CANDIDATES = [
    "data/prompts.csv",
    "data/prompts_clean.csv",
    "data/prompts_fixed.csv",
]

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

def _fallback_registry() -> Dict[str, Optional[str]]:
    # Prefer deterministic CSV sources so active digest stays stable across deploys.
    for candidate in FALLBACK_CSV_CANDIDATES:
        if not os.path.exists(candidate):
            continue
        try:
            digest = sha256_file(candidate)
        except OSError:
            continue
        json_path = f"data/prompts_{digest[:12]}.json"
        if os.path.exists(json_path):
            return {
                "active": digest,
                "versions": [{"sha256": digest, "file": json_path}],
            }

    # Fall back to the newest prompts_*.json if no canonical CSV is available.
    json_candidates = sorted(glob.glob("data/prompts_*.json"))
    if json_candidates:
        # The filename suffix only keeps the first 12 chars of the digest; keep it for visibility.
        latest = json_candidates[-1]
        short_sha = os.path.splitext(os.path.basename(latest))[0].split("_")[-1]
        return {
            "active": short_sha,
            "versions": [{"sha256": short_sha, "file": latest}],
        }

    return {"active": None, "versions": []}


def read_registry():
    if not os.path.exists(REGISTRY_FILE):
        return _fallback_registry()
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return _fallback_registry()
            data.setdefault("active", None)
            data.setdefault("versions", [])
            return data
    except Exception:
        # corrupted or unreadable registry; attempt to derive fallback values
        return _fallback_registry()

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
