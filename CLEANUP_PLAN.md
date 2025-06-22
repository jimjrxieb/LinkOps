# 🧹 CLEANUP PLAN - Files to Remove/Move

## 🗑️ Files to DELETE (Standalone/Unused)

### Root Directory
- ❌ `Dockerfile` - Outdated, replaced by backend/Dockerfile and frontend/Dockerfile
- ❌ `whis_consumer.py` - Standalone script, not imported anywhere
- ❌ `manual_orb_creator.py` - Standalone script, not imported anywhere  
- ❌ `screenshot_to_log.py` - Standalone script, not imported anywhere
- ❌ `test_ocr_setup.py` - Standalone test script
- ❌ `test_ocr.py` - Standalone test script
- ❌ `test_openai.py` - Standalone test script
- ❌ `test_gui.py` - Standalone test script
- ❌ `test_exam_frontend.py` - Standalone test script
- ❌ `test_k8s.yaml` - Standalone test file
- ❌ `test_k8s_image.png` - Test image file
- ❌ `linkops.log` - Log file (should be in logs/ directory)

### Test Files (Move to backend/tests/)
- ❌ `test_workflow_audit.py` - Move to backend/tests/
- ❌ `test_complete_workflow.py` - Move to backend/tests/
- ❌ `test_whis_training.py` - Move to backend/tests/

## 📁 Directories to CHECK

### agents/ Directory
- ⚠️ Check if this contains agent-specific code that should be in backend/
- ⚠️ Or if it's just documentation that can stay

### scripts/ Directory  
- ⚠️ Check if these are backend-related scripts
- ⚠️ Move to backend/scripts/ if applicable

### tests/ Directory
- ⚠️ Check if these are backend tests
- ⚠️ Move to backend/tests/ if applicable

### logs/ Directory
- ✅ Keep - contains log files

### docs/ Directory
- ✅ Keep - contains documentation

### screenshots/ Directory
- ⚠️ Check if this is frontend-related (UI screenshots)
- ⚠️ Or backend-related (OCR test images)

## 🔄 Files to MOVE

### To backend/
- 📦 `test_workflow_audit.py` → `backend/tests/`
- 📦 `test_complete_workflow.py` → `backend/tests/`
- 📦 `test_whis_training.py` → `backend/tests/`

### To frontend/
- ✅ Already done: `test-holocore-simple.js` → `frontend/`

## 📋 Verification Checklist

### Backend Structure
- [ ] Only one FastAPI entrypoint: `backend/main.py`
- [ ] All API routes in `backend/core/api/`
- [ ] All models in `backend/models/`
- [ ] All business logic in `backend/core/logic/`
- [ ] All database code in `backend/core/db/`

### Frontend Structure  
- [ ] Vue entrypoint: `frontend/src/main.js`
- [ ] Main component: `frontend/src/App.vue`
- [ ] Views in `frontend/src/views/`
- [ ] Components in `frontend/src/components/`
- [ ] Router in `frontend/src/router/`

### Docker Configuration
- [ ] Backend builds from `./backend`
- [ ] Frontend builds from `./frontend`
- [ ] No root Dockerfile needed

## 🚀 Next Steps

1. **Review the plan** - Confirm which files to delete
2. **Execute cleanup** - Remove unused files
3. **Move test files** - Organize tests properly
4. **Update documentation** - Remove references to deleted files
5. **Run audit script** - Verify clean structure 