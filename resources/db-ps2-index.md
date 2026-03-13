# PS2 Knowledge Base — Master Index
> **The LLM looks here FIRST.** Every PS2 topic maps to a file and section.
>
> Files live in `resources/` directory. Numbered files (01–09) are narrative references; `db-*.md` are structured knowledge bases.

---

## Quick Lookup

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **System overview / block diagram** | `db-ps2-architecture.md` | §1 System-Level Block Diagram |
| **Bus bandwidths** | `db-ps2-architecture.md` | §1 Key Bandwidths |
| **EE Core pipeline / dual-issue** | `db-ps2-architecture.md` | §2 EE Core Pipeline |
| **Branch prediction / delay slots** | `db-ps2-architecture.md` | §2 Branch Prediction |
| **Cache / Scratchpad** | `db-ps2-architecture.md` | §2 Cache Architecture |
| **DMA channels map** | `db-ps2-architecture.md` | §3 DMA Controller |
| **DMA tag format** | `db-ps2-architecture.md` | §3 DMA Tag Format |
| **DMA transfer modes** | `db-ps2-architecture.md` | §3 DMA Transfer Modes |
| **Interrupts / INTC** | `db-ps2-architecture.md` | §4 Interrupt Controller |
| **GS rendering pipeline** | `db-ps2-architecture.md` | §5 GS Rendering Pipeline |
| **GS pixel formats (PSM)** | `db-ps2-architecture.md` | §5 GS Pixel Storage Formats |
| **VRAM layout / swizzle** | `db-ps2-architecture.md` | §5 VRAM Block Layout |
| **GIF paths (PATH1/2/3)** | `db-ps2-architecture.md` | §5 GIF Data Paths |
| **GS drawing primitives** | `db-ps2-architecture.md` | §5 GS Drawing Primitives |
| **VU0 vs VU1** | `db-ps2-architecture.md` | §6 VU Architecture |
| **VU micro pipeline + hazards** | `db-ps2-architecture.md` | §6 VU Micro Pipeline |
| **VIF UNPACK formats** | `db-ps2-architecture.md` | §6 VIF Unpack Formats |
| **SPU2 / sound** | `db-ps2-architecture.md` | §7 SPU2 |
| **ADPCM format** | `db-ps2-architecture.md` | §7 SPU2 ADPCM Format |
| **SPU2 KEY ON/OFF, ENDX, AutoDMA** | `db-ps2-architecture.md` | §7 SPU2 Voice Control & DMA |
| **SPU2 effect area / reverb** | `db-ps2-architecture.md` | §7 SPU2 Voice Control & DMA |
| **IPU (MPEG decoder)** | `db-ps2-architecture.md` | §13 IPU |
| **IOP subsystem** | `db-ps2-architecture.md` | §8 IOP Subsystem |
| **SIF (EE↔IOP)** | `db-ps2-architecture.md` | §8 SIF |
| **Exception vectors** | `db-ps2-architecture.md` | §9 Exception Vectors |
| **Boot sequence** | `db-ps2-architecture.md` | §9 Boot Flow |
| **FPU quirks (non-IEEE)** | `db-ps2-architecture.md` | §10 FP Quirks |
| **Normal mapping technique** | `db-ps2-architecture.md` | §11 Normal Mapping |
| **Optimization patterns** | `db-ps2-architecture.md` | §12 Optimization Patterns |
| **Double buffering** | `db-ps2-architecture.md` | §12 DMA Double-Buffering |
| **Typical frame data flow** | `db-ps2-architecture.md` | §14 Game Data Flow |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **R5900 instructions** | `db-isa.md` | Full instruction tables |
| **Integer ALU instructions** | `db-isa.md` | CPU Integer Instructions |
| **MMI 128-bit SIMD** | `db-isa.md` | R5900 128-bit (MMI) Extensions |
| **Branch / jump instructions** | `db-isa.md` | Branch / Jump Instructions |
| **Load / store instructions** | `db-isa.md` | Load / Store Instructions |
| **COP0 instructions** | `db-isa.md` | COP0 Instructions |
| **COP1 (FPU) instructions** | `db-isa.md` | COP1 Instructions |
| **COP2 (VU0 macro) instructions** | `db-isa.md` | COP2 Instructions |
| **MIPS calling convention** | `db-isa.md` | MIPS Calling Convention |
| **SA register / QFSRV** | `db-isa.md` | SA Register |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **VU upper instructions (FMAC)** | `db-vu-instructions.md` | Upper Instructions |
| **VU lower instructions** | `db-vu-instructions.md` | Lower Instructions |
| **VU branch / flow** | `db-vu-instructions.md` | Branch Instructions |
| **VU flags (MAC, Status, Clip)** | `db-vu-instructions.md` | Flag Operations |
| **VU special regs (I, Q, P, ACC)** | `db-vu-instructions.md` | Special Registers |
| **XGKICK** | `db-vu-instructions.md` | XGKICK |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Hardware register addresses** | `db-registers.md` | All register map tables |
| **Timer registers** | `db-registers.md` | Timer section |
| **DMA registers** | `db-registers.md` | DMA section |
| **GIF registers** | `db-registers.md` | GIF section |
| **VIF registers** | `db-registers.md` | VIF section |
| **IPU registers** | `db-registers.md` | IPU section |
| **GS privileged registers** | `db-registers.md` | GS Privileged section |
| **GS general registers bit-fields** | `db-registers.md` | GS General Registers |
| **COP0 register bit-fields** | `db-registers.md` | COP0 Registers section |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Memory map / address ranges** | `db-memory-map.md` | Full address map |
| **KSEG0 / KSEG1 / KUSEG** | `db-memory-map.md` | Segment mapping |
| **ELF loading / entry point** | `db-memory-map.md` | ELF Layout |
| **Kernel memory areas** | `db-memory-map.md` | Kernel Areas |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Syscall numbers + handler** | `db-syscalls.md` | Syscall Table |
| **IOP RPC mechanism** | `db-syscalls.md` | IOP RPC |
| **Stub linking (IMPORTS/EXPORTS)** | `db-syscalls.md` | Stub Patterns |
| **Exception dispatching** | `db-syscalls.md` | Exception Handling |
| **Thread management syscalls** | `db-syscalls.md` | Thread Syscalls |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **sceDma* functions** | `db-sdk-functions.md` | DMA Functions |
| **sceGs* functions** | `db-sdk-functions.md` | GS Functions |
| **scePad* functions** | `db-sdk-functions.md` | Pad Functions |
| **Controller SPI protocol** | `db-sdk-functions.md` | PAD SPI Protocol |
| **sceVif* / sceVu* functions** | `db-sdk-functions.md` | VIF/VU Functions |
| **File I/O (sceOpen, etc.)** | `db-sdk-functions.md` | File I/O |
| **Memory allocation (malloc)** | `db-sdk-functions.md` | Memory Management |
| **sceGsSyncV / sceGsSyncPath** | `db-sdk-functions.md` | GS Sync Functions |
| **printf / sceWrite** | `db-sdk-functions.md` | Debug / Output |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **PS2Recomp pipeline / TOML** | `03-ps2recomp-pipeline.md` | Full pipeline |
| **TOML configuration** | `03-ps2recomp-pipeline.md` | Configuration |
| **Override system (*.cpp)** | `03-ps2recomp-pipeline.md` | Override System |
| **Build process (cmake)** | `03-ps2recomp-pipeline.md` | Build Process |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Ghidra analysis workflow** | `05-ghidra-ghydramcp-guide.md` | Analysis |
| **GhydraMCP tools list** | `05-ghidra-ghydramcp-guide.md` | MCP Tools |
| **Function naming conventions** | `05-ghidra-ghydramcp-guide.md` | Naming |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Game porting methodology** | `06-game-porting-playbook.md` | Step-by-step |
| **Common porting blockers** | `06-game-porting-playbook.md` | Blockers |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Decompiled code patterns** | `07-ps2-code-patterns.md` | Pattern library |
| **DMA setup patterns** | `07-ps2-code-patterns.md` | DMA Patterns |
| **VU program loading patterns** | `07-ps2-code-patterns.md` | VU Load Patterns |
| **GS init patterns** | `07-ps2-code-patterns.md` | GS Init Patterns |

