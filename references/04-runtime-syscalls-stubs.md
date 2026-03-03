# Reference: ps2xRuntime & C++ Implementation
> Use this when working in the `ps2xRuntime` directory, fixing syscalls, writing stubs, or writing Game Overrides.

The `ps2xRuntime` library is the environment executing the generated C++ code. It provides the memory model, CPU context, MMIO routing, and native SDK implementations.

## 1. The Core Loop
The execution of the game begins and remains in a very tight, highly optimized loop.
When `jal` instructions are encountered in MIPS, the generated code uses a table lookup to call the corresponding C++ function pointer. 

## 2. Memory Model
The PS2 has 32MB of main RAM starting at `0x00000000`.
In `ps2xRuntime`, memory is generally handled as a large flat `uint8_t` array.
*Crucial*: Because PS2 games assume physical memory maps, the runtime traps reads/writes to specific ranges and routes them. Let's look at MMIO routing:

### MMIO (Memory Mapped I/O)
When the game tries to read or write to addresses like `0x10000000` (IOP) or `0x12000000` (GS), normal memory access would segfault or return garbage.
The runtime handles these through explicit getters/setters in the `R5900Context` or macro-inlined memory accesses.

## 3. Syscalls (System Calls)
A `SYSCALL` instruction jumps to the BIOS exception handler. Sony provides hundreds of syscalls for threading, semaphores, interrupt handlers, and hardware initialization.
**File:** `ps2xRuntime/src/lib/ps2_syscalls.cpp`

If a game executes an unimplemented syscall, the runtime prints `[Syscall TODO]` and usually crashes. 
*Fixing it:*
1. Identify the Syscall ID from the log (e.g., `Syscall 0x02 executing`).
2. Search online (ps2dev documentation) or the hardware bible to see what Syscall `0x02` is (`GsPutDrawEnv`).
3. Add a case statement in `ps2_syscalls.cpp` handler switch.
4. Implement the logic, reading arguments from `ctx.gpr[4]` (a0), `ctx.gpr[5]` (a1), etc.

## 4. Writing C++ Stubs
When you bind an address in `game.toml` to a `handler`, you must implement that handler in C++.

### The Triage Strategy
When reverse engineering stripped games, you'll encounter hundreds of `Warning: Unimplemented PS2 stub called`. 
Instead of writing real implementations immediately, we create "Triage Stubs":
```cpp
void ret0(R5900Context& ctx) { ctx.gpr[2].words[0] = 0; } // Returns 0
void ret1(R5900Context& ctx) { ctx.gpr[2].words[0] = 1; } // Returns 1
void reta0(R5900Context& ctx) { ctx.gpr[2].words[0] = ctx.gpr[4].words[0]; } // Returns Arg0
```
Try binding unknown functions to `ret0` or `ret1`. Does the game boot further? If so, you've bypassed a check. You can figure out *what* check it was later using Ghidra.

### Writing Real Implementations (`sceCdRead` example)
When you know what a function does, emulate it natively. Example: intercepting a CD-ROM texture load.
```cpp
void my_sceCdRead(R5900Context& ctx) {
    uint32_t lsn = ctx.gpr[4].words[0]; // a0: Logical Sector Number
    uint32_t sectors = ctx.gpr[5].words[0]; // a1: Number of sectors
    uint32_t buffer_ptr = ctx.gpr[6].words[0]; // a2: Destination address in EE RAM

    // Native C++ logic to read from PC file system instead of PS2 DVD...
    // MyFileSystem::Read(lsn, sectors, memory.GetPointer(buffer_ptr));

    ctx.gpr[2].words[0] = 1; // Return 1 (success)
}
```

## 5. Game Overrides (`Game_Overrides.txt` concept)
You should keep game-specific hacks *out* of the core `ps2_syscalls.cpp` or generic SDK headers to avoid breaking other games.

Instead, create a C++ file for the specific game (e.g. `swe3_overrides.cpp`).
Register your overrides against the game's ELF ID or serial.
```cpp
// Override the binding for address 0x123456 dynamically
Runtime::OverrideFunction(0x123456, swe3_custom_cd_read);
```
This is how a single PS2Recomp runtime stays compatible with multiple games while allowing deep custom patches per game.

## 6. Vectorization and SIMD Intrinsics
PS2 math relies heavily on 128-bit vectorization.
The runtime expects heavy use of SSE/AVX intrinsics (`_mm_add_epi32`, `_mm_mul_ps`) when manually replacing VU0/MMI geometry calculations. Do NOT write naive scalar loops for math-heavy stubs; it will destroy frame rates.
