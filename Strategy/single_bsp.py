from typing import List
from Common.CEnum import KL_TYPE
from Strategy.CStrategyBase import CStrategyBase
from Chan import CChan
from ChanConfig import CChanConfig


class CSingleBSPStrategy(CStrategyBase):
    """
    缠论单单周期单买卖点策略
    
    给定一个股票列表，筛选出满足单个缠论买卖点策略的股票
    示例1：日线级别出现二买点
    示例2：30分钟级别出现一买点
    """
    
    def __init__(self, 
                 kl_type: KL_TYPE,
                 bsp_type: str,
                 start_time: str,
                 recent_n_klines: int):
        """
        初始化策略参数
        
        Args:
            kl_type: K线级别（日线、30分钟等）
            bsp_type: 买卖点类型（一买、二买、三买等）
            start_time: 获取K线数据的起始时间
            recent_n_klines: 买卖点出现在最后的N根K线内
        """
        self.kl_type = kl_type
        self.bsp_type = bsp_type
        self.start_time = start_time
        self.recent_n_klines = recent_n_klines
        
    def filter_stocks(self, stock_list: List[str], data_src) -> List[str]:
        """
        筛选满足条件的股票
        
        Args:
            stock_list: 股票列表
            data_src: 数据源
            
        Returns:
            满足条件的股票列表
        """
        qualified_stocks = []
        
        # 基础配置
        config = CChanConfig({
            "bs_type": self._get_bsp_type_str(),
            "print_warning": False
        })
        
        for stock_code in stock_list:
            try:
                chan = CChan(
                    code=stock_code,
                    begin_time=self.start_time,
                    data_src=data_src,
                    lv_list=[self.kl_type],
                    config=config
                )
                
                if self._has_bsp_in_recent_klines(chan):
                    qualified_stocks.append(stock_code)
                    
            except Exception:
                # 如果数据获取或分析失败，跳过该股票
                continue
                
        return qualified_stocks
    
    def _get_bsp_type_str(self) -> str:
        """获取买卖点类型的字符串表示"""
        return self.bsp_type
    
    def _has_bsp_in_recent_klines(self, chan: CChan) -> bool:
        """
        检查在最近N根K线内是否出现指定买卖点
        """
        kline_list = chan[self.kl_type]
        if not kline_list:
            return False
            
        # 获取指定级别的买卖点
        bsp_points = kline_list.bs_point_lst.getSortedBspList()
        if not bsp_points:
            return False
            
        # 获取最近N根K线的范围
        total_klines = len(kline_list)
        start_idx = max(0, total_klines - self.recent_n_klines)
        
        # 检查买卖点是否在指定范围内
        for bsp in bsp_points:
            for seg_idx in range(start_idx, total_klines):
                current_seg = kline_list[seg_idx] if seg_idx < len(kline_list) else None
                if current_seg and bsp.klu.idx >= current_seg.lst[0].idx:
                    return True
                    
        return False