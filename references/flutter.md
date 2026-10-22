# Flutter notes

Platform facts are in the other references; this file maps their checklist
IDs to Flutter APIs and plugin traps. Check the Flutter SDK and locked
plugin versions actually shipped: package support badges do not promise
that every method works on every listed platform.

## Layout (L1–L8) — P0

- Use `LayoutBuilder` constraints for a component's available space or
  `MediaQuery.sizeOf(context)` for its containing view. Never choose layout
  from `Platform.isX`, `defaultTargetPlatform` or raw `View.physicalSize`.
  Size-specific `MediaQuery.*Of` accessors narrow rebuild dependencies.
  Pass embedded-pane / navigation context explicitly to third-party kits
  instead of letting each invent its own mobile / desktop breakpoint.
- Keep controllers and session state above a layout switch. Stable keys /
  `PageStorage` can help retain element or scroll state; they do not replace
  process-death restoration. A `GlobalKey` is not a general-purpose state
  store and reparenting has lifecycle / performance costs.
- Insets: `MediaQuery.paddingOf` reflects safe-area padding;
  `viewPaddingOf` is independent of the keyboard; `viewInsetsOf` represents
  fully obscured areas such as a docked keyboard. `SafeArea` adjusts the
  descendant `MediaQuery`, so nested consumers must not add the original
  inset again. `Scaffold(resizeToAvoidBottomInset: true)` normally resizes
  its body above the keyboard; do not also pad that body by the same inset.
