# Product Requirements Document: Type Hints Migration

**Sprint**: 3 - Type Hints Migration  
**Feature**: Add type hints and mypy static type checking  
**Status**: 💡 Problem Statement  
**Priority**: MEDIUM  
**Estimated Effort**: 2-3 days (16-24 hours)  
**Target Date**: TBD (after Sprints 1-2)

---

## Executive Summary

Gradually add Python type hints to the codebase and integrate mypy for static type checking. This will catch type-related bugs before runtime, improve IDE autocompletion, and make the codebase more maintainable and self-documenting.

**Key Value Proposition**: Catch bugs at development time, improve code clarity, better IDE support.

---

## Problem Statement

### What problem are we solving?

Currently, the codebase has minimal or no type hints:
- Function parameters lack type annotations
- Return types are not specified
- IDE autocompletion is limited
- Type errors only discovered at runtime
- Code intent is unclear without reading implementation
- AGENTS.md requires "type hints on all functions"

**Example of current state**:
```python
def get_socket_config(self, url):
    # What type is url? What does this return?
    ...
```

**Example of desired state**:
```python
def get_socket_config(self, url: str) -> dict[str, Any]:
    # Clear contract: takes string, returns dict
    ...
```

### Who is affected?

- **Developers**: Harder to understand code without hints
- **IDE Users**: Poor autocompletion and navigation
- **Reviewers**: Must infer types from context
- **New Contributors**: Steeper learning curve

### Why now?

- Code quality foundation established (Sprint 1)
- Test coverage improved (Sprint 2)
- Project is stable - good time to add hints
- Prevents accumulation of untyped code
- Modern Python best practice (3.11+ standard)

---

## Goals and Success Metrics

### Goals

1. **Primary**: Add type hints to all public functions
2. **Secondary**: Configure mypy and integrate with CI
3. **Tertiary**: Achieve mypy clean pass (no errors)

### Success Metrics

- ✅ mypy configured in pyproject.toml
- ✅ All public functions have type hints
- ✅ Core modules pass mypy without errors
- ✅ Pre-commit hook runs mypy (optional)
- ✅ CI enforces type checking
- ✅ Documentation updated with type hint guidelines

---

## Technical Architecture

### Type Hint Strategy

**Phase 1: Low-hanging Fruit**
- Simple functions with obvious types
- Function parameters and return types
- Use built-in types (str, int, bool, list, dict)

**Phase 2: Complex Types**
- Generic types (List[str], Dict[str, Any])
- Optional types (Optional[str], str | None)
- Async types (Awaitable, Coroutine)

**Phase 3: Custom Types**
- TypedDict for structured dictionaries
- Protocol for duck typing
- Type aliases for clarity

**Phase 4: Strict Mode**
- Enable strict mypy checks
- Disallow untyped definitions
- Enforce on all new code

### Module Priority

| Priority | Module | Reason |
|----------|--------|--------|
| HIGH | bot.py | Core logic, many functions |
| HIGH | tui_bot.py | Complex interactions |
| MEDIUM | socket_io.py | Async patterns |
| MEDIUM | proxy.py | Network types |
| LOW | util.py | Helper functions |
| LOW | config.py | Already simple |

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Start lenient
check_untyped_defs = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
check_untyped_defs = false

[[tool.mypy.overrides]]
module = "socketio.*"
ignore_missing_imports = true
```

---

## Scope and Non-Goals

### Included

- ✅ Type hints for all public functions
- ✅ mypy configuration and CI integration
- ✅ Fix type errors in core modules
- ✅ Documentation of type hint patterns
- ✅ IDE configuration guidance

### Explicitly Excluded

- ❌ Strict mode enforcement (gradual migration)
- ❌ Third-party stubs creation (use ignore if needed)
- ❌ Runtime type checking (pydantic, etc.)
- ❌ Full codebase migration (focus on public APIs)

---

## User Stories

### Story 1: Developer Writes New Function

**As a** developer  
**I want** type hints on all functions  
**So that** my IDE can provide accurate autocomplete

**Acceptance Criteria**:
- IDE shows parameter types
- IDE suggests correct methods
- mypy catches type errors before runtime

### Story 2: Reviewer Reads Code

**As a** code reviewer  
**I want** clear type annotations  
**So that** I understand function contracts without reading implementation

**Acceptance Criteria**:
- Function signature shows input/output types
- Complex types documented
- No need to infer types from code

### Story 3: New Contributor Learns Codebase

**As a** new contributor  
**I want** type hints for guidance  
**So that** I know what types to pass to functions

**Acceptance Criteria**:
- Type errors caught by mypy
- Clear error messages
- Examples in documentation

---

## Acceptance Criteria

- [ ] mypy installed and configured
- [ ] pyproject.toml has mypy settings
- [ ] All public functions in bot.py have type hints
- [ ] All public functions in tui_bot.py have type hints
- [ ] Core modules pass mypy check
- [ ] CI runs mypy and fails on errors
- [ ] Pre-commit runs mypy (optional)
- [ ] Documentation updated with examples
- [ ] IDE configuration guide added

---

## Dependencies

### Library Requirements

```txt
mypy>=1.7.0
types-PyYAML>=6.0.0  # Stubs for yaml
# Add more as needed for third-party libraries
```

### Infrastructure Needs

- CI step for mypy
- Optional: pre-commit hook for mypy
- IDE extensions (already available)

---

## Rollout Plan

### Phase 1: Setup (2-3 hours)
1. Install mypy
2. Create basic mypy.ini or add to pyproject.toml
3. Run mypy to see current state
4. Document findings

### Phase 2: Easy Modules (4-6 hours)
1. Add hints to config.py, util.py
2. Fix any mypy errors
3. Commit and test

### Phase 3: Core Modules (6-8 hours)
1. Add hints to bot.py (incrementally)
2. Add hints to tui_bot.py (incrementally)
3. Fix errors as they arise
4. Commit frequently

### Phase 4: CI Integration (2-3 hours)
1. Add mypy to CI workflow
2. Configure pre-commit (optional)
3. Update documentation
4. Verify CI catches type errors

---

## Future Enhancements

### Post-MVP

1. **Strict Mode**: Enable strict mypy checks
2. **Runtime Validation**: Add pydantic for runtime type checking
3. **Third-party Stubs**: Create stubs for untyped libraries
4. **Protocol Types**: Use protocols for duck typing
5. **Literal Types**: Use Literal for constant values
6. **TypeGuard**: Use TypeGuard for type narrowing

---

## Open Questions

❓ Should mypy run in pre-commit (may slow down commits)?  
❓ Start with strict=False or strict=True?  
❓ How to handle third-party libraries without stubs?  
❓ Should we use type: ignore comments or fix all issues?

---

## References

- [mypy documentation](https://mypy.readthedocs.io/)
- [Python type hints (PEP 484)](https://peps.python.org/pep-0484/)
- [typing module docs](https://docs.python.org/3/library/typing.html)
- [Real Python: Type Checking Guide](https://realpython.com/python-type-checking/)

---

**Document Status**: ✅ Problem Statement Complete  
**Next Step**: Detailed planning after Sprint 2  
**Estimated Sorties**: 5-6 (setup, easy modules, core modules, CI, docs, refinement)
