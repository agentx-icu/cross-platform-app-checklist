# 首发技术发布门禁与数据可靠性

[English](release-reliability.md)

适用于首次公开发布、后续升级，以及会改变存储格式、数据目录、凭据或原生后端的发布。首发要验证当前产物，也要留下一份将来可实际升级的数据基线。按实际分发的 OS、架构、渠道和包形态执行。每一项沿用现有清单 ID，提交和渠道规则见[商店发布指南](stores.zh-CN.md)。

## 首发前确定数据契约

为每个持久化存储记录归属（全局、账号、访客或设备）、权威来源、目录和键名、格式版本、写入成功条件、保留／删除规则，以及备份和换机政策。把身份私钥、离线自建内容、发送队列和引用的媒体当作独立检查对象。说明什么情况下用户会丢失尚未提交的编辑。

| 数据类型 | 需要确定的行为 |
|---|---|
| 身份和凭据 | 稳定的本地身份标识、加密资料、账号指针与密钥引用。区分设备绑定凭据、可移植身份、服务端会话，以及退出、删除、改密和换机的行为。 |
| 用户内容和在途操作 | 明确历史、草稿、附件、训练、录音、待发和失败队列的保留范围。给引用和操作稳定 ID，约定升级、恢复、清除和重试的行为。 |
| 偏好、缓存和临时状态 | 标明哪些偏好随账号或设备，哪些缓存可以重建。用户创作的数据、引用中的文件和待提交操作要放在持久化位置。 |

明确支持哪些历史版本。盘点已经给测试者或用户使用的 TestFlight、测试轨道和站外包。对受支持的升级或导入路径，用真实旧产物生成测试数据。首次发布若没有受支持的前序版本，把历史覆盖升级标为不适用并记录原因。执行全新安装、有内容的档案冷启动，以及产品支持的同版本恢复。留存候选安装包、有内容的合成档案和数据格式版本，供下次发布做升级基线。可用同一交付方式的递增测试构建验证覆盖安装过程，等有受支持的跨版本路径时再验收迁移。对受支持的版本和备份格式，保留可复用的脱敏或合成样本。

分别约定新版读取旧数据、旧版处理新数据、旧备份导入和新旧客户端互通的预期行为，并设计独立的验收用例。升级后需要保留的偏好键、密钥引用和业务标识也纳入兼容范围。

## 技术放行门禁

