# Reference: Infinite Knowledge Base (PS2docs)
> Use this when you encounter a highly specific hardware register, SCMD command, SIF RPC structure, VIF packet format, or undocumented PS2 behavior that is not covered in the other reference files.

## The Absolute Source of Truth

The user maintains a local repository of exhaustive PlayStation 2 documentation, including the legendary `ps2tek` (the reverse engineering holy grail), MIPS instruction set references, and Sony architectural analyses.

**Location of Absolute Truth:**
`references/09-ps2tek.md` (Embedded locally)

If you ever find yourself stuck wondering:
- "What exactly does bit 5 of the GS `TEX0` register do?"
- "What is the exact memory layout of the SPU2 registers?"
- "How does the IPU DMA channel format its packets?"
- "What is the specific behavior of the `mfc0` instruction when reading the `Count` register?"

Do **NOT** guess. Do **NOT** hallucinate based on general MIPS knowledge.

## How to extract Infinite Knowledge

You must leverage your environment tools to read from the embedded documentation.

### 1. `grep_search` is your best friend
The most important file in that folder is:
`references/09-ps2tek.md`

Use `grep_search` with highly specific queries (e.g., `TEX0`, `DMAC`, `SIFCMD`, `0x12000000`, `PMODE`) against this specific file. Since the file is over 230 KB of pure markdown, grep is the only efficient way to find the exact tables and explanations you need.

### 2. Reading PDFs and Architectural Diagrams (`pdf_grep.py` & Vision)
If `09-ps2tek.md` does not have the answer (e.g., you need to understand the visual layout of the DMAC, or mathematically specific MIPS operations), you have a massive library of 20+ Official Sony Manuals and architecture PDFs located inside this skill's `resources/` folder.

**Notable files available in `resources/` include:**
- `PlayStation 2 Architecture _ A Practical Analysis.pdf` (16MB detailed analysis)
- `mips_instruction_set_reference.pdf`
- `EE_Users_Manual.pdf`, `EE_Core_Instruction_Set_Manual.pdf` (Emotion Engine core)
- `GS_Users_Manual.pdf` (Graphics Synthesizer)
- `VU_Users_Manual.pdf` (Vector Units)
- `SPU2_Overview_Manual.pdf` (Sound)

**Agent, you possess two distinct superpowers for PDFs. You must use the correct one based on what you are looking for:**

**DECISION LOGIC:**
- Are you looking for binary decodings, hardware register constraints, bitwise tables, or operational opcodes? -> **USE SUPERPOWER 1 (Text & Tables)**
- Are you looking at a page that `pdf_grep.py` tells you is a "Figure", a "Block Diagram", or a topological layout of hardware components? -> **USE SUPERPOWER 2 (Multimodal Vision)**

---

### Superpower 1. Text & Table Extraction (`scripts/pdf_grep.py`)
Use this for 99% of your documentation queries. You can pass the PDF path and a search string to extract highly detailed MIPS opcodes or SCMD tables on the fly. 
`python scripts/pdf_grep.py "resources/EE_Users_Manual.pdf" "DMA Channel 4"`
> **⚠️ CRITICAL: CONTEXT PROTECTION**
> Never attempt to read the entire PDF. The script enforces a max-page limit. If your query fails because it hits 20+ pages, refine it to be hyper-specific. This saves your context window from collapsing.

### Superpower 2. Visual/Diagram Parsing (`scripts/pdf_extract_image.py`)
If you need to understand an *image*, topological map, or block diagram from those PDFs (e.g., knowing how the VIF pipelines connect to the GS visually), you must deploy your native Multimodal Vision. You do this completely offline without the user's help.
1. Run the extractor script and save the output **strictly** to the `png/` directory:
   `python scripts/pdf_extract_image.py "resources/EE_Users_Manual.pdf" 112 "png/vif_architecture.png"`
2. Use your native `view_file` tool on `png/vif_architecture.png`. Because it's an image, your Multimodal Vision capability will automatically activate. You can look at the physical diagram and deduce the architectural constraints entirely autonomously.

## The Golden Rule of PS2 Porting

**"If it's hardware, it's mapped. If it's mapped, it's documented. If it's documented, it's in ps2tek."**

Never bypass an unknown hardware interaction by stubbing it with `ret0` without first checking the `ps2tek` to understand *why* the game is touching that memory. If you stub a DMAC completion flag with 0, you might cause an infinite spinlock. Read the docs!
