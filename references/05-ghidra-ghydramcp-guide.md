# Reference: Ghidra & GhydraMCP Playbook
> Use this when setting up Ghidra for a PS2 game or invoking `mcp_ghydra_*` tools for binary analysis.

## 1. Ghidra Setup for PS2 (User Prerequisites)
Before the agent can do anything via MCP, the user MUST have the environment prepared. If the user complains that Ghidra is outputting garbage, verify these plugins are installed:
- **Ghidra Version**: Strictly **11.4.2** (earlier versions may have issues with the newer EE plugin).
- **EE Plugin Requirement**: [ghidra-emotionengine-reloaded](https://github.com/chaoticgd/ghidra-emotionengine-reloaded). This adds the custom `R5900` language processor to Ghidra. Standard MIPS will **NOT** decompile PS2 correctly.
- **Importing ELF**: User must import the game ELF, select `MIPS R5900` language, and ensure `Options -> Language/Compiler Spec` is correctly set.

## 2. GhydraMCP Server Setup
GhydraMCP exposes Ghidra instances as REST/MCP tools.
**Agent Instructions:**
1. Check if tools are active by running `mcp_ghydra_instances_list()`.
2. If the user needs setup help:
   - Download the GhydraMCP zip from `https://github.com/starsong-consulting/GhydraMCP`.
   - Install via `Ghidra -> File -> Install Extension`.
   - Enable via `File -> Configure -> Configure All Plugins -> GhidraMCPPlugin` in the CodeBrowser.
   - Set Port in `Edit -> Tool Options -> Miscellaneous -> GhidraMCP HTTP Server`. (Default is usually 8888 or 8192).

## 3. GhydraMCP - Common Operation Patterns

### A. Discovering the Target
Always start by verifying the connection and setting the active instance.
- **Tool**: `mcp_ghydra_instances_list()`
- **Tool**: `mcp_ghydra_instances_use(port=8192)`

### B. Understanding Unknown Functions (`sub_xxx`)
If the game crashes at `sub_00123456`, you don't need to guess.
1. **Decompile**: `mcp_ghydra_functions_decompile(address="0x00123456")`. Read the C-like pseudocode.
2. **Look for context**: Are there debug strings? Does it call standard library functions (`memcpy`)?
3. **Check Cross-References (XRefs)**: `mcp_ghydra_xrefs_list(to_addr="0x00123456")`. Who calls this? What is passed in `a0` before the call?

### C. Finding Known Logic via Strings
A great way to locate the main menu or specific systems is via debug strings in the `.rodata` section.
1. **Search**: `mcp_ghydra_data_list_strings(filter="loading")`.
2. Find the address of the string "loading".
3. **Trace back**: Use `mcp_ghydra_xrefs_list(to_addr="<string_address>")` to find the function that uses that string.

### D. Renaming to Improve Future Analysis
Once you figure out what `sub_00123456` does, rename it permanently in Ghidra so the user (and you, in future calls) can see it clearly.
- **Tool**: `mcp_ghydra_functions_rename(address="0x00123456", new_name="Sound_Init")`

### E. Getting the Full Function Map for PS2Recomp
Ghidra can export a CSV that `ps2_analyzer` uses to identify stripped functions perfectly.
While there isn't a single MCP tool for "export all to CSV", you must guide the user to run the official script provided in the PS2Recomp repository:
- **Location:** `ps2xRecomp/tools/ghidra/ExportPS2Functions.py` (or `.java`)
- Tell the user to run this via Ghidra's Script Manager and provide you with the resulting `functions.csv` so you can run `ps2_analyzer` with it.

## 4. Ghidra Decompiler Tropes & Fixes
When reading `mcp_ghydra_functions_decompile` output:
- **`__builtin_memcpy` / `__builtin_memset`**: Sometimes Ghidra guesses library functions but applies incorrect signatures if the headers aren't imported.
- **`qword ptr` or `afff` types**: This means 128-bit vectorization (MMI) or floating point operations are happening. Ghidra struggles to render these cleanly in C.
- **Arguments mismatch**: If the decompiler shows 2 arguments but the MIPS clearly pushes to `a2` and `a3`, the decompiler's signature algorithm failed. You can fix this using `mcp_ghydra_functions_set_signature(address, "void func(int a, int b, int c, int d)")`.
