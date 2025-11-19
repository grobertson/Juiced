# Agent-Assisted Development Workflow

**Methodology**: Nano-Sprint Development with AI Agents  
**Version**: 1.0  
**Last Updated**: November 18, 2025  

---

## Overview

This document defines a **structured agent-assisted development workflow** for rapid, high-quality feature delivery. By leveraging AI coding agents (GitHub Copilot, Claude, ChatGPT, etc.) within a disciplined planning framework, teams can accelerate development while maintaining code quality, test coverage, and documentation standards.

### Core Principles

1. **Planning First**: Write comprehensive PRDs and specs before writing code
2. **Nano-Sprints**: Small, focused development cycles (1 day or less)
3. **Sorties**: Logical bundles of changes within a sprint (1+ commits per sortie)
4. **Rolling Planning**: Maintain 1-4 sprints ahead in the backlog
5. **Agent Collaboration**: Use AI for implementation, testing, and documentation
6. **Documentation-Driven**: Keep docs current as code evolves
7. **Iterative Refinement**: Build incrementally, test continuously

---

## The Workflow

```
Plan → Specify → Implement → Document → Review → Merge → Repeat
  ↓        ↓          ↓           ↓          ↓        ↓
 PRD    Sorties    Code+Tests    Guides     PR      Main
```

### Rolling Sprint Planning

**Always maintain 1-4 sprints ahead in the backlog:**

- **Current Sprint** (N): Actively implementing
- **Next Sprint** (N+1): Fully planned with PRD and sortie specs
- **Future Sprint 1** (N+2): PRD drafted, rough sortie outline
- **Future Sprint 2** (N+3): Feature ideas, problem statements
- **Future Sprint 3** (N+4): Optional - strategic roadmap items

**Why?** This ensures you never block on planning and can pivot quickly based on learnings from completed sprints.

---

## Phase 1: Product Requirements Document (PRD)

**Purpose**: Define what and why before how

**Format**: `docs/{N}-{sprint-name}/PRD-{feature-name}.md`

### Required Sections

1. **Executive Summary**
   - One-paragraph feature overview
   - Key value proposition

2. **Problem Statement**
   - What problem are we solving?
   - Who is affected?
   - Why now?

3. **Goals and Success Metrics**
   - Measurable outcomes
   - Acceptance criteria
   - Performance targets

4. **User Stories**
   - As a [user], I want [capability] so that [benefit]
   - Detailed scenarios and edge cases

5. **Technical Architecture**
   - System design and component interactions
   - Data flow diagrams
   - API contracts

6. **Dependencies**
   - External services
   - Library requirements
   - Infrastructure needs

7. **Security and Privacy**
   - Data sensitivity
   - Authentication/authorization
   - Compliance requirements

8. **Rollout Plan**
   - Deployment phases
   - Feature flags
   - Monitoring and alerts

9. **Future Enhancements**
   - Post-MVP features
   - Technical debt to address

10. **Open Questions**
    - Unresolved decisions
    - Risks and mitigations

### Agent Prompt for PRD Generation

```markdown
**Context**: [Brief description of current system state]

**Task**: Create a comprehensive PRD for [feature name]

**Requirements**:
- Problem: [What problem does this solve?]
- Users: [Who benefits?]
- Constraints: [Technical or business limitations]

**Include**:
1. Executive summary and problem statement
2. User stories with acceptance criteria
3. Technical architecture with diagrams
4. Security and privacy considerations
5. Rollout plan with success metrics
6. Future enhancements roadmap

**Format**: Use markdown with clear section headers
```

---

## Phase 2: Sortie Specifications

**Purpose**: Break PRD into implementable, testable work units

**Format**: `docs/{N}-{sprint-name}/SPEC-Sortie-{M}-{sortie-name}.md`

### What is a Sortie?

A **sortie** is a logical bundle of related changes:
- May contain 1 or more commits
- Should be completable in 2-6 hours
- Must be independently testable
- Has clear acceptance criteria

**Nano-Sprint = Collection of Sorties**

### Required Sections

1. **Overview**
   - What this sortie achieves
   - Why it's a logical unit

