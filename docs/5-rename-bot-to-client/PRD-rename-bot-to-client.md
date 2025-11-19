# Product Requirements Document: Rename "Bot" to "Client"

**Sprint**: 5 - Core Naming Refactor  
**Feature**: Rename Bot/bot to Client/client throughout codebase  
**Status**: 📋 Planned  
**Priority**: MEDIUM  
**Estimated Effort**: 1-2 days (8-16 hours)  
**Target Date**: TBD (after Sprints 1-4)

---

## Executive Summary

Rename all "Bot" and "bot" references to "Client" and "client" throughout the codebase to accurately reflect that Juiced is now a standalone TUI chat client, not a bot. This improves clarity, sets proper expectations, and aligns naming with the project's actual purpose.

**Key Value Proposition**: Clear, honest naming that reflects what Juiced actually is - a terminal user interface client, not an automated bot.

---

## Problem Statement

### What problem are we solving?

**Historical Context**: Juiced was originally extracted from the Rosey-Robot bot project. It inherited the "Bot" class name and bot-centric terminology, even though Juiced is a human-operated TUI client, not an automated bot.

**Current Issues**:

1. **Misleading naming**: `Bot` class suggests automation/AI when it's actually a client library
2. **Confused expectations**: Users/contributors expect bot behavior (automation, commands)
3. **API confusion**: Methods like `bot.chat()` are actually client operations
4. **Documentation mismatch**: README says "terminal chat client" but code says "bot"
5. **Identity crisis**: Is Juiced a bot or a client? The name says one thing, behavior says another

**Examples of confusion**:

```python
# Current (confusing)
from juiced.lib.bot import Bot
bot = Bot(domain, channel)
await bot.chat("Hello")  # I'm not a bot, I'm a human typing!

# Proposed (clear)
from juiced.lib.client import Client
client = Client(domain, channel)
await client.chat("Hello")  # I'm using a client to chat
```

```python
# Current (confusing)
class TUIBot(Bot):
    """CyTube bot with terminal user interface."""
    # But it's not a bot, it's a TUI for humans!

# Proposed (clear)
class TUIClient(Client):
    """CyTube client with terminal user interface."""
    # Clear: it's a client with a TUI
```

### Who is affected?

- **New Contributors**: Confused by bot terminology when writing client features
- **Users**: May expect automation features that don't exist
- **Documentation Readers**: README says "client" but code says "bot"
- **API Users**: Unclear what methods are for automation vs. human interaction
- **Future Developers**: Inherit confusing naming debt

### Why now?

- Code quality foundation established (Sprint 1)
- Test coverage improved (Sprint 2)
- Type hints added (Sprint 3)
- Documentation comprehensive (Sprint 4)
- **Perfect time**: Before 1.0 release, after infrastructure solid
- **Breaking change**: Better to do now than after wider adoption
- **Identity clarity**: Juiced needs to own what it is

---

## Goals and Success Metrics

### Goals

1. **Primary**: Rename `Bot` class to `Client` in all code
2. **Secondary**: Rename `TUIBot` to `TUIClient`
3. **Tertiary**: Update all documentation to use "client" terminology
4. **Stretch**: Rename `bot.py` to `client.py` (file-level)

### Success Metrics

- ✅ Zero references to "Bot" class in codebase (except deprecation aliases)
- ✅ All tests pass with new naming
- ✅ Documentation updated (README, docstrings, comments)
- ✅ No breaking changes for external users (migration path provided)
- ✅ Clear deprecation warnings for old names
- ✅ All import statements updated

### Acceptance Criteria

- [ ] `Bot` class renamed to `Client`
- [ ] `TUIBot` class renamed to `TUIClient`
- [ ] `bot.py` renamed to `client.py`
- [ ] `tui_bot.py` renamed to `tui_client.py`
- [ ] All imports updated
- [ ] All test files updated
- [ ] Deprecation aliases added for backward compatibility
- [ ] Documentation updated (README, INSTALL, docstrings)
- [ ] CHANGELOG.md documents breaking changes
- [ ] Migration guide created

---

## Technical Architecture

### Scope of Changes

