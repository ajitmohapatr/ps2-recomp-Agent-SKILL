# PS2 EE Hardware Register Map
> Maps PS2 hardware register addresses to names, subsystems, and runtime handling.

## Lookup Protocol
1. Match the address from decompiled code or IO write trace
2. Check **Subsystem** to understand context
3. **Runtime Handling**: `impl` = has write handler in `ps2_memory.cpp`, `store-only` = stored but not acted on

## Address Ranges

| Range | Subsystem | Description |
|-------|-----------|-------------|
| `0x10000000–0x100000FF` | TIMER0 | Timer 0 registers |
| `0x10000200–0x100002FF` | TIMER1 | Timer 1 registers (same layout) |
| `0x10002000–0x10002030` | IPU | Image Processing Unit |
| `0x10003800–0x100039FF` | VIF0 | Vector Interface 0 |
| `0x10003C00–0x10003DFF` | VIF1 | Vector Interface 1 |
| `0x10008000–0x100080FF` | DMA Chan 0 | VIF0 DMA |
| `0x10009000–0x100090FF` | DMA Chan 1 | VIF1 DMA |
| `0x1000A000–0x1000A0FF` | DMA Chan 2 | GIF DMA |
| `0x1000B000–0x1000B0FF` | DMA Chan 3 | fromIPU DMA |
| `0x1000B400–0x1000B4FF` | DMA Chan 4 | toIPU DMA |
| `0x1000C000–0x1000C0FF` | DMA Chan 5 | SIF0 DMA |
| `0x1000C400–0x1000C4FF` | DMA Chan 6 | SIF1 DMA |
| `0x1000C800–0x1000C8FF` | DMA Chan 7 | SIF2 DMA |
| `0x1000D000–0x1000D0FF` | DMA Chan 8 | fromSPR DMA |
| `0x1000D400–0x1000D4FF` | DMA Chan 9 | toSPR DMA |
| `0x1000E000–0x1000E0FF` | DMAC | DMA controller global registers |
| `0x1000F000–0x1000F010` | INTC | Interrupt controller (STAT, MASK) |
| `0x1000F200–0x1000F260` | SIF | SIF control registers |
| `0x10007010` | IPU_IN_FIFO | IPU input FIFO |
| `0x12000000–0x12002000` | GS Privileged | GS privileged registers (PMODE, CSR, etc.) |

---

## Timer Registers (0x10000000 / 0x10000200)

Timers 0 and 1 share the same layout. Timer 0 base = `0x10000000`, Timer 1 base = `0x10000200`.

| Offset | Name | R/W | Handling | Notes |
|--------|------|-----|----------|-------|
| `+0x00` | Tn_COUNT | RW | impl | Counter value — reads return 0 in runtime |
| `+0x10` | Tn_MODE | RW | store-only | Timer mode (clock source, gate, etc.) |
| `+0x20` | Tn_COMP | RW | store-only | Compare register |
| `+0x30` | Tn_HOLD | RW | store-only | Hold register (Timer 0/1 only) |

> Runtime: both Timer0/1 reads return 0 — timers are not emulated.

---

## IPU Registers (0x10002000)

| Address | Name | R/W | Handling | Notes |
|---------|------|-----|----------|-------|
| `0x10002000` | IPU_CMD | RW | impl | Command register — reset on CTRL.RST |
| `0x10002010` | IPU_CTRL | RW | impl | Control — bit30 write triggers full IPU reset |
| `0x10002020` | IPU_BP | RW | impl | Bit position — reset on CTRL.RST |
| `0x10002030` | IPU_TOP | R | impl | Top of bitstream |
| `0x10007010` | IPU_IN_FIFO | W | store-only | Input FIFO write |

---

## VIF1 Registers (0x10003C00)

| Address | Name | R/W | Handling | Notes |
|---------|------|-----|----------|-------|
| `0x10003C00` | VIF1_STAT | R | impl | Status register — read in sync loops |
| `0x10003C10` | VIF1_FBRST | W | impl | Force break/reset — bit0=RST, bit3=STC |
| `0x10003C30` | VIF1_MARK | RW | impl | Mark register, clears MRK flag on write |
| `0x10003C40` | VIF1_CYCLE | RW | impl | Cycle register (CL/WL) |
| `0x10003C50` | VIF1_MODE | RW | impl | Mode (0–3) |
| `0x10003C60` | VIF1_NUM | RW | impl | Number of data to process |
| `0x10003C70` | VIF1_MASK | RW | impl | Write mask |
| `0x10003C80` | VIF1_CODE | RW | impl | Current VIFcode |
| `0x10003C90` | VIF1_ITOPS | RW | impl | Interrupt TOP register |
| `0x10003CA0` | VIF1_BASE | RW | impl | Double-buffer base |
| `0x10003CB0` | VIF1_OFST | RW | impl | Double-buffer offset |
| `0x10003CC0` | VIF1_TOPS | RW | impl | TOP register |
| `0x10003CD0` | VIF1_ITOP | RW | impl | Interrupt TOP actual |
| `0x10003CE0` | VIF1_TOP | RW | impl | TOP actual |

---

## DMA Channel Layout (per-channel, base+offset)

Each DMA channel at base address `0x10008000 + N*0x1000` (or `0x1000B400` etc.):