| 检查项 | 发布要保证的结果 | 清单 ID |
|---|---|---|
| 离线冷启动和解锁 | 已保存的本地数据在断网、重启后仍可读取和编辑。按产品的认证策略解锁本地身份。凭据暂不可用时显示锁定或重试，密钥丢失时进入已定义的恢复或重新认证流程。 | [B3](lifecycle.md#b3-process-death-and-cold-start--p1)、[P5](permissions.md#p5-data-at-rest-and-backup--p1) |
| 账号隔离与密钥生命周期 | 用稳定身份隔离私钥、历史、队列、媒体和账号偏好。切换、退出、删除、改密及导入失败后，当前账号与实际目录一致。旧会话和定时器失去写权限。设备凭据放入系统安全存储或用系统保护的密钥加密。 | [B5](lifecycle.md#b5-single-instance-and-multiple-windows--p1)、[P5](permissions.md#p5-data-at-rest-and-backup--p1) |
| 写入与进程中断 | 用户看到保存成功时，数据已按定义提交且重启可读。后台和正常退出前刷新关键写入，同时在使用期间做检查点。覆盖磁盘不足、只读目录、写入错误和强杀。事务或文件替换后验证旧版或新版完整可读，记录仍在保存窗口内的数据损失界限。 | [B2](lifecycle.md#b2-persist-before-suspension--p0)、[X7](testing.md#x7-interrupted-flows-and-access-changes--p0-for-stateful--permissioned-flows) |
| 旧数据与跳版本升级 | 为数据库、文件布局、偏好键、凭据和备份格式提供版本及迁移策略。先校验源，再用单写入者、事务或可恢复日志提交数据和版本，验证新数据后才清理旧数据。重复启动或重试结果一致。升级后核对业务数据、归属和文件引用。 | [B7](lifecycle.md#b7-local-data-migrations--p0) |
| 新格式与故障恢复 | 旧客户端遇到更新、未知的格式时保留原件并提示升级，或按已验证的兼容模式工作。主档、恢复副本、合并和延迟写入都检查版本。迁移失败、数据损坏、权限受限和凭据缺失分别处理，保留可恢复数据。 | [B7](lifecycle.md#b7-local-data-migrations--p0)、[X7](testing.md#x7-interrupted-flows-and-access-changes--p0-for-stateful--permissioned-flows) |
| 备份、导入与换机 | 分别验证应用内导出、系统云备份、设备到设备迁移和重装。备份范围明确到身份、历史、队列、媒体、偏好和密钥。包含多个存储时取一致快照。导入前校验格式、完整性、大小及路径，暂存后再提交。测试错误密码、截断、篡改、磁盘不足和部分恢复。恢复失败后原数据仍可打开。 | [P5](permissions.md#p5-data-at-rest-and-backup--p1)、[B7](lifecycle.md#b7-local-data-migrations--p0) |
| 断网和投递可靠性 | 对联网应用，重启后恢复待发任务。重试沿用操作 ID，接收端在协议支持时去重，区分排队、发送、送达和已读。恢复旧备份后验证过期操作、重复发送和冲突处理。用真实对端测试弱网、断网、网络切换、引导节点或后端不可用，以及新旧客户端互通。 | [B6](lifecycle.md#b6-durable-transfers-and-retry-ownership--p1)、[B8](lifecycle.md#b8-offline-state-and-sync-conflicts--p1)、[X8](testing.md#x8-network-environments--p1-for-networked-apps) |
| 最终产物运行与降级体验 | 从实际分发包安装，以普通用户运行。按支持矩阵覆盖最低支持 OS 和当前稳定 OS，核对 app、运行时、插件和原生库的实际加载。覆盖安装后检查数据目录、凭据和首次启动路径。对已发布的核心能力实测授权和拒绝后的行为，记录冷启动、迁移耗时和临时磁盘空间。 | [X1](testing.md#x1-device-matrix--p0)、[X6](testing.md#x6-packaged-release-verification--p0-for-release)、[P3](permissions.md#p3-degraded-paths--p1)、[F2](performance.md#f2-app-size-and-startup-budgets--p1) |
| 故障诊断和止损 | 留存最终产物哈希、构建号和对应符号。诊断记录保留迁移版本、失败阶段和错误类别，并排除密钥、口令、消息和录音内容。发布前定好暂停条件和向前修复路径。停止分发后，已安装用户仍需要可读的数据或新版修复。只有旧二进制和数据降级都验证过，才提供二进制回退。 | [X6](testing.md#x6-packaged-release-verification--p0-for-release)、[X9](testing.md#x9-production-diagnostics--p1-for-released-apps) |

使用 SQLite 时，通过 Online Backup API 或其他受支持方式生成一致快照。WAL 中可能还有已提交数据，需按 SQLite 规则处理。Android 云备份与设备直传分开配置和验证。Apple 的设备绑定 Keychain 项在换机后可能缺失，测试密文与密钥是否同时可用。 [SQLite Backup API](https://www.sqlite.org/backup.html)、[SQLite WAL](https://www.sqlite.org/wal.html)、[Android Auto Backup](https://developer.android.com/identity/data/autobackup)、[Apple Keychain 可访问性](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility)

## 首发故障场景

通过产品实际入口执行适用用例，在存储或传输边界注入故障。涉及重启的场景用新进程观察。

| 场景 | 验收断言 |
|---|---|
| 主档暂时不可读（[B2](lifecycle.md#b2-persist-before-suspension--p0)、[B7](lifecycle.md#b7-local-data-migrations--p0)） | 保留可读的旧恢复副本，注入主档访问拒绝或 I/O 错误。两份数据均保持原样，提示可重试，阻止旧副本或空状态写回。恢复访问后读出当前数据。主档缺失、损坏和格式不受支持分别按对应策略复验。 |
| 保存或正常退出时提交失败（[B2](lifecycle.md#b2-persist-before-suspension--p0)、[X7](testing.md#x7-interrupted-flows-and-access-changes--p0-for-stateful--permissioned-flows)） | 在保存、登出、切换账号或关闭时注入写失败。保留未提交内容供用户重试，提交成功后再显示已保存或已生效。网络发送和本地历史写入可独立失败时，各自记录结果。关键写入完成前保留原账号指针。导入涉及文件和关联记录时，在第一处替换后注入失败，确认原文件、引用和选区仍一致。 |
| 删除身份或访客数据中断（[B5](lifecycle.md#b5-single-instance-and-multiple-windows--p1)、[B7](lifecycle.md#b7-local-data-migrations--p0)） | 明确删除何时生效。分别在生效前、旧数据已隔离但尚未清理时终止进程。新进程继续清理，旧写入任务和恢复副本无法带回已删除的数据，新身份或其他账号只看到自己的数据。重置偏好后强制读取恢复副本，确认已清除的设置不会复活。启动时分别验证存储锁不可访问和确有运行中的实例，锁不可访问时提供可重试的恢复入口。 |
| 同版本仅恢复了部分数据（[P5](permissions.md#p5-data-at-rest-and-backup--p1)、[B7](lifecycle.md#b7-local-data-migrations--p0)） | 恢复账号记录、历史、偏好和待发队列，令身份文件或设备绑定密钥缺失。按产品恢复策略保留已有数据。若可用可移植身份修复，验证完整稳定身份并认证来源。匹配的导入仅补回缺失材料，保留数据和本地账号保护。覆盖身份不匹配、口令错误、已有可用身份，以及写入偏好或恢复副本失败。恢复带回的队列暂停自动发送，待用户检查或明确授权。 |
| 取消发送或投递结果不确定（[B6](lifecycle.md#b6-durable-transfers-and-retry-ownership--p1)、[B8](lifecycle.md#b8-offline-state-and-sync-conflicts--p1)） | 原生层受理请求或报告进度时，任务仍处于待完成状态，并保留已持有的源文件。单条删除或清空成功前先持久化取消。分别在确认到达前、对端已完成但本地未持久化结果时重启，并注入上一轮回调。已提交的取消保持生效，完成事件只影响对应尝试。若承诺最多投递一次，只在确定上次未生效或接收端能去重时自动重试。结果不确定的非幂等操作保留为待确认，产品明确允许重投时按其约定处理，并记录和复验重投边界及界面状态。 |
| 首用授权、备份和播放（[P5](permissions.md#p5-data-at-rest-and-backup--p1)、[M1](media-devices.md#m1-audio-session-and-focus--p0-for-apps-that-play-or-record)） | 适用时，在身份资料写入后、账号记录提交前中断创建，重开后应恢复完整可分享的身份。在必需的备份引导完成前重开，在必需的授权前触发重连，确认各自的门禁仍生效。系统分享结果未知时，备份完成状态仍待确认。判分或进度依赖听音时，注入播放启动或输出失败，确认进度保持原状、可重试，收到对应播放完成事件后再继续。 |

iOS 备份策略规定排除某类文件时，在写入敏感数据前先标记目标目录或专用暂存目录。注入设置排除失败，确认待排除数据未落入可备份位置。替换后复查标记，并执行真实的系统备份和恢复。大文件导出和暂存要测峰值内存、临时磁盘用量。中断导入或取消传输后，核对无引用副本得到回收、仍被引用的媒体可读。 [Apple 备份排除](https://developer.apple.com/documentation/foundation/optimizing-your-app-s-data-for-icloud-backup)

## 发布草稿与渠道产物

- **发布草稿。** 渠道支持暂存时，把候选版本、标签解析出的提交、必需产物清单及哈希绑定到已审查的源码。记录远端草稿 ID。GitHub Releases 要用支持草稿的鉴权查询解析草稿，再用数字 release ID 获取元数据和核对产物。REST 按标签查询的接口面向已发布的 Release。复验上传中断后重试、缺少必需产物、意外产物或哈希不匹配、标签或提交不匹配，以及草稿已变为公开等情况。仅对匹配的草稿和产物重试。清单及检查全通过后才公开，暂存过程保留已发布的 Release 原状。 [GitHub Releases API](https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name)、[产物 API](https://docs.github.com/en/rest/releases/assets#list-release-assets)
- **Android 原生交付。** 适用 16 KB 兼容要求时，检查每个随包交付的原生库的 ELF 对齐，覆盖压缩库和未压缩库。检查直接下载和由分发渠道生成的 APK 中未压缩库的 ZIP 对齐。AAB 使用未压缩库时，用版本固定的 `bundletool` 检查实际 AAB，要求 `PAGE_ALIGNMENT_16K`。记录工具版本、AAB 哈希，以及 16 KB 样本通过、4 KB 样本拒绝的结果。两种打包方式均从目标渠道安装到 16 KB 系统，通过 Play 分发时走目标测试轨道。记录实测页大小，在系统允许时关闭兼容回退，并实际调用原生功能。 [Android 16 KB 验证](https://developer.android.com/guide/practices/page-sizes)

分别留存源码回归、模拟故障或对端、CI 平台实际执行和渠道交付包运行的证据。真实双端传输、Apple 系统恢复、实体音频及其他依赖硬件的适用场景，完成实测后再关闭验收项。 [X6](testing.md#x6-packaged-release-verification--p0-for-release)、[X7](testing.md#x7-interrupted-flows-and-access-changes--p0-for-stateful--permissioned-flows)、[X8](testing.md#x8-network-environments--p1-for-networked-apps)

## 最小验收矩阵

在各适用平台和交付路径上使用有内容的档案。有受支持的升级路径时，用旧版生成档案。样本包含能观察归属、引用和状态的不同数据，例如两个身份、历史和草稿、已读与未读消息、待发与失败项、带附件或录音的记录、非默认设置。覆盖文件较多或存储较慢的场景。进程强杀与设备断电各自记录验证结果。

| 场景 | 验收断言 |
|---|---|
| 全新安装后断网启动 | 核心离线能力和本地设置可用。网络和权限失败有清晰提示或替代路径。 |
| 有受支持的前序版本时覆盖升级 | 覆盖上一支持版本、最早支持版本和各独立迁移入口。通过实际安装路径安装，首次启动和第二次冷启动后，核对身份、关键业务内容、引用和待处理状态。对其余受支持版本运行有内容的迁移样本。 |
| 迁移中断后恢复 | 分别在提交前、跨存储提交点和提交后清理前注入失败或终止进程。重开能继续或回滚，重复启动没有重复记录，不丢失已提交数据。 |
| 新版数据由旧版打开 | 用新版主档＋旧副本、损坏或缺失的主档＋新版副本测试。启动、直接写入和延迟保存均保留未支持格式的字节。 |
| 从备份恢复或换机 | 用干净环境导入和重开，检查身份、内容、媒体引用及待发项的处理符合声明。用错误口令、绑定密钥缺失和损坏备份检查原环境仍可恢复。 |
| 关机、登出、切换和删除 | 重启后已提交且应保留的内容仍可读。按产品定义清除的数据不会被旧任务、恢复日志或缓存带回，其他账号数据可用。 |
| 卸载重装和系统备份恢复 | 按产品承诺检查本地数据、系统恢复内容、残留凭据和登录状态。新安装进入正确的初始状态，恢复后的数据归属正确。 |
| 离线积压后重连 | 用两个真实对端验证单聊或群聊、取消、重试、重复回执和网络切换，检查投递状态与协议保证一致。 |

每个结果绑定 **源码 revision、产物版本与哈希（涉及升级时记录两个产物）、实际交付路径、系统和设备、样本与数据格式版本、执行步骤、预期和实际断言、相关日志**。覆盖升级、卸载重装、跨渠道迁移、同版本修复和系统备份恢复各自记录。核心路径出现身份丢失、已提交内容丢失、账号串数据、凭据泄漏、恢复引发未授权发送或启动无法恢复时，阻止对应发布。尚无实际验收证据的适用项保留 `to do` 或 `needs device`。 [X6 发布产物证据](testing.md#x6-packaged-release-verification--p0-for-release)

## 案例

| 应用 | 应当随包验收的业务数据和风险 |
|---|---|
| toxee | 用有密码和无密码的账号、两个独立账号、旧目录及 `.tox` 导入样本，核对升级后的同一 Tox 公钥、联系人、聊天、未发／失败消息和头像。分别验收到达应用目录的接收文件，以及承诺纳入完整备份的数据。改密或恢复中断后验证原账号仍可用，测试备份里的队列是否会按产品定义重发。 [账号与会话](https://github.com/agentx-icu/toxee/blob/007b2e189a9642e045ca65e211dabfddf40eb5fa/doc/reference/ACCOUNT_AND_SESSION.zh-CN.md) |
| DitMesh | 用真实对端核对身份、好友和群组、文字和可选拍发节奏、待发状态、练习及其录音。分别验收原地升级时保留可重试队列，以及加密备份恢复后待发内容按审计描述仅供查看、不会自动发送。重点注入跨文件和安全存储的替换失败，并检查 Linux keyring 不可用时的行为。 [持久化审计](https://github.com/agentx-icu/ditmesh/blob/4dfe6f6aadc877a699fa2cdb2a8c100f864c91e2/doc/testing/PERSISTENCE_AUDIT.zh-CN.md) |
| MorseCQ | 对无账号的学习档案核对课程、错题、复习计划、通联草稿、设置及录音和索引关系。验证旧版遇到新版格式时保留数据，以及清除学习后检查点不会写回。架构记录中的可移植备份仅有存储层，且范围不含录音。若发布时承诺换机保留，要验收用户实际可用的恢复路径及其录音覆盖。 [本地学习架构](https://github.com/agentx-icu/morsecq/blob/c3805e94ae3bff0ecfb2e50fa379592c0bca7296/doc/architecture/OFFLINE_LEARNING.zh-CN.md)、[持久化审计](https://github.com/agentx-icu/morsecq/blob/fad7bd7563f90e91d6dd015aaf843f7f71f4bd44/doc/testing/PERSISTENCE_AUDIT.zh-CN.md) |
