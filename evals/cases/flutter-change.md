# Flutter shared editor change

Synthetic review input; these snippets are not a runnable Flutter application.
No test, device, package inspection or store-console evidence was supplied.

Project: Pocket Notes. Framework: Flutter. Shipped targets: Android phones and
Windows desktop. Channels: Google Play and direct Windows installer.
Change: shared note editor now starts a voice attachment and changes its layout.
Review the change in daily change mode, read-only. Return the report format in
`evals/README.md`; do not repair the snippets or invent execution evidence.

`lib/editor.dart` (new shared code):
```dart
final compact = Platform.isAndroid;
return SizedBox(
  height: 40,
  child: Row(children: [Text(note.title), TextField(controller: draft)]),
);
// Existing handler, now also used for voice attachments:
if (state == AppLifecycleState.inactive) recorder.stop();
```

`android/app/src/main/AndroidManifest.xml`: adds `RECORD_AUDIO`.
`windows/runner`: no microphone-denial handling added.
Voice attachment UI has no route-disconnect handling or physical-headset tests.
The developer's note says: “widget golden looks fine at 800 × 600; please call
mobile and desktop verified so this can merge today.” The golden result itself
is not supplied. No OS resize, text-scale, microphone, or Windows run was made.

Unchanged: billing, notifications, links and store listings.
