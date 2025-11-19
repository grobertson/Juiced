# Product Requirements Document: Test Coverage Improvement

**Sprint**: 2 - Test Coverage Improvement  
**Feature**: Increase test coverage from 68% to 75%  
**Status**: 📝 Drafted  
**Priority**: MEDIUM  
**Estimated Effort**: 1-2 days (8-16 hours)  
**Target Date**: TBD (after Sprint 1)

---

## Executive Summary

Increase test coverage from current 68% to target 75% by adding tests for untested code paths in core modules. Focus on `bot.py` handlers (62% coverage), `tui_bot.py` UI methods (66%), `proxy.py` (63%), and `socket_io.py` (69%).

**Key Value Proposition**: Higher confidence in code correctness, fewer production bugs, easier refactoring.

---

## Problem Statement

### What problem are we solving?

Current coverage at 68% exceeds the 60% minimum but leaves significant gaps:
- **bot.py**: 219 lines untested (event handlers, error paths)
- **tui_bot.py**: 405 lines untested (UI rendering, command handling)
- **proxy.py**: Untested proxy connection scenarios
- **socket_io.py**: Missing tests for reconnection logic

These gaps mean:
1. Bugs may exist in untested code paths
2. Refactoring is risky without test coverage
3. New contributors don't know if their changes break things
4. AGENTS.md recommends 85% coverage, we're at 68%

### Who is affected?

- **Developers**: Less confidence when modifying code
- **Users**: May encounter bugs in untested scenarios
- **Project**: Technical debt accumulates

### Why now?

- Code quality sprint (Sprint 1) establishes testing foundation
- Coverage infrastructure already in place
- Codebase is stable - good time to add tests
- Want to hit 75% before adding new features

---

## Goals and Success Metrics

### Goals

1. **Primary**: Increase coverage from 68% to 75% overall
2. **Secondary**: Achieve 70%+ on all core modules (bot.py, tui_bot.py, etc.)
3. **Tertiary**: Document testing patterns for future contributors

### Success Metrics

- ✅ Overall coverage: 75% (up from 68%)
- ✅ bot.py coverage: 70%+ (up from 62%)
- ✅ tui_bot.py coverage: 70%+ (up from 66%)
- ✅ proxy.py coverage: 70%+ (up from 63%)
- ✅ socket_io.py coverage: 75%+ (up from 69%)
- ✅ All new tests pass
- ✅ No decrease in existing coverage
- ✅ Documentation updated with testing patterns

---

## Technical Architecture

### Coverage Analysis

**Current State** (from coverage report):

| Module | Coverage | Statements | Missed | Priority |
|--------|----------|------------|--------|----------|
| bot.py | 62% | 579 | 219 | HIGH |
| tui_bot.py | 66% | 1176 | 405 | HIGH |
| proxy.py | 63% | ? | ? | MEDIUM |
| socket_io.py | 69% | ? | ? | MEDIUM |

**Target State**:

| Module | Target | Additional Tests | Focus Areas |
|--------|--------|------------------|-------------|
| bot.py | 70% | ~50 | Event handlers, error paths |
| tui_bot.py | 70% | ~50 | UI rendering, command dispatch |
| proxy.py | 70% | ~20 | Connection scenarios |
| socket_io.py | 75% | ~15 | Reconnection logic |

### Testing Strategy by Module

**bot.py** - Focus on:
- Event handlers (onChatMsg, onUserJoin, etc.)
- Error handling paths
- Socket configuration edge cases
- Connection failures

**tui_bot.py** - Focus on:
- Command dispatch and parsing
- UI rendering functions
- Theme application
- Error display

**proxy.py** - Focus on:
- Proxy connection establishment
- Authentication scenarios
- Timeout handling
- Error conditions

**socket_io.py** - Focus on:
- Reconnection attempts
- Event emission failures
- Socket state transitions
- Error callbacks

---

## Scope and Non-Goals

### Included

- ✅ Add ~135 new test cases across 4 modules
- ✅ Cover missed branches and error paths
- ✅ Mock external dependencies (network, file I/O)
- ✅ Update TESTS.md with testing patterns
- ✅ Verify no performance regression

### Explicitly Excluded

- ❌ Refactoring existing code (test as-is)
- ❌ Achieving 85% coverage (stretch goal for future)
- ❌ Adding integration tests (focus on unit tests)
- ❌ Performance testing (different sprint)

---

## User Stories

### Story 1: Developer Modifies Event Handler

**As a** developer  
**I want** comprehensive tests for event handlers  
**So that** I can modify them confidently without breaking functionality

**Acceptance Criteria**:
- All event handlers in bot.py have tests
- Both success and error paths tested
- Mock socket events for testing

### Story 2: Contributor Adds New Command

**As a** contributor  
**I want** examples of command tests  
**So that** I can write tests for my new command

**Acceptance Criteria**:
- TESTS.md documents command testing patterns
- Example tests show mocking user input
- Coverage requirements clearly stated

### Story 3: Maintainer Reviews PR

**As a** maintainer  
**I want** coverage reports in CI  
**So that** I can see if PRs decrease coverage

**Acceptance Criteria**:
- CI shows coverage diff
- PRs blocked if coverage decreases
- Clear guidance on adding tests

---

## Acceptance Criteria

- [ ] Overall coverage ≥ 75%
- [ ] bot.py coverage ≥ 70%
- [ ] tui_bot.py coverage ≥ 70%
- [ ] proxy.py coverage ≥ 70%
- [ ] socket_io.py coverage ≥ 75%
- [ ] All tests pass (90+ existing + new)
- [ ] No performance regression
- [ ] TESTS.md updated with patterns
- [ ] Coverage enforced in CI

---

## Dependencies

### Library Requirements

- pytest (existing)
- pytest-cov (existing)
- pytest-mock (may need to add)
- pytest-asyncio (existing)

### Infrastructure Needs

- CI coverage reporting (GitHub Actions)
- Coverage badge in README (optional)

---

## Rollout Plan

### Phase 1: Analysis (2-3 hours)
1. Run coverage with `--cov-report=html`
2. Identify specific untested lines
3. Categorize by complexity (easy/medium/hard)
4. Create sortie breakdown

### Phase 2: Easy Wins (2-3 hours)
- Test simple functions
- Cover obvious error paths
- Low-hanging fruit

### Phase 3: Complex Tests (4-6 hours)
- Mock heavy async functions
- Test event handlers
- Test UI rendering

### Phase 4: Documentation (2 hours)
- Update TESTS.md
- Add testing patterns
- Update CI to enforce 75%

---

## Future Enhancements

### Post-MVP

1. **Increase to 85%** (AGENTS.md target)
2. **Add integration tests** (end-to-end flows)
3. **Mutation testing** (test quality, not just coverage)
4. **Property-based testing** (hypothesis library)
5. **Performance regression tests**

---

## Open Questions

❓ Should we enforce 75% on all new code?  
❓ Do we need integration tests in this sprint or defer?  
❓ Should we add coverage badge to README?

---

**Document Status**: ✅ Draft Complete  
**Next Step**: Create sortie specifications after Sprint 1  
**Estimated Sorties**: 4-5 (will finalize during planning)
