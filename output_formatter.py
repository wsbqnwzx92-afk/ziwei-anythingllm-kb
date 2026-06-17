# -*- coding: utf-8 -*-
"""
输出格式化模块（Markdown 和 JSON）
针对 AnythingLLM 知识库优化
"""

import json
from typing import Dict, Any


class BaseFormatter:
    """格式化基类"""
    
    PALACE_INTERPRETATIONS = {
        '命宫': '命宫象征一个人的先天命运、性格基质和人生主线。这里的星曜组合决定了你的核心个性特质、本能反应方式、以及对人生的基本态度。命宫是整个命盘的中心，其他所有宫位都以命宫为参照。',
        '身宫': '身宫代表后天的身体、精力和日常行为表现。它反映你的实际执行力、身体状况和在生活中的具体行动方式。身宫与命宫相差五宫，代表命与运的互动关系。',
        '父母宫': '反映与父母的关系、家庭背景和童年经历对你的影响。还代表上司、长辈等权威人物。',
        '福德宫': '象征你的福报、精神世界、生活满足感和内心修养。代表精神财富和心灵境界。',
        '田宅宫': '关系到房产、不动产、居住环境和家庭稳定性。也代表遗产和家族产业。',
        '官禄宫': '代表职业、事业发展、工作环境和成就机会。是事业宫，影响你的职业运势。',
        '仆役宫': '涉及人脉、下属、朋友关系和社交圈子。代表人缘和交友运。',
        '迁移宫': '象征出门运气、变化、搬迁和外出发展的机遇。代表在外地的运势。',
        '疾厄宫': '关系到健康、疾病、生理机能和医疗方面。代表身体状况和抵抗力。',
        '财帛宫': '代表财运、收入、金钱观和经济状况。是财富宫，影响你的财运。',
        '子女宫': '反映与子女的关系、生育能力和下一代缘分。也代表晚辈。',
        '夫妻宫': '象征婚姻感情、配偶情况和两性关系。是感情宫，影响婚恋运。',
        '兄弟宫': '涉及兄弟姐妹关系、同事协作和亲属互动。代表手足和同辈。',
    }
    
    STAR_INTERPRETATIONS = {
        '紫微': '帝星。象征权力、领导力和尊贵身份。紫微坐命的人有君临天下的气质，天生领导者风范，容易获得权力和地位。性格高傲，有自我修养要求。',
        '天机': '智星。代表聪慧、变化和应变能力。天机人聪明伶俐，思维敏捷，适合从事需要智慧和创新的工作。但心思较多，容易心烦。',
        '太阳': '光明星。象征热情、开朗和施舍。太阳人光芒万丈，性格爽朗，容易获得他人好感和支持。工作能力强，但可能过于乐观。',
        '武曲': '财星。代表开创、行动力和物质收获。武曲人行动积极，执行力好，善于理财和资源管理，容易获得财富。但性格较硬，容易冲动。',
        '天同': '福星。象征温和、幸福和享受。天同人福气较好，性格温和，生活相对安逸舒适。适合享受生活，但需要警惕懒惰。',
        '廉贞': '刑星。代表廉洁、原则性强。廉贞人有骨气，原则性强，在事业上有不错的表现。但性格直率，有时过于坚持己见。',
        '天府': '库星。象征稳定、财富积累和资源掌控。天府人善于理财，有理财天赋，生活稳定，容易积累财富。性格保守但踏实。',
        '太阴': '暗星。代表温柔、感性和母性特质。太阴人感情细腻，容易多想。女性缘分好，但需要提防阴性特质过重。',
        '贪狼': '欲望星。象征野心、渴望和贪心。贪狼人有上进心，渴望成功，行动力强。但需要节制欲望，避免过度追求。',
        '巨门': '是非星。代表是非、口舌和传播。巨门人善于表达，思维敏捷，适合传播工作。但也容易卷入纠纷，需要谨言慎行。',
        '天相': '印星。象征辅助、协作和人缘。天相人人缘好，善于配合他人，适合团队合作。是很好的辅助者和合作者。',
        '天梁': '寿星。代表庇护、长寿和解厄。天梁人福气较好，有贵人相助，遇事能化解困难。性格沉稳，有阅历。',
        '七杀': '将星。象征霸气、冲劲和改革精神。七杀人有野心，容易激进，适合开创事业。但性格强硬，需要学会柔和。',
        '破军': '变星。代表变化、破坏和重生。破军人有冲劲，行动积极，容易经历变化和新开始。但也容易陷入混乱，需要稳定心态。',
        '左辅': '辅助星。象征帮助和协助。左辅提升周围星曜的正面作用。',
        '右弼': '辅助星。象征扶持和支持。右弼提升周围星曜的正面特质。',
        '文昌': '文星。代表文化、学问和考试。文昌人聪慧，适合学习和文化工作。',
        '文曲': '文星。代表文采、艺术和表达。文曲人有文采，适合创意和艺术工作。',
        '禄存': '富贵星。代表财富、存储和积累。禄存所在宫位容易获得福气和财富。',
        '天马': '动星。代表动力、行动和移动。天马提升行动力，但也容易奔波。',
        '红鸾': '感情星。代表爱情、感情和异性缘。红鸾旺盛则感情顺利。',
        '天喜': '喜庆星。代表快乐、喜庆和幸福。天喜所在宫位充满欢乐气氛。',
    }
    
    FOUR_HUA_INTERPRETATIONS = {
        '化禄': '代表顺利、获得和积累。化禄所在的事务会比较顺利，容易获得相关收益。是最吉利的化星，能让事务进展顺利。',
        '化权': '代表权力、掌控和强化。化权让人在相关事务上有掌控欲，容易强势。能强化星曜的力量，但也容易过度。',
        '化科': '代表好名声、名誉和表面光彩。化科让相关事务看起来很好，容易获得名声。但有时流于表面，需要实质内涵。',
        '化忌': '代表阻碍、忙碌和困扰。化忌所在的事务需要多费心力，容易遇到困难。需要特别关注，谨慎对待。',
    }
    
    def __init__(self, chart_data: Dict[str, Any]):
        self.chart_data = chart_data
    
    def format(self) -> str:
        """格式化方法，由子类实现"""
        raise NotImplementedError


