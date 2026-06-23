#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫薇斗数排盘脚本 - AnythingLLM 知识库版本
支持基础排盘、断语生成、Markdown/JSON 输出
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import pandas as pd
from ziwei_engine import ZiweiEngine
from output_formatter import MarkdownFormatter, JSONFormatter


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="紫薇斗数排盘工具 - 为 AnythingLLM 生成知识库内容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：

  1. 单个排盘
     python main.py --birth 1990-01-01 --hour 子 --gender 男

  2. 批量处理 CSV
     python main.py --batch batch.csv --output ./outputs

  3. 仅输出 Markdown
     python main.py --birth 2000-06-15 --hour 午 --gender 女 --format md

  4. 仅输出 JSON
     python main.py --birth 1995-12-25 --hour 申 --gender 男 --format json
        """
    )
    
    parser.add_argument(
        '--birth',
        type=str,
        help='出生日期 (格式: YYYY-MM-DD，例: 1990-01-01)'
    )
    parser.add_argument(
        '--hour',
        type=str,
        choices=['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'],
        help='出生时辰 (例: 子、午、申等)'
    )
    parser.add_argument(
        '--gender',
        type=str,
        choices=['男', '女'],
        help='性别 (男/女)'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='批量处理 CSV 文件路径'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./outputs',
        help='输出目录 (默认: ./outputs)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['both', 'md', 'json'],
        default='both',
        help='输出格式 (both/md/json，默认: both)'
    )
    
    return parser.parse_args()


def validate_birth_date(birth_str: str) -> Optional[datetime]:
    """验证并解析出生日期"""
    try:
        return datetime.strptime(birth_str, '%Y-%m-%d')
    except ValueError:
        print(f"✗ 日期格式错误: {birth_str}（应为 YYYY-MM-DD 格式）")
        return None


def process_single_birth(
    birth_date: str,
    hour: str,
    gender: str,
    output_dir: Path,
    output_format: str = 'both'
) -> bool:
    """处理单个排盘"""
    try:
        birth = validate_birth_date(birth_date)
        if birth is None:
            return False
        
        print(f"  处理: {birth_date} {hour}时 {gender}")
        
        engine = ZiweiEngine(birth, hour, gender)
        chart_data = engine.calculate()
        
        filename_base = f"{birth_date}_{hour}_{gender}"
        
        if output_format in ['both', 'md']:
            md_formatter = MarkdownFormatter(chart_data)
            md_content = md_formatter.format()
            md_file = output_dir / f"{filename_base}.md"
            md_file.write_text(md_content, encoding='utf-8')
            print(f"    ✓ Markdown: {md_file.name}")
        
        if output_format in ['both', 'json']:
            json_formatter = JSONFormatter(chart_data)
            json_content = json_formatter.format()
            json_file = output_dir / f"{filename_base}.json"
            json_file.write_text(json_content, encoding='utf-8')
            print(f"    ✓ JSON: {json_file.name}")
        
        return True
        
    except Exception as e:
        print(f"    ✗ 错误: {e}")
        return False


def process_batch(batch_file: str, output_dir: Path, output_format: str = 'both') -> None:
    """批量处理 CSV 文件"""
    try:
        df = pd.read_csv(batch_file, encoding='utf-8')
        required_cols = ['birth_date', 'hour', 'gender']
        if not all(col in df.columns for col in required_cols):
            print(f"✗ CSV 文件格式错误，需要列: {', '.join(required_cols)}")
            return
        
        total = len(df)
        success_count = 0
        print(f"\n开始批量处理 {total} 条记录...\n")
        
        for idx, row in df.iterrows():
            birth_date = str(row['birth_date']).strip()
            hour = str(row['hour']).strip()
            gender = str(row['gender']).strip()
            if process_single_birth(birth_date, hour, gender, output_dir, output_format):
                success_count += 1
        
        print(f"\n✓ 完成: {success_count}/{total} 条记录成功处理")
        
    except FileNotFoundError:
        print(f"✗ 批量文件不存在: {batch_file}")
    except Exception as e:
        print(f"✗ 批量处理错误: {e}")


def main():
    """主函数"""
    args = parse_arguments()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("紫薇斗数排盘工具 - AnythingLLM 知识库版本")
    print("="*60 + "\n")
    
    if args.birth and args.hour and args.gender:
        print("单个排盘模式")
        print(f"出生日期: {args.birth}")
        print(f"出生时辰: {args.hour}时")
        print(f"性别: {args.gender}")
        print(f"输出格式: {args.format}")
        print(f"输出目录: {output_dir}\n")
        
        if process_single_birth(args.birth, args.hour, args.gender, output_dir, args.format):
            print("\n✓ 排盘完成")
        else:
            print("\n✗ 排盘失败")
            sys.exit(1)
    elif args.batch:
        print("批量处理模式")
        print(f"批量文件: {args.batch}")
        print(f"输出格式: {args.format}")
        print(f"输出目录: {output_dir}\n")
        process_batch(args.batch, output_dir, args.format)
    else:
        print("✗ 错误: 请提供参数")
        print("  - 单个排盘: --birth YYYY-MM-DD --hour 时辰 --gender 男/女")
        print("  - 批量处理: --batch 文件.csv")
        print("\n使用 -h 查看详细帮助")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✓ 所有处理完成")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
