# 紫薇斗数排盘脚本 - AnythingLLM 知识库版本

为 **AnythingLLM 知识库**生成紫薇命盘内容的 Python 工具。支持完整的紫薇斗数排盘，生成平实易懂的 Markdown 和 JSON 格式输出。

## ✨ 功能特性

### ✅ 完整排盘算法
- **命宫、身宫计算** - 根据出生时辰和农历月份计算
- **五行局判定** - 根据出生时辰确定命盘的五行属性
- **十四主星排列** - 按五行局规则安排主星
- **辅星布置** - 安排左辅、右弼、文昌、文曲、禄存、天马等
- **四化星计算** - 根据年干计算化禄、化权、化科、化忌

### ✅ 知识库友好输出
- **Markdown 格式** - 结构清晰，包含完整表格和通俗易懂的断语
- **JSON 格式** - 结构化数据，便于程序化处理和备份
- **优化检索** - 清晰的标题结构和表格，便于 LangChain/AnythingLLM 切片

### ✅ 便捷使用
- **命令行参数** - 支持单条排盘
- **批量处理** - 支持 CSV 文件批量导入
- **灵活输出** - 可选 Markdown、JSON 或两者兼有

## 📦 安装

### 前置要求
- Python 3.9+
- pandas (用于 CSV 处理)
- python-dateutil (用于日期解析)

### 快速安装

```bash
# 1. 克隆或下载本项目
cd ziwei-anythingllm-kb

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
python main.py --birth 1990-01-01 --hour 子 --gender 男
```

## 🚀 使用方式

### 方式 1: 单个排盘

最简单的方式，用于快速查询单个人的命盘。

```bash
python main.py --birth 1990-01-01 --hour 子 --gender 男
```

**输出结果**：
- `1990-01-01_子_男.md` - Markdown 命盘（知识库内容）
- `1990-01-01_子_男.json` - JSON 结构化备份

### 方式 2: 批量处理

用于批量处理多个人的命盘数据。

```bash
python main.py --batch batch.csv --output ./outputs
```

**CSV 文件格式**（batch.csv）：
```csv
birth_date,hour,gender
1990-01-01,子,男
1995-06-15,午,女
2000-12-25,申,男
```

### 方式 3: 仅输出特定格式

```bash
# 仅输出 Markdown
python main.py --birth 1990-01-01 --hour 子 --gender 男 --format md

# 仅输出 JSON
python main.py --birth 1990-01-01 --hour 子 --gender 男 --format json
```

## 📋 参数说明

| 参数 | 必填 | 说明 | 例子 |
|------|------|------|------|
| `--birth` | ✓* | 出生日期 (YYYY-MM-DD) | `1990-01-01` |
| `--hour` | ✓* | 出生时辰 | `子`/`午`/`申` |
| `--gender` | ✓* | 性别 | `男` / `女` |
| `--batch` | ✓** | 批量 CSV 文件路径 | `batch.csv` |
| `--output` | ✗ | 输出目录 | `./outputs` (默认) |
| `--format` | ✗ | 输出格式 | `both`/`md`/`json` (默认: both) |

*注：单个排盘需要 `--birth`、`--hour`、`--gender`  
**注：批量处理需要 `--batch`

## 📂 输出示例

### 目录结构

```
outputs/
├── 1990-01-01_子_男.md       # Markdown 命盘（知识库内容）
├── 1990-01-01_子_男.json     # JSON 结构化备份
├── 1995-06-15_午_女.md
├── 1995-06-15_午_女.json
└── ...
```

### Markdown 输出内容

生成的 Markdown 文件包含以下部分：

```markdown
# 紫薇斗数命盘排盘结果

## 出生信息
- 出生日期：1990-01-01
- 出生时辰：子时
- ...

## 命盘关键指标
| 指标 | 值 |
|------|-----|
| 命宫 | 命宫位置 |
| 身宫 | 身宫位置 |
| ...

## 命宫 · 身宫深层解读
详细的命宫身宫分析...

## 十二宫位速览
表格展示所有宫位的星曜组合...

## 各宫详细说明
每个宫位的详细解释...

## 星曜详解
各个星曜的含义和影响...

## 四化星分析
四化星的具体作用...

## 综合人生解读
性格特质、人生主线、事业前景、感情婚姻等...
```

