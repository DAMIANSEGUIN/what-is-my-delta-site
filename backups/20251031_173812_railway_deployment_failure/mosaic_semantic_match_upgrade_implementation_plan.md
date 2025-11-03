# Mosaic Semantic Match Upgrade - 90 Minute Implementation Plan

## 🎯 **EXECUTIVE SUMMARY**

**Timeline**: 90 minutes maximum build time
**Budget**: $60 incremental spend guardrail
**Target**: 30% match quality improvement
**Status**: Ready for immediate implementation

---

## 📋 **DETAILED IMPLEMENTATION SEQUENCE**

### **Phase 1: Embedding Upgrade & Reindex (30 minutes)**

#### **1.1 Switch to text-embedding-3-small (15 minutes)**
```python
# Update api/rag_engine.py
- Replace OpenAI ADA-002 with text-embedding-3-small
- Update embedding dimensions handling
- Test embedding quality improvement
```

#### **1.2 Corpus Reindex (15 minutes)**
```python
# Re-embed existing corpora
- Resume corpus re-embedding
- Job description corpus re-embedding  
- Update SQLite vector storage
- Verify index integrity
```

**Expected Outcome**: +20-25% recall gain
**Cost**: ~$25 for re-embed + fresh traffic

---

### **Phase 2: Cross-Encoder Reranker (25 minutes)**

#### **2.1 Deploy CPU-Hosted Reranker (20 minutes)**
```python
# Create api/reranker.py
- Install sentence-transformers
- Configure cross-encoder/ms-marco-MiniLM-L-6-v2
- Setup CPU container deployment
- Target latency <150ms
```

#### **2.2 Integration (5 minutes)**
```python
# Integrate into api/rag_engine.py
- Rerank top 10 retrieval hits per query
- Update retrieval pipeline
- Test reranking functionality
```

**Expected Outcome**: Significant quality improvement
**Cost**: ~$20 for small autoscaling instance

---

### **Phase 3: Scoring & Telemetry (15 minutes)**

#### **3.1 Enhanced Scoring (10 minutes)**
```python
# Add to api/rag_engine.py
- Normalized cosine scoring
- Simple keyword boosts
- Pre/post-rerank score logging
```

#### **3.2 Analytics Dashboard (5 minutes)**
```python
# Create api/analytics.py
- Match score distribution tracking
- Rerank lift metrics
- Token usage monitoring
- CSV export functionality
```

**Expected Outcome**: Full observability from day one
**Cost**: Engineering time only

---

### **Phase 4: Testing & Validation (20 minutes)**

#### **4.1 Smoke Tests (10 minutes)**
```python
# Test all components
- Embedding upgrade functionality
- Reranker integration
- Logging and metrics
- Cost controls
```

#### **4.2 Performance Validation (10 minutes)**
```python
# Validate improvements
- Measure 30% match improvement
- Confirm P95 latency <1.2s
- Verify $60 budget guardrail
- Document baseline metrics
```

**Expected Outcome**: Ready for A/B testing
**Cost**: Within $60 budget

---

## 📊 **SUCCESS CRITERIA**

### **Primary KPIs**
- ✅ **Match Quality**: ≥30% improvement
- ✅ **Latency**: P95 <1.2 seconds
- ✅ **Budget**: ≤$60 incremental spend
- ✅ **Rerank Hit Rate**: Measurable improvement

### **Secondary KPIs**
- ✅ **Token Usage**: Tracked and logged
- ✅ **Manual QA**: Approval rate improvement
- ✅ **User Experience**: No degradation
- ✅ **Cost Controls**: Active monitoring

---

## 🔧 **TECHNICAL IMPLEMENTATION**

### **Files to Modify**
1. **`api/rag_engine.py`** - Embedding upgrade + reranker integration
2. **`api/reranker.py`** - New cross-encoder service
3. **`api/analytics.py`** - New telemetry system
4. **`requirements.txt`** - Add sentence-transformers
5. **`api/migrations/`** - Add analytics tables

### **Dependencies**
```python
# Add to requirements.txt
sentence-transformers>=2.2.2
scikit-learn>=1.3.0
numpy>=1.24.0
```

### **Database Changes**
```sql
-- Add analytics tables
CREATE TABLE match_analytics (
    id INTEGER PRIMARY KEY,
    query_hash TEXT,
    pre_rerank_score REAL,
    post_rerank_score REAL,
    improvement_pct REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📈 **MONTHLY ROADMAP**

### **Month 1 (Now)**
- ✅ Deliver immediate enhancements
- ✅ Finalize evaluation rubric
- ✅ Compile before/after metrics
- ✅ A/B test execution

### **Month 2**
- 🔄 Selective sparse boost (BM25/TF-IDF)
- 🔄 Refine rerank thresholds
- 🔄 Expand labeled evaluation set
- 🔄 Budget impact: +$80 max

### **Month 3**
- 🔄 Caching for frequent queries
- 🔄 Automated weekly re-embeds
- 🔄 Optional GPU-based reranker
- 🔄 Vendor commitment reassessment

---

## 🚨 **RISK MITIGATION**

### **Latency Creep**
- **Mitigation**: Small rerank candidate set (≤10)
- **Monitoring**: P95 metrics tracking
- **Fallback**: Disable reranker if >1.2s

### **Cost Overruns**
- **Mitigation**: Token usage logging
- **Guardrail**: Freeze features if near $60 cap
- **Escalation**: Alert at $50 spend

### **Data Drift**
- **Mitigation**: Weekly corpus health checks
- **Schedule**: Document re-embed cadence
- **Monitoring**: Embedding quality metrics

---

## 🎯 **HANDOFF PROTOCOL**

### **For Cursor (Implementation)**
1. **Execute**: 90-minute build sequence
2. **Test**: All components locally
3. **Document**: Diffs and test results
4. **Report**: Baseline metrics captured

### **For Claude Code (Deployment)**
1. **Review**: Infrastructure requirements
2. **Prepare**: Railway configuration updates
3. **Monitor**: Cost and performance metrics
4. **Support**: Deployment issues only

### **For CODEX (Planning)**
1. **Approve**: Implementation plan
2. **Monitor**: Progress and metrics
3. **Design**: A/B test framework
4. **Document**: Results and learnings

---

## ✅ **READY FOR IMPLEMENTATION**

**Status**: Plan approved and ready for execution
**Timeline**: 90 minutes maximum
**Budget**: $60 guardrail active
**Target**: 30% match improvement
**Next Action**: Begin Phase 1 implementation

---

**Document Version**: 1.0
**Created**: 2025-10-04
**Approved By**: Human Gatekeeper
**Implementation Owner**: Cursor (Claude in Cursor)
**Deployment Support**: Claude Code
