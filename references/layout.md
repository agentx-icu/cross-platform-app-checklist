# Layout and screens (L1–L8)

Platform details checked against the linked primary sources on 2026-10-22.
Dimensions below are logical units (Apple pt, Android dp, framework logical
pixels), unless explicitly labelled physical pixels. Test dimensions and
product recommendations are not OS limits.

## L1 Size range — P0

**Rule.** Every screen and overlay works in the smallest supported **content
area**, at short heights, and at the largest supported window size. Use the
following as starting test cases, then add the actual supported devices:

| Case | What to exercise |
|---|---|
| Small phone / narrow pane | 320 logical units wide, and narrower if a supported window mode permits it |
| Typical phone | 360, 390 and 430 wide; portrait and landscape |
| Short landscape window | About 320 high before bars and keyboard; do not assume width implies usable height |
| Tablet / foldable | Cover screen, inner screen, narrow split pane, freely resized window and maximised window |
| Desktop | Documented minimum client size through maximised / ultrawide; test a 4K display at its actual scaling |
| Android adaptive-quality reference sizes | Foldable ≈ 841 × 701 dp, 8″ tablet ≈ 1024 × 640 dp, 10.5″ tablet ≈ 1280 × 800 dp, 13″ Chromebook ≈ 1600 × 900 dp ([adaptive app quality](https://developer.android.com/docs/quality-guidelines/large-screens-app-quality)) |
| GNOME / Linux desktop | GNOME HIG: every app works at 1024 × 600; phone-capable apps at 360 × 294 ([adaptive guidelines](https://developer.gnome.org/hig/guidelines/adaptive.html)) |

**Traps.**

- A tablet model name says nothing about the size of its current pane.
  New windowing modes need not use the old one-third / half split ratios.
- A 3840-physical-pixel display at 200 % scaling is not a 3840-unit content
  area. Test display density separately under [D3–D4](display.md#d3-pixel-density--p0).
- Headers, side rails and composers consume the entire short window; make
  secondary content collapsible and the main content scrollable.
- Wide forms and dialogs need a product-defined maximum width, while
  document / media viewers may use the space. Do not stretch reading text
  across an ultrawide window or impose a phone-sized maximum on every tool.
- A desktop minimum size larger than the available work area can hide
  actions at high scaling. Window placement belongs to [W1](desktop.md).

**Verify.** Run the [X2 layout sweep](testing.md) with both width and height
varied. Manually check a narrow tablet window, the desktop minimum client
size, and the smallest supported phone with its keyboard open.

## L2 Breakpoints by available width — P0

**Rule.** Choose panes and navigation from the current window's available
size and the component's actual constraints, not the OS, model, physical
display or a cached device-type flag. Share the shell's layout policy;
pass explicit navigation context to embedded components.

**Traps.**

- The shell embeds a detail pane while a child guesses it is a phone and
  shows a back button that pops the shell. Width alone does not establish
  whether a component owns a route or is embedded.
- At 834 units, a 200-unit sidebar plus a 330-unit list leaves only 304 for
  content before gutters and insets. Measure each pane's minimum useful
  size, including large text, before selecting a multi-pane layout.
- Android window size classes describe the app window, not a permanent
  tablet classification. On Apple platforms use the current scene / view
  geometry; a global main-screen size is wrong for another scene or display.
  See [Android window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes)
  and [Apple scene resizing](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key).
- A keyboard reducing height should not unexpectedly replace the entire
  navigation shell. Define how width, height and text size affect layout.
- On Android 15+ with target 35+, `Configuration.screenWidthDp` and
  `screenHeightDp` no longer exclude system bars; `smallestScreenWidthDp`
  and `orientation` can be affected indirectly. Do not use them as the
  layout's available size; use window metrics / insets instead.
  See [Android 15 behaviour changes](https://developer.android.com/about/versions/15/behavior-changes-15).
- Prefer published breakpoints as a starting point over invented ones:
  Material 3 width classes compact < 600, medium 600–839, expanded
  840–1199, large 1200–1599, extra-large ≥ 1600 dp (height: < 480, 480–899,
  ≥ 900); Windows responsive guidance small ≤ 640, medium 641–1007, large
  ≥ 1008 effective px. Adjust to measured content capacity.
  See [Android window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes)
  and [Windows breakpoints](https://learn.microsoft.com/en-us/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design).

**Verify.** Test one logical unit below, at and above every breakpoint,
including at large native text sizes. Open the same detail as a route and
as an embedded pane; check both its available width and its back action.

## L3 Crossing a breakpoint at runtime — P0

**Rule.** Rotation, window resize, fold / unfold and display changes can
alter geometry while work is in progress. Preserve the open item, draft,
selection, scroll position, focus and ongoing session; geometry changes
need not change orientation or cross a breakpoint.

**Traps.**

- A detail pane disappears on collapse, or a duplicate pushed detail covers
  the expanded shell. Keep one selection / navigation model and reconcile
  its presentation without duplicating routes.
- Layout-mode keys recreate editors and media controllers. Keep durable
  state above the presentation switch; restore focus only to a visible view.
- Android normally recreates an Activity for relevant configuration
  changes. `android:configChanges` handles only the listed changes and
  transfers responsibility for refreshing resources to the app; copying a
  fixed list does not handle every change or process death. Use the
  framework's supported state restoration. See [configuration changes](https://developer.android.com/guide/topics/resources/runtime-changes)
  and [B2–B3](lifecycle.md).
- Android 17/API 37 no longer recreates Activities by default for several
  input-device changes, color-mode changes and transitions into / out of desk
  UI mode. Refresh affected UI in `onConfigurationChanged()`; apps that
  genuinely depend on recreation can use `android:recreateOnConfigChanges`
  for the documented cases. Attaching a keyboard is not a reliable signal
  that the screen will be rebuilt. See the same configuration-change guide.
- Restoring a raw scroll offset after columns reflow can show a different
  item. Preserve an item anchor where continuity matters.
- Popover anchors, drag coordinates and custom canvas hit regions become
  stale during resize. Recompute them in the current coordinate space.
- The transition lays out a frame at the new width using the old mode;
  transient overflow still counts as a defect.

**Verify.** Rotate / resize across a breakpoint with a draft, selection and
scrolled detail open; also resize without crossing it. Assert content and
session continuity, and that one back action returns to the expected list.
Exercise actual Android Activity recreation as well as framework relayout.
On Android 17+, also attach / detach an input device without a restart.

## L4 Safe areas and system bars — P0

**Rule.** Draw backgrounds edge to edge where appropriate, while keeping
controls and essential content clear of current occlusions. Read insets for
each window and edge; do not hard-code notch or navigation-bar dimensions.

| Platform | Rule / failure prevented |
|---|---|
| iOS / iPadOS | Use the view's safe area for cutouts, home indicator and system chrome; values change with orientation and window configuration. A fixed landscape notch allowance is unreliable. |
| Android | On Android 15+ with target SDK 35+, edge-to-edge is the default enforced behavior. Android 15 has a temporary theme opt-out; on Android 16+ for target 36+ that opt-out is disabled. Handle insets rather than using the escape hatch. |
| Android navigation / cutouts | Read status, navigation, caption and display-cutout insets on all edges. Three-button navigation can occupy a side in landscape; placement and size depend on the device / mode. |
| Desktop | Custom title bars must reserve caption controls and valid drag regions. On macOS use the content layout area / safe-area information for full-size content and display cutouts. A desktop window is not necessarily a zero-inset surface. |

See [Android edge-to-edge](https://developer.android.com/develop/ui/views/layout/edge-to-edge),
[Android 16 opt-out removal](https://developer.android.com/about/versions/16/behavior-changes-16),
[UIKit safe areas](https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide)
and [AppKit screen safe areas](https://developer.apple.com/documentation/appkit/nsscreen/safeareainsets).
Custom title-bar integration belongs to [W1](desktop.md).

**Traps.**

- Root and nested screens both apply the same inset, wasting space; an
  overlay in another window applies none. Assign ownership for each edge.
- System bars, cutout and keyboard regions can overlap. Combine their
  occupied regions rather than blindly adding all bottom values.
- Gesture-navigation areas are not identical to visual cutout areas.
  Edge drags need alternatives; keep Android gesture exclusion narrow and
  local to the control, using the [system gesture guidance](https://developer.android.com/develop/ui/views/touch-and-input/gestures/gesturenav).
- Insets can change when bars hide / reappear or a freeform caption bar
  appears. Update layout and bar-icon contrast while running.

**Verify.** Check notched and unnotched phones, both landscape directions,
Android gesture and three-button navigation, an emulated cutout, a tablet
window with a caption bar, and custom desktop title bars. Hit-test controls
near every edge and reveal system bars while content is open.

## L5 Soft keyboard — P0

**Rule.** With the keyboard open, the focused caret, validation message and
primary action remain reachable. Use actual keyboard occlusion and scrolling;
there is no fixed minimum remaining height or keyboard height.

**Traps.**

- Scaffold resizing plus manual keyboard padding applies the inset twice.
  Audit screens, nested scaffolds and separate dialog windows individually.
- A floating / split iPad keyboard is not a full-width bottom obstruction.
  UIKit's `keyboardLayoutGuide` can track an undocked keyboard with
  `followsUndockedKeyboard`; its default is `false`. Convert keyboard
  rectangles into the receiving view's coordinate space when handling them
  manually. See [Apple keyboard layout](https://developer.apple.com/documentation/uikit/adjusting-your-layout-with-keyboard-layout-guide).
- Android edge-to-edge layouts must consume IME insets as intended by their
  toolkit; `adjustResize` alone is not a universal padding solution. For
  Views, use `WindowInsetsCompat.Type.ime()` and supported inset animation
  handling. See [Android keyboard insets](https://developer.android.com/develop/ui/views/layout/sw-keyboard).
- A hardware keyboard may leave no software-keyboard inset while an
  accessory / candidate UI remains. Do not infer focus or keyboard presence
  solely from bottom padding.
- Interactive keyboard dismissal, prediction bars and keyboard-language
  changes alter occlusion during editing. Keep the caret visible without
  repeatedly jumping the entire conversation or losing focus.

**Verify.** Check every input screen and dialog in phone landscape; show
errors while typing. On iPad, move a floating keyboard over the input and
test split keyboard where available. Connect / disconnect a hardware
keyboard, switch IMEs, and dismiss the keyboard interactively.

## L6 Orientation — P0

**Rule.** Design tablet / large-window layouts for rotation and resizing;
declare only restrictions the product needs and the OS actually honors.
Supported orientations are a UI contract, not a reliable resize opt-out.

**Traps.**

- Apple: match `UISupportedInterfaceOrientations` and any iPad-specific
  `UISupportedInterfaceOrientations~ipad` to the supported UI. Support all
  interface orientations for resizable iPad scenes. `UIRequiresFullScreen`
  was deprecated in iPadOS 26. With the iOS 27 SDK or later on iOS / iPadOS
  27, keeping that key can select discrete scene resizing instead of
  preventing resizing. Migrate per [TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key);
  do not assume old Split View opt-out behavior persists.
- Android 16, target 36+: orientation, resizability and aspect-ratio
  restrictions are normally ignored on displays with smallest width
  **at least 600 dp**. Android 16 provides a temporary opt-out and documented
  exceptions; the default behavior fills the app window rather than
  preserving the lock through letterboxing. See [Android's adaptive-layout migration](https://android-developers.googleblog.com/2025/01/orientation-and-resizability-changes-in-android-16.html).
- Android 17, target 37+: the developer opt-out is removed. The dedicated
  [Android 17 restriction page](https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored)
  describes displays **greater than 600 dp**, while the [migration announcement](https://developer.android.com/blog/posts/the-first-beta-of-android-17)
  uses **at least 600 dp**; the exact boundary is inconsistent in the docs.
  The dedicated page lists game and user-override exceptions. Treat 600 dp
  as needing adaptive-layout testing rather than relying on it to retain a lock.
- Interface orientation, physical device orientation and camera sensor
  orientation are different. A tabletop fold or locked interface must not
  rotate a preview / capture incorrectly; see [M3](media-devices.md).

**Verify.** Check all four interface orientations on iPad, phone landscape
when supported, and Android tablets / foldables on target-appropriate OS
versions. Test 599 / 600 / 601 dp display configurations, freeform resizing,
rotation lock, and declarations in the merged release manifest / plist.

## L7 Overlays — P1

**Rule.** App-controlled dialogs, sheets, menus, snackbars, FABs and banners
follow L1–L5. System-owned surfaces retain the behavior of their platform.

**Traps.**

- A dialog fits at default text size but hides its actions after scaling.
  Use scrollable content and reachable actions, whether pinned or scrolling;
  wrap action rows instead of shrinking essential labels.
- A transient message contains the only copy of a critical error or action.
  Keep an equivalent persistent, accessible path; long messages must remain
  readable and announced appropriately under [I5](input.md).
- A FAB covers the final list item, or its large label is simply clamped.
  Reserve scroll padding and adapt the control without defeating [D1](display.md).
- A UIKit action sheet or share controller **presented as a popover** needs
  a valid anchor; omitting required popover configuration can raise an
  exception. Use the applicable `UIPopoverPresentationController` anchor API
  (`sourceView` and `sourceRect`, or the supported source-item API), and
  update it after resizing. This is not a rule for every iPad sheet. See
  [popover anchors](https://developer.apple.com/documentation/uikit/uipopoverpresentationcontroller/sourcerect)
  and [share-controller presentation](https://developer.apple.com/documentation/uikit/uiactivityviewcontroller).
- A menu overflows the window near an edge, or remains anchored to a view
  removed by a breakpoint change. Reposition, adapt or dismiss it safely.

**Verify.** Open each overlay near every window edge at maximum text size
and minimum height; then rotate / resize with it open. Check keyboard
occlusion, focus return, dismissal and the final list item's reachability.

## L8 Fold hinges and posture — P1 when foldables / dual screens are supported

**Rule.** Account for separating folds and occluding hinges in addition to
width. Keep controls, text and caret out of an occluded hinge; choose pane
placement from the current feature bounds and posture.

**Traps.**

- A wide window is treated as one uninterrupted rectangle and puts a submit
  button or line of text across a physical hinge.
- A fold is always treated as missing pixels. AndroidX `FoldingFeature`
  distinguishes `bounds`, `isSeparating`, `occlusionType` and `state`; a
  non-occluding crease can still suggest two logical areas. Observe updates
  from `WindowInfoTracker`, not a hard-coded device model. See
  [foldable layout guidance](https://developer.android.com/codelabs/android-window-manager-dual-screen-foldables).
- Posture changes without a width breakpoint leave controls on the wrong
  half. Tabletop layouts must keep essential actions accessible while
  preserving the same session under L3.
- Hinge bounds and touch / overlay coordinates are compared in different
  coordinate spaces. Transform them into the current window's coordinates.

**Verify.** Use an emulator with an occluding hinge and one with a flexible
fold; exercise flat, half-open, rotated and spanned windows. Change posture
with a dialog and text selection open. Confirm no essential content crosses
the hinge; validate hardware-specific behavior under [X4](testing.md).