2. **Scope and Non-Goals**
   - What's included
   - What's explicitly excluded (to prevent scope creep)

3. **Requirements**
   - Functional requirements
   - Non-functional requirements (performance, security, etc.)

4. **Design**
   - Architecture diagrams
   - Data structures
   - Algorithms
   - API interfaces

5. **Implementation Plan**
   - Files to modify
   - New files to create
   - Methods/functions to add
   - Configuration changes

6. **Testing Strategy**
   - Unit tests to write
   - Integration tests
   - Manual testing checklist
   - Performance benchmarks

7. **Acceptance Criteria**
   - Concrete checkboxes for completion
   - Each criterion must be verifiable

8. **Rollout**
   - Deployment steps
   - Database migrations
   - Configuration updates

9. **Documentation**
   - Code comments needed
   - User-facing docs to update
   - Architecture docs to revise

### Agent Prompt for Sortie Specs

```markdown
**Context**: Given PRD at docs/{N}-{sprint-name}/PRD-{feature}.md

**Task**: Break this into [X] sorties that can be implemented sequentially

**Requirements**:
- Each sortie = 2-6 hours of work
- Each sortie is independently testable
- Clear dependencies between sorties
- Include implementation details (files, methods, tests)

**Output**: Create SPEC-Sortie-{M}-{name}.md for each sortie

**Format**: Follow the sortie template with all 9 sections
```

---

## Phase 3: Implementation

**Purpose**: Execute the spec with agent assistance

### Step-by-Step Process

#### 1. Read the Spec

```markdown
**Agent Prompt**:
"Read SPEC-Sortie-{M}-{name}.md and summarize:
1. Files to modify
2. New code to write
3. Tests to create
4. Acceptance criteria"
```

#### 2. Implement Code

```markdown
**Agent Prompt**:
"Implement section 5 (Implementation Plan) from SPEC-Sortie-{M}-{name}.md

**Current State**: [Describe existing code]

**Requirements**:
- Follow existing code style and conventions
- Add docstrings/comments as specified
- Include type hints (if applicable)
- Handle error cases

**Verify**: Cross-check against acceptance criteria in section 7"
```

#### 3. Write Tests

```markdown
**Agent Prompt**:
"Create tests for the code we just implemented

**Requirements**:
- Unit tests for each new function/method
- Integration tests for end-to-end flows
- Edge case coverage
- Mock external dependencies

**Location**: [Specify test file paths]

**Coverage Target**: [e.g., 85%]"
```

#### 4. Run Tests and Verify

```bash
# Run tests
pytest --cov --cov-report=term-missing

# Run linter
flake8 .

# Check type hints
mypy src/
```

#### 5. Commit Changes

```bash
git add .
git commit -m "[Sortie M]: Brief title

- Detailed change 1
- Detailed change 2
- Detailed change 3

Implements: SPEC-Sortie-{M}-{name}.md
Related: PRD-{feature}.md
Tests: [Brief test summary]"
```

### Commit Message Guidelines

**Format**:
```
[Sortie N]: Short title (50 chars max)

- Bullet point for each significant change
- Focus on WHAT changed and WHY
- Reference files/modules

Implements: SPEC-Sortie-{N}-{name}.md
Related: PRD-{feature}.md
Fixes: #issue-number (if applicable)
```

**Rules**:
- One logical change per commit
- Each commit must compile/run
- Each commit must pass tests
- All commits squashed on PR merge

---

## Phase 4: Documentation

**Purpose**: Keep documentation synchronized with code

### Types of Documentation

#### 4.1 Code Documentation

- **Docstrings**: For all public APIs
- **Inline Comments**: For complex logic (why, not what)
- **Type Hints**: For function signatures

**Agent Prompt**:
```markdown
"Add comprehensive docstrings to [file.py]

**Requirements**:
- Use [Google/Numpy/Sphinx] style
- Document parameters, return values, exceptions
- Include usage examples for complex functions
- Explain side effects"
```

#### 4.2 User Documentation