class MarkdownFormatter(BaseFormatter):
    """Markdown 格式化器 - 针对 AnythingLLM 优化"""
    
    MAJOR_STARS = [
        '紫微', '天机', '太阳', '武曲', '天同', '廉贞',
        '天府', '太阴', '贪狼', '巨门', '天相', '天梁',
        '七杀', '破军'
    ]
    
    MINOR_STARS = ['左辅', '右弼', '文昌', '文曲', '禄存', '天马', '红鸾', '天喜']
    
    def format(self) -> str:
        """生成 Markdown 格式的命盘内容"""
        lines = []
        lines.append(self._format_header())
        lines.append(self._format_basic_info())
        lines.append(self._format_ming_shen_analysis())
        lines.append(self._format_palace_table())
        lines.append(self._format_palace_details())
        lines.append(self._format_star_interpretations())
        lines.append(self._format_four_hua_analysis())
        lines.append(self._format_comprehensive_reading())
        return '\n'.join(lines)
    
    def _format_header(self) -> str:
        """格式化标题"""
        birth_date = self.chart_data['basic_info']['birth_date']
        hour = self.chart_data['basic_info']['hour']
        gender = self.chart_data['basic_info']['gender']
        
        return f"""# 紫薇斗数命盘排盘结果

## 出生信息

- **出生日期**：{birth_date}
- **出生时辰**：{hour}时
- **性别**：{gender}
- **年干**：{self.chart_data['basic_info']['year_stem']}
- **月干**：{self.chart_data['basic_info']['month_stem']}
- **日干**：{self.chart_data['basic_info']['day_stem']}
- **五行局**：{self.chart_data['basic_info']['wu_xing_ju']}局

---
"""
    
    def _format_basic_info(self) -> str:
        """格式化关键指标表"""
        ming_gong = self.chart_data['ming_gong']
        shen_gong = self.chart_data['shen_gong']
        
        return f"""## 命盘关键指标

| 指标 | 值 | 说明 |
|------|-----|------|
| **命宫** | {ming_gong['name']} | 先天命运和性格基质 |
| **身宫** | {shen_gong['name']} | 后天行为和身体状况 |
| **五行局** | {self.chart_data['basic_info']['wu_xing_ju']}局 | 命盘的基础五行属性 |
| **年干** | {self.chart_data['basic_info']['year_stem']} | 年份天干，影响四化星 |

---
"""
    
    def _format_ming_shen_analysis(self) -> str:
        """格式化命宫、身宫的详细分析"""
        lines = []
        ming_gong = self.chart_data['ming_gong']
        shen_gong = self.chart_data['shen_gong']
        
        lines.append("## 命宫 · 身宫深层解读\n")
        lines.append(f"### 命宫：{ming_gong['name']}\n")
        lines.append(f"**宫位解释**：{self.PALACE_INTERPRETATIONS.get(ming_gong['name'], '')}\n")
        lines.append(f"**宫位序号**：第 {ming_gong['index']} 宫\n")
        
        ming_palace = self.chart_data['palaces'][ming_gong['index']]
        if ming_palace['major_stars']:
            lines.append(f"**主星**：{', '.join(ming_palace['major_stars'])}\n")
            for star in ming_palace['major_stars']:
                star_desc = self.STAR_INTERPRETATIONS.get(star, f"{star}是一颗重要的星曜。")
                lines.append(f"\n- **{star}**\n  {star_desc}\n")
        
        if ming_palace['minor_stars']:
            lines.append(f"**辅星**：{', '.join(ming_palace['minor_stars'])}\n")
        
        lines.append("\n")
        lines.append(f"### 身宫：{shen_gong['name']}\n")
        lines.append(f"**宫位解释**：{self.PALACE_INTERPRETATIONS.get(shen_gong['name'], '')}\n")
        lines.append(f"**宫位序号**：第 {shen_gong['index']} 宫\n")
        
        shen_palace = self.chart_data['palaces'][shen_gong['index']]
        if shen_palace['major_stars']:
            lines.append(f"**主星**：{', '.join(shen_palace['major_stars'])}\n")
        
        if shen_palace['minor_stars']:
            lines.append(f"**辅星**：{', '.join(shen_palace['minor_stars'])}\n")
        
        lines.append("\n---\n")
        return ''.join(lines)
    
    def _format_palace_table(self) -> str:
        """格式化十二宫位速览表"""
        lines = ["## 十二宫位速览\n"]
        lines.append("| 宫位 | 主星 | 辅星 | 四化 |")
        lines.append("|------|------|------|------|") 
        
        for palace in self.chart_data['palaces']:
            palace_name = palace['name']
            major_stars = ', '.join(palace['major_stars']) if palace['major_stars'] else '—'
            minor_stars = ', '.join(palace['minor_stars']) if palace['minor_stars'] else '—'
            four_hua_types = ', '.join([h['type'] for h in palace['four_hua']]) if palace['four_hua'] else '—'
            lines.append(f"| {palace_name} | {major_stars} | {minor_stars} | {four_hua_types} |")
        
        lines.append("\n---\n")
        return '\n'.join(lines)
    
    def _format_palace_details(self) -> str:
        """格式化各宫位的详细说明"""
        lines = ["## 各宫详细说明\n"]
        
        for palace in self.chart_data['palaces']:
            lines.append(f"### {palace['name']}\n")
            palace_name = palace['name']
            interpretation = self.PALACE_INTERPRETATIONS.get(palace_name, '')
            lines.append(f"{interpretation}\n")
            
            if palace['major_stars'] or palace['minor_stars']:
                lines.append("**星曜组合**：")
                if palace['major_stars']:
                    lines.append(f"  - 主星：{', '.join(palace['major_stars'])}")
                if palace['minor_stars']:
                    lines.append(f"  - 辅星：{', '.join(palace['minor_stars'])}")
                lines.append("")
            
            if palace['four_hua']:
                lines.append("**四化星**：")
                for hua_info in palace['four_hua']:
                    lines.append(f"  - {hua_info['type']}（{hua_info['star']}）")
                lines.append("")
            
            lines.append("")
        
        lines.append("---\n")
        return '\n'.join(lines)
    
    def _format_star_interpretations(self) -> str:
        """格式化星曜详解"""
        lines = ["## 星曜详解\n"]
        
        all_stars = set()
        for palace in self.chart_data['palaces']:
            all_stars.update(palace['major_stars'])
            all_stars.update(palace['minor_stars'])
        
        major_in_chart = [s for s in self.MAJOR_STARS if s in all_stars]
        minor_in_chart = [s for s in self.MINOR_STARS if s in all_stars]
        
        if major_in_chart:
            lines.append("### 主星\n")
            for star in major_in_chart:
                interpretation = self.STAR_INTERPRETATIONS.get(star, f"{star}是一颗重要的星曜。")
                lines.append(f"**{star}**\n\n{interpretation}\n\n")
        
        if minor_in_chart:
            lines.append("### 辅星\n")
            for star in minor_in_chart:
                interpretation = self.STAR_INTERPRETATIONS.get(star, f"{star}是一颗辅助星曜。")
                lines.append(f"**{star}**\n\n{interpretation}\n\n")
        
        lines.append("---\n")
        return ''.join(lines)
    
    def _format_four_hua_analysis(self) -> str:
        """格式化四化分析"""
        lines = ["## 四化星分析\n"]
        four_hua = self.chart_data['four_hua']
        year_stem = self.chart_data['basic_info']['year_stem']
        
        lines.append(f"**年干：{year_stem}** - 根据年干计算出该命盘的四化星组合\n")
        
        hua_types = ['化禄', '化权', '化科', '化忌']
        for hua_type in hua_types:
            lines.append(f"### {hua_type}\n")
            if hua_type in four_hua:
                info = four_hua[hua_type]
                lines.append(f"- **星曜**：{info['star']}")
                lines.append(f"- **所在宫位**：{info['palace_name']}")
                lines.append(f"- **影响范围**：{self.FOUR_HUA_INTERPRETATIONS.get(hua_type, '')}\n")
            else:
                lines.append("（本命盘无此四化）\n")
        
        lines.append("---\n")
        return ''.join(lines)
    
    def _format_comprehensive_reading(self) -> str:
        """格式化综合断语"""
        lines = ["## 综合人生解读\n"]
        lines.append("### 性格特质\n根据命宫星曜组合，你具有独特的个性特质和做事风格。\n\n")
        lines.append("### 人生主线\n根据你的命盘，建议保持对生活的热情，善于把握机遇，同时学会平衡与取舍。\n\n")
        lines.append("### 事业前景\n事业运势需要查看官禄宫。根据该宫的星曜组合，可以判断你的职业适合度和发展前景。\n\n")
        lines.append("### 感情婚姻\n感情运势需要查看夫妻宫。根据该宫的星曜组合，可以了解你的感情特质和婚恋前景。\n\n")
        lines.append("### 财富运势\n财富运势需要通过勤奋和理财来实现。建议谨慎消费，规划长期财务目标。\n\n")
        lines.append("### 运势指导\n• 保持平衡心态，既不过度乐观也不过度悲观。\n")
        lines.append("• 充分认识自身优势，发扬长处，弥补不足。\n")
        lines.append("• 重视人脉和贵人的帮助，保持良好的人际关系。\n")
        lines.append("• 定期反思和调整，让人生朝向更好的方向发展。\n\n")
        lines.append("---\n*本命盘由紫薇斗数排盘系统自动生成，仅供参考学习。*\n")
        return ''.join(lines)


class JSONFormatter(BaseFormatter):
    """JSON 格式化器 - 用于结构化数据备份"""
    
    def format(self) -> str:
        """生成 JSON 格式的命盘数据"""
        output = {
            'version': '1.0',
            'format': 'ziwei_paiupan',
            'data': self.chart_data,
            'interpretations': {
                'palaces': self.PALACE_INTERPRETATIONS,
                'stars': self.STAR_INTERPRETATIONS,
                'four_hua': self.FOUR_HUA_INTERPRETATIONS,
            }
        }
        return json.dumps(output, ensure_ascii=False, indent=2)
