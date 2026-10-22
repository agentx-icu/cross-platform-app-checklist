# Input and interaction (I1–I7)

Platform details checked against the linked primary sources on 2026-10-22.
Input capabilities can coexist and change while running: a tablet may have
a keyboard, a desktop may have touch, and a stylus may support hover.

## I1 Touch targets — P1

**Rule.** Use at least 44 × 44 pt hit areas for ordinary iOS / iPadOS touch
controls and 48 × 48 dp for Android touch controls as this checklist's
baseline. These are design recommendations, not a universal store-rejection
threshold. Separate adjacent targets enough to avoid accidental activation;
8 dp can be a starting spacing choice, not a rule for every platform widget.
See [Apple buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
and [Android touch targets](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views).

**Traps.**

- Padding lies outside the gesture detector: a visible 44 pt button has only
  a text-sized hit area. Test the actual hit region, including its edges.
- Invisible hit-area expansion overlaps a neighbour, or an ancestor clips
  it. The nearest visual control must receive the tap predictably.
- A desktop classification selects tiny controls on a touch-capable laptop.
  Keep touch usable when devices coexist; do not permanently choose density
  from the last pointer event.
- A disabled-looking label still intercepts taps, or a transparent overlay
  blocks controls below it. Verify enabled state and hit-test behavior agree.

**Verify.** Tap corners, padding and gaps between adjacent controls at
normal and maximum text size. Check touch and mouse on a hybrid device;
measure accessibility bounds as well as hit-test bounds.

## I2 Pointer and keyboard — P1 on desktop and keyboard-equipped mobile devices

**Rule.** Complete the main flows with keyboard and pointer wherever those
inputs are available. Use control-specific platform conventions rather
than treating every control as a generic clickable container.

| Input | Expected behavior / failure prevented |
|---|---|
| Hover | Indicate interactive state and explain icon-only actions, while keeping every essential action available without hover. Hover capability is not an OS classification. |
| Secondary click | Offer appropriate context actions through right-click / two-finger click and a keyboard or visible-menu path; touch long-press can expose the same actions. |
| Scrolling | Support mouse wheel, high-resolution trackpad deltas, inertia and relevant horizontal scroll. Follow the OS scrollbar visibility setting; always-visible scrollbars are not a universal desktop convention. |
| Keyboard focus | Predictable Tab / Shift-Tab traversal, visible focus and control-appropriate activation (for example Space for a button, arrows within a menu). Keep focus visible when scrolled or covered by an overlay. |
| Shortcuts | Use Command for standard Apple editing / app shortcuts and Control for their Windows / Linux equivalents. Preserve system, assistive-technology and text-editor shortcuts; publish supported commands in menus or shortcut help. |
| Drag and drop | Accept supported types with clear feedback; reject unsupported drops safely and provide a picker / other path. File-access lifetime and sandbox rules belong to [P1](permissions.md) and [W3](desktop.md). |

See [Apple keyboard guidance](https://developer.apple.com/design/human-interface-guidelines/keyboards)
and [Android input compatibility](https://developer.android.com/develop/ui/views/touch-and-input/input-compatibility-on-large-screens).

**Traps.**

- Handling a shortcut in both parent and child submits twice; a global
  handler steals copy, undo or arrows from the focused editor. Scope commands
  to the active window and control, and consume them once.
- Single-letter shortcuts fire while typing or using an IME. Use deliberate
  modifiers / focus scope and preserve the text input path under I3.
- Removing a focused item leaves focus nowhere. Move it to a logical
  neighbour; modal dialogs contain focus and restore it on dismissal.
- Mouse drag-to-scroll prevents selecting text. Provide native scrolling
  and selection behavior unless a deliberate canvas interaction needs dragging.
- iPad Full Keyboard Access exposes focus defects absent in ordinary Tab
  testing. Test it explicitly; keyboard support is not a niche-only tablet
  enhancement. See [Full Keyboard Access](https://developer.apple.com/videos/play/wwdc2021/10120/).

**Verify.** Complete sign-in, navigation, editing and one modal flow without
touch. Repeat using trackpad and mouse, with auto-hidden scrollbars, and
connect / disconnect a keyboard while an editor is focused. Test non-US
keyboard layouts, held-key repeat, and simultaneous touch / pointer use.

## I3 Text input — P0

**Rule.** Treat committed text, composition, selection and keyboard commands
as separate parts of the platform text-input protocol. Prefer native /
toolkit editors over reconstructing text from key-down events.

**Traps.**

- Enter confirms a CJK candidate and also sends the message. Respect the
  editor's composition state and commit lifecycle, not only a raw Enter
  event. UIKit exposes `markedTextRange`; Android editors use composing
  spans / `InputConnection`. A soft keyboard, dictation or handwriting may
  commit text without matching hardware-key events. See [UIKit marked text](https://developer.apple.com/documentation/uikit/uitextinput/markedtextrange)
  and [Android composition](https://developer.android.com/reference/android/view/inputmethod/InputConnection).
- A hardware-key handler submits before the editor receives the last text
  update. Submit from the editor's supported action / committed state; an
  arbitrary delay or a second global Enter handler is not a reliable fix.
- Newline / send semantics are imposed as a universal desktop rule. Choose
  them for the field and product, expose an unambiguous send / submit action,
  and document any newline modifier. Preserve multiline input and do not
  submit on held-key repeats.
- Replacing the entire text value on each keystroke resets the composing
  range, selection, undo or native selection toolbar. Apply supported editor
  updates and let system copy / paste / selection coexist with app menus.
- Numeric keyboards may lack a sign, decimal separator or Return key.
  Provide reachable actions and validate pasted / hardware-keyboard input;
  keyboard type is a hint, not an input-validation boundary.
- UTF-16 / code-point length is mistaken for user-perceived characters.
  Use appropriate grapheme-aware handling for limits and truncation; keep
  platform selection offsets in the units its API requires. Test combining
  marks and joined emoji, not only ASCII. See [Unicode text segmentation](https://www.unicode.org/reports/tr29/).
- Autofill / password-manager / one-time-code completion is broken by a
  custom field or disabled paste. Supply correct content types / autofill
  hints and preserve secure-entry behavior. Do not log secret field values.
- On iOS 16+, programmatic reads of another app's pasteboard can prompt.
  A custom button calling `UIPasteboard.general.string` is not guaranteed
  prompt-free merely because it follows a tap. Prefer the system paste menu
  or `UIPasteControl` where applicable; do not read the clipboard at launch
  or on every focus change. See [UIPasteControl](https://developer.apple.com/documentation/uikit/uipastecontrol).
  Permission denial handling belongs to [P2–P3](permissions.md).

**Verify.** Use real CJK IMEs to compose, select a candidate, cancel and
submit; repeat with a hardware keyboard and rapid typing. Check dead keys,
accented text, dictation / handwriting where supported, multiline paste,
undo / redo, autofill and paste denial. Assert exactly one complete committed
value is submitted and that an in-progress composition never submits.

## I4 Back navigation — P0

**Rule.** Each platform's back / dismiss input resolves the topmost eligible
surface without duplicate navigation or lost work. Keep one route / modal
policy shared by toolbar buttons, gestures, shortcuts and system callbacks.

**Traps.**

- Android Back pops a route underneath an open keyboard, popup or dialog.
  Let the IME / active surface handle its own dismissal, then navigate.
  Root Back normally leaves the task according to system conventions; a
  forced home-tab detour or double-back-to-exit is a product choice, not an
  Android requirement. See [Android Back principles](https://developer.android.com/guide/navigation/principles).
- For target 36+ on Android 16+, predictive system back animations are
  enabled by default, and legacy `onBackPressed()` / `KEYCODE_BACK` handling
  is unavailable on that default path. Use AndroidX `OnBackPressedCallback`
  / the supported platform API or the framework equivalent. The
  `android:enableOnBackInvokedCallback` manifest flag alone does not migrate
  custom interception. See [Android 16 Back changes](https://developer.android.com/about/versions/16/behavior-changes-16)
  and [predictive Back migration](https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture).
  For Flutter APIs see [the framework reference](flutter.md).
- A predictive / interactive gesture mutates data before it commits. A
  cancelled gesture must restore the same route, draft and focus; avoid
  irreversible work on gesture start.
- A custom iOS navigation shell loses the native interactive pop gesture,
  or assumes every back gesture starts at the physical left edge. Preserve
  current platform navigation behavior and provide a visible back action.
- Desktop Esc first belongs to the active context, such as an IME candidate
  or menu; it must not also close the underlying dialog. Support history
  shortcuts / mouse back where the product has history, not for every pane.
- Always prompting to leave is disruptive; silently discarding a changed
  form is worse. Confirm genuinely destructive abandonment or save a draft,
  consistently across all departure paths. Running background sessions use
  [B1–B4](lifecycle.md), not an unconditional stop-on-back policy.

**Verify.** Exercise toolbar Back, Android button and predictive gestures,
iOS interactive pop, keyboard history / Esc and mouse back where supported.
Cancel a gesture halfway. Repeat with the keyboard, a dialog and an unsaved
draft open, then at the root; assert no double pop or accidental exit.

## I5 Screen readers — P1

**Rule.** Expose names, roles, state, actions and sensible reading order
through the platform accessibility tree. Use native semantics where possible;
a visible label or a clickable canvas alone is not an accessible control.

**Traps.**

- Icon-only controls are unnamed, or a wrapper and its child both announce
  the same button. Give each actionable element a meaningful, localised
  name; do not include redundant role words in every name.
- Custom controls expose a name but omit selected / checked / expanded /
  disabled state, range values or available actions. Match semantics to
  behavior; avoid merging distinct child actions into one inaccessible node.
- Informative images have no equivalent description; decorative images
  clutter the reading order. Provide a useful alternative only when needed.
- An overlay leaves its background reachable, moves focus on every rebuild,
  or does not return focus when dismissed. Distinguish keyboard focus from
  screen-reader focus and preserve a logical destination under [L3](layout.md).
- Errors, progress and incoming content update visually but are not announced,
  or announce every frame / keystroke. Use appropriate status / live-region
  mechanisms with restrained updates; keep error text associated with its field.
- A virtualised list removes the focused node, changes item identities or
  auto-scrolls away while being read. Preserve context and accessible scroll /
  item actions; test long lists, not just the first screenful.

See [Apple accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
and [Android accessible app guidance](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views);
also check [Windows accessibility](https://learn.microsoft.com/en-us/windows/apps/develop/accessibility)
and [Orca's supported accessibility infrastructure](https://gnome.pages.gitlab.gnome.org/orca/help/introduction.html).

**Verify.** Complete the main flows with VoiceOver (iOS / iPadOS / macOS),
TalkBack (Android), Narrator (Windows) and Orca on supported Linux desktop /
toolkit combinations. Include modals, errors, long lists and custom drawing
surfaces. Tree inspection catches missing semantics but does not replace
an actual screen-reader pass; record untested combinations as to do.

## I6 System formats — P1

**Rule.** Format for the user's locale, calendar, time zone and explicit
regional preferences. App language alone does not determine time format,
measurement units or the first day of the week.

**Traps.**

- A hard-coded `HH:mm` ignores the chosen 12-hour setting. Android's
  `DateFormat.getTimeFormat(context)` accounts for locale and the user's
  12 / 24-hour preference; `is24HourFormat(context)` exposes the choice.
  See [Android date formatting](https://developer.android.com/reference/android/text/format/DateFormat).
- Apple date / time output is built from manually concatenated fields.
  Use localised styles / templates and the appropriate user preferences;
  cached formatters need refreshing when relevant settings change. See
  [Foundation DateFormatter](https://developer.apple.com/documentation/foundation/dateformatter).
- A calendar assumes Sunday, the Gregorian calendar or the app language's
  region despite a user override. Query calendar / regional preferences;
  test non-Gregorian calendars if the UI supports them.
- Currency is inferred solely from UI locale. Preserve the value's actual
  currency code and localise its presentation. Parse user-entered decimal /
  grouping separators appropriately instead of stripping punctuation.
- An instant, local date and wall-clock appointment are stored as the same
  thing. Test time-zone changes and daylight-saving transitions; never sort
  by localised display strings or use them as a wire format.

**Verify.** Change 12 / 24-hour time independently of language, switch region
and first weekday where supported, and exercise decimal commas, negative
values and multiple currencies. Resume after a time-zone / calendar change;
check forms, pickers and already-open views, not just newly formatted labels.

## I7 Gesture alternatives and cancellation — P1

**Rule.** Keep essential actions usable without a complex gesture, pressure,
hover, haptics or a specific pointing device. Cancelled input must leave no
accidental activation or stuck interaction state.

**Traps.**

- Reordering, swipe actions or pinch-only zoom have no visible / keyboard /
  accessibility alternative. Offer controls such as Move up / down, an
  actions menu or zoom buttons. For web surfaces, WCAG 2.2's [dragging rule](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements)
  requires a single-pointer alternative without dragging, unless excepted;
  keyboard support alone is not that alternative.
- A destructive action commits on pointer-down; dragging away or receiving
  cancellation still activates it. Prefer the native control's release /
  cancellation behavior and undo / confirmation where appropriate. See
  [pointer cancellation](https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation).
- Pointer capture, a press-and-hold timer or a drag remains active after a
  modal, focus loss, resize or cancelled touch. Clear temporary state on
  every supported cancellation path; do not convert cancellation to release.
- Stylus pressure / tilt / hover is assumed to exist on all devices. Detect
  capabilities, preserve ordinary touch / mouse operation, and handle palm
  rejection. On Android, handle `ACTION_CANCEL` and, on API 33+, relevant
  `FLAG_CANCELED` pointer-up events; roll back cancelled strokes. See
  [Android palm rejection](https://developer.android.com/develop/adaptive-apps/cookbook/stylus-palm-rejection).
- Voice Control, Switch Control / Switch Access or dwell input cannot invoke
  an action hidden behind a drag. Expose labelled semantic actions under I5.
  Provide visible feedback when haptics are absent or disabled; capability
  and permission declarations belong to [P1–P3](permissions.md).
- Ordinary focused input is implemented using a global hook. Use local
  event / command APIs; review any genuinely required global monitoring or
  automation privileges separately under [permissions](permissions.md).

**Verify.** Complete gesture-based actions using visible controls, keyboard
and the supported assistive input. Start a drag / press, then cancel it by
moving away, switching windows or opening a modal. Test touch plus stylus
with palm contact on hardware, a mouse without hover-dependent actions,
and operation with haptics disabled; record hardware checks under [X4](testing.md).