- **README.md**: Feature list, quick start, installation
- **Feature Guides**: Step-by-step usage instructions
- **API Reference**: Endpoint documentation
- **Configuration Guide**: All available settings

**Agent Prompt**:
```markdown
"Update README.md to include [feature name]

**Add**:
1. Feature description in main list
2. Quick start example
3. Configuration section
4. Link to detailed guide

**Style**: Match existing README tone and formatting"
```

#### 4.3 Architecture Documentation

- **ARCHITECTURE.md**: System overview and component diagrams
- **Data Flow**: How information moves through the system
- **Extension Points**: Where developers can add functionality

#### 4.4 Operations Documentation

- **Deployment Guide**: How to deploy
- **Monitoring**: What to monitor and why
- **Troubleshooting**: Common issues and fixes

---

## Phase 5: Review and Merge

**Purpose**: Quality gate before integration

### 1. Self-Review

**Agent Prompt**:
```markdown
"Review all changes in this nano-sprint for:

**Code Quality**:
- Follows project conventions?
- No code smells or anti-patterns?
- Appropriate abstraction levels?

**Testing**:
- Adequate test coverage?
- Edge cases handled?
- Integration points tested?

**Security**:
- Input validation?
- Authentication/authorization?
- Sensitive data handling?

**Performance**:
- No obvious bottlenecks?
- Efficient algorithms?
- Resource usage acceptable?

**Documentation**:
- All public APIs documented?
- User guides updated?
- CHANGELOG.md updated?

**Output**: List of issues found with suggestions"
```

### 2. Create Pull Request

**Title**: `[Sprint N: {sprint-name}] {Feature name}`

**Description Template**:
```markdown
## Summary
[Brief description of what this PR does]

## Related Documents
- PRD: docs/{N}-{sprint-name}/PRD-{feature}.md
- Sorties: SPEC-Sortie-1 through SPEC-Sortie-{M}

## Changes
- [Sortie 1]: [Brief description]
- [Sortie 2]: [Brief description]
- [Sortie M]: [Brief description]

## Testing
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing completed
- [ ] Coverage: [X]%

## Checklist
- [ ] Code follows project style guide
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
- [ ] Performance impact assessed
- [ ] Security review completed

## Screenshots/Demo
[If UI changes, include screenshots or demo link]
```

### 3. Automated Checks

Run CI/CD pipeline:
- Linting
- Type checking
- Unit tests
- Integration tests
- Code coverage
- Security scanning

### 4. Agent-Assisted Code Review

**Agent Prompt**:
```markdown
"Act as a senior code reviewer. Review this PR for:

**Correctness**:
- Does implementation match specification?
- Are there logical errors?
- Edge cases handled?

**Maintainability**:
- Code is readable?
- Appropriate abstractions?
- DRY principle followed?

**Testing**:
- Test coverage adequate?
- Tests are meaningful?
- Tests are maintainable?

**Security**:
- Input validation present?
- No injection vulnerabilities?
- Secure defaults?

**Performance**:
- Efficient algorithms used?
- No unnecessary computation?
- Caching where appropriate?

**Documentation**:
- Code self-documenting?
- Complex logic explained?
- User docs complete?

**Output**: Detailed review with line-specific comments and suggestions"
```

### 5. Merge to Main

Once approved:
```bash
# Squash merge (recommended for nano-sprints)
git merge --squash feature/sprint-N

# Update CHANGELOG
# Update version if needed
# Tag release
git tag -a v1.2.3 -m "Release v1.2.3: [Feature name]"
git push origin main --tags
```

---

## Sprint Planning Strategy

### The 1-4 Sprint Rule

**Always maintain rolling visibility:**

| Sprint | Status | Effort | Details |
|--------|--------|--------|---------|
| **N** (Current) | 🚀 In Progress | Full implementation | All sorties specified, actively coding |
| **N+1** (Next) | 📋 Planned | PRD + Sortie specs | Ready to start immediately |
| **N+2** (Future 1) | 📝 Drafted | PRD + rough outline | High-level breakdown |
| **N+3** (Future 2) | 💡 Ideation | Problem statement | Feature concepts |
| **N+4** (Future 3) | 🎯 Optional | Strategic goals | Long-term roadmap |

