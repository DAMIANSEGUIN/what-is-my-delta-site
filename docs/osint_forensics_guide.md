# OSINT Forensics Guide for Values-Driven Job Search

## Overview

The OSINT Forensics Engine provides deep intelligence analysis of companies through job postings, focused on **values alignment** and **passion opportunities** for Mosaic users. This system analyzes job postings to understand what companies really value, their culture, and how well they align with your personal values and passions.

## Core Philosophy: Values-Driven Job Search

Unlike traditional job search that focuses on skills and experience, Mosaic's OSINT forensics focuses on:

1. **Values Alignment**: Does this company share your values?
2. **Passion Opportunities**: Can you pursue your passions here?
3. **Cultural Fit**: Will you thrive in their culture?
4. **Growth Potential**: Do they invest in areas you care about?

## OSINT Analysis Process

### Phase 1: Discovery
- **Source**: Official careers sites + job boards (LinkedIn, Indeed, BuiltIn)
- **Timeframe**: Recent postings (<90 days), older marked as ARCHIVE
- **Data Collected**: Title, location, date, source, compensation, key snippets

### Phase 2: Signal Detection
From job postings, we identify:

**Values Indicators**:
- **Environmental**: "sustainability", "green", "climate", "renewable"
- **Social Impact**: "social impact", "community", "nonprofit", "mission-driven"
- **Learning**: "learning", "education", "training", "development", "mentorship"
- **Innovation**: "innovation", "cutting-edge", "breakthrough", "pioneer"
- **Collaboration**: "collaborative", "team", "partnership", "cross-functional"
- **Transparency**: "transparent", "open", "honest", "authentic"

**Passion Opportunities**:
- **Creative**: "creative", "design", "artistic", "aesthetic"
- **Technical**: "technical", "engineering", "development", "coding"
- **Leadership**: "leadership", "management", "mentor", "inspire"
- **Analytical**: "analytical", "data", "research", "analysis"
- **Communication**: "communication", "presentation", "writing", "storytelling"
- **Problem Solving**: "problem-solving", "solutions", "challenges"

**Culture Signals**:
- **Remote Friendly**: "remote", "flexible", "work from home"
- **Collaborative**: "collaborative", "team", "cross-functional"
- **Innovative**: "innovative", "cutting-edge", "breakthrough"
- **Inclusive**: "inclusive", "diverse", "equity"
- **Fast Paced**: "fast-paced", "dynamic", "agile"
- **Stable**: "stable", "established", "long-term"

**Growth Indicators**:
- **New Team**: "new team", "first hire", "90-day pilot"
- **Expansion**: "expanding", "growing", "scaling"
- **Investment**: "investment", "funding", "backed"
- **Innovation**: "innovation", "R&D", "research"

### Phase 3: Values-Driven Insights

**1. Values Alignment Analysis**
- What values does this company demonstrate?
- How well do they align with your personal values?
- What values are missing that you care about?

**2. Passion Opportunities Analysis**
- What passion areas does this company support?
- How well do they align with your passions?
- What passion opportunities are missing?

**3. Cultural Insights**
- What's their dominant culture?
- How diverse is their cultural approach?
- Will you thrive in their environment?

**4. Growth Signals**
- Where are they investing?
- What growth areas are strongest?
- Do they align with your career goals?

**5. Watch Outs**
- Red flags and risk indicators
- Stale postings or reposted jobs
- Vague descriptions or missing information

**6. User-Specific Alignment**
- How well do they match your values?
- What passion opportunities align with your skills?
- What's missing for your ideal role?

### Phase 4: Receipts Table

Provides evidence for all claims:
- **Claim**: Key insight from analysis
- **Snippet**: Verbatim text from job posting
- **Job**: Title and location
- **Date**: Posting date and source
- **Confidence**: 0-100 score based on evidence quality
- **Archive**: Marked if >90 days old
- **Values Indicators**: Specific values detected
- **Passion Opportunities**: Specific passions identified

## API Endpoints

### Analyze Company OSINT
**Endpoint**: `POST /osint/analyze-company`

**Request**:
```json
{
  "company_name": "Google",
  "job_postings": [
    {
      "title": "Software Engineer",
      "location": "Mountain View, CA",
      "date": "2025-10-01",
      "source": "LinkedIn",
      "compensation": "$120k-180k",
      "description": "Join our innovative team building sustainable technology solutions..."
    }
  ],
  "user_values": ["environmental", "innovation", "collaboration"],
  "user_passions": ["technical", "problem_solving", "leadership"]
}
```

