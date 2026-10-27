# cross-platform-app-checklist

[English](README.md)

用于支持 `SKILL.md` 的 agent 的跨平台应用检查技能，覆盖 iOS、iPadOS、
Android、macOS、Windows、Linux 的窗口尺寸与断点、DPI、旋转／分屏／折叠、
安全区与键盘、大字体、输入、权限、生命周期、后台、媒体与设备能力。
同时检查所选应用／软件商店的发布准备：主体与包身份、隐私与内容声明、
商店素材与审核入口、签名产物、测试轨道、发布控制和安全升级。

规则来自实际跨平台应用缺陷，每项包含要求、常见失败和验证方法。
平台事实不限于 Flutter；Flutter API 与插件注意事项单独维护。

## 项目结构

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 精简入口：两种模式、按需加载、证据及输出契约 |
| [完整清单](references/checklist.md) | 发布审查使用，保留全部 65 个稳定 ID |
| [layout](references/layout.md)、[display](references/display.md) | L1–L8 布局与屏幕；D1–D7 字体、密度、资源、主题、动效 |
| [input](references/input.md) | I1–I9 触摸、指针、键盘、无障碍、系统格式、链接和跨应用内容 |
| [lifecycle](references/lifecycle.md) | B1–B8 生命周期、持久化、进程死亡、后台、实例、任务、迁移、同步 |
| [permissions](references/permissions.md) | P1–P9 权限、隐私、备份、文件访问、捕获、支付、商店功能规则 |
| [media-devices](references/media-devices.md) | M1–M8 音频、路由、摄像头、格式、内存、通知、可选硬件、屏幕采集 |
| [desktop](references/desktop.md) | W1–W4 窗口、关闭／退出／托盘、文件系统、打包与 Apple 兼容分发 |
| [performance](references/performance.md) | F1–F3 帧节奏、包体与启动、能耗与温控 |
| [testing](references/testing.md) | X1–X9 设备矩阵、布局扫描、状态恢复、对等检查、正式产物、网络、诊断 |
| [flutter](references/flutter.md) | 对应 Flutter API、插件和验证注意事项 |
| [sources](references/sources.md) | 官方来源、版本／商店规则日期、商店来源索引、相关项目 |
| [商店发布指南](references/stores.zh-CN.md)／[English](references/stores.md) | 在 P4／P8／P9／W4／X6 下细化不同渠道的提审与发布证据 |
| [tools/check_skill.py](tools/check_skill.py) | frontmatter、ID、项目 Markdown 链接／锚点、行尾和基础泄漏检查 |
| [tools/test_check_skill.py](tools/test_check_skill.py) | 临时副本中的校验器正例、断链和锚点负例 |
| [evals](evals/README.md) | 复现案例、边界探针、报告契约、手写样例及独立 agent 记录 |
| [ClawHub 发布](docs/CLAWHUB.md)／[来源核查](docs/PROVENANCE.md) | 发布流程及 MIT-0 许可核查 |
| [CHANGELOG](CHANGELOG.md)／[VERSION](VERSION) | 版本元数据与发布记录（当前：0.1.1） |

## 安装

克隆项目并链接到 agent 的技能目录，例如读取 `~/.agents/skills` 的工具：

```bash
git clone https://github.com/agentx-icu/cross-platform-app-checklist.git
mkdir -p ~/.agents/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.agents/skills/cross-platform-app-checklist
```

可在项目 `AGENTS.md` 中约定：

> 日常 UI／平台变更使用 `cross-platform-app-checklist` 的 change 模式，
> 发布前使用 release 模式。默认只读；记录范围、ID、平台、证据、真机计划和阻塞。

## 使用与渠道范围

默认**只读审查**。输入明确项目／路径及 revision、变更 diff 或发布候选、
框架、目标平台／形态、渠道／包模型／地区；能从文件推断则先检查，未知项明确标注。
共享代码到达的其他平台也纳入范围，X1 检查商店默认可达形态。

- **change（日常变更）**：仅展开受影响领域及关联风险；考虑 X1／X4／X5，
  产物／分发变化另纳入 X6。报告所选 ID、排除领域及范围理由；不输出全部
  65 行，也不把未审领域写成 N/A。
- **release（完整发布）**：读取 [完整清单](references/checklist.md)，对每个
  实际分发平台覆盖全部 65 个 ID；按领域和所选渠道逐步加载详细参考。

输出先列范围与假设，再按优先级列 `ID／平台／状态／证据或缺口／下一步`，
并单列**真机计划**、**发布阻塞**及未验证限制。状态为 verified、to do、
needs device 或附理由的 not applicable。部分通过须拆分已证实与待验证案例。
记录构建、OS、逻辑尺寸、缩放、语言等；源码、正式产物、运行、真机及商店批准
互不替代。使用技能不自动授权修改、签名、上传、收集秘密或接受平台条款。

