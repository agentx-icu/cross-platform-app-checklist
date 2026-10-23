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
| [SKILL.md](SKILL.md) | 技能入口、适用场景、工作方法及稳定的 65 个清单 ID |
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
| [tools/check_skill.py](tools/check_skill.py) | frontmatter、ID、全部 README／reference 的链接、锚点、行尾和基础泄漏检查 |
| [tools/test_check_skill.py](tools/test_check_skill.py) | 临时副本中的校验器正例、断链和锚点负例 |

## 安装

克隆项目并链接到 agent 的技能目录，例如读取 `~/.agents/skills` 的工具：

```bash
git clone https://github.com/agentx-icu/cross-platform-app-checklist.git
mkdir -p ~/.agents/skills
ln -s "$PWD/cross-platform-app-checklist" ~/.agents/skills/cross-platform-app-checklist
```

可在项目 `AGENTS.md` 中约定：

> UI、生命周期、权限、媒体、打包及商店发布变更使用
> `cross-platform-app-checklist` 检查；在设计记录／PR 中记录
> verified、to do、needs device 或附理由的 not applicable。

## 使用与渠道范围

先明确实际分发的平台和可达形态，再逐项给出状态及证据，适用时读取对应
reference 后再改代码。共享代码到达的其他平台也要检查；只有截图或模拟器
不能证明真实硬件、原生系统能力或商店批准。记录构建、OS、逻辑尺寸、缩放、
语言和相关设置；功能支持状态与实际验证状态分开。

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
覆盖时深化既有条目；新增 ID 必须在 `SKILL.md` 与对应 reference 中一致。
中英文项目文档和商店指南同步维护，来源索引保持可发现。

商店规则使用官方直链，标注日期、准确渠道／地区／触发条件、要求等级和
可观察证据。不把费用、SDK 截止日期或某一家商店的要求写成通用固定常量。

## 验证

在所用 Python 环境安装 PyYAML，然后执行：

```bash
python3 -B -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/check_skill.py
git diff --check
```

[CI](.github/workflows/check.yml) 在 push 和 pull request 上运行校验器回归与
一致性检查，覆盖 frontmatter、ID 对应、全部 README 和 reference 的本地
链接／标题锚点、换行和选定泄漏模式。负例证明中文 README 断链和中文
reference 错误锚点会被拒绝。这些检查不验证远程政策时效、agent 遵守情况、
应用二进制或真实商店提审；后者按 [发布证据模板](references/stores.zh-CN.md#报告记录)
单独记录。

原生发布还需按 [X6](references/testing.md#x6-packaged-release-verification--p0-for-release)
检查最终 app／engine／plugin 的二进制架构清单，分开记录 host CPU、工具
进程 ABI、目标和包标签；另核对安装器／包元数据与商店目标，并保留目标机器
加载／smoke 测试证据。本仓库 CI 不提供应用架构或真机验证结论。

## 许可证

GPL-3.0，见 [LICENSE](LICENSE)。
