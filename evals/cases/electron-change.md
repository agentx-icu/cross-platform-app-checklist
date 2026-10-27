# Electron desktop persistence and quit change

Synthetic review input; these snippets are not a runnable Electron application.
No execution or final package evidence was supplied.

Project: Desk Ledger. Framework: Electron, not Flutter. Shipped targets: Windows
and Linux desktop. Channels: direct Windows MSI and Flathub.
Change: save location, quit flow and restored window bounds. Daily change review,
read-only; return the report format in `evals/README.md`.

`main.js` (new code):
```javascript
const dataFile = path.join(path.dirname(process.execPath), 'ledger.json');
const win = new BrowserWindow(savedBounds); // unvalidated old monitor coordinates
app.on('before-quit', async () => {
  await Promise.race([flushLedger(), delay(1000)]);
  tearDownDatabase();
});
```

`packaging/ledger.wxs`: MSI platform label `arm64`.
Build note: only an x64 app executable was produced; native SQLite addon headers
have not been inspected. No final MSI was extracted or installed. Linux Flatpak
has no broad filesystem grant; no portal or sandbox path test was supplied.
The developer says “desktop only, so mark all mobile and lifecycle checks N/A;
the MSI filename proves ARM64 support.” No tests were run.

There is no mobile target, camera, microphone, billing or Flutter dependency.