### JSON 输出结构

```json
{
  "version": "1.0",
  "format": "ziwei_paiupan",
  "data": {
    "basic_info": {
      "birth_date": "1990-01-01",
      "hour": "子",
      "gender": "男",
      "year_stem": "庚",
      "wu_xing_ju": 2,
      ...
    },
    "palaces": [...],
    "major_stars": {...},
    "four_hua": {...}
  },
  "interpretations": {...}
}
```

## 🔗 与 AnythingLLM 集成

### 方式 1：直接导入 Markdown（推荐）

最简单的方式，直接利用生成的 Markdown 文件。

1. **运行排盘脚本生成 Markdown 文件**
   ```bash
   python main.py --batch people.csv --format md
   ```

2. **在 AnythingLLM 中上传文件**
   - 登录 AnythingLLM 工作区
   - 进入「文档管理」或「知识库」
   - 上传生成的 `.md` 文件
   - 系统自动切片和索引

3. **开始对话**
   - 用户可以查询具体人的命盘信息
   - AI 会自动从知识库中检索相关内容

**优势**：
- 文本格式易于搜索和检索
- 自然语言友好，断语易读
- 支持向量化和语义搜索

### 方式 2：程序化集成

如果需要与其他系统集成，使用 JSON 输出。

```python
import json
from ziwei_engine import ZiweiEngine
from output_formatter import JSONFormatter

# 创建排盘
engine = ZiweiEngine(birth, hour, gender)
chart_data = engine.calculate()

# 输出 JSON
formatter = JSONFormatter(chart_data)
json_str = formatter.format()
data = json.loads(json_str)

# 进一步处理...
```

## 📝 项目结构

```
.
├── main.py                 # 主程序入口（CLI）
├── ziwei_engine.py         # 核心排盘引擎（真实算法）
├── output_formatter.py     # 输出格式化（Markdown/JSON）
├── batch_example.csv       # 批量处理示例
├── requirements.txt        # 依赖列表
└── README.md              # 本文件
```

## 🧮 算法说明

### 排盘核心算法

#### 1. 命宫计算
```
命宫 = (时支序号 + 农历月数 - 1) % 12
```

#### 2. 身宫计算
```
身宫 = (命宫 + 5) % 12
```

#### 3. 五行局判定
根据出生时辰的地支确定：
- 子、丑 → 水二局
- 寅、卯 → 木三局
- 辰、巳 → 土五局
- 午、未 → 火六局
- 申、酉 → 金七局
- 戌、亥 → 土八局

#### 4. 十四主星排列
根据五行局和命宫位置，按特定序列排列主星。

#### 5. 四化星计算
根据年干查表得出：
- 甲年：廉贞禄、破军权、武曲科、太阳忌
- 乙年：天机禄、天梁权、紫微科、武曲忌
- ...等（共 10 个天干）

## ⚠️ 注意事项

1. **阳历输入**：所有日期输入应为阳历（公历）
2. **学派差异**：本脚本基于民间常见紫薇斗数学派，不同学派可能有差异
3. **参考用途**：排盘结果仅供参考学习，不构成任何决策依据
4. **准确性**：使用简化算法，部分细节可能与专业排盘有偏差

## 🔧 故障排除

### 问题 1：找不到模块错误

```
ModuleNotFoundError: No module named 'pandas'
```

**解决**：安装依赖
```bash
pip install -r requirements.txt
```

### 问题 2：日期格式错误

```
日期格式错误: 1990/01/01（应为 YYYY-MM-DD 格式）
```

**解决**：使用正确的日期格式 `YYYY-MM-DD`

### 问题 3：时辰输入错误

**解决**：使用以下正确的时辰字符：
`子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥`

## 🚀 后续改进计划

- [ ] 支持农历直接输入
- [ ] 加入大运、流年计算
- [ ] 扩展断语库，增加更多详细解释
- [ ] 支持生成 HTML 网页版本
- [ ] 提供 HTTP API 服务
- [ ] 优化算法准确度，对标专业排盘软件

## 📄 License

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- 项目讨论区

---

**最后更新**：2024 年  
**版本**：1.0.0  
**Python 版本**：3.9+
