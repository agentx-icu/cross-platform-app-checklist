---
name: cross-platform-app-checklist
description: Compatibility checklist for apps that ship on several of iOS, iPadOS, Android, macOS, Windows and Linux. Use when designing, implementing or reviewing any UI, layout, lifecycle, permission, media, notification, packaging or platform-integration change in a multi-platform app (Flutter, React Native, Kotlin/Compose Multiplatform, .NET MAUI, Electron, native) — screen sizes and breakpoints, high-DPI and fractional scaling, rotation, split screen and foldables, safe areas and keyboards, large text, permission declarations, background limits, mobile device features, and desktop-vs-mobile differences.
---

# Cross-platform app checklist

Apps that run on phones, tablets and desktops break in the same places again
and again: a layout that only works at the size the developer tested, a
permission declared on one platform and forgotten on another, a lifecycle
event that means "the user left" on one OS and "a window lost focus" on
another. This skill is the list of those places, distilled from real defects
found while shipping multi-platform apps, with a rule, the failure it
prevents, and how to verify each one.

It is a **standing constraint, not a one-off audit**: apply it whenever work
touches UI, lifecycle, permissions, media, notifications, packaging or any
platform API.

## How to use it

1. **Scope.** List the platforms the app ships on and the form factors the
   change can reach (phone, tablet, foldable, desktop window). A change in
   shared code reaches all of them, even when it was written for one.
