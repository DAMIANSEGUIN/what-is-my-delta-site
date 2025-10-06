#!/usr/bin/env python3
"""
Secure Key Loader for Mosaic 2.0 Job Search APIs
Loads all job search API keys securely without exposing them
"""

import os
import getpass
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

class SecureJobSearchKeyLoader:
    def __init__(self):
        self.keys_loaded = False
        self.key_cache = {}
        # USER-PROVIDED API KEYS (You will add these)
        self.required_keys = {
            'OPENAI_API_KEY': {
                'name': 'OpenAI API Key',
                'url': 'https://platform.openai.com/',
                'required': True,
                'description': 'AI embeddings and semantic search'
            },
            'CLAUDE_API_KEY': {
                'name': 'Claude AI API Key',
                'url': 'https://docs.anthropic.com/',
                'required': True,
                'description': 'Job analysis and competitive intelligence'
            }
        }
        
        # Public APIs that don't need keys
        self.public_apis = {
            'GREENHOUSE': 'Public job board API - no key needed',
            'INDEED': 'Public XML feed - no key needed', 
            'REDDIT': 'Public API - no key needed',
            'LINKEDIN': 'Public job search - no key needed',
            'GLASSDOOR': 'Public company data - no key needed',
            'DICE': 'Public tech jobs - no key needed',
            'MONSTER': 'Public job board - no key needed',
            'ZIPRECRUITER': 'Public job search - no key needed',
            'CAREERBUILDER': 'Public job board - no key needed'
        }
    
    def load_all_keys_securely(self):
        """Load all job search API keys securely without exposing them."""
        print("🔒 Secure Job Search API Key Loading")
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
    
    def save_keys_to_env_file(self, filename: str = ".env.jobsearch"):
        """Save loaded keys to environment file (for production use)."""
        if not self.keys_loaded:
            print("❌ No keys loaded to save")
            return False
        
        env_content = []
        env_content.append("# Job Search API Keys - DO NOT COMMIT TO GIT")
        env_content.append("# Generated by secure_key_loader.py")
        env_content.append("")
        
        for key_name, key_info in self.required_keys.items():
            if key_name in os.environ:
                env_content.append(f"{key_name}={os.environ[key_name]}")
        
        with open(filename, 'w') as f:
            f.write('\n'.join(env_content))
        
        # Set secure permissions
        os.chmod(filename, 0o600)
        print(f"✅ Keys saved to {filename} with secure permissions")
        return True
    
    def load_keys_from_env_file(self, filename: str = ".env.jobsearch"):
        """Load keys from environment file."""
        if not Path(filename).exists():
            print(f"❌ Environment file {filename} not found")
            return False
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
            
            print(f"✅ Keys loaded from {filename}")
            return True
        except Exception as e:
            print(f"❌ Error loading keys from {filename}: {e}")
            return False
    
    def fix_missing_keys(self):
        """Interactive mode to fix missing required keys."""
        print("🔧 FIXING MISSING REQUIRED KEYS")
        print("=" * 40)
        
        missing_keys = []
        for key_name, key_info in self.required_keys.items():
            if key_info['required'] and key_name not in os.environ:
                missing_keys.append((key_name, key_info))
        
        if not missing_keys:
            print("✅ No missing required keys found")
            return True
        
        for key_name, key_info in missing_keys:
            print(f"\n📋 {key_info['name']} (REQUIRED)")
            print(f"   URL: {key_info['url']}")
            
            try:
                key_value = getpass.getpass(f"   Enter {key_info['name']}: ")
                if key_value.strip() and self._validate_key(key_value, key_info['name']):
                    os.environ[key_name] = key_value
                    self.key_cache[key_name] = self._hash_key(key_value)
                    print(f"   ✅ {key_info['name']} loaded successfully")
                else:
                    print(f"   ❌ {key_info['name']} validation failed")
                    return False
            except KeyboardInterrupt:
                print(f"\n   ⏹️  {key_info['name']} input cancelled")
                return False
        
        print("\n✅ All missing required keys fixed!")
        return True

def main():
    """Main function with command line options."""
    import sys
    
    loader = SecureJobSearchKeyLoader()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fix-missing":
            loader.fix_missing_keys()
        elif sys.argv[1] == "--load-from-file":
            filename = sys.argv[2] if len(sys.argv) > 2 else ".env.jobsearch"
            loader.load_keys_from_env_file(filename)
        elif sys.argv[1] == "--save-to-file":
            filename = sys.argv[2] if len(sys.argv) > 2 else ".env.jobsearch"
            loader.save_keys_to_env_file(filename)
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python3 secure_key_loader.py                    # Load all keys interactively")
            print("  python3 secure_key_loader.py --fix-missing      # Fix missing required keys")
            print("  python3 secure_key_loader.py --load-from-file   # Load from .env.jobsearch")
            print("  python3 secure_key_loader.py --save-to-file     # Save to .env.jobsearch")
            print("  python3 secure_key_loader.py --help            # Show this help")
        else:
            print(f"❌ Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Interactive mode
        loaded, skipped, missing = loader.load_all_keys_securely()
        loader.verify_keys_loaded()
        
        if missing:
            print(f"\n🔧 To fix missing keys, run:")
            print(f"   python3 secure_key_loader.py --fix-missing")
        else:
            print(f"\n✅ All keys loaded successfully!")
            print(f"💾 To save keys for later use, run:")
            print(f"   python3 secure_key_loader.py --save-to-file")

if __name__ == "__main__":
    main()
