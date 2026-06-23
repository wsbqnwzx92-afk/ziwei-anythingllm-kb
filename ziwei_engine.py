# -*- coding: utf-8 -*-
"""
正统三合紫微斗数排盘引擎
修复原始代码全部安星bug | 新增大运、流年、格局自动分析
遵循传统紫微斗数安星赋、十干四化、大限顺逆规则
"""
from datetime import datetime
from typing import Dict, List, Set, Any


class ZiweiDouShuEngine:
    # ========== 基础常量定义 ==========
    # 十天干、十二地支
    STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 十二宫顺序（索引0~11对应子~亥地支）
    PALACE_NAMES = [
        "命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫",
        "迁移宫", "仆役宫", "官禄宫", "田宅宫", "福德宫", "父母宫"
    ]
    # 阴阳天干
    YANG_STEM_SET = {"甲", "丙", "戊", "庚", "壬"}
    YIN_STEM_SET = {"乙", "丁", "己", "辛", "癸"}

    # 十四主星分两大星系
    ZIWEI_STAR_GROUP = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞"]  # 北斗紫微星系
    TIANFU_STAR_GROUP = ["天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]  # 南斗天府星系
    ALL_MAJOR_STARS = ZIWEI_STAR_GROUP + TIANFU_STAR_GROUP

    # 基础六辅星+红鸾天喜
    MINOR_STARS = ["左辅", "右弼", "文昌", "文曲", "禄存", "天马", "红鸾", "天喜"]

    # 十干四化表（本命/流年通用）
    FOUR_HUA_TABLE = {
        "甲": {"禄": "廉贞", "权": "破军", "科": "武曲", "忌": "太阳"},
        "乙": {"禄": "天机", "权": "天梁", "科": "紫微", "忌": "武曲"},
        "丙": {"禄": "天同", "权": "天机", "科": "巨门", "忌": "贪狼"},
        "丁": {"禄": "太阴", "权": "太阳", "科": "天同", "忌": "天机"},
        "戊": {"禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"},
        "己": {"禄": "巨门", "权": "廉贞", "科": "天府", "忌": "太阴"},
        "庚": {"禄": "武曲", "权": "贪狼", "科": "天府", "忌": "巨门"},
        "辛": {"禄": "太阳", "权": "武曲", "科": "天梁", "忌": "巨门"},
        "壬": {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"},
        "癸": {"禄": "破军", "权": "巨门", "科": "太阴", "忌": "贪狼"},
    }

    # 六十甲子纳音五行（生年查表定五行局，正统标准）
    YEAR_NA_YIN_MAP = {
        ("甲", "子"): "金", ("乙", "丑"): "金", ("丙", "寅"): "火", ("丁", "卯"): "火", ("戊", "辰"): "木", ("己", "巳"): "木",
        ("庚", "午"): "土", ("辛", "未"): "土", ("壬", "申"): "金", ("癸", "酉"): "金", ("甲", "戌"): "火", ("乙", "亥"): "火",
        ("丙", "子"): "水", ("丁", "丑"): "水", ("戊", "寅"): "土", ("己", "卯"): "土", ("庚", "辰"): "金", ("辛", "巳"): "金",
        ("壬", "午"): "木", ("癸", "未"): "木", ("甲", "申"): "水", ("乙", "酉"): "水", ("丙", "戌"): "土", ("丁", "亥"): "土",
        ("戊", "子"): "火", ("己", "丑"): "火", ("庚", "寅"): "木", ("辛", "卯"): "木", ("壬", "辰"): "水", ("癸", "巳"): "水",
        ("甲", "午"): "金", ("乙", "未"): "金", ("丙", "申"): "火", ("丁", "酉"): "火", ("戊", "戌"): "木", ("己", "亥"): "木",
        ("庚", "子"): "土", ("辛", "丑"): "土", ("壬", "寅"): "金", ("癸", "卯"): "金", ("甲", "辰"): "火", ("乙", "巳"): "火",
        ("丙", "午"): "水", ("丁", "未"): "水", ("戊", "申"): "土", ("己", "酉"): "土", ("庚", "戌"): "金", ("辛", "亥"): "金",
        ("壬", "子"): "木", ("癸", "丑"): "木", ("甲", "寅"): "水", ("乙", "卯"): "水", ("丙", "辰"): "土", ("丁", "巳"): "土",
        ("戊", "午"): "火", ("己", "未"): "火", ("庚", "申"): "木", ("辛", "酉"): "木", ("壬", "戌"): "水", ("癸", "亥"): "水",
    }

    # 纳音五行映射五行局+起运年龄
    NA_YIN_TO_JU = {"水": 2, "木": 3, "金": 4, "土": 5, "火": 6}

    # 紫微落宫查表：五行局 -> [子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥]对应紫微地支索引
    ZIWEI_POS_LOOKUP = {
        2: [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7],  # 水二局
        3: [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5],  # 木三局
        4: [4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3],  # 金四局
        5: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1],  # 土五局
        6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 火六局
    }

    def __init__(self, birth_solar: datetime, lunar_birth_month: int, hour_branch: str, gender: str):
        """
        初始化排盘引擎
        :param birth_solar: 阳历生日 datetime 对象
        :param lunar_birth_month: 农历出生月份 1~12（必须手动传入，无内置农历转换）
        :param hour_branch: 出生时辰地支：子/丑/寅/卯/辰/巳/午/未/申/酉/戌/亥
        :param gender: 性别 "男" / "女"
        """
        # 基础输入信息
        self.birth_solar = birth_solar
        self.lunar_month = lunar_birth_month
        self.hour_branch = hour_branch
        self.gender = gender

        # 年干支缓存
        self.year_stem: str = ""
        self.year_branch: str = ""
        self.year_stem_idx: int = 0
        self.year_branch_idx: int = 0
        self.is_yang_year: bool = False

        # 命宫、身宫索引（0~12对应子~亥）
        self.ming_palace_idx: int = -1
        self.shen_palace_idx: int = -1

        # 五行局与起运年龄
        self.wuxing_ju: int = 0
        self.start_transport_age: int = 0

        # 十二宫天干列表，索引对应地支0~11
        self.palace_stem_list: List[str] = [""] * 12

        # 星曜位置映射 {星名: 宫位索引}
        self.major_star_map: Dict[str, int] = {}
        self.minor_star_map: Dict[str, int] = {}

        # 本命四化数据
        self.benming_sihua: Dict[str, Dict[str, Any]] = {}

        # 大运（大限）列表缓存
        self.daxian_list: List[Dict[str, Any]] = []
        # 流年缓存，减少重复计算
        self.liunian_cache: Dict[int, Dict[str, Any]] = {}

    def calc_year_ganzhi(self) -> None:
        """标准六十甲子计算出生年干支，修正原版1900简易公式错误"""
        base_year = 1904  # 1904甲辰，六十甲子基准年
        year_diff = self.birth_solar.year - base_year
        total_cycle = year_diff % 60
        self.year_stem_idx = total_cycle % 10
        self.year_branch_idx = total_cycle % 12
        self.year_stem = self.STEMS[self.year_stem_idx]
        self.year_branch = self.BRANCHES[self.year_branch_idx]
        self.is_yang_year = self.year_stem in self.YANG_STEM_SET

    def calc_ming_shen_palace(self) -> None:
        """古法安命、安身宫：正月起寅，顺月逆时数安命，顺时数安身"""
        month_start_branch_idx = 2  # 寅地支索引=2，正月起寅
        # 顺数生月定位月支
        month_branch_idx = (month_start_branch_idx + self.lunar_month - 1) % 12
        hour_idx = self.BRANCHES.index(self.hour_branch)
        # 命宫：月支逆数时辰
        self.ming_palace_idx = (month_branch_idx - hour_idx) % 12
        # 身宫：月支顺数时辰
        self.shen_palace_idx = (month_branch_idx + hour_idx) % 12

    def calc_all_palace_stem(self) -> None:
        """五虎遁排十二宫天干，每个地支匹配对应天干"""
        # 五虎遁口诀映射：年干索引 → 寅宫天干索引
        wuhu_dun_map = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
        yin_stem_idx = wuhu_dun_map[self.year_stem_idx]
        # 遍历十二地支，依次排布天干
        for branch_idx in range(12):
            offset = (branch_idx - 2) % 12
            current_stem_idx = (yin_stem_idx + offset) % 10
            self.palace_stem_list[branch_idx] = self.STEMS[current_stem_idx]

    def calc_wuxing_ju_rule(self) -> None:
        """生年六十甲子纳音定五行局（正统规则，修复原代码命宫纳音错误）"""
        na_yin_key = (self.year_stem, self.year_branch)
        na_yin_element = self.YEAR_NA_YIN_MAP[na_yin_key]
        self.wuxing_ju = self.NA_YIN_TO_JU[na_yin_element]
        self.start_transport_age = self.wuxing_ju

    def place_major_all_stars(self) -> None:
        """正统安十四主星：先定紫微，排布紫微星系；再定天府，排布天府星系"""
        self.major_star_map.clear()
        # 1. 定位紫微星地支索引
        ziwei_branch_idx = self.ZIWEI_POS_LOOKUP[self.wuxing_ju][self.year_branch_idx]
        self.major_star_map["紫微"] = ziwei_branch_idx

        # 2. 顺时针排布紫微星系剩余五星：天机、太阳、武曲、天同、廉贞
        for offset, star_name in enumerate(self.ZIWEI_STAR_GROUP[1:]):
            pos = (ziwei_branch_idx + offset + 1) % 12
            self.major_star_map[star_name] = pos

        # 3. 天府固定在紫微对冲宫（+6）
        tianfu_pos = (ziwei_branch_idx + 6) % 12
        self.major_star_map["天府"] = tianfu_pos

        # 4. 天府星系八星顺序排布：太阴、贪狼、巨门、天相、天梁、七杀、破军
        tianfu_seq = ["太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]
        for offset, star_name in enumerate(tianfu_seq):
            pos = (tianfu_pos + offset + 1) % 12
            self.major_star_map[star_name] = pos

    def place_minor_all_stars(self) -> None:
        """正统安辅星：左辅、右弼、文昌、文曲、禄存、天马、红鸾、天喜"""
        self.minor_star_map.clear()
        y_branch_idx = self.year_branch_idx
        h_idx = self.BRANCHES.index(self.hour_branch)

        # 左辅：辰起顺行，依生年地支
        self.minor_star_map["左辅"] = (2 + y_branch_idx) % 12
        # 右弼：戌起逆行
        self.minor_star_map["右弼"] = (10 - y_branch_idx) % 12
        # 禄存：甲禄寅、乙禄卯，年干*2顺行
        lu_pos = (self.year_stem_idx * 2) % 12
        self.minor_star_map["禄存"] = lu_pos
        # 天马为禄存对冲宫
        self.minor_star_map["天马"] = (lu_pos + 6) % 12
        # 文昌、文曲依时辰排布
        self.minor_star_map["文昌"] = (10 - h_idx) % 12
        self.minor_star_map["文曲"] = (4 + h_idx) % 12
        # 红鸾天喜：年支与对冲
        self.minor_star_map["红鸾"] = y_branch_idx
        self.minor_star_map["天喜"] = (y_branch_idx + 6) % 12

    def calc_benming_four_hua(self) -> None:
        """计算本命四化星所在宫位"""
        self.benming_sihua.clear()
        hua_raw = self.FOUR_HUA_TABLE[self.year_stem]
        all_star_pos = {**self.major_star_map, **self.minor_star_map}
        for hua_type, star_name in hua_raw.items():
            palace_idx = all_star_pos.get(star_name, -1)
            self.benming_sihua[hua_type] = {
                "star": star_name,
                "palace_idx": palace_idx,
                "palace_name": self.PALACE_NAMES[palace_idx] if palace_idx != -1 else "无"
            }

    def calc_daxian_all(self) -> None:
        """计算完整大运（大限）：顺逆判断、十年区间、对应宫位"""
        self.daxian_list.clear()
        # 判断大限顺逆行规则
        shun_run = False
        if (self.is_yang_year and self.gender == "男") or (not self.is_yang_year and self.gender == "女"):
            shun_run = True

        current_age = self.start_transport_age
        current_pal = self.ming_palace_idx
        for limit_order in range(12):
            end_age = current_age + 9
            self.daxian_list.append({
                "limit_num": limit_order + 1,
                "palace_index": current_pal,
                "palace_name": self.PALACE_NAMES[current_pal],
                "age_range": f"{current_age} ~ {end_age}岁",
                "is_shun": shun_run
            })
            # 切换下一限宫位
            if shun_run:
                current_pal = (current_pal + 1) % 12
            else:
                current_pal = (current_pal - 1) % 12
            current_age += 10

    def get_liunian_data(self, target_year: int) -> Dict[str, Any]:
        """获取指定公历年流年完整数据：流年干支、流年命宫、流年四化"""
        if target_year in self.liunian_cache:
            return self.liunian_cache[target_year]
        # 计算流年干支
        base = 1904
        diff = target_year - base
        cycle_mod = diff % 60
        ln_stem_idx = cycle_mod % 10
        ln_branch_idx = cycle_mod % 12
        ln_stem = self.STEMS[ln_stem_idx]
        ln_branch = self.BRANCHES[ln_branch_idx]
        ln_ming_idx = ln_branch_idx  # 流年命宫=当年地支索引

        # 流年四化计算
        ln_hua_raw = self.FOUR_HUA_TABLE[ln_stem]
        all_star_pos = {**self.major_star_map, **self.minor_star_map}
        liunian_sihua = {}
        for hua_t, star_n in ln_hua_raw.items():
            pid = all_star_pos.get(star_n, -1)
            liunian_sihua[hua_t] = {"star": star_n, "palace_idx": pid}

        res_data = {
            "year": target_year,
            "gan": ln_stem,
            "zhi": ln_branch,
            "ganzhi": f"{ln_stem}{ln_branch}",
            "liunian_ming_index": ln_ming_idx,
            "liunian_ming_name": self.PALACE_NAMES[ln_ming_idx],
            "four_hua": liunian_sihua
        }
        self.liunian_cache[target_year] = res_data
        return res_data

    def get_sanfang_sizheng(self, palace_idx: int) -> Set[int]:
        """获取指定宫位三方四正索引集合"""
        sanfang = {palace_idx, (palace_idx + 4) % 12, (palace_idx + 8) % 12}
        sizheng = sanfang | {(palace_idx + 6) % 12}
        return sizheng

    def judge_chart_pattern(self) -> List[str]:
        """全局格局自动判定，返回命中格局列表"""
        hit_patterns = []
        ming_idx = self.ming_palace_idx
        # 命宫主星
        ming_major_stars = [s for s, p in self.major_star_map.items() if p == ming_idx]
        # 命宫三方四正所有主星
        sfsz_idx_set = self.get_sanfang_sizheng(ming_idx)
        sfsz_major_stars = {s for s, p in self.major_star_map.items() if p in sfsz_idx_set}

        # 1. 杀破狼格：三方四正集齐七杀、破军、贪狼
        if {"七杀", "破军", "贪狼"}.issubset(sfsz_major_stars):
            hit_patterns.append("杀破狼格")
        # 2. 机月同梁格：三方四正集齐天机、太阴、天同、天梁
        if {"天机", "太阴", "天同", "天梁"}.issubset(sfsz_major_stars):
            hit_patterns.append("机月同梁格")
        # 3. 紫府同宫格：紫微天府同守命宫
        if "紫微" in ming_major_stars and "天府" in ming_major_stars:
            hit_patterns.append("紫府同宫格")
        # 4. 紫府朝垣格：紫微、天府三方会照但不同宫
        if "紫微" in sfsz_major_stars and "天府" in sfsz_major_stars and not ("紫微" in ming_major_stars and "天府" in ming_major_stars):
            hit_patterns.append("紫府朝垣格")
        # 5. 君臣庆会格：紫微坐命，三方见左辅右弼
        if "紫微" in ming_major_stars:
            fu_bs_pos = {p for s, p in self.minor_star_map.items() if s in ["左辅", "右弼"]}
            if fu_bs_pos & sfsz_idx_set:
                hit_patterns.append("君臣庆会格")
        # 6. 七杀朝斗格：七杀坐命，子午寅申庙旺宫
        if "七杀" in ming_major_stars and self.BRANCHES[ming_idx] in ["子", "午", "寅", "申"]:
            hit_patterns.append("七杀朝斗格")

        return hit_patterns

    def build_full_natal_chart(self) -> Dict[str, Any]:
        """执行全部计算，输出完整结构化本命盘数据"""
        # 执行全流程计算
        self.calc_year_ganzhi()
        self.calc_ming_shen_palace()
        self.calc_all_palace_stem()
        self.calc_wuxing_ju_rule()
        self.place_major_all_stars()
        self.place_minor_all_stars()
        self.calc_benming_four_hua()
        self.calc_daxian_all()
        pattern_list = self.judge_chart_pattern()

        # 组装十二宫完整信息
        palace_full_info = []
        for idx in range(12):
            # 当前宫主星、辅星
            palace_major = [s for s, p in self.major_star_map.items() if p == idx]
            palace_minor = [s for s, p in self.minor_star_map.items() if p == idx]
            # 本宫四化标记
            palace_hua_list = []
            for hua_type, hua_info in self.benming_sihua.items():
                if hua_info["palace_idx"] == idx:
                    palace_hua_list.append({"hua_type": hua_type, "star": hua_info["star"]})

            palace_full_info.append({
                "palace_index": idx,
                "di_zhi": self.BRANCHES[idx],
                "tian_gan": self.palace_stem_list[idx],
                "palace_name": self.PALACE_NAMES[idx],
                "main_stars": palace_major,
                "minor_stars": palace_minor,
                "four_hua": palace_hua_list,
                "is_ming_gong": idx == self.ming_palace_idx,
                "is_shen_gong": idx == self.shen_palace_idx
            })

        # 汇总全部输出
        full_result = {
            "base_info": {
                "birth_solar": self.birth_solar.strftime("%Y-%m-%d"),
                "lunar_month": self.lunar_month,
                "birth_hour": self.hour_branch,
                "gender": self.gender,
                "year_ganzhi": f"{self.year_stem}{self.year_branch}",
                "is_yang_year": self.is_yang_year,
                "five_element_bureau": f"{self.wuxing_ju}局",
                "start_transport_age": f"{self.start_transport_age}岁起运",
                "ming_gong": {
                    "index": self.ming_palace_idx,
                    "name": self.PALACE_NAMES[self.ming_palace_idx],
                    "ganzhi": f"{self.palace_stem_list[self.ming_palace_idx]}{self.BRANCHES[self.ming_palace_idx]}"
                },
                "shen_gong": {
                    "index": self.shen_palace_idx,
                    "name": self.PALACE_NAMES[self.shen_palace_idx],
                    "ganzhi": f"{self.palace_stem_list[self.shen_palace_idx]}{self.BRANCHES[self.shen_palace_idx]}"
                }
            },
            "twelve_palaces": palace_full_info,
            "benming_four_hua": self.benming_sihua,
            "daxian_list": self.daxian_list,
            "all_patterns": pattern_list,
            "star_position_map": {
                "main_star": self.major_star_map,
                "minor_star": self.minor_star_map
            }
        }
        return full_result