### When to Plan

- **During Sprint N**: Finalize specs for N+1, draft PRD for N+2
- **Sprint Retrospective**: Review N, adjust N+1, plan N+2
- **Weekly Planning**: Update N+2 and N+3
- **Monthly Review**: Adjust strategic direction for N+4

### Planning Sessions with Agent

**Monthly Sprint Planning**:
```markdown
"Review completed sprints [list] and upcoming features [list]

**Task**: Plan next 4 sprints

**For Sprint N+1** (next):
- Create PRD for [feature]
- Break into sorties
- Estimate effort

**For Sprint N+2**:
- Draft PRD for [feature]
- Identify dependencies
- Rough sortie outline

**For Sprint N+3**:
- Problem statement for [feature]
- User stories
- Technical feasibility

**For Sprint N+4**:
- Strategic goals
- Research needed
- Exploratory work

**Output**: 
- 4 PRD files at appropriate detail levels
- Dependency map
- Risk assessment"
```

---

## Directory Structure

### Standard Layout

```
project-root/
├── docs/
│   ├── 1-{sprint-name}/
│   │   ├── PRD-{feature}.md
│   │   ├── SPEC-Sortie-1-{name}.md
│   │   ├── SPEC-Sortie-2-{name}.md
│   │   └── ...
│   ├── 2-{sprint-name}/
│   │   └── ...
│   ├── 3-{sprint-name}/
│   │   └── ...
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── {FEATURE}_GUIDE.md
├── src/                      # Source code
├── tests/                    # Test files
├── AGENTS.md                 # This workflow guide
├── README.md                 # Project overview
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
└── ...
```

### Sprint Naming Convention

**Format**: `{number}-{descriptive-name}`

**Examples**:
- `1-foundation` - Initial setup and core features
- `2-authentication` - User auth system
- `3-api-endpoints` - REST API implementation
- `4-database-migration` - Move to new DB
- `5-deployment-pipeline` - CI/CD setup
- `5a-hotfix-security` - Critical security fix (interrupt sprint)

**Sub-sprints**: Use letters (5a, 5b) for unplanned but necessary work that interrupts the main sequence.

---

## Agent Prompting Patterns

### Pattern 1: Feature Planning

```markdown
**Context**: [Describe current system state]

**Goal**: Add [feature description]

**Task**: Create a comprehensive PRD

**Include**:
1. Executive summary (why this feature matters)
2. Problem statement (what problem it solves)
3. User stories (who benefits and how)
4. Technical architecture (how it works)
5. Security considerations (data protection, auth)
6. Implementation plan (phases, timeline)
7. Success metrics (how we measure success)

**Constraints**:
- [Technical constraint 1]
- [Business constraint 2]
- [Time constraint 3]

**Format**: Markdown with sections as specified above

**Output**: Complete PRD ready for sprint planning
```

### Pattern 2: Sortie Breakdown

```markdown
**Context**: PRD at docs/{N}-{sprint}/PRD-{feature}.md

**Task**: Break into implementable sorties

**Requirements**:
- Each sortie = 2-6 hours work
- Sorties have clear dependencies
- Each sortie independently testable
- Include implementation details

**For Each Sortie**:
1. Overview (what it accomplishes)
2. Files to modify
3. Methods/functions to add
4. Tests to write
5. Acceptance criteria (checkboxes)

**Estimate**: Sprint should be 1 day total (8 hours)

**Output**: SPEC-Sortie-{M}-{name}.md for each sortie
```

### Pattern 3: Implementation

```markdown
**Context**: Implement SPEC-Sortie-{M}-{name}.md

**Current State**: 
- Read: [list relevant files]
- Summarize: [key classes/functions]

**Task**: Implement section 5 (Implementation Plan)

**Requirements**:
- Follow existing code style
- Add [docstring style] documentation
- Include type hints
- Handle errors gracefully
- Log important events

**Verification**: Check acceptance criteria (section 7)

**Output**: Implementation code ready for testing
```

### Pattern 4: Testing

