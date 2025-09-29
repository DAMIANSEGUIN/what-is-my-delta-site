# CSV ARCHITECTURE CONTEXT - COACHVOX AI GUIDELINES

**CRITICAL**: The CSV was architected following CoachVox AI specifications for AI-based coaching systems.

## CoachVox AI Guidelines Implemented

### CSV Structure Design
The prompts.csv follows CoachVox AI best practices:
- **Prompt column**: User input patterns for matching
- **Completion column**: AI-optimized coaching responses
- **Labels column**: Categorization for improved matching (Experimentation & Testing, Decision-Making, etc.)

### AI Integration Pattern
This is NOT just a static lookup table. The CSV is designed to:
1. **Train matching algorithms** with real coaching scenarios
2. **Provide context** for AI API calls when no direct match exists
3. **Enable learning loops** where API responses can be cached back to expand the knowledge base
4. **Follow coaching methodology** (PS101) in response patterns

### Response Quality Standards
Each completion follows CoachVox AI quality standards:
- Empathetic acknowledgment
- Actionable guidance 
- Specific next steps
- Professional coaching tone
- Aligned with PS101 framework

## Integration Requirements

The CSV must be:
- **Parsed correctly** to maintain response quality
- **Matched intelligently** using semantic similarity, not just keyword matching
- **Combined with PS101 framework** for contextualized responses
- **Connected to API** for continuous learning and improvement

## Parsing Importance
Given CoachVox AI guidelines, the CSV parsing MUST handle:
- Quoted fields with embedded commas (coaching responses contain lists)
- Maintaining response integrity (no truncated advice)
- Preserving categorization labels for improved matching

**This explains why simple split(',') parsing breaks the entire coaching intelligence system.**

The system was designed to be a learning AI coach, not just a static FAQ lookup. The CSV is the foundation of that intelligence.