# w-File Workbench MCP

English | [Simplified Chinese](README.zh-CN.md)

`w-file_workbench_mcp_server.py` exposes directory listing, text reads/writes,
metadata, same-directory renaming and restoration as MCP tools. Messages default
to English; Chinese is selected with `language="zh"`. Both English and Chinese
paths and content are preserved.

## Install and run

Use Python 3.12. From this directory:

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv
python w-file_workbench_mcp_server.py
```

Connect to `http://<server-ip>:16682/mcp`. To stop, press Ctrl+C.
The optional `.env` file configures the server settings below.

### Naming and migration

The service is **w-File Workbench MCP**, with MCP server name `w-FileWorkbenchMCP`
and primary script `w-file_workbench_mcp_server.py`. This is the only supported
startup entry; update old launch commands to use it. The `w-` prefix is the
owner's name initial and applies to future MCP service names and primary scripts
in this project. The script can be launched directly or loaded using
`importlib.util.spec_from_file_location`.
Existing `FILE_MCP_*` settings, port 16682, and `secure_rename_history.json`
are retained so existing data and launch configurations remain usable.
The repository's numbered `02_file-mcp-server` directory also remains unchanged.
After upgrading, restart the service and refresh the client's tool list.

## Tools

The table summarizes the parameters. All tools except `ping`
also accept optional `language="en"` (`en` or `zh`); use keyword arguments for new options.
Existing calls remain valid; default human-readable messages now use English.
Refresh the tool list in your MCP client after upgrading.

| Tool | Behavior |
| --- | --- |
| `ping()` | Server, OS, network and path-separator diagnostics |
| `list_allowed_roots()` | Compatibility endpoint: reports no server root allowlist |
| `list_files(directory=".", base_dir="", pattern="*", limit=200, offset=0)` | Filter and paginate names with metadata; returns total and next_offset |
| `read_file(filepath, base_dir="", offset=0, max_bytes=0, encoding="auto")` | Read a bounded byte range; UTF-8/GB18030; returns next_offset at a complete character boundary |
| `get_file_info(filepath, base_dir="")` | File/directory size, paths and timestamps |
| `create_directory(directory, base_dir="", parents=true)` | Create a directory and optionally its parents |
| `create_file(filepath, content, base_dir="", overwrite=false, create_parent_dirs=true)` | Write UTF-8 text |
| `rename_file(old_path, new_name, base_dir="")` | Rename a file within its current directory |
| `view_rename_history(filter_dir="")` | View recorded renames, optionally by directory |
| `restore_last_rename(filter_dir="")` | Restore only the last matching rename |
| `batch_rename_files(renames, base_dir="", dry_run=true, expected_plan_id="")` | Preview up to 100 renames, then apply the reviewed plan |
| `delete_file(filepath, base_dir="")` | Recoverable regular-file deletion; returns deletion_id |
| `restore_deleted_file(deletion_id)` | Verify a backup and restore without overwriting |
| `list_deleted_files(filter_dir="", limit=100, offset=0)` | Find deletion IDs, status, and malformed-record diagnostics |
| `cleanup_backups(older_than_days=30, dry_run=true, expected_plan_id="")` | Preview and explicitly purge old completed deletion backups and snapshots |
| `create_directory_snapshot(directory, base_dir="")` | Save recursive regular files and empty-directory structure |
| `list_directory_snapshots()` | Find snapshot IDs and source directories |
| `restore_directory_snapshot(snapshot_id, dry_run=true, expected_plan_id="")` | Preview, restore, and verify names, directory structure, and SHA-256 hashes |

### English and Chinese examples

Create a file with default English messages:

```json
{"filepath": "notes/meeting.txt", "content": "Meeting notes"}
```

Create a file with Chinese service messages:

```json
{"filepath": "notes/meeting.txt", "content": "Meeting notes", "language": "zh"}
```

Read that same path with English messages:

```json
{"filepath": "notes/meeting.txt", "language": "en"}
```

Rename it using `rename_file`:

```json
{"old_path": "notes/meeting.txt", "new_name": "meeting-notes.txt", "language": "zh"}
```

The language option only affects service-authored messages. Filenames, paths,
text content, timestamps, JSON keys and error codes are not translated.
OS or third-party exception text retains its original language.

### File behavior

- Relative paths resolve against `base_dir`, or the server working directory.
- The server accesses its own machine's filesystem. A Windows client path such
  as `E:\test` cannot access a Windows drive through a server running on Linux.
  Run the service on that Windows machine, or mount the directory on the server.
- `read_file` reads at most `FILE_MCP_MAX_READ_BYTES` bytes (default 200,000).
  A truncated response has `truncated=true`; incomplete trailing multibyte
  characters are omitted rather than misinterpreted as another encoding.
  UTF-8 and GB18030 decoding are supported; encoding detection is heuristic.
- Writes use UTF-8. Existing files require `overwrite=true` to replace them.
- Writes encode and stage bytes before publication. Failed encoding/staging leaves
  the original intact. Supplied LF and CRLF are preserved exactly.
- Existing directories return success with `created=false`.
- Rename targets are filenames, not paths. Existing targets are never replaced.
  Windows reserved names, invalid characters, trailing spaces and periods are
  rejected for cross-platform compatibility.
- Renames are recorded in `secure_rename_history.json` using an atomic history
  write. Restoration affects only the last matching entry, not a batch.
- A thread lock and OS file lock serialize tools sharing the same state directory.
  Corrupt history is reported and preserved. History-write failure triggers rename
  rollback; failed rollback returns explicit partial-operation details.
- Undo verifies a recorded file fingerprint. Changed/replaced files are rejected.
  Legacy history without fingerprints remains readable but cannot be automatically
  undone. Legacy deletion backups without checksums require manual recovery.
- Use `read_file`'s returned `encoding` and `next_offset` for the next chunk.
  Offsets count bytes, not characters; arbitrary offsets may split a character.
  `max_bytes=0` uses the configured maximum. A limit too small for one character
  returns `read_limit_too_small`.
- Windows `ctime` usually represents creation; Unix `ctime` represents metadata
  changes. The response uses `metadata_changed_or_created_at` for this reason.

## Response contract

Success responses contain `ok=true` plus operation-specific fields. Failures
contain `ok=false`, a stable `error` code and a localized `message`, for example:

```json
{"ok": false, "error": "not_found", "message": "File not found: notes/missing.txt"}
```

Codes such as `not_found`, `target_exists`, `invalid_new_name`, `invalid_path`
and `empty_history` remain unchanged when selecting Chinese.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `FILE_MCP_HOST` | `0.0.0.0` | Bind address |
| `FILE_MCP_PORT` | `16682` | HTTP port |
| `FILE_MCP_MAX_READ_BYTES` | `200000` | Maximum text-read bytes |
| `FILE_MCP_STATE_DIR` | Server script directory | Shared history, lock, deletion backups, and snapshots |
| `FILE_MCP_MAX_BACKUP_BYTES` | `1073741824` | Shared backup capacity limit; new backups fail before source deletion if the budget is insufficient |
| `FILE_MCP_MAX_SNAPSHOT_ENTRIES` | `10000` | Maximum recursive file/directory entries per snapshot operation |
| `FILE_MCP_ENABLE_DNS_REBINDING_PROTECTION` | `false` | Enable Host/Origin validation |
| `FILE_MCP_ALLOWED_HOSTS` | `127.0.0.1:<port>,localhost:<port>` | Comma-separated hosts when validation is enabled |
| `FILE_MCP_ALLOWED_ORIGINS` | empty | Comma-separated origins |
| `FILE_MCP_UVICORN_TIMEOUT_KEEP_ALIVE` | `1` | HTTP keep-alive timeout, seconds |
| `FILE_MCP_UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN` | `2` | Graceful shutdown timeout, seconds |

