# Process and parity (X1–X8)

Use this reference to choose test profiles and evidence. Platform behaviour
belongs in [layout](layout.md), [display](display.md), [input](input.md),
[lifecycle](lifecycle.md), [permissions](permissions.md),
[media and devices](media-devices.md), and [desktop](desktop.md).
Version-sensitive claims below were checked against the linked official
sources on 2026-10-22; recheck them when SDKs or release requirements change.

## X1 Device matrix — P0

**Rule.** Exercise a change on every relevant shipped platform and profile.
Record device / emulator, OS build, app build / revision, build SDK and
Android `minSdk` / `targetSdk`, window size in logical units, pixel ratio,
display / text settings, and distribution channel. The installed Android
API level is independent of `targetSdk`; cover the oldest supported OS,
current stable OS, and boundaries of affected APIs. Label preview runs
separately. Android distinguishes [changes for all apps from target-gated
changes](https://developer.android.com/guide/app-compatibility/test-debug).

Minimum applicable profiles; one device can cover several rows:

| Profile | Failure it catches |
|---|---|
| Smallest supported phone in portrait; additional narrow stress widths such as 320 / 375 pt or dp | Unreachable actions; these sample widths are not OS minimums |
| Cutout / notched phone, both landscape directions and portrait; a non-cutout profile | Asymmetric insets and assumptions that every phone has a bottom safe-area inset |
| Android phone, gesture navigation and 3-button navigation, with / without a cutout | System bars or back handling covering / bypassing controls; inspect actual side and bottom insets |
| Phone with soft keyboard open in portrait and landscape | Short usable height, hidden validation and submit buttons |
| iPad full screen and resizable windows on supported OS modes; legacy Split View / Stage Manager where available | A fixed set of pane ratios misses freely resized windows and breakpoint transitions |
| Android tablet and foldable: folded, unfolded, available tabletop / book postures, multi-window / desktop windowing where supported | Stale sizes, hinge occlusion, assumed portrait locks and activity recreation |
| Each desktop OS at its minimum supported window, maximised and full screen; 100 %, fractional and high scale where offered | Layout / physical-pixel confusion, clipped native chrome and oversized minimums |
| macOS window on Retina and non-Retina displays where supported; Windows at e.g. 125 % / 150 % / 175 % and 200 %; mixed-scale monitor transitions | Blurry assets, misplaced popup anchors and pointer coordinates after scale changes |
| Linux sessions and packaging actually supported: Wayland / X11 or XWayland as applicable, relevant compositor and scale | One display backend passing does not verify another or its portal integration |
| Tablet / touch-capable desktop with keyboard and pointer; keyboard-only desktop | Touch-only navigation, hover-only actions, wrong shortcuts and lost focus |
| A lower-memory physical device within the support policy; constrained storage | Memory pressure, interrupted persistence and storage errors; RAM alone does not prove process-death handling |
| Optional camera, microphone, location or biometric hardware absent / disabled; external devices disconnected | Permission granted being mistaken for hardware availability |

Apply largest text settings, increased display size / zoom where supported,
RTL and the longest shipped strings, light / dark, screen reader and
reduced motion. Combine high-risk settings, such as large text + narrow
landscape + keyboard, rather than changing each setting only in isolation.
See [display](display.md) and [input](input.md) for the acceptance rules.

**Version traps.**

- On Android 16, apps targeting API 36 have orientation, aspect-ratio and
  resizability restrictions ignored by default on displays with smallest
  width ≥ 600 dp, subject to documented exceptions and a temporary opt-out.
  API 37 targeting removes that developer opt-out on Android 17 large
  screens, subject to documented game and user-setting exceptions. Test
  below, at and above 600 dp as well as app breakpoints; Android's current
  documentation is inconsistent about inclusivity at exactly 600 dp for
  API 37. Do not assume an activity's current pane width determines whether
  the rule applies. Official sources:
  [Android 16](https://developer.android.com/about/versions/16/behavior-changes-16)
  and [Android 17](https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored).
- iPadOS 26 introduced expanded windowing and deprecated
  `UIRequiresFullScreen`. With the iOS / iPadOS 27 SDK, that key no longer
  opts an app out of resizing on iOS / iPadOS 27; it can instead select
  discrete scene resizing. Test the shipped SDK / OS combination rather
  than treating the key as a permanent full-screen guarantee. See
  [Apple TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key).
- A synthetic 320-wide viewport does not establish support for an old
  phone's OS, and a logical 800-wide window at 200 % is not a 1600-wide
  layout. Record logical and captured pixel dimensions separately.

**Verify.** Publish the selected matrix with results and explicit gaps.
If a profile is unavailable, record `to do` or `needs device` with an owner
and test plan; another OS's screenshot cannot close that gap.

## X2 Automated layout sweep — P0 for UI-heavy apps

**Rule.** Render every affected screen **and overlay** (dialogs, sheets,
menus, dropdowns, snackbars, loading / error / empty states, validation and
results) across:

- logical window sizes from X1, including minimum height and widths just
  below / at / above each app breakpoint;
- default, intermediate and maximum platform text settings. Numeric
  multipliers such as 1.0 / 1.3 / 2.0 are supplemental stress cases, not a
  substitute for Android 14+ [non-linear scaling up to
  200 %](https://developer.android.com/about/versions/14/features#non-linear-font-scaling)
  or iOS [Dynamic Type accessibility
  categories](https://developer.apple.com/documentation/swiftui/dynamictypesize);
- every shipped locale, including plural / formatted values, long user
  content, RTL and mixed-direction text;
- safe-area profiles: notch portrait / landscape, gesture / button
  navigation, tablet taskbar / caption bar, keyboard open / closed, and
  desktop native chrome. Zero mobile safe-area insets do not mean a custom
  title bar has no occlusion;
- supported pixel ratios, including fractional ones, independently of
  logical window size; both themes and relevant accessibility settings;
- live size and setting changes without rebuilding the app from scratch.

**Trap.** A golden image can faithfully capture a broken layout. A 2×
linear text multiplier does not reproduce a non-linear scaler, and mocked
insets do not verify the OS's actual delivery of them.

Detectors that fail the test:

- framework overflow errors;
- essential text ellipsised, line-limited, silently clipped or faded; allow
  intentional truncation only with a documented way to obtain the content;
- laid-out text / line bounds outside their available box, labels outside
  buttons, or app-bar titles outside the toolbar;
- controls obscured by system UI, a keyboard, or an overlay at the end of a
  scroll; scroll to and activate the last action;
- text reduced below the project's documented minimum in logical units,
  or scaling disabled to hide overflow; there is no universal 12 physical
  pixel accessibility floor;
- focus order / hit bounds that no longer match the visible controls;
- lost state, duplicate requests or recreated sessions after relayout.

**Verify.**

- Load the app's actual fonts and required script / emoji fallbacks before
  capture; check for missing glyphs. Placeholder test fonts hide shaping
  and wrapping defects. In Flutter, explicitly load fonts for goldens;
  the rendering notes describe the default test font's [replacement by
  FlutterTest](https://docs.flutter.dev/release/breaking-changes/rendering-changes).
  Do not assume a test runner has the production font fallback chain.
- Pin framework / renderer and fonts, and record the host OS for goldens;
  keep baselines per renderer where necessary. Review visual diffs and do
  not let CI update its expected images automatically. See Flutter's
  [golden matcher](https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html).
- Run intentionally broken fixtures to prove each detector fires. Include
  a silent clip, missing font and obscured final button, not just an obvious
  framework overflow.
- Use semantics and interaction assertions alongside screenshots; exercise
  native pickers / platform views and actual screen readers on the app.
  Widget-only rendering cannot establish those integrations.
- Keep a representative sweep in PR CI and the larger matrix on a scheduled
  run; record any combinations omitted. See [framework notes](flutter.md)
  for framework-specific test APIs.

## X3 Rotation / resize test — P1

**Rule.** At least one integration test runs the app on every affected
mobile platform and changes orientation through the OS, where supported;
also resize tablet and desktop windows across a breakpoint in both
directions. Changing a mock viewport alone does not cover native lifecycle
or window events. If the OS refuses rotation, verify that result and test
the available resize path instead.

**Trap.** A screenshot before and after a full relaunch misses state loss,
duplicated network work and stale popup anchors during a live transition.

**Verify.** Start with a selected tab / item, draft with selection, scroll
position, keyboard and an open dialog or media session. Rotate both ways,
resize rapidly through the breakpoint and return. Assert the logical edit
state and selected content survive; editing can resume if the OS dismisses
the keyboard. Check overlay placement, scroll reachability, session
continuity and that callbacks / submissions occur once. Repeat relevant
transitions while a permission prompt or picker is open (X7).

Move desktop windows and open popups between different-scale monitors;
change scale while running, then disconnect / reconnect a display. Check
sharpness, hit testing and dialog coordinates, not just outer window size.
Exercise supported docking / remote-session paths. Microsoft lists these
as distinct [DPI-change
scenarios](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows).
See D4 in [display](display.md) and [window management](desktop.md) for
expected behaviour.

## X4 Label what needs a real device — P0

**Rule.** Separate a simulated code path from hardware, OS integration and
distribution-channel evidence. Record what the test environment actually
supports instead of treating every simulator or emulator as identical.

Hardware checks include:

- headset / Bluetooth routing, acoustic output, proximity sensing and the
  device's available silent / ringer controls;
- physical camera orientation, mirroring, autofocus, capture quality and
  supported multitasking camera features;
- actual cellular / Wi-Fi handover, carrier behaviour and external devices;
- real memory pressure, thermal throttling and vendor battery policies;
- genuine multi-monitor / docking behaviour on desktop, beyond injected
  scale factors or virtual screens in headless CI.

**Traps: simulation can cover part of the flow.**

| Test | What it establishes and what remains |
|---|---|
| iOS Simulator push injection | Payload parsing / UI routing, not server-to-APNs delivery |
| Sandbox APNs on supported Simulator / Mac configurations | Supported configurations can register and receive remote notifications; record host / runtime. Still test the chosen release channel and physical-device presentation / background behaviour |
| Emulator camera / location / sensor input | Injected-state handling, not physical sensor quality or device routing |
| Android forced Doze or simulated low memory | Specific forced behaviour, not vendor battery policy or natural timing |
| Controlled IPv6-only / DNS64-NAT64 network or captive portal | Real transport / recovery behaviour if the app actually uses that network; these are network-environment tests, not inherently hardware-only |

Apple documents [Simulator sandbox APNs support in Xcode 14 release
notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-14-release-notes);
payload injection and remote delivery are different tests. For networking,
use X8 rather than inferring coverage from the simulator's network icon.
Apple also distinguishes [simulated-device behaviour from physical-device
verification](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices).

**Verify.** Mark remaining hardware cases **needs device**, with an owner,
device, steps and expected result. A passing simulator test may close its
specific case; it cannot close the remaining device cases. "Implemented"
does not mean "verified".

## X5 Parity — P0

**Rule.** Shared-code changes can affect every caller; verify the platforms
and features they reach. For platform-specific fixes, reproduce the
equivalent scenario on other shipped platforms, then fix or record why it
does not apply. A shared patch alone does not prove identical behaviour.

**Trap.** Marking a feature "implemented" on all platforms hides a release
whose Windows permission denial and Android cold start were never tested.

**Verify.** Keep a feature × platform table with support status
(`implemented` / `partial` / `missing`) separate from verification status
(`verified` / `to do` / `needs device` / `not applicable` with reason).
Link the regression scenario, build and evidence. Split rows when one ID
has mixed results; do not convert an untested platform into `not applicable`.

## X6 Packaged release verification — P0 for release

**Rule.** Inspect and install artifacts from the actual release pipeline,
including every shipped architecture and relevant package / sandbox model.
Source declarations and a debug launch do not establish release behaviour.
Use [permissions](permissions.md) for the required declarations and
[packaging](desktop.md) for distribution rules.

**Traps and verification.**

| Artifact / environment | Check and failure prevented |
|---|---|
| Android release APKs generated from the shipped bundle | Inspect final permissions, SDK levels, components and hardware requirements; run release shrinking / obfuscation and invoke plugins / native libraries. The [manifest merger](https://developer.android.com/build/manage-manifests) includes variants and dependencies, so the main source manifest is insufficient |
| Android device availability | Check Play device filtering as well as sideload installation. Optional hardware permissions can imply required features; inspect camera and autofocus separately, then test without the hardware. See [`uses-feature`](https://developer.android.com/guide/topics/manifest/uses-feature-element) |
| Android native libraries, including framework / SDK binaries | Check packaged ELF and ZIP alignment and run on a 16 KB page-size system with compatibility fallback disabled where available; a passing 4 KB emulator is insufficient. Follow the current [16 KB testing procedure](https://developer.android.com/guide/practices/page-sizes) and record the measured page size |
| Apple exported app and embedded extensions / frameworks | Inspect built usage strings and localisations, privacy manifests, deployment minima and signed entitlements / provisioning where applicable. Install the distribution build and invoke protected features; debug signing can hide release access failures |
| Windows shipped package or unpackaged installer | Verify the actual manifest / identity and capabilities where used, then exercise system privacy settings. [Capability requirements depend on the app model](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations); an unpackaged build does not validate an MSIX build |
| Linux shipped package and supported desktop session | Install on a clean supported system; exercise file / device portals with the shipped sandbox permissions. Developer-machine libraries and permission overrides can hide failures. See [Flatpak sandbox and portal guidance](https://docs.flatpak.org/en/latest/sandbox-permissions.html) when applicable |

**Verify.** Record artifact identifiers / hashes and installation channel.
Test both clean install with fresh consent and upgrade from the previous
released version with existing data and consent. Reinstall, OS update,
backup restore and account change are separate cases when affected; do not
assume reinstall resets permissions or credentials. Exercise launch, a
protected feature, links / associations and any changed update / migration
path as a standard user without developer permission overrides.

Store validation and privacy declarations need their own evidence; an
accepted upload or local permission prompt is not approval of all policies.
See P4 in [permissions](permissions.md).

## X7 Interrupted flows and access changes — P0 for stateful / permissioned flows

**Rule.** Verify each interruption separately, using the real app and OS
where possible. Follow [lifecycle](lifecycle.md) and
[permission-flow](permissions.md) rules; assert recoverable state and
exactly-once handling of results, rather than only "no crash".

| Scenario | Verification |
|---|---|
| Activity / view recreation | Rotate or recreate while editing. Android's "Don't keep activities" destroys activities when left; it is not a process-death test. See [developer options](https://developer.android.com/studio/debug/dev-options) |
| Background process death | Save a draft, background the app, detach the debugger and terminate only its background process with a supported test method; verify it actually exited. Resume via the existing task and separately test a notification / link cold start |
| System picker / camera / permission UI open | Cancel, rotate / resize where permitted, background / lock, and return; on supported platforms also recreate or terminate the host process while external UI is active. Assert pending actions recover or offer a safe retry, with no duplicate upload / route |
| Denial and access change | On fresh consent, test grant, deny, restricted / permanently denied where applicable, limited / approximate / one-time access where offered, and revocation in Settings. Return with a draft; verify a fresh access check, state recovery if the OS restarts the process, and a usable fallback |
| Visible but unfocused / multiple windows | Focus another app or scene while a session runs; apply resource-specific policy. Close one scene without corrupting another; see B1 / B5 |
| Lock / unlock and desktop sleep / wake | Verify saved data, allowed background work, credential / file access and reconnection; unavailable resources produce a recoverable state |

**Trap.** Force-stop, task dismissal, activity destruction and OS process
reclamation have different effects. Do not label a force-stop / relaunch
as a complete low-memory restoration or background-delivery test.
Android's [`am kill`](https://developer.android.com/tools/adb#am) targets
processes safe to kill; it may not kill one retained by a foreground
service, so check process exit. Android also does [not guarantee
`onDestroy()` on process
death](https://developer.android.com/guide/components/activities/state-changes).

**Verify.** Capture the initial state, interruption method, observed process
/ scene transition, restored state and delivered result count. Reset
developer options afterwards. Test consent under the release identity (X6)
and label emulator-only evidence accurately (X4).

## X8 Network environments — P1 for networked apps

**Rule.** Exercise network-dependent flows under controlled failures and
address-family changes. A Wi-Fi indicator or a connectivity callback is
not evidence that DNS, TLS, the API or a long-lived connection works.

**Traps.** A developer host's network path can mask a device's failure;
automatic retries can duplicate non-idempotent submissions; a DNS64-NAT64
test network can translate to IPv4 without proving the server's native
IPv6 endpoint works. Apple's [IPv6 testing
guide](https://developer.apple.com/library/archive/documentation/NetworkingInternetWeb/Conceptual/NetworkingOverview/UnderstandingandPreparingfortheIPv6Transition/UnderstandingandPreparingfortheIPv6Transition.html)
documents that last limitation; [IPv6-only support](https://developer.apple.com/support/ipv6/)
also remains a release check for applicable App Store apps.

**Verify.**

- Run launch / sign-in, download, upload and reconnect offline, with failed
  DNS, a timeout, and service errors. Assert bounded retries, cancellation,
  preserved drafts and safe retry of uncertain submissions.
- Test IPv4, a controlled IPv6-only / DNS64-NAT64 path, and native IPv6
  service reachability where applicable. Record DNS / route setup and
  evidence that the app used it; disable alternate cellular or other
  fallback routes on the test device.
- Where relevant, test captive-portal entry / exit, metered / restricted
  data, VPN / proxy and Wi-Fi ↔ cellular transitions; use hardware for
  actual carrier handover (X4). Repeat an active operation after sleep /
  wake or airplane mode, without creating duplicate sessions.
- For local discovery, test peer isolation and absent peers separately
  from permission denial. Cross-link [permissions](permissions.md) and
  [media / device](media-devices.md) results instead of reporting all
  failures as "no internet".

## Report template

Evidence is scoped to a case. Include app build / artifact, OS build,
device or simulator, logical size, pixel ratio, text / locale settings,
steps, expected / observed result, and test / log / screenshot link as
relevant. Do not put credentials or private user data in artifacts.

```markdown
| ID | Status | Evidence |
|----|--------|----------|
| L1 | verified | build A, iPadOS 27 simulator: resizable window crosses the documented breakpoint; size / text settings and screenshots attached |
| L3 | to do | build A, Android 17 emulator: rotation loses the edit-dialog draft; regression case attached |
| M2 | not applicable | this app ships no audio feature |
| P1 | verified | release artifact A: final Android manifest, built Apple purpose strings and signed entitlements inspected; capability inventory and artifact hashes attached |
| P2 | to do | declaration inspection complete; fresh-consent denial and Settings revocation not exercised |
| X4 | needs device | Bluetooth route switch; owner: release QA; plan: paired physical phone / headset, disconnect during playback, verify fallback and continued session |
| X6 | to do | release APK starts on 4 KB image; 16 KB native-library test pending |
```