---

| I need to know about... | Go to | Section |
|------------------------|-------|---------|
| **Deep hardware reference** | `09-ps2tek.md` | Everything (232K) |

---

## File Inventory

| File | Size | Last Updated | Content Type |
|------|------|-------------|-------------|
| `db-ps2-architecture.md` | ~40 KB | 2026-03-13 | System diagrams (mermaid), pipelines, data flow |
| `db-ps2-index.md` | ~9 KB | 2026-03-13 | THIS FILE — master topic → file+section map |
| `db-isa.md` | ~24 KB | 2026-03-13 | R5900 instruction tables (630 lines) |
| `db-vu-instructions.md` | ~15 KB | 2026-03-13 | VU0/VU1 micro instruction tables |
| `db-registers.md` | ~53 KB | 2026-03-13 | All HW register addresses + bit-fields |
| `db-sdk-functions.md` | ~34 KB | 2026-03-13 | SDK function signatures + PAD protocol |
| `db-syscalls.md` | ~15 KB | 2026-03-13 | Syscall table, stubs, RPC, exception handling |
| `db-memory-map.md` | ~7 KB | 2026-03-13 | Address space map, ELF layout |
| `03-ps2recomp-pipeline.md` | ~9 KB | 2026-03-13 | PS2Recomp tool pipeline + TOML config |
| `05-ghidra-ghydramcp-guide.md` | ~5 KB | 2026-03-04 | Ghidra/GhydraMCP analysis workflow |
| `06-game-porting-playbook.md` | ~6 KB | 2026-03-05 | Game porting methodology |
| `07-ps2-code-patterns.md` | ~4 KB | 2026-03-03 | Decompiled code pattern recognition |
| `09-ps2tek.md` | ~232 KB | 2026-02-18 | Deep hardware reference (all registers) |

**Total knowledge base**: ~453 KB of structured, searchable PS2 knowledge.