```markdown
**Context**: We just implemented [feature/component]

**Task**: Create comprehensive test suite

**Requirements**:

**Unit Tests**:
- Test each public method
- Test edge cases
- Test error conditions
- Mock external dependencies

**Integration Tests**:
- Test component interactions
- Test end-to-end flows
- Test with real dependencies (if safe)

**Coverage Target**: [X]%

**Test Files**: [Specify locations]

**Output**: Complete test suite with passing tests
```

### Pattern 5: Documentation

```markdown
**Context**: Feature [X] implemented in [files]

**Task**: Update all documentation

**User Documentation**:
- README.md: Add to features list
- Create docs/{FEATURE}_GUIDE.md
- Update QUICKSTART.md if needed

**Developer Documentation**:
- ARCHITECTURE.md: Add components/diagrams
- API_REFERENCE.md: Document new endpoints
- Add code comments for complex logic

**Operations Documentation**:
- Update deployment guide if needed
- Add monitoring/alerting info
- Update troubleshooting guide

**Style**: Match existing documentation tone and format

**Output**: All docs updated and consistent
```

### Pattern 6: Code Review

```markdown
**Context**: Review PR for Sprint {N}: {feature}

**Files Changed**: [List]

**Task**: Comprehensive code review

**Check**:

1. **Correctness**
   - Matches specification?
   - Logic is sound?
   - Edge cases handled?

2. **Code Quality**
   - Follows style guide?
   - DRY principle?
   - Appropriate abstractions?

3. **Testing**
   - Adequate coverage?
   - Meaningful tests?
   - Integration tests present?

4. **Security**
   - Input validation?
   - SQL injection prevention?
   - XSS prevention?
   - Sensitive data handling?

5. **Performance**
   - Efficient algorithms?
   - No N+1 queries?
   - Caching appropriate?

6. **Documentation**
   - Public APIs documented?
   - Complex logic explained?
   - User docs updated?

**Output**: Detailed review with specific suggestions and line numbers
```

### Pattern 7: Sprint Retrospective

```markdown
**Context**: Sprint {N} complete

**Completed Sorties**: [List]

**Metrics**:
- Planned time: [X] hours
- Actual time: [Y] hours
- Test coverage: [Z]%
- Bugs found post-merge: [N]

**Task**: Sprint retrospective and plan next sprint

**Analyze**:
1. What went well?
2. What went poorly?
3. What surprised us?
4. Where did we over/underestimate?
5. Technical debt created?

**Action Items**:
- Process improvements
- Documentation gaps to fill
- Refactoring needed

**Next Sprint**:
- Review Sprint {N+1} PRD
- Adjust based on learnings
- Update effort estimates

**Output**: 
- Retrospective summary
- Action items list
- Updated Sprint {N+1} plan
```

---

## Best Practices

### Working with AI Agents

#### ✅ Do's

1. **Provide Context**: Reference files, docs, existing patterns
2. **Be Specific**: Vague requests → vague results
3. **Iterate**: Refine through conversation
4. **Verify**: Always review generated code
5. **Document Decisions**: Capture rationale in comments
6. **Use Templates**: Consistent prompts → consistent results
7. **Break Down**: Complex tasks → smaller subtasks

#### ❌ Don'ts

1. **Don't Skip Planning**: Never code without PRD/specs
2. **Don't Trust Blindly**: AI makes mistakes
3. **Don't Merge Without Review**: Test everything
4. **Don't Ignore Warnings**: Address security/performance concerns
5. **Don't Skip Tests**: Coverage < 85% → not done
6. **Don't Forget Docs**: Update docs with code
7. **Don't Over-Optimize**: Premature optimization is evil

### Code Quality Standards

#### Language-Agnostic

- **Clear Naming**: Variables, functions, classes
- **Single Responsibility**: Each unit does one thing
- **DRY**: Don't repeat yourself
- **YAGNI**: You aren't gonna need it
- **Test First**: Write tests with/before code
- **Document Why**: Comments explain rationale, not mechanics

#### Language-Specific

