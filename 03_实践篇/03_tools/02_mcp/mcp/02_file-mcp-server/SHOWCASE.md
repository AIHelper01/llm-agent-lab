English | [Simplified Chinese](SHOWCASE.zh-CN.md)

# Organizing Source Files with Natural Language: A w-File Workbench MCP Showcase

Test date: October 17, 2026. Client: Codex desktop app. Service: `local_file_mcp`, implemented in `w-file_workbench_mcp_server.py`. Test directory: `D:\files` on the local Windows machine.

The service is now named w-File Workbench MCP (`w-FileWorkbenchMCP`). During the
original session, its entry script was `secure_file_mcp_server.py`; that name
has since been removed; use the current primary script. `local_file_mcp` is the client connector alias.

## Starting files

The directory contained five UTF-8 text files and no subdirectories. Each file held a file-operation code example.

| File | Original size | Contents |
| --- | ---: | --- |
| a.txt | 288 bytes | Python: read, overwrite, and append |
| b.txt | 411 bytes | Go: create a file and write through a buffer |
| c.txt | 533 bytes | Java: create a file and write to it; public class named Main |
| d.txt | 218 bytes | C: write using fopen, fprintf, and fclose |
| e.txt | 293 bytes | Node.js: asynchronous writes and reads using fs |

## Original conversation and actual execution

The prompts below are English translations of the original Chinese requests. Descriptive file names are also translated into English for this edition; they are illustrative equivalents of the names used in the actual session. Original fixture names (a.txt through e.txt), tool names, sizes, and execution results are preserved.

| Step | User request | Actual tools and result |
| --- | --- | --- |
| 1 | What files are in D:\files? Use MCP. | `list_files` returned a.txt through e.txt. |
| 2 | Suggest suitable names based on their contents. | Five `read_file` calls identified the languages and purposes; names were suggested without changing files. |
| 3 | Apply the changes. | Five `rename_file` calls applied the descriptive names below. |
| 4 | Change each file's type as well. | Five `rename_file` calls applied source-code extensions; the Java file became Main.java. |
| 5 | Add a TypeScript example in a new file. | `create_file` added the example; `read_file` verified its contents. |
| 6 | Delete the Go file in the folder. | MCP had no deletion tool at the time. PowerShell Remove-Item deleted the file; Test-Path returned False. |
| 7 | Restore the folder to its initial state. | MCP restored four names and recreated b.txt. PowerShell removed the added TS file and corrected b.txt's line endings. |

### File-name mapping

| Original | Descriptive name | Source-code name |
| --- | --- | --- |
| a.txt | python_file_read_write_append.txt | python_file_read_write_append.py |
| b.txt | go_file_create_buffered_write.txt | go_file_create_buffered_write.go |
| c.txt | java_file_create_write.txt | Main.java |
| d.txt | c_file_create_write.txt | c_file_create_write.c |
| e.txt | nodejs_async_file_read_write.txt | nodejs_async_file_read_write.js |

Changing an extension does not compile, convert, or execute code. The Java file was named Main.java to match its `public class Main` declaration.

The added file, shown here as `typescript_file_read_write_append.ts`, used `writeFileSync`, `appendFileSync`, and `readFileSync` from `node:fs` to operate sequentially on `typescript.txt`, with explicit string types. The example was created and read back; it was not executed.

### Issues revealed by the experiment

1. **Missing tool:** deleting a file required leaving MCP, preventing an entirely MCP-based workflow.
2. **Limited recovery:** `restore_last_rename` only undoes a rename. It cannot undo file creation, deletion, or content replacement. The Go file was reconstructed from content previously read into the conversation, rather than restored from a backup.
3. **Line-ending fidelity:** on Windows, default text writing converted supplied CRLF line endings again. The recreated b.txt grew from 411 to 431 bytes. Removing the extra CR characters restored its size to 411 bytes.
4. **Verification limits:** the final directory contained the five original names, and the Go file was back to 411 bytes. No complete SHA-256 comparison was performed for all five files, so this does not establish exact restoration of all contents and metadata.

## Workflow with the newly added MCP tools

Restart the server and refresh the client's tool list before using the new tools. The following is a reproduction procedure, **not a record of calls made in the original conversation**.

```text
list_files(directory="D:\\files")
read_file(filepath="D:\\files\\b.txt")
rename_file(old_path="D:\\files\\b.txt", new_name="go_file_create_buffered_write.go")
delete_file(filepath="D:\\files\\go_file_create_buffered_write.go")
# Save the returned deletion_id.
restore_deleted_file(deletion_id="32-character ID returned by delete_file")
restore_last_rename(filter_dir="D:\\files")
list_files(directory="D:\\files")
```

Deletion now claims the source entry under a temporary name, saves and verifies its bytes and supported file attributes under `FILE_MCP_STATE_DIR/.deleted_files/<deletion_id>/`, then removes the claimed entry. Detected changes cancel deletion. Restoration stages and verifies bytes before publication and refuses to overwrite an existing path. This is a server-managed backup, not the operating system's recycle bin. `cleanup_backups` can preview and permanently purge old completed backups. There is no standalone recursive directory deletion tool.

For a complete replay, copy the five fixtures into a temporary directory and record their original names and SHA-256 hashes. Check the returned `ok` at every step. Finally, verify that only a.txt through e.txt remain and that their hashes match the originals. The added TS file can be removed with `delete_file`. Conversation history should not be treated as a reliable backup.

## Improvements implemented after the experiment

| Area | Current implementation |
| --- | --- |
| Directory snapshots | Create/list snapshots, preview restoration, require the reviewed plan ID, and verify final names, structure, and hashes. |
| History and concurrency | Thread and OS file locks protect shared state; atomic history writes, corruption reporting, file identity checks, and rollback on history-write failure. |
| Deletion records and retention | Paginated record queries, a configurable capacity budget, retention previews, and explicit cleanup. Pending/failed deletion records are retained. |
| Atomic writes and recovery | Encode and stage before publication, verify backup hashes, refuse overwrite during recovery, and report partial failures. |
| Batch rename previews | Preview and validate 1..100 renames, require a current plan ID, and return completed items on failure. Swaps and chains are rejected. |
| Directory pagination | Filter by name pattern and page with limit/offset/next_offset. |
| Read ranges | Read bounded byte ranges with explicit or automatic UTF-8/GB18030 decoding and a character-aligned next_offset. Preserve supplied line endings on writes. |
| Deployment | Retain the original trusted-environment access model; authentication remains an external gateway or deployment responsibility. |

These additions were validated after the original conversation; they do not change its historical results. The shared lock coordinates participating server calls, not external file writers. Directory restoration is not a directory-wide transaction; interrupted processes may leave staging/quarantine files or pending records. Full filesystem metadata preservation and crash-transactional recovery remain outside the contract. See [validation details](TESTING.md).

## Local regression checks

From this directory:

```bash
python -B test_file_lifecycle.py
python -B test_file_http.py
```

From the parent `mcp` directory, run the existing checks:

```bash
python -B test_bilingual_tools.py
```

Tests use temporary directories and do not modify the real `D:\files` directory. Coverage includes English and Chinese scenarios, real HTTP MCP dispatch, CRLF/LF preservation, binary recovery, interrupted writes, backup corruption, history failures, thread/process concurrency, retention cleanup, and full snapshot restoration after renaming, creating, deleting, and changing files.
