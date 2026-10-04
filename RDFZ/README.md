# RDFZ 2024级风云

校园题材的现代 2D 抽卡策略 RPG。

当前版本包含完整系统主页、风云招募、十连保底、重复角色碎片、伙伴图鉴、自动编队、章节冒险，以及带原创 2D 角色立绘和场景的回合战斗。

新版使用 IndexedDB 保存账号、伙伴、背包、关卡和剧情进度。角色、关卡、卡池和剧情的扩展方式见 `EXTENDING.md`。

## 启动

### Windows

解压后双击 `start-windows.bat`。电脑需要安装 Node.js 18+，启动后访问 `http://127.0.0.1:4173`。

### WSL / Linux

```bash
cd RDFZ
bash start.sh
```

然后访问 `http://127.0.0.1:4173`。

`start.sh` 使用 Node.js 18+，先构建 `dist` 再启动仅监听本机的静态服务器，无需 Python。

## 操作

- 点击角色：切换当前行动角色
- 点击技能：消耗技能星并释放技能
- 空格：普通攻击
- 数字键 1、2、3：快速释放对应技能
- 每轮敌方行动结束后，全队恢复 3 点技能星

游戏进度保存在浏览器本地存储中。

游戏文件本身不包含存档。把整个游戏目录压缩后发给其他人，对方会在自己的浏览器中建立独立的新存档。

## Web 发布与按需加载

Vercel 导入仓库后，将 **Root Directory 设置为 `RDFZ`**，Framework 选择 **Other**。目录中的 `vercel.json` 已配置：

- Build Command：`node tools/build_web.mjs`
- Output Directory：`dist`
- 无需安装 Node 依赖，无需 Python 服务或数据库。

本地验证发布产物：

```bash
cd RDFZ
node tools/build_web.mjs
python3 -m http.server 4173 --directory dist
```

网页使用已经提交的高质量 WebP 资源，原始 PNG 保留用于维护。开始界面不下载游戏图片；图鉴和编队按可见区域加载缩略图，详情与战斗使用全尺寸图片；剧情只在进入时加载当前图，并最多预取下一张。未启用离线缓存或 Service Worker，存档仍保存在用户浏览器中。

图片文件名含内容哈希，可长期缓存；HTML、JS、CSS 会重新验证版本。发布目录仅包含页面代码和 WebP，不包含 PNG 原图、工具或 Android 工程。

修改原图后，重新生成资源并提交 `assets/web/` 与两个清单文件：

```bash
python3 -m pip install Pillow
python3 tools/optimize_web_assets.py
node tools/build_web.mjs
```

新增 CSS 图片时，使用 `var(--asset-相对路径)`，例如 `assets/story/example.png` 对应 `var(--asset-story-example)`，生成脚本会自动输出变量。JavaScript 使用 `RDFZAssets.art('assets/story/example.png')`；长列表用 `data-art-src` 与 `RDFZAssets.observe(container)`。发布构建不包含原图，不应新增直接指向 PNG 的浏览器请求。

性能数据、画质验证及测试命令见 [WEB_PERFORMANCE.md](WEB_PERFORMANCE.md)。

## 正常经济模式与测试配置

默认新存档拥有 **3000 召唤石**，单抽扣 300，十连扣 2700；不再自动开启无限招募或赠送测试角色。

| 构建环境变量 | 默认值 | 含义 |
| --- | --- | --- |
| `RDFZ_INITIAL_GEMS` | `3000` | 新存档初始召唤石；非负安全整数，包括 0 |
| `RDFZ_UNLIMITED_GEMS` | `false` | 仅接受 `true` / `false`；开启后抽卡不扣费 |

Vercel 项目根目录保持 `RDFZ`，构建命令保持 `node tools/build_web.mjs`。在项目的 Environment Variables 中设置以上变量，并选择 Production 或 Preview 对应范围后重新部署。不设置即使用正常模式。变量在**构建时**写入公开的 `dist/game-config.js`，不读取浏览器中的服务器环境变量，也不会把其他环境变量打包到网页。

本地普通启动（仓库根目录）：

```bash
bash RDFZ/start.sh
```

本地测试，无需修改全局环境：

```bash
RDFZ_INITIAL_GEMS=30000 RDFZ_UNLIMITED_GEMS=true PORT=4174 bash RDFZ/start.sh
# 有限余额测试：
RDFZ_INITIAL_GEMS=6000 RDFZ_UNLIMITED_GEMS=false PORT=4174 bash RDFZ/start.sh
```

也可以只构建：`RDFZ_INITIAL_GEMS=30000 RDFZ_UNLIMITED_GEMS=true node RDFZ/tools/build_web.mjs`，再用静态服务器托管 `RDFZ/dist`。直接托管源码目录只使用 `game-config.js` 中的默认正常配置；修改进程环境不会改变未经构建的源码网页。更改配置后需重新构建／重启本地脚本；端口已占用时可用 `PORT` 指定空闲端口。

初始金额不会覆盖已有正常存档余额。旧存档若保存了无限模式，在正常配置下首次打开时会关闭无限、将召唤石重置为配置的初始金额，保留已有角色、碎片、强化、关卡和剧情进度；后续正常扣费与奖励会照常保存，不会每次补回初始金额。测试模式和正式模式在同一网址下共用存档，建议使用不同端口或独立浏览器档案进行测试。

回归：`node RDFZ/tools/test_game_config.mjs`；在 `rdfz2024` Conda 环境执行 `python RDFZ/tools/test_economy.py` 验证真实浏览器扣费及存档迁移。