**File Renames**:
```
juiced/lib/bot.py           → juiced/lib/client.py
juiced/tui_bot.py           → juiced/tui_client.py
tests/test_bot.py           → tests/test_client.py
tests/test_bot_handlers.py  → tests/test_client_handlers.py
tests/test_bot_more.py      → tests/test_client_more.py
tests/test_tui_bot.py       → tests/test_tui_client.py
tests/test_tui_bot_extra.py → tests/test_tui_client_extra.py
tests/test_tui_bot_more.py  → tests/test_tui_client_more.py
```

**Class Renames**:
```python
# Core library
class Bot → class Client

# TUI application
class TUIBot(Bot) → class TUIClient(Client)

# Database (if exists)
class BotDatabase → class ClientDatabase (or SessionDatabase)
```

**Import Statement Changes**:
```python
# Old
from juiced.lib.bot import Bot
from juiced.tui_bot import TUIBot
from juiced.lib import Bot

# New
from juiced.lib.client import Client
from juiced.tui_client import TUIClient
from juiced.lib import Client
```

**Variable Name Changes**:
```python
# Old
bot = Bot(...)
tui_bot = TUIBot(...)

# New (in examples/docs)
client = Client(...)
tui = TUIClient(...)
```

**Documentation Updates**:
- README.md: Change "bot" to "client" in descriptions
- INSTALL.md: Update code examples
- Docstrings: "CyTube bot" → "CyTube client"
- Comments: Update bot references
- Error messages: Update terminology

### Backward Compatibility Strategy

**Deprecation Aliases**:
```python
# In juiced/lib/client.py
class Client:
    """CyTube client."""
    pass

# Backward compatibility alias (deprecated)
class Bot(Client):
    """Deprecated: Use Client instead.
    
    This is a backward compatibility alias. The class was renamed
    from Bot to Client in v0.3.0 to better reflect that Juiced is
    a terminal user interface client, not an automated bot.
    
    This alias will be removed in v1.0.0.
    """
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "Bot is deprecated, use Client instead. "
            "This alias will be removed in v1.0.0.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(*args, **kwargs)
```

**Import Compatibility**:
```python
# In juiced/lib/__init__.py
from .client import Client
from .client import Bot  # Deprecated alias

__all__ = [
    'Client',
    'Bot',  # Deprecated, use Client
    # ... other exports
]
```

### Database Considerations

**Current**:
```python
# In bot.py
db_path='bot_data.db'
class BotDatabase
```

**Options**:
1. **Rename to `ClientDatabase`**: Aligns with new naming
2. **Rename to `SessionDatabase`**: More semantically accurate
3. **Keep as `BotDatabase`**: Minimize churn (not recommended)

**Recommendation**: Rename to `SessionDatabase` (more accurate than either "bot" or "client")

---

## Scope and Non-Goals

### Included

- ✅ Rename `Bot` class to `Client`
- ✅ Rename `TUIBot` to `TUIClient`
- ✅ Rename `bot.py` to `client.py`
- ✅ Rename `tui_bot.py` to `tui_client.py`
- ✅ Update all test files
- ✅ Update all imports
- ✅ Add deprecation aliases
- ✅ Update documentation
- ✅ Create migration guide
- ✅ Update CHANGELOG.md

### Explicitly Excluded

- ❌ Renaming local variables in user code (up to users)
- ❌ Renaming database tables/columns (backward compatibility)
- ❌ Renaming git history (keep history intact)
- ❌ Changing API behavior (naming only)
- ❌ Renaming "Rosey-Robot" references (different project)

---

## User Stories

### Story 1: New Contributor Understands Architecture

**As a** new contributor  
**I want** clear naming that reflects what the code does  
**So that** I can understand the system without confusion

**Acceptance Criteria**:
- Class names match what they represent
- "Client" suggests user interaction, not automation
- Documentation and code aligned

### Story 2: Existing User Upgrades

**As an** existing user  
**I want** my code to keep working after upgrade  
**So that** I don't have to rewrite everything immediately

**Acceptance Criteria**:
- Deprecation warnings guide migration
- Old imports still work (with warnings)
- Migration guide provides clear steps

### Story 3: New User Discovers Juiced

**As a** new user reading documentation  
**I want** consistent terminology  
**So that** I understand what Juiced is (client, not bot)

**Acceptance Criteria**:
- README says "client" and code says "Client"
- No confusion about automation expectations
- Clear identity as TUI client

---

## Implementation Plan (High-Level)