For local-only use, set `FILE_MCP_HOST=127.0.0.1`. To enable Host checks, set
`FILE_MCP_ENABLE_DNS_REBINDING_PROTECTION=true` and include the actual server
hostname/port in `FILE_MCP_ALLOWED_HOSTS`. Update the client URL if the port changes.
A `421 Misdirected Request` can indicate a missing allowed Host value.
The short shutdown timeouts limit waiting for open HTTP connections; if needed,
press Ctrl+C again to force exit.

## MCP client example

```json
{
  "mcpServers": {
    "w-FileWorkbenchMCP": {
      "url": "http://<server-ip>:16682/mcp",
      "type": "streamableHttp"
    }
  }
}
```

Client configuration syntax varies. Verify a create operation using the returned
`ok`/`path`, then call `read_file` on that path rather than relying on the model's
natural-language claim that the operation succeeded.

## Deployment boundaries

The existing teaching defaults bind to all interfaces, disable Host/Origin
validation and provide no authentication or root-directory allowlist. Access
is determined by the service account's OS permissions. A reachable client can
read accessible text and create, overwrite or rename accessible files.

Use a low-privilege account and restrict network access through a firewall/VPN
or an authenticated gateway. The history file contains absolute paths; do not
publish it. Host validation alone is not authentication or filesystem isolation.

No standalone recursive directory deletion, full-text search, arbitrary binary
writes, user roles or built-in approvals are provided. Put human approval
in the MCP client or Agent middleware when required.

## Recoverable file deletion

`delete_file(filepath, base_dir="", language="en")` backs up a regular file before
deleting it and returns a `deletion_id`. Directories and symlinks are rejected;
wildcards and recursive deletion are not supported.
`restore_deleted_file(deletion_id, language="en")` restores the original path
without overwriting an existing target. Its parent directory must still exist.

Backups live under `FILE_MCP_STATE_DIR/.deleted_files/<deletion_id>/`, persist after
restoration, and are not the OS recycle bin. Deletion first claims the source entry
using a temporary name in its original directory, copies and verifies the backup,
then removes that entry. Detected changes cancel deletion and trigger rollback.
Rollback conflicts return the retained quarantine path for manual recovery.
Restoration stages and verifies bytes before publishing without overwriting.
Failed/pending deletion records are never automatically purged.

Do not publish backups. All processes sharing a state directory cooperate through
the OS lock. External writers do not participate in that lock: detected changes
stop the operation, but applications retaining open file handles still require
external coordination. Crashes can leave staging/quarantine files or pending records.
This is not a crash-transactional filesystem or a full metadata backup system.

### Preview and apply

Batch renaming, backup cleanup, and snapshot restoration default to `dry_run=true`.
Inspect the returned plan, then repeat with `dry_run=false` and its
`expected_plan_id`. A changed plan is rejected. Batch failures report completed
items and stop; earlier successful renames remain applied and have undo records.
Name swaps and chains are rejected rather than partially interpreted.

Snapshot restoration backs up changed/added live files before removal and stages
all needed snapshot bytes before changing the directory. It also restores empty
directories and removes extra empty directories. It reports partial progress and
deletion IDs on failure; it is not a directory-wide transaction. Snapshots reject
symlinks/junctions and roots overlapping backup storage. The original root must
exist. Cleanup permanently removes selected backups, not live source files.

`create_file` preserves supplied LF/CRLF exactly and uses exclusive creation when
`overwrite=false`. Restart the server and refresh client tools to load changes.
Run `python -B test_file_lifecycle.py` for temporary-directory regression checks.
Run `python -B test_file_http.py` for a real isolated HTTP MCP server/client test.
See [validation details](TESTING.md) for the coverage and platform limits.
See the [conversation showcase and improvement backlog](SHOWCASE.md)
for the original experiment, its limits, and the revised MCP-only workflow.

## Verification

From the parent `mcp` directory, run the offline regression checks:

```bash
python -B test_bilingual_tools.py
```

These use temporary directories, with English/Chinese names, content, messages,
UTF-8/GB18030 reads, truncation, renaming/restoration and MCP schema checks.
