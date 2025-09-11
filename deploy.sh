#!/bin/bash

# Mosaic Platform Deployment Script
echo "🚀 Deploying Mosaic Platform (WIMD + OpportunityBridge)"

# Check if in correct directory
if [ ! -f "api/index.py" ]; then
    echo "❌ Error: Run this script from the mosaic_vercel_api directory"
    exit 1
fi

# Option 1: Push to GitHub
echo "📋 Deployment Options:"
echo "1. Push to GitHub + Deploy to Vercel"
echo "2. Deploy directly to Vercel"
read -p "Choose option (1 or 2): " option

if [ "$option" == "1" ]; then
    echo "🔑 GitHub deployment selected"
    
    # Check if git repo exists
    if [ ! -d ".git" ]; then
        echo "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial Mosaic platform commit"
    fi
    
    # Prompt for GitHub token
    read -p "Enter your GitHub Personal Access Token: " token
    
    # Set remote with token
    git remote remove origin 2>/dev/null || true
    git remote add origin https://$token@github.com/DAMIANSEGUIN/mosaic-vercel-api.git
    
    # Push to GitHub
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    echo "✅ Code pushed to GitHub!"
    echo "🌐 Now deploy to Vercel:"
    echo "   1. Go to vercel.com"
    echo "   2. Import mosaic-vercel-api repository"
    echo "   3. Add OPENAI_API_KEY environment variable"
    echo "   4. Deploy!"
    
elif [ "$option" == "2" ]; then
    echo "📦 Creating deployment package..."
    
    # Create clean deployment package
    zip -r mosaic-deployment.zip . -x "*.git*" ".venv/*" "*/__pycache__/*" "deploy.sh"
    
    echo "✅ Deployment package created: mosaic-deployment.zip"
    echo "🌐 Manual Vercel deployment:"
    echo "   1. Go to vercel.com → New Project"
    echo "   2. Upload mosaic-deployment.zip"
    echo "   3. Add OPENAI_API_KEY environment variable"
    echo "   4. Deploy!"
fi

echo ""
echo "🎯 Your Mosaic Platform includes:"
echo "   • WIMD (What Is My Delta) - Career discovery"
echo "   • OpportunityBridge - Values-aligned job matching"
echo "   • Foundation coaching principles"
echo "   • Multi-format file processing"
echo ""
echo "📍 API Endpoints once deployed:"
echo "   • GET  /health"
echo "   • POST /wimd"
echo "   • POST /wimd/opportunities"
echo "   • POST /opportunities"
echo "   • GET  /test"
echo ""
echo "🎉 Deployment complete!"