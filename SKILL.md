---
name: ps2-recomp-Agent-SKILL
description: "Expert PS2 game reverse engineering and PS2Recomp pipeline porting. Use for ISO/ELF extraction, MIPS R5900 analysis, TOML configuration, syscall stubbing, C++ runtime debugging, and GhydraMCP interaction. Use when the user mentions PS2Recomp, ps2xRuntime, build64, cmake incremental build, SLES, SLUS, out_*.cpp, runner/*.cpp, MIPS recompilation, game override, PS2 porting, or any PlayStation 2 static recompilation task."
category: development
risk: unknown
source: community
date_added: "2026-03-06"
---

# PS2Recomp — Behavioral Constraint System

## 🔄 REFRESH PROTOCOL (READ THIS FIRST)

This skill degrades as your context window fills. The following loop counteracts this.

### Bootstrap (first session only)
1. Locate the user's PS2Recomp project root (ask if unknown).
2. Check if `PS2_PROJECT_STATE.md` exists in that root. If NOT, create it by copying the template from **this skill's** `scripts/project-state-template.md`.
3. The state file header contains the critical rules. Every time you read it, you re-read the rules.

### Continuous Loop (every session, every 5 turns)
1. **Re-read** `PS2_PROJECT_STATE.md` in the user's project root — its header repeats the prohibitions.
2. **Re-read** the `⛔ ABSOLUTE PROHIBITIONS` section below in this file.
3. **Before ANY build command:** Re-read prohibition #1 AND #9 below. The ONLY safe command is `cmake --build build64` from inside a **x64 Native Tools Command Prompt** environment.
4. **Before creating or deleting ANY file:** Re-read prohibition #5 and #7 below, then verify with `list_dir` or `find_by_name`.
5. **After ANY major action:** Update the user's `PS2_PROJECT_STATE.md` with what you did and the result.

**This creates a loop: SKILL → state file → SKILL. Follow it.**

## 🚀 BOOT SEQUENCE (Mandatory — First Session Action)

Before doing ANY work, you MUST load the pipeline knowledge. Rules without domain understanding produce wrong decisions. You cannot skip this.

