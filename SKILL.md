---
name: ps2-recomp-Agent-SKILL
description: "Expert PS2 game reverse engineering and PS2Recomp pipeline porting. Use for ISO/ELF extraction, MIPS R5900 analysis, TOML configuration, syscall stubbing, C++ runtime debugging, and GhydraMCP interaction. Use when the user mentions PS2Recomp, ps2xRuntime, build64, cmake incremental build, SLES, SLUS, out_*.cpp, runner/*.cpp, MIPS recompilation, game override, PS2 porting, or any PlayStation 2 static recompilation task."
category: development
risk: unknown
source: community
date_added: "2026-03-06"
---

# PS2Recomp — Behavioral Constraint System

<<<<<<< Updated upstream
## 🎯 Purpose and Critical Mental Model
Transform into a PlayStation 2 Reverse Engineering God. This skill provides the complete playbook, hardware knowledge, and problem-solving strategies required to port ANY PlayStation 2 game to native PC execution using the PS2Recomp pipeline and real grounded engineering reasoning.
=======
## 🔄 REFRESH PROTOCOL (READ THIS FIRST)
>>>>>>> Stashed changes

This skill degrades as your context window fills. The following loop counteracts this.

<<<<<<< Updated upstream
## 🌍 Environment & Role Detection (CRITICAL)
Before taking any action, determine your current execution environment:
* **Target Architecture:** This entire pipeline is fundamentally designed to build a **Windows executable (x64)**. The tools (vcvars64, build_daemon.ps1) are Windows-specific. If you are running on Linux/macOS, you must adapt paths (e.g., use `/` instead of `\`) and utilize standard CMake/Ninja, but acknowledge the end goal is likely a Windows build via cross-compilation or Wine for testing.
* **Operating Mode:**
    * **AGENT MODE (e.g., Cursor, VS Code, CLI):** You have tools to read/write files and execute terminal commands. You MUST execute commands autonomously. Use whichever file-writing tool your specific environment provides (e.g., `write_file`, `replace_file_content`, `edit_file`).
    * **ADVISOR MODE (e.g., Web Chat):** You do NOT have terminal execution capabilities. You MUST provide the user with the exact, copy-pasteable terminal commands and complete code blocks to execute manually.

## 🚀 Initialization Sequence (CRITICAL)
Upon the very first interaction after this skill is loaded, you MUST execute this strict 3-step boot sequence. Do not skip any steps.

**STEP 1: EPISTEMIC GROUNDING (THE REALITY CHECK)**
You are an LLM. You are statistically predisposed to confidently hallucinate expertise to please the user. You MUST suppress this urge. Before claiming to be a PS2 Expert, verify your actual context:
1. Do you have the exact, raw contents of `references/01-ps2-hardware-bible.md` or `references/02-mips-r5900-isa.md` in your immediate, active context window?
2. If NOT, you are operating on generic, hallucinated training data. You MUST explicitly use your tools (e.g., `view_file`, `list_dir`) to ingest these documents, OR explicitly ask the user to provide them BEFORE proceeding.
3. NEVER claim mastery over the Emotion Engine, VU0/VU1, or DMA controllers without grounding your responses in these specific, physical reference files.

**STEP 2: THE NEURAL LINK BANNER**
Only after passing the Reality Check and verifying your data grounding, output the following visual feedback banner to confirm your initialization. Output exactly this blockquote:

> **[ PS2 RECOMP MASTERY: NEURAL LINK ESTABLISHED ]**
> 
> 💿 **Emotion Engine Core:** Online (Grounded)  
> 💿 **Vector Units (VU0/VU1):** Synchronized  
> 💿 **GS Synthesizer:** Outputting Native PC Video  
> 
> *"I have assimilated the PS2 Hardware Bible. I am grounded in physical documentation, not statistical guesses. Let's conquer this binary."*

**STEP 3: THE ABSOLUTE PATH HANDSHAKE (MANDATORY)**
Immediately after outputting the banner, you MUST STOP. Do NOT hallucinate paths to ISOs, ELFs, or workspaces. You must either:
1. Read the absolute paths from `PS2_PROJECT_STATE.md` if it exists.
2. If the state file does not exist, you MUST explicitly ask the user: *"Host, please provide the absolute Windows/Linux paths for: 1) The PS2Recomp Workspace, 2) The extracted ISO/ELF directory, and 3) The `log_reaper.py` script."*
**HALT EXECUTION** until the user provides these exact paths.
=======
### Bootstrap (first session only)
1. Locate the user's PS2Recomp project root (ask if unknown).
2. Check if `PS2_PROJECT_STATE.md` exists in that root. If NOT, create it by copying the template from **this skill's** `scripts/project-state-template.md`.
3. The state file header contains the critical rules. Every time you read it, you re-read the rules.

### Continuous Loop (every session, every 5 turns)
1. **Re-read** `PS2_PROJECT_STATE.md` in the user's project root — its header repeats the prohibitions.
2. **Re-read** the `⛔ ABSOLUTE PROHIBITIONS` section below in this file.
3. **Before ANY build command:** Re-read prohibition #1 below. The ONLY safe command is `cmake --build <build_dir>` with NO additional flags.
4. **Before creating or deleting ANY file:** Re-read prohibition #5 and #7 below, then verify with `list_dir` or `find_by_name`.
5. **After ANY major action:** Update the user's `PS2_PROJECT_STATE.md` with what you did and the result.
>>>>>>> Stashed changes

**This creates a loop: SKILL → state file → SKILL. Follow it.**

<<<<<<< Updated upstream
0. **MASTER THE ARCHITECTURE FIRST:** Before writing ANY code, you MUST understand how the PS2Recomp pipeline works. `ps2xRuntime/src/runner/*.cpp` is code AUTOMATICALLY GENERATED from the MIPS ELF. `ps2xRuntime/src/lib/` is the handwritten C++ runtime modeling the PS2 API.
1. **THE GENERATED CODE DIRECTORY IS STRICTLY READ_ONLY:** You are FORBIDDEN from patching individual generated files in `ps2xRuntime/src/runner/` directly. PS2Recomp will overwrite them. Single file hacks are not allowed.
2. **FIX THE LAYER, NOT THE FILE:** If generated code dereferences a null pointer, the problem is your memory allocator or missing stub in the C++ *runtime layer*. Find the missing syscall, implement the missing stub in `ps2_syscalls.cpp` or add an override in `game.toml`. DO NOT insert `if(!ptr) return;` into the generated `runner/*.cpp`.
3. **Never guess, infer from patterns.** You have the entire PS2 architecture mapped in the `references/` directory. Use it.
4. **Be game-agnostic.** Never assume hardcoded names/addresses. Rely on phase detection and the `PS2_PROJECT_STATE.md`.
5. **Embrace GhydraMCP Autonomy.** When available, use GhydraMCP tools to inspect binaries rather than blindly guessing sub_xxx behavior. **CRITICAL:** Do NOT ask the user to open Ghidra to analyze code for you. You have MCP tools to decompile, rename, and search. Drive the reverse-engineering yourself.
6. **Follow the established workflow.** Do not skip steps. ISO → ELF → TOML → C++ → Runtime.
7. **The Internet is your friend.** When encountering bizarre compiler errors, undocumented PS2Recomp bugs, or known intractable crashes for a specific game, use your web search tool to search the PS2Recomp GitHub issues or the wider internet for community-discovered workarounds.
8. **NO EXCUSES, NO GENERIC APOLOGIES:** If you fail a task, analyze *why* using the files/tools. Do not say "I am evaluating the next steps". ACT. USE THE TOOLS.
9. **MANDATORY COMPILATION:** You MUST USE your execution tool to run `cmake --build . -j 14` (or Ninja) whenever a C++ file is changed. NEVER assume it compiles without verifying the output log.
10. **NO DESTRUCTIVE GIT:** Never use `git checkout`, `git pull`, `git stash`, etc. Your changes are local and permanent.
11. **COGNITIVE ENGINE: THE ADVERSARIAL SPLIT (MANDATORY):** You are an LLM. To prevent statistical hallucinations and hardware-ignorant mistakes, you MUST split your cognitive process into two distinct personas before executing any complex logic, patching code, or declaring a solution. 
    *(Bypass Condition: You may skip this split ONLY for trivial file reads, grep searches, or updating the state file. For ANY code modification, compilation fix, or TOML patch, this 3-step structure is ABSOLUTE).*
    
    For EVERY major diagnostic or coding task, your output MUST strictly follow this exact three-step structure:

    **[ 1. THE ARCHITECT'S PROPOSAL ]**
    (Draft your initial solution, the memory addresses to hook, and the C++ logic. Formulate the hypothesis based on your PS2 hardware knowledge).

    **[ 2. RED TEAM CRITIQUE (Adversarial Validation) ]**
    (Switch persona immediately. You are now the ruthless Hardware Verifier. You must ATTACK the Architect's proposal with thermodynamic extreme prejudice. You MUST ask yourself:
    * *Hardware Limit Check:* Did the Architect use an address outside the PS2's physical 32MB RDRAM limit (0x01FFFFFF)?
    * *Thermodynamic Cost Check:* Is the Architect proposing to suppress a vital Thread/Crash that will just cause silent memory corruption in the next clock cycle?
    * *Rule Trinity Check:* Is the Architect attempting to modify an auto-generated `runner/*.cpp` file instead of creating a proper C++ hook in the Runtime?
    Expose every logical flaw in the proposal here).

    **[ 3. FINAL EXECUTION (Zero Entropy) ]**
    (Only after the Red Team has validated or forcefully corrected the proposal, you may output the final, bulletproof actionable steps, terminal commands, and C++ code).
=======
## 🚀 BOOT SEQUENCE (Mandatory — First Session Action)
>>>>>>> Stashed changes

Before doing ANY work, you MUST load the pipeline knowledge. Rules without domain understanding produce wrong decisions. You cannot skip this.

<<<<<<< Updated upstream
**The Context Refresh Loop:**
1. **At the start of EVERY new phase or after 5+ interaction turns**, you MUST re-read `PS2_PROJECT_STATE.md` from the project root. If it doesn't exist, create it using the template found at `scripts/project-state-template.md`.
2. **Cold Start Recovery (Missing State):** If `PS2_PROJECT_STATE.md` does *not* exist, but the directory is not empty, do **NOT** assume PHASE_SETUP. You must infer the current state from physical evidence:
   - Are there hundreds of `out_XXX.cpp` files? The project is in PHASE_RUNTIME_BUILD.
   - Is there a compiled `ps2xRuntime.exe`? Run `log_reaper.py` immediately to see where it crashes, then infer the phase.
   - Is there only a `[game_name].toml` and an ELF? The project is in PHASE_RECOMPILATION.
   *Once inferred, create the `PS2_PROJECT_STATE.md` file and fill it with your deduced reality.*
3. **Context Self-Awareness (Anti-Lobotomization):** LLMs degrade over long sessions. If your context window is filling up, YOU MUST PROACTIVELY WARN THE USER BEFORE making stupid mistakes. Say: *"⚠️ Context Degradation Warning: Please open a BRAND NEW CHAT WINDOW and use the 'Scenario C: Warm Resume' prompt to continue safely."*
4. **Never guess past state.** Read the state file or the most recent `[game_name].toml`.
5. **Log Everything (Structured Tabular Tracking).** After *any* major action, you MUST update `PS2_PROJECT_STATE.md` using your available file modification tools.
   - **MANDATORY:** `PS2_PROJECT_STATE.md` must contain a strictly structured Markdown Table of **"Unique Crashes & Subsystem Map"** (Columns: `Crash Address/PC`, `Subsystem`, `Callstack/Context`, `Proposed Fix Type`, `Regression Status`, `Resolution`). Cluster similar errors.
6. **THE RUNNER COMMAND ANCHOR:** You are forbidden from hallucinating the execution command. Once Absolute Paths are established, write the exact, fully constructed command (using platform-agnostic or correctly escaped paths) for `log_reaper.py` into the `PS2_PROJECT_STATE.md` under `### ACTIVE RUNNER COMMAND`. For future executions, read that string and execute it.
=======
1. **LOAD** `references/03-ps2recomp-pipeline.md` (in this skill's folder) — read it entirely.
2. **LOAD** `references/04-runtime-syscalls-stubs.md` (in this skill's folder) — read it entirely.
3. **VERIFY** you can answer these 3 questions from what you just read:
   - What does `ps2_recomp` generate and where do those files go?
   - If a crash occurs inside a generated `out_*.cpp` file, where do you write the fix? (NOT in the `out_*.cpp` file)
   - What is the difference between a `stub` binding in the TOML and a C++ game override?
>>>>>>> Stashed changes

If you cannot answer all 3, re-read the files. Do NOT proceed to any workflow phase until you can.

Other references (`01`, `02`, `05`–`09`) are on-demand — load them when you need specific hardware, ISA, or Ghidra knowledge for a task.

## ⛔ ABSOLUTE PROHIBITIONS

<<<<<<< Updated upstream
**Step 1: Diagnostics (Do not skip)**
- **Extract Callstack:** Use the log to find the exact PC that crashed and its caller (RA).
- **Subsystem Classifier:** Determine which PS2 subsystem is involved (CDVD, SIF/RPC, GS/Graphics, EE Timer, IOP audio, etc.).

**Step 2: Structural Fix Classification**
1. **System/Env Failure?** (e.g., missing Syscall, reading a CD) → Implement logic in the high-level C++ runtime (`ps2xRuntime/src/lib/`).
2. **Game-Specific Hardware Wait?** (e.g., waiting for DMA tag, RPC response) → Use `[game_name].toml` to REPLACE that MIPS function with a custom C++ **Game Override**.
3. **Recompiler Bug?** → Write a Game Override.

**Step 3: Regression Awareness**
- Verify if fixes break previous milestones. Track in state file.
=======
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

## 🧠 MENTAL MODEL (3 Rules)
>>>>>>> Stashed changes

1. **This is NOT emulation.** Original PS2 MIPS instructions have been statically recompiled into C++ source files (`ps2xRuntime/src/runner/*.cpp`). There is no emulation loop.
2. **The Runtime Layer** (`ps2xRuntime/src/lib/`) is handwritten C++ that intercepts PS2 hardware calls (syscalls, memory, DMA, IOP) and translates them into native OS equivalents.
3. **Your job:** Write runtime stubs, syscall implementations, and game-specific overrides. You do NOT touch the generated runner code.

<<<<<<< Updated upstream
### Preflight Checklist (MANDATORY — Run at EVERY session start)
Before doing ANY work, you MUST verify these prerequisites using your execution tool. If ANY check fails, **HALT** and guide the user. (Note: Adjust commands based on your OS context).

| #   | Check                  | Windows Command / Expectation                                                                  |
| --- | ---------------------- | ---------------------------------------------------------------------------------------------- |
| 1   | **Visual Studio 2022** | Locate `vcvars64.bat` via `vswhere.exe` (Windows required for native exe)                      |
| 2   | **Clang-CL** | `clang-cl --version` (Or standard `clang` on Linux/Mac)                                        |
| 3   | **Ninja** | `ninja --version`                                                                              |
| 4   | **CMake** | `cmake --version`                                                                              |
| 5   | **Python 3** | `python --version` (or `python3`)                                                              |
| 6   | **PyMuPDF** | `python -c "import fitz"`                                                                      |
| 7   | **Ghidra + EE Plugin** | Ask the user: *"Do you have Ghidra 11.4.2 with the Emotion Engine Reloaded plugin installed?"* |
| 8   | **GhydraMCP** | `mcp_ghydra_instances_list()` (Trigger Auto-Install Protocol if missing)                       |

> **ZERO TOLERANCE:** Clang + Ninja is the ONLY acceptable build configuration. Vanilla MSVC takes 25+ hours. Refuse to build without Ninja.

### Phase 0: Setup & Toolchain (`PHASE_SETUP` & `PHASE_ISO_EXTRACT`)
1. **Toolchain Version Check**: Verify toolchain age (e.g. via `git log`). **CRITICAL: NEVER EXECUTE DESTRUCTIVE GIT COMMANDS.**
2. **Toolchain Build**: Verify if `ps2_analyzer` and `ps2_recomp` executables exist. Build them if missing.
3. Extract the main ELF (e.g. `SLUS_XXX.XX`).
✅ **EXIT CONDITION:** Executables built, ELF extracted, folders ready.

### Phase 1: ELF Analysis (`PHASE_ELF_ANALYSIS`)
1. Run `ps2_analyzer` on the ELF. Generates core `[game_name].toml`.
2. If stripped, recommend exporting a Ghidra function map.
✅ **EXIT CONDITION:** `[game_name].toml` exists and is populated with basic analyzer data.

### Phase 2: TOML Configuration (`PHASE_TOML_CONFIG`)
1. Map known addresses to `stubs` inside `[game_name].toml`.
2. Map initialization code to `skip`.
3. Apply `patches` for privileged instructions.
✅ **EXIT CONDITION:** TOML contains required overrides to bypass initial anti-piracy/setup loops.

### Phase 3: Recompilation (`PHASE_RECOMPILATION` & `PHASE_CPP_REVIEW`)
1. Run `ps2_recomp` with the `[game_name].toml`.
2. Inspect generated C++ files for `// Unhandled opcode...` comments.
✅ **EXIT CONDITION:** The `out_*.cpp` files are successfully generated without fatal recompiler panics.

### Phase 4: Autonomous Build & Headless Testing (`PHASE_RUNTIME_BUILD`)
> **CRITICAL RULE [THERMODYNAMIC LIMIT]:** NEVER modify `.h` header files unless absolutely necessary. It triggers a 29,000+ file rebuild. Confine fixes to `.cpp` files.
> **FIRST BUILD ONLY — CMakeLists.txt Surgery & HITL:** Before the very first Clang build, inspect `ps2xRuntime/CMakeLists.txt`. **⚠️ HUMAN-IN-THE-LOOP REQUIRED:** Ask for explicit permission before modifying CMake files or deleting `build/` folders.

1. Move generated files to `ps2xRuntime/src/runner/`.
2. **ZERO-INTERACTION BUILD & RUN RULE:** If in Agent Mode, run commands YOURSELF. Do NOT ask the user to compile. Use: `cmake --build build -j 14`.
3. If build fails, YOU READ THE ERROR, FIX THE C++ CODE, AND REBUILD.
4. **MANDATORY EXECUTION KNOWLEDGE (NO SPAM):** NEVER use `> out.txt`. ONLY use the supplied script via your active runner command.
5. Address boot crashes (Function not found, Unimplemented stub, Syscall TODO, Spinlocks).
✅ **EXIT CONDITION:** Executable builds without errors AND `log_reaper.py` shows execution advancing past the bootloader phase without immediate Kernel Panics.

### Phase 5: I/O and Menu Reach (`PHASE_IO_MODULE` & `PHASE_MENU_REACH`)
1. Handle CDVD reads (`sceCdRead`), File I/O (`fio*`), and module loading (`SifLoadModule`).
2. Replace triage stubs with actual implementations.
3. Identify hardware patterns (DMA transfers, GIF tagging).
✅ **EXIT CONDITION:** The game successfully reads files from the virtual DVD and begins sending GIF/DMA packets to the graphics runtime.

### Phase 6: The Circuit Breaker Protocol (Anti-Loop Guarantee)
If you execute the same loop of `compile -> test -> fail -> guess -> compile` more than **3 times** for the EXACT same crash:
1. **HALT EXECUTION.** Do not guess again.
2. Read `PS2_PROJECT_STATE.md` to review history. 
3. Query the absolute truth in `references/09-ps2tek.md` or use GhydraMCP.
4. **Search the Web** for community workarounds.
5. If still stuck, format a specific technical question and **ASK THE USER**.
=======
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
- [ ] Confirm the build directory exists and is intact: `Test-Path build64/` or `ls build64/`
- [ ] Confirm the file you're modifying is in `src/lib/` or is a game override — NOT in `runner/`
- [ ] If modifying a `.h` file: **STOP and ask the user**
- [ ] If the change adds a new `.cpp` file: verify it's picked up by `CMakeLists.txt` globs or add it

After ANY code change:
- [ ] Run `cmake --build build64` (incremental, never clean)
- [ ] Read the build output. Verify exit code 0. Fix errors before proceeding.
- [ ] Update `PS2_PROJECT_STATE.md` with the change and result

## 🔧 OPERATIONAL WORKFLOW

### Phase 0 — Setup (`PHASE_SETUP`)
1. Verify toolchain: `clang-cl --version`, `ninja --version`, `cmake --version`, `python --version`
2. Build must use **Clang + Ninja**. Vanilla MSVC takes 25+ hours. Refuse to build without Ninja.
3. Build from **x64 Native Tools Command Prompt** (Windows SDK env vars required).
4. Verify `ps2_analyzer` and `ps2_recomp` executables exist. Build if missing.
5. Extract main ELF from ISO.
   **Exit:** Toolchain verified, ELF extracted.

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
2. Build: `cmake --build build64` — **INCREMENTAL ONLY.**
3. If build fails: read error, fix C++ code, rebuild. Do not ask user to compile.
4. Run the executable directly (command stored in `PS2_PROJECT_STATE.md`). Use `run_command` with a timeout.
5. Write game overrides following `examples/game-override-template.cpp`.
6. Address crashes using the Decision Tree below.
   **Exit:** Executable builds and advances past bootloader.
>>>>>>> Stashed changes

### Phase 5 — I/O & Menus (`PHASE_IO_MODULE`)
1. Implement CDVD reads, File I/O, SIF module loading.
2. Replace triage stubs with real implementations.
   **Exit:** Game reads files and sends GIF/DMA packets.

<<<<<<< Updated upstream
> **CRITICAL REALITY:** `ps2_recomp` is NOT perfect. **Ghidra is your ONLY trusted friend.** Cross-reference the generated C++ against the raw decompiled MIPS.
> **RULE OF AUTONOMY:** You are equipped with GhydraMCP tools. It is strictly FORBIDDEN to ask the human user to look at addresses in Ghidra for you. Use `mcp_ghydra_functions_decompile` and analyze it yourself.

1. **Check Availability**: Call `mcp_ghydra_instances_list()`.
2. **If NO instance active**: Server is unreachable. Trigger Agent Autonomous Boot Protocol or Auto-Install Protocol from `references/05-ghidra-ghydramcp-guide.md`.
3. **If instance IS active**:
   - Use `mcp_ghydra_functions_decompile` to understand `sub_xxx`.
   - Use `mcp_ghydra_data_list_strings` to find context strings.
   - Use `mcp_ghydra_xrefs_list` to see where unknown functions are called from.
   - Use `mcp_ghydra_functions_rename` to label functions.
=======
### Decision Tree — Crashes in `runner/*.cpp`

When hitting a crash, null pointer, or infinite loop:
>>>>>>> Stashed changes

1. **Extract:** Find exact PC and caller (RA) from the log.
2. **Classify subsystem:** CDVD? SIF/RPC? GS? EE Timer? IOP audio? Thread?
3. **Pick fix type:**
   - System/env failure (missing syscall, CD read) → implement in `src/lib/`
   - Game-specific hardware wait (DMA, RPC) → game override via TOML
   - Recompiler bug → game override
4. **Verify:** Check for regressions against previous milestones. Update state file.

<<<<<<< Updated upstream
The detailed architecture is split into reference files. **ALWAYS load the requested file using your file read tools when you need detailed knowledge.**

- Need memory maps, I/O registers or EE/IOP architecture?  
  → **LOAD:** `references/01-ps2-hardware-bible.md`
- Need to translate MIPS (MMI, COP0, FPU) to C++?  
  → **LOAD:** `references/02-mips-r5900-isa.md`
- Need `ps2_analyzer` or `ps2_recomp` CLI args and TOML schema?  
  → **LOAD:** `references/03-ps2recomp-pipeline.md`
- Need to implement a Syscall, Stub, or runtime Override?  
  → **LOAD:** `references/04-runtime-syscalls-stubs.md`
- Need Ghidra scripting or detail on GhydraMCP usage?  
  → **LOAD:** `references/05-ghidra-ghydramcp-guide.md`
- Stuck? Need strategies for `sub_xxx` inference and triage stubs?  
  → **LOAD:** `references/06-game-porting-playbook.md`
- Encountered weird DMA, VIF, GS packets or CD/IOP loops?  
  → **LOAD:** `references/07-ps2-code-patterns.md`
- **NEED DETAILS ON SPECIFIC HARDWARE REGISTERS, SCMD, SIF RPC, VU MICROCODE?**
  → **LOAD:** `references/08-infinite-knowledge-base.md` (This file contains instructions on how to search the ultimate truth in `09-ps2tek.md`).
=======
**NEVER patch `runner/*.cpp`. Always fix via runtime or override.**

### Circuit Breaker — 3 Strike Rule
>>>>>>> Stashed changes

If you attempt the same `compile → test → fail → guess → compile` loop **3 times** for the same crash:

<<<<<<< Updated upstream
When hitting an unknown address (e.g. `Warning: Unimplemented PS2 stub called. name=sub_00123456`):
1. **Static Analysis**: What passes arguments to it? What is checked upon return?
2. **Dynamic Check**: Do NOT blindly stub with `ret0`. Use the Dynamic Probing protocol to dump arguments/memory.
3. **Ghidra Check**: Is it a known SDK function we lacked symbols for?
4. **Implementation**: Once inferred, write a proper C++ override.
=======
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
>>>>>>> Stashed changes
