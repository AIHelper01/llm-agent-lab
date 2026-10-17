# w-File Workbench MCP validation

English | [Simplified Chinese](TESTING.zh-CN.md)

Validation date: October 17, 2026. Execution platform: Windows, Python 3.12.
All fixtures and server state are isolated in temporary directories. The real
`D:\files` directory and the existing running server are not modified.

## Commands

From this directory, with `mcp>=1.12,<2` and `python-dotenv` installed:

```bash
python -B test_file_lifecycle.py
python -B test_file_http.py
```

From the parent `mcp` directory, with `requests` also installed:

```bash
python -B test_bilingual_tools.py
```

The first suite contains 20 tests, the HTTP suite contains one end-to-end test
with English and Chinese scenarios, and the existing suite contains seven tests after removing the retired helper test.
Result: all 28 tests passed. Ruff checks and the English showcase ASCII-only
check also passed.

## Coverage

| Area | Checks |
| --- | --- |
| Languages | Default English and explicit Chinese messages; both Latin and Chinese paths and contents; stable JSON fields/error codes |
| Encoding | UTF-8/GB18030, exact LF/CRLF, bounded reads, multibyte boundaries, and byte-range continuation |
| Writes | Existing targets are preserved; invalid Unicode and failed publication cannot truncate the original |
| Deletion | Binary fidelity, directory rejection, backup failure, concurrent external update detection, capacity limits, source rollback |
| Recovery | No overwrite, checksum verification, interrupted copy leaves no partial destination, retry succeeds |
| History | Corrupt history is preserved; rename/undo roll back after history-write failure; replaced files cannot be undone |
| Workflow compatibility | Rename, delete, restore deletion, then undo the rename |
| Concurrency | Twelve threaded renames and four separate worker processes retain all history records |
| Batch renaming | Preview-only default, plan requirement, collision checks, partial failure reporting |
| Snapshots | Full conversation replay, final byte comparison, empty directories, file/directory type changes, stale plans, corrupt backup rejection |
| Retention | Record lookup, preview-only cleanup, plan requirement, explicit cleanup, failed deletion records are retained |
| Error contract | Permission failures return localized structured responses |
| MCP | Schema checks and dispatch; a real subprocess server and Streamable HTTP client perform both language workflows |

The HTTP test uses an ephemeral loopback port, a separate `FILE_MCP_STATE_DIR`,
and a hidden subprocess on Windows. It terminates that subprocess after testing.

## Limits

These tests establish the listed behavior on Windows. The POSIX lock and
link-based rename branches are implemented but have not been executed on Linux
or macOS in this session. Filesystems without hard-link support return errors
instead of using an overwrite-prone fallback.

The server lock coordinates participating processes with the same state
directory. It does not synchronize arbitrary external writers or protect against
all open-handle races. Process termination/power loss can leave pending records
or staging/quarantine files. Multi-file operations report partial progress rather
than promising a directory-wide transaction. Snapshots preserve file bytes and
directory structure, with supported stat metadata copied where possible; they
are not full ACL/ownership/alternate-stream backups.