**Response**:
```json
{
  "company_name": "Google",
  "analysis_date": "2025-10-03T19:30:00.000Z",
  "values_alignment": {
    "values_detected": {
      "environmental": 3,
      "innovation": 5,
      "collaboration": 4
    },
    "user_values_alignment": {
      "environmental": 3,
      "innovation": 5,
      "collaboration": 4
    },
    "top_values": [
      ["innovation", 5],
      ["collaboration", 4],
      ["environmental", 3]
    ]
  },
  "passion_opportunities": {
    "passions_detected": {
      "technical": 6,
      "problem_solving": 4,
      "leadership": 2
    },
    "user_passions_alignment": {
      "technical": 6,
      "problem_solving": 4,
      "leadership": 2
    },
    "top_passions": [
      ["technical", 6],
      ["problem_solving", 4],
      ["leadership", 2]
    ]
  },
  "cultural_insights": {
    "culture_signals": {
      "innovative": 5,
      "collaborative": 4,
      "remote_friendly": 3
    },
    "dominant_culture": ["innovative", 5],
    "culture_diversity": 3
  },
  "growth_signals": {
    "growth_signals": {
      "new_team": 2,
      "expansion": 3,
      "investment": 1
    },
    "growth_strength": 6,
    "top_growth_areas": [
      ["expansion", 3],
      ["new_team", 2],
      ["investment", 1]
    ]
  },
  "watch_outs": {
    "red_flags": {
      "Stale posting (>90 days)": 1
    },
    "total_red_flags": 1,
    "risk_level": "low"
  },
  "receipts_table": [
    {
      "claim": "Join our innovative team building sustainable technology...",
      "snippet": "Join our innovative team building sustainable technology solutions...",
      "job": "Software Engineer - Mountain View, CA",
      "date": "2025-10-01",
      "source": "LinkedIn",
      "confidence": 85,
      "archive": "",
      "values_indicators": "environmental: sustainable, innovation: innovative",
      "passion_opportunities": "technical: technology, problem_solving: solutions"
    }
  ],
  "user_values_match": {
    "match_score": 85.0,
    "matched_values": ["environmental", "innovation", "collaboration"],
    "missing_values": [],
    "alignment_strength": "strong"
  },
  "passion_skills_alignment": {
    "match_score": 80.0,
    "matched_passions": ["technical", "problem_solving", "leadership"],
    "missing_passions": [],
    "alignment_strength": "strong"
  }
}
```

### OSINT Health Check
**Endpoint**: `GET /osint/health`

**Response**:
```json
{
  "status": "operational",
  "cache_size": 5,
  "values_keywords": 6,
  "passion_indicators": 6,
  "last_updated": "2025-10-03T19:30:00.000Z"
}
```

## Use Cases

### 1. Values-Driven Company Research
- Research companies that align with your values
- Identify companies that share your passion for environmental causes
- Find organizations that prioritize learning and development

### 2. Passion-Opportunity Mapping
- Discover companies that support your creative passions
- Find roles that align with your technical interests
- Identify leadership opportunities that match your goals

### 3. Cultural Fit Assessment
- Understand company culture before applying
- Identify remote-friendly vs. office-focused companies
- Find collaborative vs. competitive environments

### 4. Growth Potential Analysis
- Identify companies investing in areas you care about
- Find organizations with strong growth signals
- Avoid companies with red flags or stagnant hiring

### 5. Strategic Job Applications
- Target applications to companies with strong values alignment
- Focus on roles that match your passion opportunities
- Avoid companies with cultural mismatches

## Integration with Mosaic

### Values-Driven Job Search
The OSINT forensics system integrates with Mosaic's values-driven approach:

1. **User Values Input**: Users specify their core values
2. **Passion Mapping**: Users identify their passion areas
3. **Company Analysis**: OSINT analyzes companies for alignment
4. **Match Scoring**: System calculates alignment scores
5. **Strategic Recommendations**: Users get targeted company recommendations

### Experiment Integration
OSINT analysis can inform Mosaic experiments:

1. **Values Experiments**: Test different values in job applications
2. **Passion Experiments**: Explore different passion areas
3. **Cultural Experiments**: Test different cultural approaches
4. **Growth Experiments**: Focus on different growth areas

### Learning and Development
OSINT insights can guide learning:

1. **Skills Development**: Focus on skills that align with target companies
2. **Values Clarification**: Better understand your own values
3. **Passion Exploration**: Discover new passion areas
4. **Cultural Awareness**: Learn about different company cultures

## Benefits

### For Job Seekers
1. **Values Alignment**: Find companies that share your values
2. **Passion Opportunities**: Discover roles that match your passions
3. **Cultural Fit**: Avoid companies with poor cultural fit
4. **Growth Potential**: Identify companies with strong growth signals
5. **Strategic Applications**: Focus on high-alignment opportunities

### For Career Development
1. **Values Clarification**: Better understand your own values
2. **Passion Discovery**: Explore new passion areas
3. **Cultural Awareness**: Learn about different company cultures
4. **Skills Alignment**: Focus on skills that matter to target companies
5. **Strategic Planning**: Make informed career decisions

### For Mosaic Users
1. **Personalized Insights**: Analysis tailored to your values and passions
2. **Strategic Recommendations**: Targeted company and role recommendations
3. **Learning Opportunities**: Insights that inform your development
4. **Experiment Guidance**: Data to inform your Mosaic experiments
5. **Values-Driven Career**: Align your career with your values and passions

## Technical Implementation

### Performance
- **Caching**: Intelligent caching of company analyses
- **Batch Processing**: Efficient analysis of multiple job postings
- **Real-time Updates**: Fresh analysis of recent job postings

### Accuracy
- **Confidence Scoring**: 0-100 confidence scores for all insights
- **Source Verification**: Multiple sources for validation
- **Archive Detection**: Automatic detection of stale postings

### Scalability
- **Concurrent Analysis**: Handle multiple company analyses simultaneously
- **Batch Processing**: Efficient analysis of large job posting datasets
- **Resource Management**: Cost controls and usage tracking

## Future Enhancements

1. **Real-time Company Data**: Integrate with company databases
2. **Industry Analysis**: Deep dive into specific industry trends
3. **Competitive Landscape**: Analyze competitor hiring patterns
4. **Salary Intelligence**: Market rate analysis for specific roles
5. **Culture Fit Scoring**: Quantify cultural alignment potential
6. **Values Evolution**: Track how company values change over time
7. **Passion Mapping**: Map passion opportunities across industries
8. **Growth Forecasting**: Predict company growth based on hiring patterns
