#!/usr/bin/env python3
"""
Test script to diagnose booking router import issue
Run this on Railway to see the actual error
"""

import sys
import traceback

print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

print("\n1. Testing typing imports...")
try:
    if sys.version_info >= (3, 8):
        from typing import Literal
        print("✅ Literal from typing")
    else:
        from typing_extensions import Literal
        print("✅ Literal from typing_extensions")
except Exception as e:
    print(f"❌ Literal import failed: {e}")
    traceback.print_exc()

print("\n2. Testing google calendar service import...")
try:
    from api.google_calendar_service import get_calendar_service
    print("✅ Google calendar service imported")
except Exception as e:
    print(f"❌ Google calendar service import failed: {e}")
    traceback.print_exc()

print("\n3. Testing paypal service import...")
try:
    from api.paypal_service import get_paypal_service
    print("✅ PayPal service imported")
except Exception as e:
    print(f"❌ PayPal service import failed: {e}")
    traceback.print_exc()

print("\n4. Testing storage import...")
try:
    from api.storage import get_conn
    print("✅ Storage imported")
except Exception as e:
    print(f"❌ Storage import failed: {e}")
    traceback.print_exc()

print("\n5. Testing booking router import...")
try:
    from api.booking import router as booking_router
    print(f"✅ Booking router imported successfully!")
    print(f"   Prefix: {booking_router.prefix}")
    print(f"   Tags: {booking_router.tags}")
    print(f"   Routes: {len(booking_router.routes)}")
except Exception as e:
    print(f"❌ Booking router import failed: {e}")
    traceback.print_exc()

print("\n6. Testing FastAPI app import...")
try:
    from api.index import app
    print(f"✅ FastAPI app imported")
    print(f"   Total routes: {len(app.routes)}")
    booking_routes = [r for r in app.routes if hasattr(r, 'path') and '/booking' in r.path]
    print(f"   Booking routes: {len(booking_routes)}")
    for route in booking_routes:
        print(f"     - {route.path}")
except Exception as e:
    print(f"❌ FastAPI app import failed: {e}")
    traceback.print_exc()
