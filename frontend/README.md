# What is my Delta? — Dynamic Widget Testing

This is the production version with dynamic widget switching for A/B testing different chat solutions.

## Widget Testing URLs:
- `https://what-is-my-delta.vercel.app/` → Clean (no widget)
- `https://what-is-my-delta.vercel.app/?widget=crisp` → Crisp chat only
- `https://what-is-my-delta.vercel.app/?widget=tidio` → Tidio chat only  
- `https://what-is-my-delta.vercel.app/?widget=tawk` → Tawk.to chat only

## Features:
- 8-prompt coaching flow (simplified from 10-step)
- Dynamic widget loading without conflicts
- Widget tracking in analytics
- LocalStorage with optional Supabase integration

Last updated: 2025-08-23