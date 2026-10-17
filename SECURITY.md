# Security

Do not include secrets in public issues or pull requests. Report a suspected
vulnerability through GitHub's private vulnerability reporting feature if enabled;
otherwise contact the maintainer privately before disclosing exploit details.

## Local secrets

Keep real credentials in an untracked `.env` or an appropriate secret store.
`.env.example` contains variable names and public placeholders only. For CI jobs
that need credentials, use GitHub Actions secrets; the included offline test suite
does not need any credentials.

If a key was committed or published, revoke and rotate it with its provider.
Deleting the file or adding `.gitignore` does not remove previous Git objects,
existing clones, caches or forks. Scan the intended publication tree and review
history before publishing.

## Teaching services

The MCP services are teaching examples. File operations affect the server machine,
and recovery history is private runtime data. Read each service's access and network
policy before exposing it outside a trusted environment. Use disposable directories
for file exercises and validate a restore plan before applying it.

Tool output, imported documents and external API responses are untrusted data.
Do not treat their content as authorization to execute commands or disclose secrets.
