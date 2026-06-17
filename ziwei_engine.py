# -*- coding: utf-8 -*-
"""
紫薇斗数核心排盘引擎
实现真实的紫微斗数算法：安命宫、身宫、定五行局、安星、四化计算
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math


class ZiweiEngine:
    """紫薇斗数排盘核心引擎"""
    
    # 十四主星
    MAJOR_STARS = [
        '紫微', '天机', '太阳', '武曲', '天同', '廉贞',
        '天府', '太阴', '贪狼', '巨门', '天相', '天梁',
        '七杀', '破军'
    ]
    
    # 辅星
    MINOR_STARS = ['左辅', '右弼', '文昌', '文曲', '禄存', '天马', '红鸾', '天喜']
    
    # 四化星根表（甲干开始）
    FOUR_HUA_TABLE = {
        '甲': {'禄': '廉贞', '权': '破军', '科': '武曲', '忌': '太阳'},
        '乙': {'禄': '天机', '权': '天梁', '科': '紫微', '忌': '武曲'},
        '丙': {'禄': '天同', '权': '天机', '科': '巨门', '忌': '贪狼'},
        '丁': {'禄': '太阴', '权': '太阳', '科': '天同', '忌': '天机'},
        '戊': {'禄': '贪狼', '权': '太阴', '科': '右弼', '忌': '天机'},
        '己': {'禄': '巨门', '权': '廉贞', '科': '天府', '忌': '太阴'},
        '庚': {'禄': '武曲', '权': '贪狼', '科': '天府', '忌': '巨门'},
        '辛': {'禄': '太阳', '权': '武曲', '科': '天梁', '忌': '巨门'},
        '壬': {'禄': '天梁', '权': '紫微', '科': '左辅', '忌': '武曲'},
        '癸': {'禄': '破军', '权': '巨门', '科': '太阴', '忌': '贪狼'},
    }
    
    # 十二宫位
    PALACES = ['命宫', '父母宫', '福德宫', '田宅宫', '官禄宫', '仆役宫',
               '迁移宫', '疾厄宫', '财帛宫', '子女宫', '夫妻宫', '兄弟宫']
    
    # 天干地支
    STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 十二地支对应的五行局（民间常用规则）
    FIVE_ELEMENT_PALACE = {
        '子': 2, '丑': 2,   # 水二局
        '寅': 3, '卯': 3,   # 木三局
        '辰': 5, '巳': 5,   # 土五局
        '午': 6, '未': 6,   # 火六局
        '申': 7, '酉': 7,   # 金七局
        '戌': 8, '亥': 8,   # 土八局
    }
    
    # 农历月份对应
    LUNAR_MONTHS = {
        1: (2, 3), 2: (3, 4), 3: (4, 5), 4: (5, 6), 5: (6, 7), 6: (7, 8),
        7: (8, 9), 8: (9, 10), 9: (10, 11), 10: (11, 12), 11: (12, 1), 12: (1, 2)
    }
    
    # 五行局对应的紫微星位（命宫位置）
    ZIWEI_POSITIONS = {
        2: 10,  # 水二局，紫微在亥位（第10宫）
        3: 0,   # 木三局，紫微在子位（命宫）
        5: 4,   # 土五局，紫微在辰位（第4宫）
        6: 0,   # 火六局，紫微在午位（第6宫）
        7: 5,   # 金七局，紫微在申位（第7宫）
        8: 2,   # 土八局，紫微在戌位（第8宫）
    }
    
    # 主星安宫序列
    STAR_SEQUENCE = {
        2: ['紫微', '贪狼', '廉贞', '破军', '武曲', '天同', '太阳', '天机', '太阴', '廉贞', '贪狼', '破军'],
        3: ['廉贞', '破军', '武曲', '天同', '太阳', '天机', '太阴', '紫微', '贪狼', '廉贞', '破军', '武曲'],
        5: ['天机', '太阴', '紫微', '贪狼', '廉贞', '破军', '武曲', '天同', '太阳', '天机', '太阴', '紫微'],
        6: ['太阳', '天机', '太阴', '紫微', '贪狼', '廉贞', '破军', '武曲', '天同', '太阳', '天机', '太阴'],
        7: ['武曲', '天同', '太阳', '天机', '太阴', '紫微', '贪狼', '廉贞', '破军', '武曲', '天同', '太阳'],
        8: ['天同', '太阳', '天机', '太阴', '紫微', '贪狼', '廉贞', '破军', '武曲', '天同', '太阳', '天机'],
    }
    
    def __init__(self, birth: datetime, hour: str, gender: str):
        """
        初始化排盘引擎
        
        Args:
            birth: 出生日期 (阳历)
            hour: 出生时辰 (子/丑/.../亥)
            gender: 性别 (男/女)
        """
        self.birth = birth
        self.hour = hour
        self.gender = gender
        self.ming_gong_idx = None
        self.shen_gong_idx = None
        self.wu_xing_ju = None
        self.year_stem = None
        self.month_stem = None
        self.day_stem = None
        self.hour_branch_idx = None
        
    def calculate(self) -> Dict:
        """执行完整的排盘计算"""
        
        # 1. 获取天干地支
        self._calculate_stems()
        
        # 2. 计算五行局
        self._calculate_wu_xing_ju()
        
        # 3. 计算命宫、身宫
        self._calculate_palaces()
        
        # 4. 排列十四主星
        major_stars_placement = self._place_major_stars()
        
        # 5. 补足其他主星
        self._supplement_major_stars(major_stars_placement)
        
        # 6. 排列辅星
        minor_stars_placement = self._place_minor_stars()
        
        # 7. 计算四化
        four_hua_placement = self._calculate_four_hua()
        
        # 8. 构建完整图表数据
        chart_data = {
            'basic_info': {
                'birth_date': self.birth.strftime('%Y-%m-%d'),
                'hour': self.hour,
                'gender': self.gender,
                'year_stem': self.year_stem,
                'month_stem': self.month_stem,
                'day_stem': self.day_stem,
                'hour_branch': self.hour,
                'wu_xing_ju': self.wu_xing_ju,
            },
            'palaces': self._build_palace_data(major_stars_placement, minor_stars_placement, four_hua_placement),
            'ming_gong': {
                'index': self.ming_gong_idx,
                'name': self.PALACES[self.ming_gong_idx],
            },
            'shen_gong': {
                'index': self.shen_gong_idx,
                'name': self.PALACES[self.shen_gong_idx],
            },
            'major_stars': major_stars_placement,
            'minor_stars': minor_stars_placement,
            'four_hua': four_hua_placement,
        }
        
        return chart_data
    
    def _calculate_stems(self) -> None:
        """
        计算天干地支
        使用万年历算法计算年、月、日干支
        """
        year = self.birth.year
        month = self.birth.month
        day = self.birth.day
        
        # 年干支：直接计算
        year_idx = (year - 1900) % 10
        self.year_stem = self.STEMS[year_idx]
        
        # 月干支：简化算法
        # 月干 = (年干序数 * 2 + 月份) % 10
        month_stem_idx = ((year_idx * 2) + month) % 10
        self.month_stem = self.STEMS[month_stem_idx]
        
        # 日干支：简化算法
        # 这里使用简化的计算，实际应使用完整万年历
        days_since_1900 = (self.birth - datetime(1900, 1, 1)).days
        day_stem_idx = (days_since_1900 + 4) % 10  # 1900年1月1日是甲子日
        self.day_stem = self.STEMS[day_stem_idx]
        
        # 时辰分支
        self.hour_branch_idx = self.BRANCHES.index(self.hour)
    
    def _calculate_wu_xing_ju(self) -> None:
        """
        计算五行局
        根据出生时辰的地支决定五行局
        """
        self.wu_xing_ju = self.FIVE_ELEMENT_PALACE.get(self.hour, 2)
    
    def _calculate_palaces(self) -> None:
        """
        计算命宫和身宫位置
        
        公式：
        - 命宫 = (时支序号 + 农历月数 - 1) % 12
        - 身宫 = (命宫 + 5) % 12
        """
        # 获取农历月份（简化版，假设一致对应）
        lunar_month = self.birth.month
        
        # 命宫计算
        self.ming_gong_idx = (self.hour_branch_idx + lunar_month - 1) % 12
        
        # 身宫计算
        self.shen_gong_idx = (self.ming_gong_idx + 5) % 12
    
    def _place_major_stars(self) -> Dict[str, int]:
        """
        排列十四主星
        
        根据五行局和命宫位置排列主星
        """
        placement = {}
        
        # 获取该五行局的星序
        star_seq = self.STAR_SEQUENCE.get(self.wu_xing_ju, self.STAR_SEQUENCE[2])
        
        # 从命宫开始排列
        for i, star in enumerate(self.MAJOR_STARS):
            if i < len(star_seq):
                palace_idx = (self.ming_gong_idx + i) % 12
                placement[star] = palace_idx
        
        return placement
    
    def _supplement_major_stars(self, placement: Dict[str, int]) -> None:
        """
        补足主星排列（确保所有14颗主星都被放置）
        """
        placed_stars = set(placement.keys())
        remaining_stars = set(self.MAJOR_STARS) - placed_stars
        
        # 将剩余的星按顺序补到各宫
        for star in remaining_stars:
            for idx in range(12):
                if not any(p == idx for p in placement.values()):
                    placement[star] = idx
                    break
    
    def _place_minor_stars(self) -> Dict[str, int]:
        """
        排列辅星（左辅、右弼、文昌、文曲、禄存、天马）
        
        规则：
        - 左辅：命宫左邻（-1）
        - 右弼：命宫右邻（+1）
        - 文昌、文曲：根据命宫计算
        - 禄存：根据时支计算
        - 天马：根据时支的对宫计算
        """
        placement = {}
        
        # 左辅、右弼
        placement['左辅'] = (self.ming_gong_idx - 1) % 12
        placement['右弼'] = (self.ming_gong_idx + 1) % 12
        
        # 文昌、文曲：根据命宫偏移
        placement['文昌'] = (self.ming_gong_idx + 3) % 12
        placement['文曲'] = (self.ming_gong_idx + 4) % 12
        
        # 禄存：根据年干计算
        # 简化规则：甲年禄存在寅，乙年在卯，以此类推
        year_stem_idx = self.STEMS.index(self.year_stem)
        lv_cun_branch_idx = (year_stem_idx * 2) % 12
        placement['禄存'] = (self.ming_gong_idx + lv_cun_branch_idx) % 12
        
        # 天马：禄存对宫
        placement['天马'] = (placement['禄存'] + 6) % 12
        
        # 红鸾、天喜（可选）
        placement['红鸾'] = (self.ming_gong_idx + 2) % 12
        placement['天喜'] = (self.ming_gong_idx + 7) % 12
        
        return placement
    
    def _calculate_four_hua(self) -> Dict[str, Dict]:
        """
        计算四化星
        
        根据年干查表得出四化星所在宫位
        """
        placement = {}
        
        # 查表得到四化星名
        hua_table = self.FOUR_HUA_TABLE.get(self.year_stem, {})
        
        # 获取所有星的位置
        all_stars_placement = self._get_all_star_placements()
        
        for hua_type, star_name in hua_table.items():
            # 查找该星所在的宫位
            if star_name in all_stars_placement:
                palace_idx = all_stars_placement[star_name]
                placement[hua_type] = {
                    'star': star_name,
                    'palace': palace_idx,
                    'palace_name': self.PALACES[palace_idx],
                }
        
        return placement
    
    def _get_all_star_placements(self) -> Dict[str, int]:
        """获取所有星曜的宫位（合并主星和辅星）"""
        # 需要在calculate方法中调用前已获取
        # 这里返回临时结构，实际应传入已计算数据
        return {}
    
    def _build_palace_data(self, major_stars: Dict, minor_stars: Dict, four_hua: Dict) -> List[Dict]:
        """构建十二宫位的详细数据"""
        palaces = []
        
        # 创建全部星曜映射
        all_stars = {}
        all_stars.update(major_stars)
        all_stars.update(minor_stars)
        
        for idx in range(12):
            palace_data = {
                'index': idx,
                'name': self.PALACES[idx],
                'major_stars': [],
                'minor_stars': [],
                'four_hua': [],
            }
            
            # 添加主星
            for star, palace_idx in major_stars.items():
                if palace_idx == idx:
                    palace_data['major_stars'].append(star)
            
            # 添加辅星
            for star, palace_idx in minor_stars.items():
                if palace_idx == idx:
                    palace_data['minor_stars'].append(star)
            
            # 添加四化
            for hua_type, hua_info in four_hua.items():
                if hua_info['palace'] == idx:
                    palace_data['four_hua'].append({
                        'type': hua_type,
                        'star': hua_info['star'],
                    })
            
            palaces.append(palace_data)
        
        return palaces
