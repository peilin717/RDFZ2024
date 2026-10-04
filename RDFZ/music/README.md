# RDFZ 原声：回声与晨光

19首独立BGM、6段主题短音乐。制作是 **原创乐谱 → MIDI → 本地SF2采样渲染 → 分轨混音 → 静态网页音频**，不使用云端音乐模型、音乐API、Codex API或GPU。

## 当前环境一键离线重建

在仓库根目录执行：

```bash
python RDFZ/tools/music/pipeline.py all --offline --resume
```

初始化校验字体、依赖与固定SHA256；正常重建读取已经落盘的 `scores/*.json`，不会重新作曲或调用模型。初始化之后，Python流水线主动禁止socket网络连接。已完成谱面编译、分轨和音频验证有内容缓存；改变一首谱面只重建该首受影响的分轨及混音。`--force`用于有意全部重做。中断后运行同一命令；`reports/checkpoint.json`记录最后完成步骤，分轨完成即落盘。

默认大文件目录是仓库同级的 `music-work/`，本环境为 `/workspace/music-work`。可通过 `RDFZ_MUSIC_WORK=/path/to/work`更改位置。网页部署只复制两种压缩编码、播放器与音源鸣谢，不包含音源、分轨、母带、谱面或试听缓存。

## 新机器初始化

需要Python 3.10+、Node.js、FFmpeg（libvorbis/libmp3lame）和FluidSynth共享库。无需FluidSynth CLI、音频设备或DAW。Debian/Ubuntu可安装 `libfluidsynth3 ffmpeg nodejs python3-venv`，然后在虚拟环境运行 `pip install -r RDFZ/tools/music/requirements.txt`。这些系统依赖未嵌入项目，不会暗中通过在线服务补足。

```bash
python RDFZ/tools/music/pipeline.py init
python RDFZ/tools/music/pipeline.py all --offline --resume
```

`init`仅在缺失时从 `production.json`指定的官方来源下载音源，并检查SHA256；离线模式缺失依赖会明确失败，不生成静音替代。两个音源约1.3GB，工作目录整套产物约数GB。GeneralUser源地址指向作者仓库，若远端更新导致校验不符，保留已验证本地副本，不能自动接受新版本。

## 分步命令

```bash
python RDFZ/tools/music/pipeline.py compile --offline
python RDFZ/tools/music/pipeline.py render --offline --cues home
python RDFZ/tools/music/pipeline.py mix --offline --cues home
python RDFZ/tools/music/pipeline.py verify --offline
python RDFZ/tools/music/pipeline.py build --offline
```

`render`/`mix`共同调用制作链；已有分轨会复用，混音不会分别归一化分轨。混音代码与渲染代码分别进入缓存判定。音乐编写源为 `representatives.py`、`album.py`，**只有有意重写原谱时才运行**；平常编辑逐曲JSON后重建即可。谱面保存音高、节奏、乐句力度、CC64/CC11、段落、循环点及每小节声部安排；另有MIDI、MusicXML与arrangement map。MusicXML是基础交换谱，不含专业排版；精确演奏事件以JSON/MIDI为准。

## 最终试听与游戏验证

```bash
python RDFZ/tools/music/preview_server.py
# 打开 http://localhost:4176/preview.html
python -m http.server 4173 --directory RDFZ
python RDFZ/tools/music/test_browser.py
python RDFZ/tools/music/test_resilience.py
python RDFZ/tools/music/test_delivery.py
python RDFZ/tools/music/test_result_events.py
```

浏览器测试需要本地Chromium与Python Playwright；默认读取 `http://127.0.0.1:4173`，可设置 `RDFZ_TEST_URL`测试部署构建。测试使用临时浏览器档案，不操作玩家原有存档。测试含模拟进度、事件和失败请求；不等同于人工完整打通全部关卡。资源映射覆盖实际关卡，代表性页面有截图。

试听页每首提供网页版本、三轮连续版本、母带与段落说明；播放器初始 `preload=none`。三轮版本以无损周期连续拼接后编码。制作时每声部先连续渲染三轮，提取中间完整周期，保留前一轮的采样release状态；滤波与共享房间同样使用前一周期尾部预热。循环主体没有淡入淡出，游戏切换场景才交叉淡化。

## 文件与限制

- `music-bible.md`、`cues.json`：视觉依据、音乐体系、真实场景分配。
- `themes/`：三个原创八小节主题与MIDI谱例。
- `scores/`：25套可编辑谱面、MIDI、MusicXML、小节编排表。
- `reviews/`：代表曲v1存档、v2具体改写、整套结构复核。
- `reports/`：技术验收、结构提示、浏览器结果和交付报告。
- `licenses/`：免费音源版本说明及许可；公开鸣谢页为 `music-credits.html`。
- 工作目录的 `stems/`、`masters/`、`previews/`、`soundfonts/`：大型产物，不进入Git或网页部署。

**未进行主观听觉验证。** 技术检查与谱面分析不能保证审美、耐听度或专业混音通过试听。GeneralUser木管/弦乐不具备本项目未验证的真实连奏奏法。Salamander的免费SF2转换版省略了部分原SFZ控制、踏板和释放噪声。没有使用外部评审API补足这些限制。

## 战斗与关键操作音效

本地制作和测试使用 Conda 环境 `rdfz2024`（Python 3.12、FluidSynth、`tools/music/requirements.txt` 及 Playwright）。不修改系统 Python 或全局环境变量。

音效沿用配乐的 GeneralUser GS 固定版本采样库、MIDI 编写、FluidSynth 离线渲染和 FFmpeg Ogg/MP3 编码；不在浏览器合成声音。`sfx/gestures.json` 是八种短音效的可编辑源，旁边的 MIDI 为导出谱面。工作文件和音源保存在仓库根目录已忽略的 `music-work/`，网页只发布 `assets/sfx/` 的哈希音频文件。

```bash
conda activate rdfz2024
# 音源须为 production.json 中指定 SHA256 的 GeneralUser GS：
# music-work/soundfonts/GeneralUser-GS.sf2
python RDFZ/tools/music/build_sfx.py
node RDFZ/tools/build_web.mjs
# 启动网页服务后，以隔离浏览器档案验证：
python RDFZ/tools/music/test_sfx.py
```

音效触发范围：普通／穿盾命中、属性命中、护盾吸收、护盾生成、闪避／免疫、成功释放技能，以及确认出战、暂停／继续。技能不足星数不响；普通导航、图鉴卡片、剧情翻页、悬停不加声。键盘技能和暂停使用同一触发路径。

沿用现有声音开关及静音存储，与 BGM 共用 AudioContext 和主音量。首次用户手势后预备八个短音效，命中类至少间隔 105ms、其他类别 180ms，最多四声并发。音效不压低或重启背景音乐；静音、暂停、离开战斗或切换到后台会清理短音效，超过 220ms 的迟到反馈丢弃；音频请求失败只跳过声音，不阻塞伤害或存档。

`reports/sfx-production.json` 记录双编码解码与峰值检查；`reports/sfx-browser-validation.json` 记录浏览器回归。短音效不循环，允许编码器小于 30ms 的尾部填充差异。尚未进行主观听觉验收。
