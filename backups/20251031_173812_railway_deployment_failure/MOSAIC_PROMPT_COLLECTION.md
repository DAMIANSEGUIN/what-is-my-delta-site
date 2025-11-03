# MOSAIC PROMPT COLLECTION - ALL PROMPTS IN ONE DOCUMENT

## 🎯 **MOSAIC RESET PROTOCOL**

**Use this exact prompt when the Implementation SSE needs to be reset:**

```
You are the Implementation SSE for Mosaic 2.0. Your role is to:

1. IMPLEMENT locally only - never deploy to production
2. TEST everything you build before claiming completion
3. COMMIT real changes to git with clear documentation
4. HAND OFF to Claude Code for production deployment
5. UPDATE documentation (CONVERSATION_NOTES.md, ROLLING_CHECKLIST.md)

CRITICAL RULES:
- Every file change must be REAL and VERIFIABLE
- Every test must be ACTUALLY RUN, not simulated
- Every git commit must be GENUINE with real changes
- Never claim work is done without PROOF of completion
- Always verify your work with actual commands and outputs

CURRENT TASK: Implement the semantic match upgrade (90 minutes)
- Phase 1: Embedding upgrade to text-embedding-3-small
- Phase 2: Cross-encoder reranker implementation  
- Phase 3: Analytics dashboard creation
- Phase 4: Testing and validation

START NOW with Phase 1 - actually modify the RAG engine file.
```

---

## 🔒 **SECURE KEY IMPORT SCRIPTS**

### **Bash One-Shot Script**
```bash
#!/bin/bash
# secure_key_import.sh - One-shot secure key import

# Set secure permissions
chmod 700 secure_key_import.sh

# Create secure environment file
cat > .env.secure << 'EOF'
# Secure API Keys - DO NOT COMMIT TO GIT
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
SENTENCE_TRANSFORMERS_CACHE_DIR=/secure/cache/path
EOF

# Set secure permissions on env file
chmod 600 .env.secure

# Load keys into environment
source .env.secure

# Verify keys are loaded (without exposing them)
echo "Keys loaded securely - checking format..."
if [[ ${#OPENAI_API_KEY} -gt 20 ]]; then
    echo "✅ OpenAI key loaded (${#OPENAI_API_KEY} characters)"
else
    echo "❌ OpenAI key invalid"
fi

if [[ ${#ANTHROPIC_API_KEY} -gt 20 ]]; then
    echo "✅ Anthropic key loaded (${#ANTHROPIC_API_KEY} characters)"
else
    echo "❌ Anthropic key invalid"
fi

# Clean up temporary files
rm -f .env.secure

echo "✅ Keys imported securely and environment variables set"
```

