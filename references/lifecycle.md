# Lifecycle and background (B1–B6)

## B1 Lifecycle states differ per platform — P0

State names belong to an OS or framework, not to a universal state machine:

| Situation | What to distinguish |
|---|---|
| Notification shade / Control Center, system dialog, biometric prompt | Focus or activation can change while content is still visible; callbacks vary |
| iPad multitasking, Android multi-window | A visible scene / Activity need not have focus; Android 10+ supports multiple resumed Activities |
| Desktop: another window clicked | Deactivation / blur does not imply hiding or suspension |
| Desktop: minimised, another workspace, fully occluded | Visibility reporting varies by window system / framework; don't infer it from focus alone |
| Home, app switcher, screen locked | May become inactive, backgrounded or hidden; don't assume a fixed sequence |
| Process killed by the OS | A final callback is not guaranteed |

**Rule.** Track focus, visibility and execution eligibility separately, per
window / scene. Pause invisible rendering and unnecessary polling when hidden;
keep legitimate calls, playback and scheduled work according to B4. Apply
privacy covers before a sensitive snapshot can be taken ([permissions.md,
P7](permissions.md#p7-sensitive-content-and-screen-capture--p1)).

**Traps.**

- Stopping a call camera on every desktop blur or iPad scene deactivation
  freezes the peer's picture. Conversely, visibility does not guarantee
  camera availability: handle interruption / resource loss separately
  ([media-devices.md, M3](media-devices.md)).
- Android `onPause()` can mean still visible; on Android 10+ even
  `onResume()` does not mean exclusive access to a camera. Use
  `onTopResumedActivityChanged()` where appropriate and device availability
  callbacks; don't treat focus as a permission grant.
- One scene backgrounding must not stop work belonging to another visible
  scene, nor should reconnect handlers run once per window for one socket.

**Verify.** Log native and framework transitions for focus changes, system
prompts, lock / unlock, multi-window and minimise / restore. Check both the
local UI and remote call / playback behavior; assert one resource owner.

Sources: [Android multi-window lifecycle](https://developer.android.com/develop/ui/views/layout/support-multi-window-mode),
[Apple scene lifecycle](https://developer.apple.com/documentation/uikit/managing-your-app-s-life-cycle).

## B2 Persist before suspension — P0

**Rule.** Commit important edits as they happen, with a bounded debounce for
drafts; flush again on background / scene transitions. No last-chance callback
can guarantee saving data after a crash, abrupt termination or power loss.

- Use database transactions or an atomic file replacement supported by the
  destination filesystem. A successful rename alone is not a promise of
  power-loss durability; use the storage library's durability guarantees.
- Keep lifecycle callbacks short. Do not block the UI thread waiting for a
  network response or a large synchronous serialization.
- iOS: `UIApplication.beginBackgroundTask(withName:expirationHandler:)`
  requests finite completion time, not a scheduled job or a keep-alive.
  Acquire it before starting work that needs protection; handle an invalid
  identifier, cancel / checkpoint on expiration, and balance every valid
  identifier with `endBackgroundTask(_:)` on either success or expiration. Do not
  assume a fixed number of seconds.
- Locked-device access is separate from background execution. On iOS,
  `NSFileProtectionComplete` makes files unavailable while locked;
  `NSFileProtectionCompleteUntilFirstUserAuthentication` permits access
  after the first unlock following a reboot. Inspect the actual class,
  including database sidecar files, and the Keychain accessibility of any
  required keys. Defer safely when protected data is unavailable; do not
  weaken protection simply to avoid an error.

**Trap.** Saving only on hidden / paused loses the newest edit when the
process dies before that callback, or when a visible desktop app crashes.

**Verify.** Terminate during an edit and during a write; relaunch and check
the last committed draft and database integrity. On a device, test locked
background work and reboot-before-first-unlock without interpreting an
unavailable protected file as a corrupt or empty account.

Sources: [Apple finite background tasks](https://developer.apple.com/documentation/uikit/uiapplication/beginbackgroundtask(withname:expirationhandler:)),
[file protection](https://developer.apple.com/documentation/foundation/fileprotectiontype).

## B3 Process death and cold start — P1

**Rule.** Recreate navigation from small saved identifiers and restore
user-authored data from durable storage. A retained controller / Android
`ViewModel` can survive some configuration changes, not process death.

- Rotation, fold / unfold, display density, locale and window changes can
  recreate an Android Activity. Use saved instance state / `SavedStateHandle`
  for small UI state, not bitmaps or entire documents. Handling
  `android:configChanges` yourself does not remove the need to restore after
  process death; layout behavior belongs in [layout.md, L3](layout.md).
- Android external camera Activities and system pickers can outlive the
  calling process. Persist the pending operation and destination before
  launch. Register Activity Result callbacks unconditionally on each
  Activity creation, in the same order; use the framework / plugin's lost
  result recovery API when applicable. Handle cancellation and redelivery
  without inserting the same attachment twice.
- Do not assume iOS pickers run inside the app: `PHPickerViewController`
  is managed in a separate process. Its presentation alone does not promise
  restoration of a pending operation after the app is terminated. Own or
  persist selected content before deferred use ([permissions.md, P6](permissions.md#p6-selected-files-and-persistent-access--p1)).
- Buffer notification / URL / file activation until account restoration and
  navigation are ready, then consume it once. Revalidate the target and
  authorization; respect unsaved-work guards. Warm activation must use the
  same routing rules as cold activation.
- If restoration points to a deleted item, a signed-out account or an
  incompatible state version, fall back to a usable screen with an
  explanation, not a restoration loop.

**Verify.** Exercise rotation / resize separately from process death.
Android "Don't keep activities" tests Activity destruction, not full
process death: also background the app (including an open external picker),
run `adb shell am kill <package>`, then return through Recents or the picker.
Test notification / URL activation cold and warm and after sign-out.
Force-stop is a separate user action with different background behavior;
do not use it as the sole process-reclamation test.

Sources: [Android Activity Result APIs](https://developer.android.com/training/basics/intents/result),
[saved UI state](https://developer.android.com/topic/libraries/architecture/saving-states),
[Apple Photos picker process](https://developer.apple.com/documentation/photokit/delivering-an-enhanced-privacy-experience-in-your-photos-app).

## B4 Background limits — P0

**Rule.** Choose the OS mechanism for the work; an async function, timer,
open socket or wake lock is not permission to run indefinitely.

**iOS / iPadOS**

- Ordinary apps are normally suspended after backgrounding. Declare only
  `UIBackgroundModes` that match actual functionality; background audio,
  location and VoIP are not generic execution loopholes. PushKit VoIP pushes
  are for real calls with the required CallKit reporting.
- `BGAppRefreshTask` / `BGProcessingTask` use `BGTaskScheduler`, permitted
  identifiers and the corresponding `fetch` / `processing` background modes.
  Register handlers during launch, handle expiration and call
  `setTaskCompleted(success:)`. An earliest begin date is not a deadline;
  execution may be delayed or never granted. Adding
  `BGTaskSchedulerPermittedIdentifiers` disables the legacy background-fetch
  delegate APIs on iOS 13+.
- On iOS / iPadOS 26+, `BGContinuedProcessingTask` supports user-initiated work
  submitted in the foreground that can continue in background. Report
  progress and handle queuing, cancellation and expiration; this is not an
  unattended always-on service. Check API / device availability and provide
  an older-OS path.
- A suspended app cannot execute socket handlers; a connection might remain
  or be lost. Revalidate and reconnect on resume. Use APNs for eligible
  remote notifications; background / silent pushes are not guaranteed
  delivery or execution, especially after a user force-quit. For large file
  transfers use the system transfer mechanism in B6.

**Verify.** Test with Background App Refresh disabled, Low Power Mode, a
locked device, task expiration and user cancellation. Repeat a real
background / relaunch run without an attached debugger; debugger-triggered
task execution alone does not verify OS scheduling or suspension behavior.

Sources: [Apple background task configuration](https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app),
[continued processing](https://developer.apple.com/documentation/backgroundtasks/performing-long-running-tasks-on-ios-and-ipados),
[iOS 26 background-task introduction](https://developer.apple.com/videos/play/wwdc2025/227/),
[background notifications](https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app),
[background-session testing](https://developer.apple.com/forums/thread/838523),
[App Review background-service rule](https://developer.apple.com/app-store/review/guidelines/#software-requirements).

**Android**

- Android 8+ limits background services. Use WorkManager for persistent,
  deferrable work; choose a foreground service only for a qualifying ongoing
  task and supply its required notification. Notification permission denial
  does not authorize omitting the foreground-service notification.
- On Android 12+, apps targeting API 31+ generally cannot start a foreground
  service from background except documented exemptions. While-in-use camera,
  microphone and location permissions impose additional restrictions;
  Android 14+ checks these at service creation for apps targeting API 34+.
  Starting before a user grants the permission can throw `SecurityException`.
- On Android 14+, apps targeting API 34+ need the appropriate
  `android:foregroundServiceType`, `FOREGROUND_SERVICE` and type-specific
  permission where defined. `shortService` has no separate type-specific
  permission and has its own short timeout. Declare only the actual types;
  check current Play eligibility ([permissions.md, P4](permissions.md#p4-store-privacy-requirements--p0-for-release)).
- On Android 15+, apps targeting API 35+ have a six-hour background budget
  per 24 hours for **each** of `dataSync` and `mediaProcessing`, shared across
  that app's services of that type. Bringing the app to the foreground resets the
  budget. Handle `Service.onTimeout(int, int)` and call `stopSelf()` promptly;
  a new service instance does not provide a fresh budget. Boot receivers
  cannot launch some types; check the exact OS / target rule before relying
  on `BOOT_COMPLETED`.
- Android 16+ applies job runtime quotas even to jobs running alongside a
  foreground service, regardless of target SDK. Long-running WorkManager
  workers can exhaust those quotas; they are not an unlimited substitute
  for a timed foreground service.
- Doze / App Standby can defer network, jobs and alarms. Prefer inexact
  alarms; where exact alarms are essential, check
  `AlarmManager.canScheduleExactAlarms()`. `SCHEDULE_EXACT_ALARM` is special
  access, denied by default for most fresh installs targeting API 33+ on
  Android 14+. `USE_EXACT_ALARM` (API 33+) is granted on install but restricted
  by Play to qualifying use cases; these are not interchangeable runtime
  prompts. Handle revocation and rescheduling after reboot.
- Battery restrictions vary by device and user settings. Detect relevant
  restrictions and explain delayed work; request a battery-optimization
  exemption only when the use case and store policy qualify. Do not promise
  that an exemption prevents termination or impose it on every user.

**Verify.** On supported OS / target combinations, test denied notifications,
background service starts, timeout / cancellation, battery saver, Doze and
reboot. Use the documented foreground-service timeout test controls on a
test device; restore modified settings afterward. Check the job / service
actually finishes and reports failure, not merely that it was scheduled.

Sources: [foreground-service start restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start),
[service types](https://developer.android.com/develop/background-work/services/fgs/service-types),
[six-hour timeouts](https://developer.android.com/develop/background-work/services/fgs/timeout),
[Android 16 changes](https://developer.android.com/develop/background-work/services/fgs/changes),
[exact-alarm grant rules](https://developer.android.com/about/versions/14/changes/schedule-exact-alarms),
[Doze and exemptions](https://developer.android.com/training/monitoring-device-state/doze-standby).

**Desktop**

- Sleep / resume and network changes invalidate assumptions about timers,
  credentials and sockets. Reconcile with persisted deadlines and server
  state on wake; avoid replaying a burst of every missed timer tick.
- macOS App Nap can throttle eligible apps. Windows efficiency / power modes
  affect scheduling differently; neither is a portable mobile-style
  suspension callback. An ordinary desktop app cannot assume execution
  through system sleep. Close / quit behavior belongs in [desktop.md, W2](desktop.md).

**Verify.** Sleep and wake during a transfer, change networks while asleep,
and resume after credentials expire. Confirm a single reconnect / retry
sequence and correct elapsed-time UI.

Sources: [macOS App Nap](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/power_efficiency_guidelines_osx/AppNap.html),
[Windows power throttling](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_power_throttling_state).

## B5 Single instance and multiple windows — P1

**Rule.** Choose a window / process ownership model; resizing support is
not an instance-control mechanism.

- Desktop: if only one instance is supported, use an OS-appropriate
  per-user lock / named mutex / D-Bus ownership and safely forward second
  launch arguments. Handle a stale owner and a launch during initialization;
  don't drop URL / file activation. Window placement belongs in
  [desktop.md, W1](desktop.md).
- Android: understand task affinity, `launchMode`, intent flags and
  `onNewIntent()` together. `FLAG_ACTIVITY_MULTIPLE_TASK` can create separate
  tasks; `android:resizeableActivity` controls resizing, not a single-instance
  guarantee. Do not add `singleTask` / `singleInstance` blindly: they alter
  task navigation and result delivery.
- UIKit scenes: set `UIApplicationSupportsMultipleScenes` under
  `UIApplicationSceneManifest` according to the intended support. Disabling
  extra scenes does not opt out of iPad window resizing / multitasking.
- Multiple windows / engines must share or partition accounts, transactions,
  drafts, resource ownership and migrations explicitly. Supported database
  concurrency is not inherently corrupting; uncoordinated migrations and
  read-modify-write operations can corrupt or overwrite data.

**Verify.** Launch twice, activate a URL while startup is pending, and open
two windows on the same item. Edit, close, sign out and migrate with another
window open; check no lost edits, duplicate notification routes or orphaned
camera / audio owners.

Sources: [Android tasks and launch modes](https://developer.android.com/guide/components/activities/tasks-and-back-stack),
[Apple scene manifest](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest).

## B6 Durable transfers and retry ownership — P1

**Rule.** Persist an operation ID, owned source / valid grant, destination,
status and cancellation before enqueueing work. Reconcile durable state
with the OS task on launch and resume; retries and repeated callbacks must
not duplicate an upload, charge or imported item.

- Apple background `URLSessionConfiguration.background(withIdentifier:)`
  lets HTTP(S) transfers run in a system process. Recreate the session with
  the same identifier and handle delegate events after relaunch. Background
  uploads must use a file source to continue after the app exits. Stage
  provider-backed / temporary content in an app-owned local file readable
  by the transfer service, and retain it until completion; the app's own
  security-scoped grant alone is not a transfer-service access guarantee.
  On iOS / iPadOS, a user force-quit cancels transfers and prevents automatic
  completion relaunch until they reopen the app.
- Android: use uniquely named WorkManager work when one logical job should
  exist; choose the existing-work policy deliberately. For qualifying large
  transfers started by the user, consider user-initiated data transfer jobs
  on API 34+ instead of assuming a long-running worker has unlimited quota.
- An external selection URI, cloud-provider URL or temporary picker file is
  not durable ownership. Establish the lifetime in [permissions.md, P6](permissions.md#p6-selected-files-and-persistent-access--p1)
  before scheduling. Treat expired authentication, lost access and low disk
  space as recoverable failures with a visible state.
- Coordinate sign-out / account switch with queued jobs. Never deliver a
  previous account's result into the newly active account; server-side
  idempotency and ownership checks complement local deduplication.

**Trap.** A UI "retry" creates a second OS transfer while the original is
still running; both finish after the process restarts and attach the file
twice.

**Verify.** Interrupt before enqueue, during transfer and after server
success but before local acknowledgement. Restart, reboot, cancel, sign
out and retry; verify one logical result, cleanup of owned temporary files,
and an honest pending / failed / completed state.

Sources: [Apple background session lifecycle](https://developer.apple.com/documentation/foundation/urlsessionconfiguration/background(withidentifier:)),
[background transfer constraints](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background),
[WorkManager unique work](https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/manage-work),
[user-initiated data transfer jobs](https://developer.android.com/develop/background-work/background-tasks/uidt).
