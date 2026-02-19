# ⚠️ WARNING: Complete Rename from "test" to "internal_marks"

## What You're Asking For

You want to rename ALL instances of:
- `test_score` → `internal_marks`
- `test` → `internal_marks`  
- `Test` → `Internal_Marks`

This includes:
1. Database column names
2. Python variable names
3. Function parameter names
4. HTML form field names
5. JavaScript variable names
6. Template variables

## ⚠️ CRITICAL ISSUES

### 1. Database Schema Change
Renaming `test_score` column requires:
- ALTER TABLE statements
- Data migration
- Potential data loss if not done correctly
- All existing prediction history will need column rename

### 2. Breaking Changes
- Existing CSV files with `test_score` column won't work
- Any external integrations will break
- Backup/restore procedures need updating

### 3. Code Complexity
- 100+ occurrences across files
- Risk of missing instances
- JavaScript/HTML form synchronization required

## Recommended Approach

### Option A: User-Facing Only (ALREADY DONE ✅)
- Keep technical names as `test_score`
- Display as "Internal Marks" to users
- No database changes needed
- No breaking changes
- **This is what we already completed**

### Option B: Complete Rename (RISKY ⚠️)
Requires:
1. Database migration script
2. Update all Python code
3. Update all templates
4. Update all JavaScript
5. Test everything thoroughly
6. Backup database first

## If You Want to Proceed with Option B

I can create:
1. Database migration script
2. Systematic code updates
3. Testing checklist

But I STRONGLY recommend Option A (already done) because:
- Less risky
- No data migration needed
- Easier to maintain
- Industry standard (internal names != display names)

## Your Decision

Do you want to:
1. **Keep current approach** (technical: test_score, display: Internal Marks) ✅ RECOMMENDED
2. **Proceed with full rename** (requires database migration, high risk) ⚠️

Please confirm before I proceed with the risky full rename.