1. **LOAD** `references/03-ps2recomp-pipeline.md` (in this skill's folder) — read it entirely.
2. **LOAD** `references/04-runtime-syscalls-stubs.md` (in this skill's folder) — read it entirely.
3. **VERIFY** you can answer these 3 questions from what you just read:
   - What does `ps2_recomp` generate and where do those files go?
   - If a crash occurs inside a generated `out_*.cpp` file, where do you write the fix? (NOT in the `out_*.cpp` file)
   - What is the difference between a `stub` binding in the TOML and a C++ game override?

If you cannot answer all 3, re-read the files. Do NOT proceed to any workflow phase until you can.

Other references (`01`, `02`, `05`–`09`) are on-demand — load them when you need specific hardware, ISA, or Ghidra knowledge for a task.

## ⛔ ABSOLUTE PROHIBITIONS

Violating ANY of these is an immediate, unrecoverable failure. No exceptions.

1. **NEVER clean the build.** Forbidden commands/flags:
   - `--clean-first`
   - `Remove-Item build64` / `rm -rf build*/`
   - `cmake --build ... --target clean`
   - ANY action that deletes `.obj` / `.o` files inside the build directory
   - Full rebuild takes **30+ hours** (~33,000 object files). Incremental rebuild takes seconds.
2. **NEVER modify `runner/*.cpp` files.** These are auto-generated from MIPS. The recompiler will overwrite your changes. Fix the runtime layer or write a game override instead.
3. **NEVER modify `.h` header files without explicit user approval.** A header change triggers recompilation of every file that includes it — potentially thousands.
4. **NEVER run destructive git commands.** No `git checkout`, `git clean`, `git reset`, `git stash`, `git pull`. Changes are local and permanent.
5. **NEVER assume file names or paths.** Use `list_dir`, `find_by_name`, or `grep_search` to verify. Game assets vary per title (some have COREC.BIN, others don't; some have multiple SLES, others one).
6. **NEVER claim code compiles without reading the build output.** Run `cmake --build build64` and verify exit code 0.
7. **NEVER delete, overwrite, or clean ANY build artifact without asking the user first.** This includes object files, libraries, executables, and CMake cache.
8. **NEVER use `> out.txt` or pipe build output to files.** Run the executable directly and read stdout.
9. **NEVER run `cmake` outside a vcvars64 environment.** If you run `cmake --build build64` from a plain PowerShell/cmd, it WILL fail with missing SDK headers (`winresrc.h`, `windows.h`). You MUST be inside an **x64 Native Tools Command Prompt for VS** or wrap every cmake call with: `cmd.exe /c "call ""<vcvars64_path>"" && cmake --build build64"`

## 🧠 MENTAL MODEL (5 Rules)

1. **This is NOT emulation.** Original PS2 MIPS instructions have been statically recompiled into C++ source files (`ps2xRuntime/src/runner/*.cpp`). There is no emulation loop.
2. **The Runtime Layer** (`ps2xRuntime/src/lib/`) is handwritten C++ that intercepts PS2 hardware calls (syscalls, memory, DMA, IOP) and translates them into native OS equivalents.
3. **Your job:** Write runtime stubs, syscall implementations, and game-specific overrides. You do NOT touch the generated runner code.
4. **The target is ALWAYS a Windows x64 executable.** The ideal toolchain is `clang-cl` (LLVM via Visual Studio) + `Ninja` + `Release` mode — this cuts a 25-hour MSVC build to ~1 hour. But the user may not have it yet. Your job is to **detect** the current config, **report** it, and **suggest** the optimal path if missing. Never assume.
5. **The build environment is x64 Native Tools Command Prompt for VS.** Without it, Windows SDK headers are invisible to the compiler. This is non-negotiable regardless of which compiler is used (MSVC or clang-cl).

## ⚔️ ADVERSARIAL SPLIT — Mandatory for Code Changes

Before writing ANY C++ fix, override, or stub, you MUST execute this 3-step structure:

1. **PROPOSE:** Draft your solution — which address to hook, what C++ logic, which file. State your hypothesis about *why* this fixes the crash.
2. **ATTACK:** Immediately switch stance. Try to destroy your own proposal:
   - Does the address exceed PS2's 32MB RDRAM (0x01FFFFFF)?
   - Are you suppressing a crash that will just cause silent corruption later?
   - Are you modifying a `runner/*.cpp` file instead of the runtime layer?
   - Does this break any previous milestone in the state file?
3. **EXECUTE:** Only after the attack finds no fatal flaws, output the final code and commands.

Skip this ONLY for trivial reads, greps, or state file updates. For **any code modification**, this structure is mandatory.

## ✅ MANDATORY CHECKLIST — Before Every Code Change

Before writing or modifying ANY code, verify ALL of these:

- [ ] Read `PS2_PROJECT_STATE.md` if it exists (or create it from `scripts/project-state-template.md`)
- [ ] Confirm you are inside a **vcvars64** environment (check: `$env:VSINSTALLDIR` is set, or `where cl` returns a path)
- [ ] Confirm the build directory exists and is intact (check `build64/` or `build/` — the name varies per project)
- [ ] Confirm the file you're modifying is in `src/lib/` or is a game override — NOT in `runner/`
- [ ] If modifying a `.h` file: **STOP and ask the user**
- [ ] If the change adds a new `.cpp` file: verify it's picked up by `CMakeLists.txt` globs or add it

After ANY code change:
- [ ] Run `cmake --build build64` (incremental, never clean) — **from vcvars64 environment**
- [ ] Read the build output. Verify exit code 0. Fix errors before proceeding.
- [ ] Update `PS2_PROJECT_STATE.md` with the change and result

## 🔧 OPERATIONAL WORKFLOW

### Phase 0 — Setup (`PHASE_SETUP`)
1. **Verify vcvars64 environment.** Test: `where cl` must return a path (NOT "not found"). If not, you MUST source it or wrap commands.
2. **Detect build directory.** Look for `build64/` or `build/`. If found, read `CMakeCache.txt` and extract these 3 values:
   - `CMAKE_GENERATOR` (Ninja? Visual Studio?)
   - `CMAKE_CXX_COMPILER` (clang-cl? cl.exe/MSVC?)
   - `CMAKE_BUILD_TYPE` (Release? Debug? empty?)
3. **Report & suggest.** Tell the user what you found and rate it:
   | Config | Rating | Agent Action |
   |--------|--------|--------------|
   | clang-cl + Ninja + Release | ⚡ Optimal | Use as-is. Do NOT reconfigure. |
   | MSVC + Ninja | ⚠️ Acceptable | Suggest clang-cl upgrade (see `references/03-ps2recomp-pipeline.md` §4) |
   | MSVC + VS Solution | ❌ Critical | **STRONGLY** recommend switching to Ninja+clang-cl. 25h→1h difference. |
   | No build dir at all | 🆕 Fresh | Guide user through initial cmake configure (see pipeline reference). |
   
   **NEVER reconfigure or delete the build directory without explicit user approval.** Only suggest; let the user decide.
4. Verify `ps2_analyzer` and `ps2_recomp` executables exist. Build if missing.
5. Extract main ELF from ISO.
   **Exit:** Toolchain verified, build config reported, ELF extracted.

### Phase 1 — ELF Analysis (`PHASE_ELF_ANALYSIS`)
1. Run `ps2_analyzer` on the ELF → generates `[game].toml`.
2. If stripped, export Ghidra function map.
   **Exit:** TOML exists with analyzer data.

### Phase 2 — TOML Configuration (`PHASE_TOML_CONFIG`)
1. Map known addresses to `stubs` in TOML. See `examples/toml-config-template.toml` for syntax.
2. Map init code to `skip`. Apply `patches` for privileged instructions.
   **Exit:** TOML has overrides to bypass setup loops.

### Phase 3 — Recompilation (`PHASE_RECOMPILATION`)
1. Run `ps2_recomp` with the TOML.
2. Check output for `// Unhandled opcode` comments.
   **Exit:** `out_*.cpp` files generated without fatal panics.

### Phase 4 — Build & Runtime (`PHASE_RUNTIME_BUILD`)
1. Move generated files to `ps2xRuntime/src/runner/`.
2. Build: `cmake --build build64` — **INCREMENTAL ONLY, from vcvars64 environment.**
3. If build fails: read error, fix C++ code, rebuild. Do not ask user to compile.
4. Run the executable directly (command stored in `PS2_PROJECT_STATE.md`). Use `run_command` with a timeout.
5. Write game overrides following `examples/game-override-template.cpp`.
6. Address crashes using the Decision Tree below.
   **Exit:** Executable builds and advances past bootloader.

### Phase 5 — I/O & Menus (`PHASE_IO_MODULE`)
1. Implement CDVD reads, File I/O, SIF module loading.
2. Replace triage stubs with real implementations.
   **Exit:** Game reads files and sends GIF/DMA packets.

### Decision Tree — Crashes in `runner/*.cpp`

When hitting a crash, null pointer, or infinite loop:

1. **Extract:** Find exact PC and caller (RA) from the log.
2. **Classify subsystem:** CDVD? SIF/RPC? GS? EE Timer? IOP audio? Thread?
3. **Pick fix type:**
   - System/env failure (missing syscall, CD read) → implement in `src/lib/`
   - Game-specific hardware wait (DMA, RPC) → game override via TOML
   - Recompiler bug → game override
4. **Verify:** Check for regressions against previous milestones. Update state file.

**NEVER patch `runner/*.cpp`. Always fix via runtime or override.**

### Circuit Breaker — 3 Strike Rule

If you attempt the same `compile → test → fail → guess → compile` loop **3 times** for the same crash:

1. **STOP.** Do not guess again.
2. Re-read `PS2_PROJECT_STATE.md`.
3. Consult `references/09-ps2tek.md` or use GhydraMCP.
4. Search the web for community workarounds.
5. If still stuck: format a specific technical question and **ask the user**.

## 🔍 GhydraMCP

- Check availability: `mcp_ghydra_instances_list()`
- **NEVER** ask the user to look at Ghidra for you. You have MCP tools — use them.
- `mcp_ghydra_functions_decompile` — understand `sub_xxx` functions
- `mcp_ghydra_data_list_strings` — find context strings
- `mcp_ghydra_xrefs_list` — trace callers/callees
- `mcp_ghydra_functions_rename` — label discovered functions

## 📚 REFERENCE INDEX — Load On Demand

Only load these files when you need specific knowledge. Do not pre-load all of them.

| File | Content |
|---|---|
| `references/01-ps2-hardware-bible.md` | Memory maps, I/O registers, EE/IOP architecture |
| `references/02-mips-r5900-isa.md` | MIPS translation (MMI, COP0, FPU) to C++ |
| `references/03-ps2recomp-pipeline.md` | `ps2_analyzer` / `ps2_recomp` CLI args, TOML schema |
| `references/04-runtime-syscalls-stubs.md` | Syscall implementation, stubs, runtime overrides |
| `references/05-ghidra-ghydramcp-guide.md` | Ghidra scripting, GhydraMCP usage |
| `references/06-game-porting-playbook.md` | `sub_xxx` inference, triage strategies |
| `references/07-ps2-code-patterns.md` | DMA, VIF, GS packets, CD/IOP loops |
| `references/08-infinite-knowledge-base.md` | Instructions for searching `09-ps2tek.md` |

## 🧰 SCRIPTS & EXAMPLES

| File | Purpose |
|---|---|
| `scripts/vif_gif_surgeon.py` | DMA/VIF/GIF packet decoder for memory dumps (future use) |
| `scripts/install_ghydramcp.py` | One-shot GhydraMCP installer |
| `scripts/project-state-template.md` | Template for `PS2_PROJECT_STATE.md` |
| `examples/toml-config-template.toml` | TOML config syntax reference (stubs, skip, patches) |
| `examples/game-override-template.cpp` | C++ override pattern (`ret0`, `ret1`, `RegisterGameOverrides`) |

## 📋 Persistent State Protocol

1. At session start: check for `PS2_PROJECT_STATE.md` in the user's project root.
2. If it doesn't exist: create it from **this skill's** `scripts/project-state-template.md`. If you can also infer the phase from physical evidence (hundreds of `out_*.cpp` = PHASE_RUNTIME_BUILD), fill in the phase.
3. Every 5 turns and after every major action: re-read the state file (its header contains the rules) and update it with results.
4. Runner command is stored under `## Active Runner Command` — read it verbatim, never reconstruct from memory.

## 🔁 SESSION CLOSE (Mandatory — Before Ending Work)

Before ending any session, you MUST complete this feedback loop:

1. **SYNTHESIZE:** Write your top discoveries into `## Learned Patterns` in the state file. Write **patterns**, not events. "`X causes Y, fix with Z`" > "`X happened`".
2. **UPDATE:** Mark boot checkboxes, update crash table, update current phase if it changed.
3. **VERIFY:** Read back the state file once to confirm your updates are coherent with the existing entries.

This is what makes the next session smarter than this one. Skip it and the next agent starts from scratch.