调用示例（项目、版本请替换为真实值）：
```text
使用 $cross-platform-app-checklist，change 模式，只读检查 ./app 的 base..HEAD。
Flutter；Android 手机 + Windows；Google Play + 站外安装器。
审查共享编辑器／麦克风变更，列范围、优先级问题、证据、真机计划和阻塞。

使用 $cross-platform-app-checklist，change 模式，检查 ./ledger 的 base..HEAD。
Electron；Windows + Linux；MSI + Flathub。检查持久化和退出流程。

使用 $cross-platform-app-checklist，release 模式，检查 ./app 的 RC1。
Flutter；Android + Windows；Google Play + Microsoft Store，美国。
逐平台覆盖全部 65 个 ID，区分缺失证据和实际验证。
```

参见 [三个复现案例与评测边界](evals/README.md)、[版本变更](CHANGELOG.md)
及 [ClawHub 发布文档](docs/CLAWHUB.md)。已公开版本见
[ClawHub](https://clawhub.ai/agentx-icu/skills/cross-platform-app-checklist)。使用当前
ClawHub CLI 执行 `clawhub install @agentx-icu/cross-platform-app-checklist` 可安装
最新公开版本；添加 `--version` 可选择已有版本。也可继续 Git 克隆／链接，
Codex 用户可链接到 `~/.codex/skills`。

提审、更新或分发变更时读取 [商店发布指南](references/stores.zh-CN.md)，
按“渠道／包模型 × 国家地区 × 应用类型”选择适用路径。覆盖 App Store
（iOS／iPadOS／macOS）、Google Play、Microsoft Store、Flathub、Snap Store；
国内 Android 选取华为、小米、OPPO 作为代表；WinGet、Homebrew Cask、F-Droid、
站外下载／发行版仓库仅在实际选择时适用。**保留既有 65 个 ID**，不再制造
一套独立编号；证据汇入 P4、P8、P9、W4、X6。

指南将强制、条件强制、建议与验证状态分开。公开来源核验日期为
**2026-10-22**，发布时必须重读动态政策和后台。有些厂商公开页面只能读取
索引摘要，详细规则明确交由账号负责人核验。后台检查、真机测试、实际审核
结论是不同证据；准备清单不额外授权外部发布，也不代表任何商店已接受应用。

发布证据须绑定最终已审 head、实际 job／step 结果、执行用例、条件跳过及
最终制品 hash（X6）。references 补充二进制与符号配对、诊断隐私（X9）、
可见编辑检查点（B2）、运行中动画偏好（D7）、原生命令的过期归属（I2）、
粘贴分发（I3）、文件系统机制（W3）、有界 UI 轮询及准确体积指标（F2–F3）。
这些改进深化原有 ID；项目专属预算与实现仍由项目决定。剩余代码缺陷、产品
决策、负责人材料与设备验证分别记录，报告不收集秘密值。

## 贡献规则

仅在实际缺陷暴露缺口时增加规则，写清防止的失败及验证方法。能由原有要求
覆盖时深化既有条目；新增 ID 必须在完整清单与对应 reference 中一致，
不能改变既有稳定 ID；确需新增时主动同步校验器的稳定 ID 集。
中英文项目文档和商店指南同步维护，来源索引保持可发现。

商店规则使用官方直链，标注日期、准确渠道／地区／触发条件、要求等级和
可观察证据。不把费用、SDK 截止日期或某一家商店的要求写成通用固定常量。

## 验证

在所用 Python 环境安装 PyYAML，然后执行：

```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
python3 tools/evaluate_review.py --examples
git diff --check
```

[CI](.github/workflows/check.yml) 在 push 和 pull request 上运行校验器回归与
一致性检查，覆盖 frontmatter、ID 对应、项目 Markdown 的本地
链接／标题锚点、换行和选定泄漏模式，以及完整 ID 集、版本与许可元数据。
CI 也重新评分已保存的合成场景 agent 报告，不启动新 agent。负例证明中文 README 断链和中文
reference 错误锚点会被拒绝。这些检查不验证远程政策时效、agent 遵守情况、
应用二进制或真实商店提审；后者按 [发布证据模板](references/stores.zh-CN.md#报告记录)
单独记录。

原生发布还需按 [X6](references/testing.md#x6-packaged-release-verification--p0-for-release)
检查最终 app／engine／plugin 的二进制架构清单，分开记录 host CPU、工具
进程 ABI、目标和包标签；另核对安装器／包元数据与商店目标，并保留目标机器
加载／smoke 测试证据。本仓库 CI 不提供应用架构或真机验证结论。

## 许可证

MIT-0（MIT No Attribution），见 [LICENSE](LICENSE) 和
[许可来源核查](docs/PROVENANCE.md)。外链作品保留自身许可证，本次不重授外部作品，
也不改写历史快照已经授予的许可。