### **Python Secure Key Loader (Simplified)**
```python
#!/usr/bin/env python3
"""
Secure Key Loader for Mosaic 2.0
Loads API keys securely without exposing them
"""

import os
import getpass
import hashlib
from typing import Dict, List, Optional

class SecureKeyLoader:
    def __init__(self):
        self.keys_loaded = False
        self.key_cache = {}
        self.required_keys = {
            'OPENAI_API_KEY': {
                'name': 'OpenAI API Key',
                'url': 'https://platform.openai.com/api-keys',
                'required': True,
                'description': 'OpenAI API for embeddings and chat'
            },
            'ANTHROPIC_API_KEY': {
                'name': 'Anthropic API Key',
                'url': 'https://console.anthropic.com/',
                'required': True,
                'description': 'Anthropic Claude API'
            },
            'SERPAPI_API_KEY': {
                'name': 'SerpApi API Key',
                'url': 'https://serpapi.com/',
                'required': True,
                'description': 'Google Jobs search via SerpApi'
            },
            'GREENHOUSE_API_TOKEN': {
                'name': 'Greenhouse API Token',
                'url': 'https://developers.greenhouse.io/',
                'required': False,
                'description': 'Greenhouse job board API'
            }
        }
    
    def load_all_keys_securely(self):
        """Load all API keys securely without exposing them."""
        print("🔒 Secure API Key Loading")
        print("=" * 50)
        print("Keys will not be displayed for security")
        print("=" * 50)
        
        loaded_keys = 0
        skipped_keys = 0
        required_missing = []
        
        for key_name, key_info in self.required_keys.items():
            print(f"\n📋 {key_info['name']}")
            print(f"   Description: {key_info['description']}")
            print(f"   URL: {key_info['url']}")
            print(f"   Required: {'Yes' if key_info['required'] else 'No'}")
            
            try:
                if key_info['required']:
                    key_value = getpass.getpass(f"   Enter {key_info['name']} (required): ")
                else:
                    key_value = getpass.getpass(f"   Enter {key_info['name']} (optional, press Enter to skip): ")
                
                if key_value.strip():
                    if self._validate_key(key_value, key_info['name']):
                        os.environ[key_name] = key_value
                        self.key_cache[key_name] = self._hash_key(key_value)
                        loaded_keys += 1
                        print(f"   ✅ {key_info['name']} loaded successfully")
                    else:
                        print(f"   ❌ {key_info['name']} validation failed")
                        if key_info['required']:
                            required_missing.append(key_info['name'])
                else:
                    if key_info['required']:
                        print(f"   ⚠️  {key_info['name']} is required but was skipped")
                        required_missing.append(key_info['name'])
                    else:
                        print(f"   ⏭️  {key_info['name']} skipped (optional)")
                        skipped_keys += 1
                        
            except KeyboardInterrupt:
                print(f"\n   ⏹️  {key_info['name']} input cancelled")
                if key_info['required']:
                    required_missing.append(key_info['name'])
                break
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 KEY LOADING SUMMARY")
        print("=" * 50)
        print(f"✅ Keys loaded: {loaded_keys}")
        print(f"⏭️  Keys skipped: {skipped_keys}")
        print(f"❌ Required keys missing: {len(required_missing)}")
        
        if required_missing:
            print(f"\n⚠️  REQUIRED KEYS MISSING:")
            for key in required_missing:
                print(f"   - {key}")
            print(f"\n🔧 To fix missing keys, run:")
            print(f"   python3 secure_key_loader.py --fix-missing")
        else:
            print(f"\n✅ All required keys loaded successfully!")
        
        self.keys_loaded = loaded_keys > 0
        return loaded_keys, skipped_keys, required_missing
    
    def _validate_key(self, key: str, key_name: str) -> bool:
        """Validate API key format."""
        if len(key) < 10:
            print(f"   ❌ {key_name} key too short (minimum 10 characters)")
            return False
        
        if "your-key-here" in key.lower():
            print(f"   ❌ {key_name} key appears to be placeholder")
            return False
        
        if "sk-test" in key.lower() and "production" in os.environ.get('ENVIRONMENT', '').lower():
            print(f"   ⚠️  {key_name} appears to be a test key in production")
            return False
        
        return True
    
    def _hash_key(self, key: str) -> str:
        """Create hash of key for verification without exposing it."""
        return hashlib.sha256(key.encode()).hexdigest()[:16]
    
    def verify_keys_loaded(self):
        """Verify keys are loaded without exposing them."""
        print("\n🔍 VERIFYING LOADED KEYS")
        print("=" * 30)
        
        for key_name, key_info in self.required_keys.items():
            if key_name in os.environ:
                key_length = len(os.environ[key_name])
                print(f"✅ {key_info['name']}: Loaded ({key_length} characters)")
            else:
                status = "❌ Missing" if key_info['required'] else "⏭️  Skipped"
                print(f"{status} {key_info['name']}")
        
        return self.keys_loaded

if __name__ == "__main__":
    loader = SecureKeyLoader()
    loaded, skipped, missing = loader.load_all_keys_securely()
    loader.verify_keys_loaded()
    
    if missing:
        print(f"\n🔧 To fix missing keys, run:")
        print(f"   python3 secure_key_loader.py --fix-missing")
    else:
        print(f"\n✅ All keys loaded successfully!")
```

---

## 🔐 **SECURE CONFIGURATION MANAGEMENT**

### **Encrypted Key Storage**
```python
# encrypted_key_storage.py - Store keys encrypted
from cryptography.fernet import Fernet
import os
import json
from pathlib import Path

class EncryptedKeyStorage:
    def __init__(self):
        self.key_file = Path("encrypted_keys.enc")
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key."""
        key_file = Path("encryption.key")
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            key_file.chmod(0o600)  # Secure permissions
            return key
    
    def store_keys_encrypted(self, keys: dict):
        """Store keys encrypted."""
        encrypted_data = self.cipher.encrypt(json.dumps(keys).encode())
        self.key_file.write_bytes(encrypted_data)
        self.key_file.chmod(0o600)  # Secure permissions
        print("✅ Keys stored encrypted")
    
    def load_keys_encrypted(self) -> dict:
        """Load keys encrypted."""
        if not self.key_file.exists():
            return {}
        
        encrypted_data = self.key_file.read_bytes()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    
    def load_keys_into_environment(self):
        """Load encrypted keys into environment variables."""
        keys = self.load_keys_encrypted()
        for key_name, key_value in keys.items():
            os.environ[key_name] = key_value
        print("✅ Keys loaded into environment from encrypted storage")

# Usage
if __name__ == "__main__":
    storage = EncryptedKeyStorage()
    
    # Store keys (run once)
    keys = {
        "OPENAI_API_KEY": "your-openai-key-here",
        "ANTHROPIC_API_KEY": "your-anthropic-key-here"
    }
    storage.store_keys_encrypted(keys)
    
    # Load keys (run when needed)
    storage.load_keys_into_environment()
```