### Phase 1: Core Library Rename (4-6 hours)
1. Rename `bot.py` to `client.py`
2. Rename `Bot` class to `Client`
3. Add deprecation alias `Bot = Client`
4. Update internal references in same file
5. Run tests to verify nothing broke

### Phase 2: TUI Rename (3-4 hours)
1. Rename `tui_bot.py` to `tui_client.py`
2. Rename `TUIBot` to `TUIClient`
3. Update imports from `juiced.lib`
4. Add deprecation alias
5. Run tests

### Phase 3: Test Suite Updates (2-3 hours)
1. Rename test files
2. Update imports in all tests
3. Update test class names
4. Update fixture names
5. Run full test suite

### Phase 4: Package Updates (2-3 hours)
1. Update `juiced/__init__.py`
2. Update `juiced/lib/__init__.py`
3. Update imports in utility modules
4. Update any scripts (`juiced.py`, `juiced.bat`)
5. Test package imports

### Phase 5: Documentation (2-3 hours)
1. Update README.md
2. Update INSTALL.md
3. Update all docstrings
4. Update CHANGELOG.md
5. Create MIGRATION.md guide
6. Update sprint planning docs

### Phase 6: Final Validation (1-2 hours)
1. Run full test suite
2. Test actual application startup
3. Verify deprecation warnings work
4. Check all imports resolve
5. Manual smoke testing

---

## Testing Strategy

### Automated Tests

**Import Tests**:
```python
def test_new_imports():
    from juiced.lib.client import Client
    from juiced.tui_client import TUIClient
    assert Client is not None
    assert TUIClient is not None

def test_deprecated_imports_with_warning():
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        from juiced.lib.client import Bot
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "Bot is deprecated" in str(w[0].message)
```

**Functionality Tests**:
- All existing tests must pass with new names
- Deprecation aliases must work identically
- No behavior changes

**Integration Tests**:
- Application starts with new names
- Old imports still work (with warnings)
- Configuration files still work

### Manual Testing Checklist

- [ ] Application starts: `python -m juiced config.yaml`
- [ ] Can connect to server
- [ ] Can send messages
- [ ] Commands work
- [ ] TUI renders correctly
- [ ] Deprecation warnings shown but don't break functionality
- [ ] Fresh install works
- [ ] Upgrade from old version works

---

## Migration Guide Template

```markdown
# Migrating from Bot to Client (v0.2.x → v0.3.0)

## What Changed?

Juiced was renamed from "Bot" to "Client" to better reflect its purpose
as a terminal user interface client, not an automated bot.

## Quick Migration

**Before (v0.2.x)**:
```python
from juiced.lib.bot import Bot
from juiced.tui_bot import TUIBot

bot = Bot(domain, channel)
```

**After (v0.3.0+)**:
```python
from juiced.lib.client import Client
from juiced.tui_client import TUIClient

client = Client(domain, channel)
```

## Backward Compatibility

Old names still work with deprecation warnings:
```python
# Still works, but warns
from juiced.lib.bot import Bot  # DeprecationWarning
```

These aliases will be removed in v1.0.0.

## File Renames

| Old | New |
|-----|-----|
| `juiced/lib/bot.py` | `juiced/lib/client.py` |
| `juiced/tui_bot.py` | `juiced/tui_client.py` |

## Action Required

1. Update imports to use new names
2. Address deprecation warnings
3. Update variable names (optional but recommended)
4. Test your code

## Timeline

- **v0.3.0**: New names introduced, old names deprecated
- **v1.0.0**: Old names removed

Questions? Open an issue!
```

---

## Rollout Plan

### Pre-Release (v0.3.0-alpha)
1. Implement all changes
2. Add deprecation warnings
3. Test thoroughly
4. Alpha testing with volunteers

### Beta Release (v0.3.0-beta)
1. Announce breaking changes
2. Share migration guide
3. Collect feedback
4. Fix issues

### Stable Release (v0.3.0)
1. Finalize documentation
2. Update README badges
3. Tag release
4. Announce widely

### Future (v1.0.0)
1. Remove deprecation aliases
2. Clean breaking change

---

## Dependencies

### Library Requirements
- No new dependencies (pure refactor)

### Infrastructure Needs
- Git file renames (preserve history)
- CI updates (if file paths referenced)

---

## Risk Assessment

### Risks