- Modal routes need their own inset handling. In
  `showModalBottomSheet(useSafeArea: true, isScrollControlled: true)`,
  `useSafeArea` covers **top / left / right**, not the bottom or keyboard.
  Give sheet content appropriate bottom safe-area / keyboard padding and
  scrolling, using the route's constraints. `isScrollControlled` alone
  neither scrolls arbitrary content nor keeps a text field visible. See
  [bottom-sheet semantics](https://api.flutter.dev/flutter/material/showModalBottomSheet.html).
- Android 15 / target API 35 enables edge-to-edge by default; target API 36
  on Android 16+ removes the old opt-out. Prefer migrating insets over
  relying on `SystemChrome.setEnabledSystemUIMode` / colour calls to undo
  platform enforcement. Check gesture and 3-button navigation on-device.
  See [Flutter's migration](https://docs.flutter.dev/release/breaking-changes/default-systemuimode-edge-to-edge).
- `SystemChrome.setPreferredOrientations` is a request with platform limits.
  Android 16 / target API 36 generally ignores orientation / resizability
  restrictions on displays with smallest width ≥ 600 dp (with documented
  exceptions and a temporary opt-out); target API 37 removes that opt-out.
  Test actual resize / rotation instead of assuming a portrait call locks
  the device. See [Android large-screen changes](https://developer.android.com/blog/posts/prepare-your-app-for-the-resizability-and-orientation-changes-in-android-17).
- On letterboxed Android, `MediaQuery.size` is the letterboxed app size;
  that is right for UI layout. If an orientation policy needs display size,
  use the current view's `View.of(context).display` and convert its units
  with the display's pixel ratio. Do not use the display size for pane
  breakpoints. iPad multitasking can ignore orientation requests too;
  full-screen opt-outs are not a durable adaptation strategy. See
  [orientation API limits](https://api.flutter.dev/flutter/services/SystemChrome/setPreferredOrientations.html)
  and [orientation rules](layout.md).
- Use scrollable / collapsing headers on short windows.
  `AlertDialog(scrollable: true)` scrolls title and content; its actions use
  an `OverflowBar`. Keep action area height reachable and constrain dialog
  width to available space / a product maximum; 560 logical pixels is a
  common Material width, not an OS requirement.
- Foldables: use `MediaQuery.displayFeaturesOf(context)` and supported
  display-feature-aware layouts. Dialog / sheet `anchorPoint` can choose the
  intended sub-screen. Test both vertical and horizontal hinges rather than
  treating all foldables as two equal portrait panes.

**Verify.** Pump narrow / short and wide constraints, keyboard / safe-area
profiles, hinge profiles and breakpoint transitions; then rotate / resize
an Android tablet and iPad window in a real app. Open sheets, dialogs and
menus with the keyboard visible. See [layout.md](layout.md) for the matrix.

## Text (D1–D2) — P0 for essential content

- Respect `MediaQuery.textScalerOf(context)` and use `TextScaler.scale`
  when manually measuring text. Do not replace a nonlinear scaler with a
  single multiplier. If a specific decorative element must clamp, use the
  scaler instance's `clamp` or `MediaQuery.withClampedTextScaling` locally
  and justify the limit; do not disable accessibility scaling app-wide.
  See [TextScaler](https://api.flutter.dev/flutter/painting/TextScaler-class.html).
- Avoid `FittedBox(fit: BoxFit.scaleDown)` around essential text that should
  wrap. Chips, segmented controls and action rows need tests with long
  labels and large text. `DropdownButton(isExpanded: true, isDense: false)`
  can help sizing but does not prove selected / menu labels remain readable.
- `flutter gen-l10n`: generated getters catch unknown resource IDs, but
  missing locale translations can still fall back. Configure
  `untranslated-messages-file` and have CI fail if it reports missing
  translations (an empty JSON object is not a missing translation).
  `required-resource-attributes` requires ARB metadata, **not translation
  completeness**. Include the intended `supportedLocales` and localisation
  delegates; strings outside widgets must refresh on locale change. See
  [localisation configuration](https://docs.flutter.dev/ui/internationalization).
- Widget tests default to Ahem square glyphs. Load shipped fonts with
  `FontLoader` and control fallback fonts on CI for meaningful wrapping /
  glyph checks; system font availability is not guaranteed by installing
  one font family.

**Verify.** Test long / RTL text with real fonts and a nonlinear `TextScaler`,
then the actual maximum accessibility settings on mobile. Confirm CI fails
for an intentionally missing translation before trusting its coverage.

## Density and assets (D3–D5) — P1

- `Image.asset` resolves density variants such as `2.0x/` and `3.0x/`.
  Provide suitable raster sources or vector rendering; naming one asset a
  high-density variant does not improve its resolution.
- Decode near rendered size, for example
  `Image.asset(name, cacheWidth: (logicalWidth * dpr).ceil())`, or use
  `ResizeImage` with an `ImageProvider`. The plain `Image` constructor has
  no `cacheWidth` parameter. `MediaQuery.devicePixelRatioOf(context)` can
  change at runtime; update derived decode / screenshot sizes without
  rescaling the logical UI twice. Bound caches and repeated decode work.
  See [Image.asset](https://api.flutter.dev/flutter/widgets/Image/Image.asset.html)
  and [M5](media-devices.md).
- `flutter_launcher_icons` supports platform-specific sources and Android
  `adaptive_icon_monochrome`; do not claim that it cannot generate a
  monochrome layer. Inspect generated artifacts for the locked version:
  launcher, notification and tray icons are different assets, and generating
  sizes cannot fix unsuitable artwork / geometry. See the
  [package configuration](https://pub.dev/packages/flutter_launcher_icons)
  and [platform icon rules](display.md).
- Keep the Windows runner's PerMonitorV2 DPI-awareness declaration when
  customising it. Verify the compiled runner and native plugin windows,
  rather than assuming every historical template has the same manifest.

**Verify.** Move a release desktop window across mixed-DPI monitors and
change scaling while an image / popup is visible. Check sharpness, decode
memory, icon artifacts and native plugin UI as well as Flutter widgets.

## Input (I1–I6) — P1 (P0 for navigation / text loss)

- `MaterialTapTargetSize.padded` / `kMinInteractiveDimension` help supported
  Material controls reach 48 logical pixels; they do not enforce the actual
  hit area of arbitrary widgets or overrides. Measure the interactive
  render box and tap edges. Run accessibility guideline matchers.
- Use `MouseRegion`, `Tooltip`, secondary-tap handlers, `Shortcuts` /
  `Actions`, `FocusTraversalGroup` and visible focus as appropriate.
  `SingleActivator(..., meta: true)` versus `control: true` follows the
  shortcut convention; platform detection is appropriate for conventions,
  not layout. Prefer Flutter's text-editing actions over overriding native
  selection / copy / paste shortcuts. See [input.md](input.md).
- Material desktop scroll behaviour adds scrollbars to many scrollables;
  thumbs fade by default. `Scrollbar(thumbVisibility: true)` needs the
  appropriate `ScrollController`; do not attach one controller to multiple
  independently interactive scrollbars. Avoid duplicate automatic / manual
  bars. Mouse drag-to-scroll is not the same as wheel / trackpad scrolling;
  configure `ScrollBehavior.dragDevices` deliberately. See
  [Scrollbar](https://api.flutter.dev/flutter/material/Scrollbar-class.html).
- For a custom Enter-to-send handler, active IME composition requires a
  **valid, non-collapsed** composing range. `isValid` alone also accepts an
  empty range and can suppress sending forever. Prefer `TextField` editing
  / submission actions where they match the flow; test composition commit,
  multiline input, key repeat and Shift+Enter on actual IMEs.
- Back: `PopScope(canPop:, onPopInvokedWithResult:)` must expose whether a
  pop is allowed before the predictive gesture. The callback reports whether
  it already happened; do not pop again when `didPop` is true. Check the
  merged `android:enableOnBackInvokedCallback` configuration and SDK / router
  support instead of assuming adding a manifest flag completes migration.
  See [PopScope](https://api.flutter.dev/flutter/widgets/PopScope-class.html).
- `IconButton.tooltip` normally supplies its accessible description; avoid
  duplicate wrapper labels. For custom controls expose the correct name,
  role, state and action with `Semantics`. Use `tester.ensureSemantics()`,
  `find.bySemanticsLabel` and guideline matchers such as
  `androidTapTargetGuideline`, `labeledTapTargetGuideline` and
  `textContrastGuideline`, then exercise a platform screen reader.
- Use `MediaQuery.alwaysUse24HourFormatOf(context)` for a user-requested
  time convention alongside locale-aware formatting; do not format time by
  concatenating translated fragments.

**Verify.** Complete core flows by keyboard, pointer, touch and screen
reader on shipping platforms. Test a composing IME, nested back navigation,
cancelled predictive back and long text in menus; see [input.md](input.md).

## Lifecycle (B1–B5) — P0 for state / session loss

- `AppLifecycleListener` / `WidgetsBindingObserver`: `inactive` can be
  visible without focus; `hidden` means all views are hidden; `paused` is
  a mobile lifecycle state, not a desktop focus-loss event. Callbacks can
  be skipped during abrupt termination. Persist important edits as they
  happen; do not wait exclusively for `detached` or `onExitRequested`.
  See [AppLifecycleState](https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html).
- Apply resource-specific policy: a focus change alone should not end a
  call, but camera plugins / OS capture interruptions may require releasing
  and reacquiring capture even on `inactive`. Likewise valid background
  audio must not be stopped merely because the app becomes hidden. See
  [media rules](media-devices.md) and the camera note below.
- `RestorationMixin` / `restorationScopeId` restore participating state;
  controllers, files and app data are not automatically persisted. For
  Android `image_picker`, run `retrieveLostData()` during startup, handle
  errors and reconcile recovered attachments with drafts once (M4).
- Call `getNotificationAppLaunchDetails()` on a
  `FlutterLocalNotificationsPlugin` instance on supported implementations;
  buffer routing until navigation is ready and handle foreground /
  background response callbacks
  separately. Plugin background handlers have platform / isolate limits;
  do not assume a UI navigator is available there.
- Desktop window / single-instance packages need a per-platform capability
  check. `window_manager` / `screen_retriever` do not remove Wayland
  placement restrictions. A lock must distinguish a live owner from stale
  state and route second-launch arguments to the intended window (W1 / B5).
- An Android foreground-service plugin still needs the host manifest,
  matching service type / permissions and a legally startable service.
  Follow [B4](lifecycle.md); a Dart timer is not background execution policy.

**Verify.** Abrupt process loss during editing / a system picker, focus
loss with an active call, hidden / resumed capture and second launch with
activation arguments. Confirm durable state and no duplicated attachments.

## Permissions (P1–P5) — P0

- `permission_handler`: host declarations remain necessary. CocoaPods
  integrations enable the required `PERMISSION_*` macros in the Podfile
  (for example `PERMISSION_CAMERA=1`). Current Swift Package Manager
  integrations derive enabled permissions from usage-description keys in
  the app's Info.plist; they do not use the Podfile setup. Follow the
  **locked version's** instructions and validate flavor / build-specific
  plists and SPM caching behaviour. See
  [permission_handler setup](https://pub.dev/packages/permission_handler).
- Use the returned request result and re-check on return from Settings;
  handle limited / restricted / permanently denied states according to
  the capability. `openAppSettings()` opens settings; it does not grant
  access. macOS / Linux support must come from an actual implementation,
  not an assumed `permission_handler` method.
- Inspect the merged Android **release / flavor** manifest and packaged
  Info.plist / privacy manifests / entitlements, including plugin-added
  declarations. Intermediate paths vary by Gradle / plugin version; use
  the build's manifest-merger report or APK Analyzer instead of hard-coding
  one directory. See [permissions.md](permissions.md).
- In typical macOS runners, check both `DebugProfile.entitlements` and
  `Release.entitlements`, plus any custom configurations. Keep functional
  capabilities aligned while retaining debug-only signing differences (W4).
- `flutter_secure_storage`: Keychain items can survive uninstall; apply an
  explicit reinstall / sign-out policy to entries owned by the app, not an
  unconditional wipe of shared credentials. Linux implementations need the
  documented native Secret Service / keyring dependencies; handle locked /
  missing services without hanging startup. See [P5](permissions.md).

**Verify.** Fresh installed release, first request denied, limited access,
Settings change and each flavor's artifact. Check that permission dialogs
actually appear on the relevant device and unsupported hosts degrade.

## Media and audio (M1–M8) — P0 if used

- Audio plugins can each configure `AVAudioSession`. Coordinate with
  `audio_session` or the call engine's documented integration and reapply
  the intended configuration after plugin initialization where necessary.
  A common Dart API does not make focus / routing behaviour identical on
  all hosts. See [audio_session](https://pub.dev/packages/audio_session).
- `wakelock_plus` controls display wakefulness, not an Android CPU wakelock
  or background-service permission. One owner should release it when the
  last qualifying visible session ends, including error paths (M1).
- `camera` does not handle lifecycle for the app. Its documented mobile
  example disposes on `inactive` and recreates on `resumed`; do not blindly
  override that with a hidden-only rule. Retaining capture during iPad
  multitasking requires verified OS **and plugin** support. Serialise
  initialization / disposal and ignore stale async completions so resume
  cannot install an already-disposed controller. Handle denied / restricted
  initialization errors. See [camera lifecycle](https://pub.dev/packages/camera).
- The endorsed `camera` package does not imply desktop camera support.
  Likewise desktop `image_picker` file selection does not provide a camera
  UI by default; a supported `cameraDelegate` or separate capture backend
  is needed. Check actual backend support for external cameras (M3).
- Do not assume `image_picker` quality / maximum-size options force HEIC
  into JPEG. Inspect the result and explicitly transcode if required by
  the receiver. Camera results can live only in cache; move / copy durable
  attachments before cleanup. Test HEIC on a physical Apple device and
  cloud-only items offline. See [image_picker](https://pub.dev/packages/image_picker)
  and [format / access rules M4](media-devices.md).
- For ZIP / a protocol defined with POSIX separators use `path.posix`;
  use the local `path` context for real filesystem paths. A content URI is
  not a local path; do not run it through `File(uriString)` (M4 / W3).

**Verify.** Use the media reference's real-device route / camera / capture
checks, including permission denied, lock / resume, another plugin taking
over audio, resize during capture and rapid cancel / reopen.

## Testing and release integration (X1–X6, W4) — P0 for release

- Build a plugin matrix by method / platform / architecture, including
  native dependencies and minimum OS. For unsupported methods provide a
  fallback before invocation; catching `MissingPluginException` only after
  a user action is not a completed feature. Widget mocks cannot verify
  plugin registration, native signing or hardware support.
- Layout sweeps should vary `tester.view.physicalSize` and
  `devicePixelRatio` consistently with logical size; reset view overrides,
  locale / inset overrides and error handlers in teardown. Use real fonts
  and nonlinear text scaling. Preserve normal `FlutterError.onError`
  reporting while collecting overflow evidence, and check
  `RenderParagraph.didExceedMaxLines` after layout. It detects truncation,
  not every parent clip / occlusion; add visibility / hit tests for essential
  actions. See [truncation API](https://api.flutter.dev/flutter/rendering/RenderParagraph/didExceedMaxLines.html).
- Use `integration_test` for real flows; drive rotation / window resize
  from device / emulator / desktop controls too. Calling
  `SystemChrome.setPreferredOrientations` alone cannot prove a resize
  occurred on a platform that ignores it. Assert size actually changed and
  the open item, draft, selection and navigation state survived.
- Golden tests need controlled fonts, renderer / SDK and host assumptions;
  platform differences require deliberate baselines, not a broad tolerance
  that hides clipped content. Goldens do not prove native overlays or
  screen-reader behaviour; see [testing.md](testing.md).
- Build and install every shipped native architecture. Keep iOS device
  and simulator artifacts separate; an arm64 simulator library is not an
  arm64 device library. Check deployment targets against every bundled
  native framework, and exercise macOS / Windows ARM dependencies where
  supported. Verify desktop releases on a clean machine (W4).
- Android Flutter apps include native engine / plugin libraries. Validate
  **all** bundled `.so` files and APK / bundle packaging for 16 KB page
  compatibility, then run on a 16 KB device / emulator. Updating Dart code
  or the engine does not rebuild an incompatible prebuilt plugin library.
  Check current Play enforcement and any app-specific extension rather
  than copying an old deadline. See
  [Android's 16 KB checks](https://developer.android.com/guide/practices/page-sizes).

**Verify.** Record the SDK / locked plugin versions, artifact, host OS /
architecture and device evidence. A widget test / successful build is not
"verified" for permissions, real audio routes, external hardware, native
pickers or store / installed-release behaviour.