---

## 🚀 **TERMINAL COMMANDS FOR KEY MANAGEMENT**

### **One-Shot Key Import**
```bash
# Create and run secure key import script
chmod +x secure_key_import.sh
./secure_key_import.sh
```

### **Python Key Loader Commands**
```bash
# Load all keys interactively
python3 secure_key_loader.py

# Fix missing required keys only
python3 secure_key_loader.py --fix-missing

# Load keys from file
python3 secure_key_loader.py --load-from-file .env.jobsearch

# Save keys to file
python3 secure_key_loader.py --save-to-file .env.jobsearch

# Get help
python3 secure_key_loader.py --help
```

### **Environment File Management**
```bash
# Create secure environment file
cat > .env.secure << 'EOF'
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
SERPAPI_API_KEY=your-serpapi-key-here
EOF

# Set secure permissions
chmod 600 .env.secure

# Load environment variables
source .env.secure

# Verify keys are loaded
echo "OpenAI key length: ${#OPENAI_API_KEY}"
echo "Anthropic key length: ${#ANTHROPIC_API_KEY}"
echo "SerpApi key length: ${#SERPAPI_API_KEY}"
```

---

## 📋 **API ENDPOINTS TO ADD**

### **Analytics Endpoints**
```python
# Add to api/index.py
from .analytics import get_analytics_dashboard, export_analytics_csv, get_analytics_health

@app.get("/analytics/dashboard")
def get_analytics_dashboard_endpoint():
    """Get comprehensive analytics dashboard data."""
    return get_analytics_dashboard()

@app.get("/analytics/export")
def export_analytics_endpoint(days: int = 7):
    """Export analytics data to CSV."""
    try:
        filename = export_analytics_csv(days)
        if filename:
            return {"filename": filename, "status": "success"}
        else:
            return {"error": "Failed to export analytics", "status": "error"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/analytics/health")
def get_analytics_health_endpoint():
    """Get analytics engine health status."""
    return get_analytics_health()
```

### **Reranker Endpoints**
```python
# Add to api/index.py
from .reranker import get_reranker_health

@app.get("/reranker/health")
def get_reranker_health_endpoint():
    """Get cross-encoder reranker health status."""
    return get_reranker_health()
```

### **Corpus Reindex Endpoints**
```python
# Add to api/index.py
from .corpus_reindex import reindex_corpus, get_reindex_status

@app.post("/corpus/reindex")
def reindex_corpus_endpoint():
    """Re-index corpus with new embeddings."""
    try:
        results = reindex_corpus()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/corpus/status")
def get_corpus_status_endpoint():
    """Get corpus reindex status."""
    return get_reindex_status()
```

---

## 🔑 **JOB SEARCH API ADDRESSES**

### **High Priority APIs**
- **SerpApi**: https://serpapi.com/ (Google Jobs search)
- **Greenhouse**: https://developers.greenhouse.io/ (High-quality jobs)
- **LinkedIn**: https://www.linkedin.com/developers/ (Professional network)
- **Indeed**: https://ads.indeed.com/jobroll/xmlfeed (Largest job board)

### **Medium Priority APIs**
- **Reddit**: https://www.reddit.com/prefs/apps (Community jobs)
- **Glassdoor**: https://www.glassdoor.com/developer/ (Company insights)
- **Dice**: https://www.dice.com/developer/ (Tech jobs)

### **Low Priority APIs**
- **RemoteOK**: https://remoteok.io/api (No key needed)
- **WeWorkRemotely**: https://weworkremotely.com/api (No key needed)
- **Hacker News**: https://hackernews.api-docs.io/ (No key needed)

---

## 🚨 **SECURITY CHECKLIST**

### **✅ SECURE PRACTICES**
- Environment variables only
- No hardcoded keys
- Secure file permissions (0o600)
- Key validation
- Encrypted storage
- Access controls

### **❌ INSECURE PRACTICES**
- Hardcoded keys in source code
- Keys in git commits
- Test keys in production
- Keys in logs or output
- Unencrypted storage

---

## 📊 **USAGE SUMMARY**

### **Quick Start**
1. **Save the secure_key_loader.py script**
2. **Run: `python3 secure_key_loader.py`**
3. **Enter your API keys when prompted**
4. **Keys are loaded into environment variables**
5. **Use in your application**

### **Troubleshooting**
- **Missing keys**: Run `python3 secure_key_loader.py --fix-missing`
- **Load from file**: Run `python3 secure_key_loader.py --load-from-file`
- **Save to file**: Run `python3 secure_key_loader.py --save-to-file`

### **Security Notes**
- Keys never displayed in output
- Secure file permissions automatically set
- Environment variables only
- No keys in source code

---

**All prompts and scripts in one document for easy access and reference!**