1. **Breaking existing code**
   - **Mitigation**: Deprecation aliases, clear warnings
   - **Severity**: MEDIUM (mitigated by compatibility layer)

2. **Test failures**
   - **Mitigation**: Update tests incrementally, run frequently
   - **Severity**: LOW (controlled by us)

3. **Documentation lag**
   - **Mitigation**: Update docs in same PR
   - **Severity**: LOW (can catch in review)

4. **User confusion**
   - **Mitigation**: Clear migration guide, changelog
   - **Severity**: MEDIUM (communication is key)

5. **Git history complexity**
   - **Mitigation**: Use `git mv` to preserve history
   - **Severity**: LOW (git handles renames well)

---

## Open Questions

❓ Should we rename `bot_data.db` to `client_data.db` or `session_data.db`?  
**Recommendation**: Keep as `bot_data.db` for backward compatibility, or offer config option

❓ Should we update database class names in this sprint or defer?  
**Recommendation**: Include if simple, defer if complex

❓ Do we need a compatibility shim for Python package name?  
**Recommendation**: No, package is `juiced`, not `juiced_bot`

❓ Timeline for removing deprecation aliases?  
**Recommendation**: v1.0.0 (gives users time to migrate)

---

## Level of Effort (LOE) Analysis

### Detailed Breakdown

| Task | Complexity | Hours | Notes |
|------|------------|-------|-------|
| Core library rename | MEDIUM | 4-6 | Careful with imports |
| TUI rename | MEDIUM | 3-4 | Inherits from core |
| Test suite updates | LOW | 2-3 | Mechanical changes |
| Package/imports | LOW | 2-3 | Update `__init__.py` files |
| Documentation | LOW | 2-3 | Search and replace mostly |
| Deprecation layer | MEDIUM | 2-3 | Warnings, aliases |
| Migration guide | LOW | 1-2 | Template-based |
| Testing & validation | MEDIUM | 2-3 | Thorough testing needed |
| **TOTAL** | **MEDIUM** | **18-27 hours** | **2-3 days** |

### Complexity Factors

**Why MEDIUM Complexity?**
- Large number of files affected (10+ files)
- Risk of breaking changes
- Need careful testing
- Documentation updates extensive
- Deprecation layer adds complexity

**Why Not HIGH?**
- No algorithm changes
- No behavior changes
- Clear, mechanical refactor
- Good test coverage helps
- Can be done incrementally

### Sprint Sizing

**Best Case**: 18 hours (2 days) if everything goes smoothly  
**Realistic**: 22 hours (2.75 days) with normal hiccups  
**Worst Case**: 27 hours (3.5 days) if unexpected issues arise

**Recommendation**: Schedule as **2-3 day sprint** with buffer

---

## Success Criteria

### Definition of Done

- [ ] All files renamed
- [ ] All classes renamed
- [ ] All imports updated
- [ ] Deprecation aliases working
- [ ] All tests passing (90+ tests)
- [ ] No coverage decrease
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Migration guide created
- [ ] Manual testing complete
- [ ] No regressions

### Post-Sprint Validation

- Application starts and connects
- All commands work
- No unexpected warnings (except deprecation)
- Documentation accurate
- Users can migrate successfully

---

## Future Enhancements

### Post-MVP (v1.0.0+)

1. **Remove Deprecation Aliases**: Clean breaking change in v1.0
2. **Rename Database**: Consider `SessionDatabase` instead of `BotDatabase`
3. **API Cleanup**: Review all method names for clarity
4. **Terminology Audit**: Ensure all docs use "client" consistently

---

## References

- [Semantic Versioning](https://semver.org/)
- [Python Deprecation Best Practices](https://peps.python.org/pep-0565/)
- Git file renames: `git mv` preserves history
- Juiced README.md: Already says "terminal chat client"

---

**Document Status**: ✅ Complete  
**Next Step**: Schedule after Sprint 4, plan detailed sorties  
**Estimated Effort**: 18-27 hours (2-3 days)  
**Complexity**: MEDIUM  
**Breaking Changes**: YES (with migration path)  

**Recommendation**: This is a good cleanup sprint to do **after** the quality infrastructure is solid (Sprints 1-4) but **before** v1.0 release. The refactor is mechanical but needs care. Perfect for a focused 2-3 day sprint with clear deliverables.