| Offset | Name | Description |
|--------|------|-------------|
| `+0x00` | Dn_CHCR | Channel control (bit8=STR start) |
| `+0x10` | Dn_MADR | Memory address |
| `+0x20` | Dn_QWC | Quadword count |
| `+0x30` | Dn_TADR | Tag address (chain mode) |
| `+0x40` | Dn_ASR0 | Address stack 0 (call/ret chains) |
| `+0x50` | Dn_ASR1 | Address stack 1 |

**DMA Channel Base Addresses:**

| Channel | Base | Purpose |
|---------|------|---------|
| 0 | `0x10008000` | VIF0 |
| 1 | `0x10009000` | VIF1 |
| 2 | `0x1000A000` | GIF |
| 3 | `0x1000B000` | fromIPU |
| 4 | `0x1000B400` | toIPU |
| 5 | `0x1000C000` | SIF0 (IOP→EE) |
| 6 | `0x1000C400` | SIF1 (EE→IOP) |
| 7 | `0x1000C800` | SIF2 |
| 8 | `0x1000D000` | fromSPR |
| 9 | `0x1000D400` | toSPR |

---

## DMAC Global Registers (0x1000E000)

| Address | Name | R/W | Handling | Notes |
|---------|------|-----|----------|-------|
| `0x1000E000` | D_CTRL | RW | impl | DMAC master enable (bit0) |
| `0x1000E010` | D_STAT | RW | impl | Status — low10=W1C channel status, bits16–25=toggle mask |
| `0x1000E020` | D_PCR | RW | store-only | Priority control |
| `0x1000E030` | D_SQWC | RW | store-only | Skip quadword count |
| `0x1000E040` | D_RBSR | RW | store-only | Ring buffer size |
| `0x1000E050` | D_RBOR | RW | store-only | Ring buffer offset |

---

## GS Privileged Registers (0x12000000)

| Address | Offset | Name | R/W | Notes |
|---------|--------|------|-----|-------|
| `0x12000000` | 0x0000 | PMODE | RW | CRT mode control |
| `0x12000010` | 0x0010 | SMODE1 | RW | Sync mode 1 |
| `0x12000020` | 0x0020 | SMODE2 | RW | Sync mode 2 (interlace) |
| `0x12000070` | 0x0070 | DISPFB1 | RW | Display framebuffer 1 |
| `0x12000080` | 0x0080 | DISPLAY1 | RW | Display output 1 |
| `0x12000090` | 0x0090 | DISPFB2 | RW | Display framebuffer 2 |
| `0x120000A0` | 0x00A0 | DISPLAY2 | RW | Display output 2 |
| `0x120000B0` | 0x00B0 | EXTBUF | RW | External buffer (feedback write) |
| `0x120000C0` | 0x00C0 | EXTDATA | RW | External data (feedback area) |
| `0x120000D0` | 0x00D0 | EXTWRITE | RW | External write trigger |
| `0x120000E0` | 0x00E0 | BGCOLOR | RW | Background color |
| `0x12001000` | 0x1000 | CSR | RW | System status — bits0–1 W1C |
| `0x12001010` | 0x1010 | IMR | RW | Interrupt mask |
| `0x12001040` | 0x1040 | BUSDIR | RW | Bus direction |
| `0x12001080` | 0x1080 | SIGLBLID | RW | Signal/label ID |

---

## SIF Registers (0x1000F200)

| Address | Name | R/W | Handling | Notes |
|---------|------|-----|----------|-------|
| `0x1000F200` | SIF_MSCOM | RW | store-only | SIF main→sub communication |
| `0x1000F210` | SIF_SMCOM | RW | store-only | SIF sub→main communication |
| `0x1000F220` | SIF_MSFLG | RW | store-only | Main→sub flag |
| `0x1000F230` | SIF_SMFLG | R | impl | Sub→main flag — **reads return `0x60000`** |
| `0x1000F240` | SIF_CTRL | R | impl | Control — **reads return `0xF0000002`** |
| `0x1000F260` | SIF_BD6 | RW | store-only | Unknown |

> Runtime: `SIF_SMFLG` returns `0x60000` and `SIF_CTRL` returns `0xF0000002` — hardcoded to satisfy initialization checks.

---

## INTC Registers (0x1000F000)

| Address | Name | R/W | Handling | Notes |
|---------|------|-----|----------|-------|
| `0x1000F000` | I_STAT | RW | store-only | Interrupt status (W1C) |
| `0x1000F010` | I_MASK | RW | store-only | Interrupt mask (toggle) |

---

## DMA Chain Tag Format

```
Bits [15:0]  = QWC  (quadword count for this transfer)
Bits [28:26] = ID   (tag type: 0=REFE, 1=CNT, 2=NEXT, 3=REF, 5=CALL, 6=RET, 7=END)
Bit  [31]    = IRQ  (interrupt request)
Bits [62:32] = ADDR (31-bit address for REF/NEXT/CALL tags)
```

**Tag IDs:**
- `0` REFE — transfer data at ADDR, end chain
- `1` CNT — transfer data following tag, continue at end of data
- `2` NEXT — transfer data following tag, next tag at ADDR
- `3`/`4` REF — transfer data at ADDR, next tag follows this tag
- `5` CALL — like NEXT but pushes return address to ASR stack
- `6` RET — pops return address from ASR stack
- `7` END — transfer data following tag, end chain