**Python**:
- Type hints on all functions
- Google/Numpy docstrings
- PEP 8 style
- 85%+ test coverage
- async/await for I/O

**JavaScript/TypeScript**:
- TypeScript for type safety
- JSDoc comments
- ESLint + Prettier
- Jest for testing
- async/await, avoid callbacks

**Go**:
- gofmt for formatting
- golint for style
- Table-driven tests
- Error handling explicit
- Defer for cleanup

**Rust**:
- rustfmt for formatting
- clippy for lints
- Result<T, E> for errors
- Comprehensive tests
- Documentation examples

---

## Troubleshooting

### Agent Not Following Spec

**Problem**: Generated code doesn't match specification

**Solution**:
```markdown
"The generated code doesn't match section [X] of the spec.

**Specific Issues**:
- [Issue 1]
- [Issue 2]

Please re-read SPEC-Sortie-{M}-{name}.md section [X] and regenerate code to match exactly:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]"
```

### Inconsistent Code Style

**Problem**: Agent uses different patterns than existing code

**Solution**:
```markdown
"Review existing code in [file.ext] for style patterns:
- [Pattern 1]
- [Pattern 2]

Then regenerate [new code] to match:
- Same naming conventions
- Same error handling approach
- Same documentation style
- Same testing patterns

Show me the diff before applying."
```

### Missing Edge Cases

**Problem**: Agent doesn't consider error scenarios

**Solution**:
```markdown
"Review [implementation] for edge cases:

**Consider**:
- What if input is null/empty/invalid?
- What if external service is down?
- What if database connection fails?
- What if user has insufficient permissions?
- What if rate limit is exceeded?
- What if data is corrupt?

Add error handling for each scenario with:
- Appropriate exception types
- Helpful error messages
- Logging
- Graceful degradation"
```

### Incomplete Documentation

**Problem**: Generated docs lack examples or details

**Solution**:
```markdown
"Expand [doc file] with:

**Add**:
1. Quick start (< 5 minutes to running)
2. Step-by-step setup guide
3. Configuration examples (at least 3 scenarios)
4. API reference (all endpoints/methods)
5. Troubleshooting section (top 5 issues)
6. FAQ (at least 10 questions)

**For Each Section**:
- Include code examples
- Show expected output
- Explain common mistakes

**Style**: Conversational, beginner-friendly"
```

---

## Metrics and Success

### Track These Metrics

1. **Velocity**
   - Sorties per sprint
   - Story points per sprint
   - Sprint completion rate

2. **Quality**
   - Test coverage %
   - Bugs per sprint
   - Production incidents
   - Code review feedback count

3. **Efficiency**
   - Plan time vs. implement time
   - Estimate accuracy
   - Rework rate

4. **Agent Effectiveness**
   - Time saved vs. manual coding
   - First-pass acceptance rate
   - Prompt iteration count

### Success Criteria

**Sprint is Successful When**:
- All sorties completed
- All acceptance criteria met
- Test coverage ≥ 85%
- Documentation updated
- PR merged to main
- No critical bugs in production

**Process is Successful When**:
- Team velocity is predictable
- Estimate accuracy > 80%
- Agent-generated code requires minimal revision
- Documentation stays current
- Technical debt is managed

---

## Advanced Workflows

### Multi-Agent Collaboration

For complex sprints, use specialized agents:

1. **Architect Agent**: System design, component interactions
2. **Implementation Agent**: Code generation, refactoring
3. **Testing Agent**: Test generation, coverage analysis
4. **Documentation Agent**: User guides, API references
5. **Review Agent**: Code review, security analysis

**Workflow**:
```
PRD → Architect Agent (design)
    → Implementation Agent (code)
    → Testing Agent (tests)
    → Documentation Agent (docs)
    → Review Agent (review)
    → Human (approve)
```

### Continuous Refinement

**Weekly Maintenance Prompt**:
```markdown
"Review codebase for maintenance needs:

**Dependencies**:
- Check for outdated packages
- Security vulnerabilities?
- Deprecated features?

**Code Quality**:
- Identify code smells
- Find duplicated code
- Spot missing tests

**Documentation**:
- Undocumented features?
- Outdated guides?
- Broken links?

**Performance**:
- Profile slow operations
- Identify bottlenecks
- Suggest optimizations

**Output**: Prioritized maintenance backlog with effort estimates"
```

