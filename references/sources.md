# Sources, version gates and related projects

The checklist IDs are this skill's own; this file maps them to the official
guidelines they align with, lists dated platform / store gates, and points
to related projects. Last checked: **2026-10-22**. Dates and thresholds
change: re-check the linked source before relying on one, and record the
date you checked in the evidence (SKILL.md step 6).

## Official guidelines

| Source | Covers | Checklist IDs |
|---|---|---|
| [Android core app quality](https://developer.android.com/docs/quality-guidelines/core-app-quality) | Back navigation, state preservation, runtime permissions, notifications, backup, 48 dp targets, contrast | I1, I4, B2–B3, P2, P5, M6 |
| [Android adaptive app quality tiers](https://developer.android.com/docs/quality-guidelines/large-screens-app-quality) ([tier 3](https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/tier-3)) | Configuration changes and combinations (resize then rotate, rotate then fold), multi-window, multi-resume, camera preview, keyboard / mouse / stylus, reference device sizes | L1–L3, L6, L8, I2, B1, M3, X1, X3 |
| [Android 15 behaviour changes](https://developer.android.com/about/versions/15/behavior-changes-15), [Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16) | Edge-to-edge, `Configuration` sizes incl. system bars, foreground-service limits, large-screen orientation / resizability, predictive back, `elegantTextHeight`, locale code changes | L2, L4, L6, D2, I4, B4 |
| [Android foreground-service changes](https://developer.android.com/develop/background-work/services/fgs/changes) | Service types, permissions, timeouts and start restrictions per version | B4, P1 |
| [Android 16 KB page sizes](https://developer.android.com/guide/practices/page-sizes) | Native library alignment and testing | X6 |
| [Android / Material window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes) | Breakpoints | L2 |
| [Google Play Data safety](https://support.google.com/googleplay/android-developer/answer/10787469), [target API requirements](https://support.google.com/googleplay/android-developer/answer/11926878) | Store privacy declarations, target SDK deadlines | P4 |
| [Apple HIG: layout](https://developer.apple.com/design/human-interface-guidelines/layout), [multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) | Safe areas, size classes, 44 pt targets, resizable windows | L1–L4, I1, I5 |
| [TN3192: migrating from `UIRequiresFullScreen`](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) | iPadOS 26 resizable windows, scene size restrictions | L2, L6 |
| [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) | 2.4.1 iPhone apps on iPad, 2.5.4 background modes only for their purpose, 5.1.1 purpose strings, pickers over full library access, alternatives when consent is denied | L1, B4, P1–P3 |
| [Apple privacy manifest](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), [required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) | `PrivacyInfo.xcprivacy`; file timestamp, system boot time, disk space, active keyboards and `UserDefaults` categories | P4 |
| [Apple upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) | Submission SDK and minimum-target gates | P4, W4 |
| [Windows high-DPI desktop development](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows) | Per-Monitor V2, `WM_DPICHANGED`, mixed-DPI test list | D3–D4, W1 |
| [Windows breakpoints](https://learn.microsoft.com/en-us/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design), [app capability declarations](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations) | Effective-pixel breakpoints and scale plateaus; packaged capabilities, restricted capabilities | L2, D3, P1 |
| [GNOME HIG: adaptive](https://developer.gnome.org/hig/guidelines/adaptive.html), [KDE HIG](https://develop.kde.org/hig/) | Linux minimum sizes, adaptive layouts | L1, W1 |
| [Flatpak sandbox permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html), [Flathub quality guidelines](https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines/quality-guidelines) | Portals over broad filesystem access, Wayland socket with X11 fallback; square SVG or PNG icon ≥ 256 × 256 px, metadata and screenshots | P1, D5, W4 |
| [freedesktop Desktop Entry](https://specifications.freedesktop.org/desktop-entry-spec/latest/) and [Icon Theme](https://specifications.freedesktop.org/icon-theme-spec/latest/) specs | `.desktop` files, MIME / URL handlers, hicolor icons | D5, W4 |
| [Flutter adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive) ([best practices](https://docs.flutter.dev/ui/adaptive-responsive/best-practices)) | Don't lock orientation, don't branch on device type, `MediaQuery.sizeOf` / `LayoutBuilder`, input, capabilities | L1–L3, L6, I2 |
| [Flutter accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility) | Release checklist: targets, contrast, screen readers, large scale factors | D1, D6, I1, I5 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WCAG2Mobile](https://www.w3.org/TR/wcag2mobile-22/) (informative draft guidance) | Contrast, WCAG 2.2 SC 2.5.8 target size (24 × 24 CSS px minimum at AA, subject to its exceptions), orientation, reflow, text resize, motion | D1, D6, D7, I1, I7, L6 |
| [OWASP MASVS](https://mas.owasp.org/MASVS/) (MASVS-STORAGE, MASVS-PRIVACY) | Data at rest, privacy disclosures matching store declarations | P4, P5, P7 |

## Dated gates (checked 2026-10-22)

Confidence: **high** — read on the official page; **medium** — official
page partly unreadable or history inconsistent.

| Gate | Date / threshold | Confidence |
|---|---|---|
| Google Play: new apps and updates must target API 36 (Wear OS / Automotive 35, TV / XR 34) | 2026-08-31, extension to 2026-11-01 on request | high |
| Google Play: updates must support 16 KB memory pages (64-bit native code) | 2027-02-01 for updates per the current page; earlier dates were announced for new apps | medium |
| Android 16, target 36: orientation / resizability / aspect-ratio restrictions ignored on sw ≥ 600 dp; temporary opt-out property | Opt-out removed for target 37 (Android 17); boundary wording differs between pages, see [L6](layout.md) | high (behaviour), medium (boundary) |
| Android 16, target 36: predictive back animations on by default; `onBackPressed` / `KEYCODE_BACK` no longer delivered unless opted out | Target 36 | high |
| Android 15, target 35: edge-to-edge enforced; Android 16 target 36 removes the opt-out attribute | Target 35 / 36 | high |
| Android 15, target 35: `dataSync` / `mediaProcessing` foreground services limited to 6 h per 24 h in background | Target 35 | high |
| Android local network permission | Opt-in testing on 16; enforced for target 37 (see [P1](permissions.md)) | medium |
| App Store Connect uploads for iOS / iPadOS / tvOS / visionOS / watchOS: Xcode 26+ and the respective OS 26+ SDK (macOS not listed) | 2026-04-28 | high |
| iPadOS 26: `UIRequiresFullScreen` deprecated, to be ignored in a future release | iPadOS 26 | high |
| Apple required-reason API declarations | Enforced since 2024-05-01 | high |

## Related projects

| Project | Worth borrowing | Licence |
|---|---|---|
| [flutter/agent-plugins](https://github.com/flutter/agent-plugins) | Flutter team's agent skills (responsive layout, layout fixes, localisation, integration tests); complementary, task-level rather than a compatibility checklist | BSD-3-Clause |
| [OWASP MASVS](https://mas.owasp.org/MASVS/) / [MASTG](https://mas.owasp.org/MASTG/) | Control phrasing and linked privacy tests; the historical checklist spreadsheet was [retired in MASTG v2](https://mas.owasp.org/news/2026/07/14/checklists-removal/) | CC BY 4.0 for current website content; check historical artifacts separately |
| [gskinnerTeam/flutter-adaptive-demo](https://github.com/gskinnerTeam/flutter-adaptive-demo), [Wonderous](https://github.com/gskinnerTeam/flutter-wonderous-app) | Reference adaptive Flutter implementations | see repositories |
| [oisin/app-release-checklist](https://github.com/oisin/app-release-checklist) | Store and localisation pre-release items (dated) | see repository |
| [bbc/bbc-a11y](https://github.com/bbc/bbc-a11y), [BBC Mobile Accessibility Guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/) | Which accessibility checks can be automated | see repository |
