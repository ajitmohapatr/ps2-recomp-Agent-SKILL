# PS2 EE Memory Map
> Complete address space layout for the PS2 Emotion Engine as modeled in ps2xRuntime.

## Lookup Protocol
1. Check the address against the ranges below
2. **Runtime Column** shows how `ps2_memory.cpp` handles accesses
3. Use this to understand what memory regions a game address falls into

---

## Physical Memory Layout

| Start | End | Size | Region | Runtime Handling |
|-------|-----|------|--------|-----------------|
| `0x00000000` | `0x01FFFFFF` | 32 MB | **EE RDRAM** | `m_rdram[]` — main R/W memory |
| `0x10000000` | `0x1000FFFF` | 64 KB | **EE Registers** | `m_ioRegisters{}` — see db-registers.md |
| `0x10002000` | `0x10002030` | — | IPU registers | Write handler with IPU reset logic |
| `0x10003800` | `0x100039FF` | — | VIF0 registers | Store-only |
| `0x10003C00` | `0x10003DFF` | — | VIF1 registers | Full write handler for all VIF1 fields |
| `0x10008000` | `0x1000DFFF` | — | DMA channels | DMA start handler (CHCR bit8) |
| `0x1000E000` | `0x1000E0FF` | — | DMAC global | D_CTRL, D_STAT with W1C/toggle logic |
| `0x1000F000` | `0x1000F010` | — | INTC | Interrupt controller (STAT, MASK) |
| `0x1000F200` | `0x1000F260` | — | SIF registers | SIF_SMFLG/CTRL have hardcoded reads |
| `0x11000000` | `0x11003FFF` | 16 KB | **VU0 Code** | Not modeled in runtime |
| `0x11004000` | `0x11007FFF` | 16 KB | **VU0 Data** | Not modeled |
| `0x11008000` | `0x1100BFFF` | 16 KB | **VU1 Code** | Not modeled |
| `0x1100C000` | `0x1100FFFF` | 16 KB | **VU1 Data** | Not modeled |
| `0x12000000` | `0x12001FFF` | 8 KB | **GS Privileged** | `gs_regs` struct with CSR W1C handling |
| `0x1C000000` | `0x1C1FFFFF` | 2 MB | **IOP RAM** | `iop_ram[]` — allocated, zero-filled |
| `0x70000000` | `0x70003FFF` | 16 KB | **Scratchpad** | `m_scratchpad[]` — fast R/W |
| `0xBFC00000` | `0xBFC7FFFF` | 512 KB | **Boot ROM** | Not modeled |
| (internal) | — | 4 MB | **GS VRAM** | `m_gsVRAM[]` — used by DMA GIF/VIF1 paths |

---

## Virtual → Physical Address Translation

The runtime's `translateAddress()` handles MIPS address segments:

| Virtual Range | Segment | Translation |
|---------------|---------|-------------|
| `0x00000000–0x7FFFFFFF` | KUSEG | `addr & 0x1FFFFFFF` (strip TLB bits, mask to physical) |
| `0x80000000–0x9FFFFFFF` | KSEG0 | `addr & 0x1FFFFFFF` (cached, no TLB) |
| `0xA0000000–0xBFFFFFFF` | KSEG1 | `addr & 0x1FFFFFFF` (uncached, no TLB) |
| `0xC0000000–0xDFFFFFFF` | KSSEG | TLB mapped (not used in practice) |
| `0xE0000000–0xFFFFFFFF` | KSEG3 | TLB mapped (not used in practice) |
| `0x70000000–0x70003FFF` | Scratchpad | Detected by `isScratchpad()` before translation |

**Key runtime masks:**

```cpp
constexpr uint32_t PS2_RAM_SIZE         = 0x02000000;  // 32 MB
constexpr uint32_t PS2_RAM_MASK         = 0x01FFFFFF;  // 32 MB - 1
constexpr uint32_t PS2_IO_BASE          = 0x10000000;
constexpr uint32_t PS2_IO_SIZE          = 0x00010000;  // 64 KB
constexpr uint32_t PS2_SCRATCHPAD_SIZE  = 0x00004000;  // 16 KB
constexpr uint32_t PS2_GS_PRIV_REG_BASE = 0x12000000;
constexpr size_t   PS2_GS_VRAM_SIZE     = 4u * 1024u * 1024u;  // 4 MB
```

---

## Memory Access Alignment Rules

| Width | Alignment | Runtime Check |
|-------|-----------|---------------|
| 8-bit | None | — |
| 16-bit | 2-byte | `address & 1` → throws |
| 32-bit | 4-byte | `address & 3` → throws |
| 64-bit | 8-byte | `address & 7` → throws |
| 128-bit | 16-byte | `address & 15` → throws |

---

## Special Memory Regions

### Scratchpad (SPR)
- **Address**: `0x70000000–0x70003FFF`
- **Size**: 16 KB
- **Purpose**: Fast on-chip SRAM, used for DMA staging and temporary buffers
- **Detection**: `isScratchpad()` checks `(addr & 0x7FFFC000) == 0x70000000`
- **DMA**: SPR→RDRAM transfers handled by DMA channel 8/9

### GS Privileged Registers
- **Address**: `0x12000000–0x12001FFF`
- **Detection**: `isGsPrivReg()` checks range
- **Special**: CSR register at `0x12001000` has write-one-to-clear bits 0–1
- **Access**: Direct pointer via `gsRegPtr()` into `GsPrivRegs` struct

### DMA Control Flow
When CHCR.STR (bit 8) is written:
1. `writeIORegister()` detects DMA start
2. Reads MADR and QWC from channel registers
3. For GIF (ch2) and VIF1 (ch1): parses chain tags if mode=1
4. Enqueues `PendingTransfer` for later processing
5. `processPendingTransfers()` submits GIF packets / VIF1 data

---

## ELF Loading Layout

Typical PS2 game ELF sections mapped into RDRAM:

| Typical Range | Section | Notes |
|---------------|---------|-------|
| `0x00100000–0x001XXXXX` | `.text` | Game code (entry point usually here) |
| `0x002XXXXX–0x003XXXXX` | `.data` / `.rodata` | Initialized data |
| `0x004XXXXX–...` | `.bss` | Zero-initialized data |
| `0x00FXXXXX–0x01FFFFFF` | Heap/Stack | Game-managed, grows from InitHeap |
| `0x70000000` | SPR | Scratchpad (separate from RDRAM) |

> [!NOTE]
> Actual addresses vary per game. Use the ELF program headers (`readelf -l`) to determine exact mappings. The recompiler loads segments directly into `m_rdram`.
