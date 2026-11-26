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

明确支持哪些历史版本。盘点已经给测试者或用户使用的 TestFlight、测试轨道和站外包。如果其中存在受支持的同渠道升级或显式导入路径，就用真实旧产物生成测试数据。没有前序包时，从正式候选版生成有内容的基线，留存候选安装包、合成档案和数据版本。可用同一交付方式的递增测试构建验证覆盖安装，同时给实际跨版本迁移留待验证状态。对用户承诺支持的旧版本和备份格式，保留能重复使用的脱敏或合成样本。

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

## 最小验收矩阵

在各适用平台和交付路径上，用有内容的旧版档案测试迁移。样本包含能观察归属、引用和状态的不同数据，例如两个身份、历史和草稿、已读与未读消息、待发与失败项、带附件或录音的记录、非默认设置。覆盖文件较多或存储较慢的场景。进程强杀与设备断电各自记录验证结果。

| 场景 | 验收断言 |
|---|---|
| 全新安装后断网启动 | 核心离线能力和本地设置可用。网络和权限失败有清晰提示或替代路径。 |
| 上一支持版本、最早支持版本及各独立迁移入口覆盖升级 | 通过实际安装路径安装，首次启动和第二次冷启动后，身份、关键业务内容、引用和待处理状态符合预期。对其余受支持版本运行有内容的迁移样本。 |
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
