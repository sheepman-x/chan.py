#!/usr/bin/env python3

import json
import sys
from typing import Dict, List, Any
from Common.CEnum import KL_TYPE, DATA_SRC
from Strategy.single_bsp import CSingleBSPStrategy


def load_config(config_file: str) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_single_bsp_strategy(config: Dict[str, Any]) -> List[str]:
    """运行单单周期单买卖点策略"""
    strategy_config = config['strategy_config']
    
    # 转换枚举类型
    kl_type = KL_TYPE[strategy_config['kl_type']]
    bsp_type = strategy_config['bs_type']
    data_src = DATA_SRC[strategy_config['data_src']]
    
    # 创建策略实例
    strategy = CSingleBSPStrategy(
        kl_type=kl_type,
        bsp_type=bsp_type,
        start_time=strategy_config['start_time'],
        recent_n_klines=strategy_config['recent_n_klines']
    )
    
    # 执行策略
    result = strategy.filter_stocks(
        stock_list=config['stocks'],
        data_src=data_src
    )
    
    return result


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python run_strategy.py <config_file.json>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        # 加载配置
        config = load_config(config_file)
        
        # 根据策略类型调用相应函数
        strategy_name = config.get('strategy_type', 'single_bsp')
        
        if strategy_name == 'single_bsp':
            result = run_single_bsp_strategy(config)
        else:
            print(f"不支持的策略类型: {strategy_name}")
            sys.exit(1)
        
        # 输出结果
        print("=" * 50)
        print(f"策略结果:")
        print(f"策略类型: {strategy_name}")
        print(f"满足条件的股票数量: {len(result)}")
        print(f"股票列表: {result}")
        print("=" * 50)
        
    except FileNotFoundError:
        print(f"配置文件不存在: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"配置文件格式错误: {config_file}")
        sys.exit(1)
    except KeyError as e:
        print(f"配置文件缺少必要字段: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"运行策略时发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()