2. **Walk the checklist below.** For every item, answer one of:
   - **verified** — say how (test name, device / simulator / emulator and OS
     version, screenshot, measured value);
   - **to do** — what is missing and where;
   - **needs device** — the untested behaviour and a hardware test plan;
   - **not applicable** — with a reason ("no camera use", "desktop-only
     screen"). A bare "N/A" is not an answer.
3. **Open the reference** for an area when an item applies, before writing
   the code. The references hold the platform specifics, the known traps and
   the verification recipe.
4. **Report** the answers as a table (`ID | status | evidence`) in the design
   note, PR description or review reply. Record the build, OS version,
   window size, scale and relevant settings. Source declarations alone do
   not verify packaged declarations or runtime behaviour; a local test does
   not establish store approval. See the evidence template in the testing
   reference.
5. **Fix at the cause in shared code** where possible, then check the fix on
   every platform the shared code reaches. When a bug is fixed on one
   platform, state whether it exists on the others and fix it there too or
   say why it does not apply (parity rule, `X5`).
6. **Check version gates.** Separate the installed OS from build SDK,
   Android target SDK, deployment minimum and distribution channel. For a
   version threshold or store requirement, check current official guidance
   and record the source and date; a preview test is labelled as such.

Priorities used in the references: **P0** — a core function or a store /
platform rule breaks without it; **P1** — a common scenario is noticeably
degraded; **P2** — enhancement or niche.

## The checklist

### Layout and screens — [references/layout.md](references/layout.md)

- **L1 Size range.** Usable at the smallest supported phone / window size
  through a maximised desktop window, including phone landscape, tablet
  panes, resizable iPad windows and foldables. Include narrow stress cases
  such as 320 pt / dp; that is a test width, not a universal OS minimum.
- **L2 Breakpoints by available width.** Layout decisions read the window's
  available size, never the OS or a "device type" guess; every component
  that has its own idea of "mobile vs desktop" agrees with the shell.
- **L3 Breakpoint crossing at runtime.** Rotation, split-screen resize, fold
  / unfold and desktop window resize keep the open screen, drafts, selection,
  scroll position, focus and running media.
- **L4 Safe areas and system bars.** Nothing important under the notch /
  Dynamic Island / cutout, rounded corners, home indicator, Android
  edge-to-edge status, navigation and caption bars (including side insets
  where present), or macOS full-size-content title bar controls.
- **L5 Soft keyboard.** Inputs and their actions stay visible with the
  keyboard open, in landscape, with supported iPad floating / split
  keyboards; keyboard avoidance is applied exactly once and handles
  keyboards that do not occupy the bottom edge.
- **L6 Orientation.** Declarations match the intended orientations; layouts
  also handle OS-imposed rotation and resizing. Check runtime and target-SDK
  rules for iPad and Android large screens in the layout reference.
- **L7 Overlays.** Dialogs, sheets, menus, snackbars and FABs obey the same
  rules as screens: they scroll, respect safe areas, have a max width on wide
  windows and do not cover content at the end of a list.
- **L8 Fold hinges and posture.** Account for separating folds and occluding
  hinges in window coordinates; posture changes preserve the active flow
  even without a width breakpoint.

### Text, density and assets — [references/display.md](references/display.md)

- **D1 Large text.** No overflow, clipping, silent fade or ellipsised
  essential text through the supported OS's largest text settings, including
  Android 14+ non-linear scaling up to 200 % and iOS accessibility Dynamic
  Type categories. Labels wrap, rows become columns and containers grow;
  one multiplier cannot represent every text style's scaling curve.
- **D2 Localised and long text.** Longest shipped language, CJK, RTL; no
  string concatenation that breaks word order; missing translations are
  detected, with any intentional fallback recorded.
- **D3 Pixel density.** Raster assets at every density the platform asks
  for (or vectors); layout uses logical units, with deliberate pixel
  alignment for fine strokes; hairlines and icons stay sharp at supported
  fractional scales such as 125 % / 150 % / 175 %.
- **D4 Scale changes at runtime.** Moving a window between monitors with
  different scale factors, or changing display scaling while running,
  re-lays out and re-rasterises without blur or stale sizes.
- **D5 Platform icons.** App, tray / menu-bar, notification and window icons
  follow the platform's format rules; launch screens follow their separate
  platform requirements.
- **D6 Theme and contrast.** Light / dark follows the system or an explicit
  saved preference, including startup; secondary text meets contrast in
  both; state is never shown by colour alone.
- **D7 Reduced motion.** Follow animation preferences for custom and native
  content; navigation, progress, cancellation and focus still work with
  animations disabled.

### Input and interaction — [references/input.md](references/input.md)

- **I1 Touch targets.** Use the recommended touch hit areas of at least
  44 × 44 pt (iOS / iPadOS) / 48 × 48 dp (Android), measured rather than
  inferred from padding; check the input reference for context.
- **I2 Pointer and keyboard.** Hover states, right-click / secondary-click
  menus, scroll wheel and trackpad, drag-and-drop, focus traversal, visible
  focus and platform shortcut conventions (including Cmd vs Ctrl) — on
  desktop and on tablets with a keyboard / trackpad.
- **I3 Text input.** Enter-to-send never fires during IME composition;
  hardware-keyboard handling does not race the characters typed before it;
  long-press menus do not fight the system text-selection menu.
- **I4 Back navigation.** Android back / predictive back and supported iOS
  back gestures follow the route stack; desktop Esc follows the platform's
  dismissal conventions. No action pops past the root unexpectedly.
- **I5 Screen readers.** Every control has an accessible name and role;
  VoiceOver / TalkBack / Narrator / Orca can complete the main flows.
- **I6 System formats.** 12 / 24-hour time, locale date and number formats,
  first day of week come from the system setting.
- **I7 Gesture alternatives and cancellation.** Essential actions do not
  depend only on complex gestures, pressure, hover or one pointing device;
  cancelled input leaves no accidental activation or stuck state.

### Lifecycle and background — [references/lifecycle.md](references/lifecycle.md)

- **B1 Lifecycle states mean different things per platform.** Focus loss,
  visibility, scene activation and background execution are distinct.
  Choose camera, audio, rendering and privacy behaviour per resource and
  platform; do not treat every blur as backgrounding or defer all privacy
  protection until hidden.
- **B2 Persist before suspension.** Checkpoint user data during use and on
  supported lifecycle transitions; recover committed data after background
  process death without relying on a final callback.
- **B3 Process death and cold start.** After the OS reclaims the process the
  app restores the supported state and recovers or safely retries a pending
  system picker / camera operation; a notification tap on cold start is not
  dropped or doubled.
- **B4 Background limits.** Work that must run in background respects iOS
  suspension and background-task budgets, Android foreground-service types
  and time limits, Doze and OEM battery killers; desktop sleep / resume is
  handled.
- **B5 Single instance and multiple windows.** A second launch, an Android
  multi-instance window or an iPad second scene does not contend for the
  same data; the design either supports several windows or prevents them.
- **B6 Durable transfers and retry ownership.** Persist operation ownership
  and reconcile background jobs after restart; retries, cancellation and
  account changes cannot duplicate or misattribute results.

### Permissions, privacy and data — [references/permissions.md](references/permissions.md)

- **P1 Declarations match use on every platform.** Inspect the declarations
  required by the actual API and distribution model: Android manifest,
  Apple usage strings / entitlements, Windows package capabilities, or Linux
  sandbox permissions / portals. Use localised purpose strings where
  required; remove unused access. Not every capability needs every kind of
  declaration, and unpackaged apps may have no package manifest.
- **P2 Runtime flow.** Ask in context, in the foreground, following the
  platform's request sequence without repeated-prompt loops; explain denial,
  restriction and revocation mid-use, and offer settings recovery where the
  user can change access; the first denial is never silent.
- **P3 Degraded paths.** The feature still works or explains itself when a
  permission is denied (notifications off, limited photo access, approximate
  location).
- **P4 Store privacy requirements.** Applicable Apple privacy manifests,
  required-reason API declarations and privacy labels, Play Data safety,
  sensitive-permission / foreground-service declarations, and submission
  SDK / target-API requirements match the shipped app and bundled SDKs.
- **P5 Data at rest and backup.** Use the OS credential store for secrets;
  on Android protect encrypted secrets with Keystore-backed keys. Decide
  backup inclusion. Handle both retained and missing credentials after
  reinstall; iOS Keychain retention after uninstall is an
  [implementation detail](https://developer.apple.com/forums/thread/36442).
- **P6 Selected files and persistent access.** A picker result is scoped
  access, not a permanent path; copy into app storage or retain the
  supported grant / bookmark before deferred work.
- **P7 Sensitive content and screen capture.** Decide what may appear in
  app-switcher snapshots, screenshots, recordings and mirroring; apply the
  per-platform protection before sensitive content is shown.

### Media, audio and devices — [references/media-devices.md](references/media-devices.md)

- **M1 Audio session and focus.** Playback and recording choose the right
  iOS audio session category and Android audio focus; silent switch,
  interruptions (calls, alarms, other apps) and resumption behave as users
  expect; components sharing one session do not undo each other.
- **M2 Audio routes.** Speaker / earpiece / wired / Bluetooth routes, and
  devices connecting or disconnecting mid-use.
- **M3 Camera.** Front / back switch, mirroring, rotation, release after use
  (verify this app stops capture in OS privacy UI), a clear state when the OS
  takes the camera away (multitasking, background, another app).
- **M4 Formats crossing platforms.** Media and files produced on one
  platform open on the others (HEIC / HEVC to Windows / Linux, path
  separators and case in archives, line endings).
- **M5 Memory.** Decode previews near their rendered physical size
  (logical size × device pixel ratio); reserve full-resolution decoding for
  features that need it; stream large files and handle low storage.
- **M6 Notifications.** Channels, badges, grouping, lock-screen content
  privacy, tap routing, and platform behaviour when notifications are off.
- **M7 Optional hardware and device capabilities.** Detect hardware and
  service availability separately from permissions; absent or disconnected
  devices have a usable fallback and intentional store filtering.
- **M8 Screen and system-audio capture.** Treat screen, microphone, system
  audio and remote input as separate capabilities; verify consent, capture
  dimensions, interruption and cleanup for each supported backend.

### Desktop specifics — [references/desktop.md](references/desktop.md)

- **W1 Window management.** Sensible default and minimum size clamped to the
  work area; size / position restored only onto a display that still
  exists; full screen, maximise, snap layouts; Wayland restrictions.
- **W2 Close vs quit vs tray.** Platform-correct semantics for closing the
  last window, quitting (Cmd+Q, taskbar, logout / shutdown), and
  minimising to tray; tray / menu-bar support gaps per desktop environment
  never crash startup.
- **W3 File system.** Per-OS app data, cache and documents directories;
  separators, case-insensitive and case-preserving file systems, long paths,
  non-ASCII user names; never write next to the executable.
- **W4 Packaging and distribution.** Apply the signing, notarization,
  installer and update requirements of each distribution channel; register
  file associations and URL schemes per platform.

### Process and parity — [references/testing.md](references/testing.md)

- **X1 Device matrix.** The change was exercised on the profiles in the
  testing reference that it can reach, not only on the developer's machine.
- **X2 Automated layout sweep.** Screens and overlays are rendered across
  sizes × text scales × locales × safe-area profiles with detectors for
  overflow, clipping, ellipsis and lost state.
- **X3 Rotation / resize test.** At least one real-app test rotates or
  resizes across a breakpoint and asserts state survives.
- **X4 Real-device-only behaviour is labelled.** Items that need hardware
  (headsets, available silent controls, cellular handover, real camera) are
  marked "needs device" with a plan, never reported as verified from a
  simulator.
- **X5 Parity.** A bug fixed on one platform is checked on the others; the
  answer is recorded either way.
- **X6 Packaged release verification.** Inspect and exercise the actual
  release artifacts, declarations, architectures and install / upgrade
  paths; debug-build success does not establish release compatibility.
- **X7 Interrupted flows and access changes.** Test recreation, background
  process death, permission revocation and interrupted system UI separately,
  with explicit state and result-delivery assertions.
- **X8 Network environments.** Exercise offline recovery, address-family
  coverage and relevant network changes using a documented network setup;
  a connection indicator is insufficient evidence of service reachability.

## Framework notes and sources

- Flutter specifics (APIs, plugins and their traps): [references/flutter.md](references/flutter.md).
- Official guidelines this checklist aligns with, dated version / store
  gates and related projects: [references/sources.md](references/sources.md).
  Re-check a dated gate against its source before relying on it.
- For other frameworks the platform facts in the references still apply;
  map the Flutter notes to the framework's equivalents.

## Red flags — stop and re-check

- "It works on my Mac / my phone."
- A breakpoint computed from `Platform.isIOS` / `isAndroid` / user agent.
- A fixed `height:` on anything that contains text.
- `Row` + `Text` with no wrapping or flex.
- A permission added to one platform's manifest only.
- One blanket stop / continue policy for camera, audio and sync on
  "inactive" / "blur".
- Waiting for a termination callback to save user data.
- Treating source declarations, screenshot goldens or activity recreation
  as proof of packaged permissions, native UI or process-death recovery.
- A new `UIBackgroundModes` / foreground-service type "just in case".
- "Verified" on a simulator for something the simulator cannot do.