### Knowledge Transfer

**Onboarding New Team Members**:
```markdown
"Create an ONBOARDING.md guide for new contributors:

**Include**:
1. Project overview (what it does, why it exists)
2. Architecture tour (components, data flow)
3. Development setup (step-by-step)
4. Workflow guide (how we work)
5. First contribution (easy starter task)
6. Testing strategy (how to write tests)
7. Documentation standards (what we document)
8. Common pitfalls (what to avoid)
9. Who to ask (team contacts)
10. Resources (links to docs, tools)

**Style**: Welcoming, comprehensive, actionable"
```

---

## Adapting to Your Project

### Customization Checklist

- [ ] Update directory structure to match your project
- [ ] Adjust sprint sizing (1 day is a guideline, not a rule)
- [ ] Modify PRD template for your domain
- [ ] Customize sortie template for your tech stack
- [ ] Define your code quality standards
- [ ] Set your test coverage targets
- [ ] Choose your documentation style
- [ ] Adapt commit message format
- [ ] Update agent prompts with your conventions

### Project-Specific Examples

Add examples from your project:
- Completed sprint showcase
- Sample PRD
- Sample sortie spec
- Example commit messages
- Code review examples

### Team Agreement

Document your team's agreements:
- Sprint duration (1 day? 1 week?)
- Sortie granularity
- Code review process
- Definition of "done"
- When to merge
- How to handle blockers

---

## Conclusion

This agent-assisted workflow enables rapid, high-quality development through:

1. **Disciplined Planning**: PRDs and specs prevent false starts
2. **Nano-Sprints**: Small, focused cycles maintain momentum
3. **Rolling Planning**: 1-4 sprints ahead prevents blocking
4. **Agent Collaboration**: AI accelerates implementation
5. **Continuous Documentation**: Docs evolve with code
6. **Quality Gates**: Review and testing ensure standards

**The key to success**:
- **Plan first**, code second
- **Implement incrementally**, test continuously  
- **Document constantly**, review thoroughly
- **Trust but verify** agent output
- **Iterate and improve** the process

AI agents are powerful tools, but they require structure and discipline to be effective. This workflow provides that structure.

---

## Quick Reference Card

### Daily Workflow

```
Morning:
1. Review current sortie spec
2. Prompt agent to implement
3. Review generated code
4. Write/run tests
5. Commit changes

Afternoon:
6. Update documentation
7. Move to next sortie
8. Repeat steps 2-6

Evening:
9. Review sprint progress
10. Update next sprint plan
11. Commit all changes
```

### Agent Prompt Templates

**Create PRD**: `"Create PRD for [feature] with [constraints]"`  
**Break into Sorties**: `"Break PRD into [N] sorties of 2-6 hours each"`  
**Implement**: `"Implement SPEC-Sortie-{M}-{name}.md section 5"`  
**Test**: `"Create comprehensive tests for [component]"`  
**Document**: `"Update docs for [feature]"`  
**Review**: `"Review PR for [quality checks]"`  

### Sprint Status Check

```markdown
**Sprint N**: [Status]
- PRD: ✅ Complete
- Sorties: [M/N] done
- Tests: [X]% coverage
- Docs: ✅ Updated
- PR: 🔄 In review

**Sprint N+1**: [Status]
- PRD: ✅ Complete
- Sorties: ✅ Specified
- Ready to start: [Yes/No]

**Sprint N+2**: [Status]
- PRD: 📝 Draft
- Sorties: 📋 Outlined

**Sprint N+3**: [Status]
- PRD: 💡 Ideas
```

---

**Workflow Version**: 1.0  
**Last Updated**: November 18, 2025  
**License**: MIT (adapt freely for your projects)  
**Feedback**: Improve this workflow based on your team's learnings

**Remember**: This is a guide, not a rulebook. Adapt to your team's needs and continuously refine based on what works.
