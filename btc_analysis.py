from Chan import CChan
from ChanConfig import CChanConfig
from Common.CEnum import AUTYPE, DATA_SRC, KL_TYPE
from Plot.PlotDriver import CPlotDriver

if __name__ == "__main__":
    # BTC/USDT symbol for Binance
    code = "BTC/USDT"
    begin_time = "2024-01-01"
    end_time = None
    data_src = DATA_SRC.CCXT
    lv_list = [KL_TYPE.K_DAY]

    config = CChanConfig({
        "bi_strict": True,
        "trigger_step": False,
        "skip_step": 0,
        "divergence_rate": float("inf"),
        "bsp2_follow_1": False,
        "bsp3_follow_1": False,
        "min_zs_cnt": 0,
        "bs1_peak": False,
        "macd_algo": "peak",
        "bs_type": '1,2,3a,1p,2s,3b',
        "print_warning": True,
        "zs_algo": "normal",
    })

    plot_config = {
        "plot_kline": True,
        "plot_kline_combine": True,
        "plot_bi": True,
        "plot_seg": True,
        "plot_eigen": False,
        "plot_zs": True,
        "plot_macd": True,
        "plot_mean": False,
        "plot_channel": False,
        "plot_bsp": True,
        "plot_extrainfo": False,
        "plot_demark": False,
        "plot_marker": False,
        "plot_rsi": False,
        "plot_kdj": False,
    }

    plot_para = {
        "seg": {
            "plot_trendline": True,
        },
        "bi": {
            "show_num": True,
            "disp_end": True,
        },
        "figure": {
            "x_range": 200,
        },
        "marker": {}
    }

    chan = CChan(
        code=code,
        begin_time=begin_time,
        end_time=end_time,
        data_src=data_src,
        lv_list=lv_list,
        config=config,
        autype=AUTYPE.NONE,  # No price adjustment for crypto
    )

    plot_driver = CPlotDriver(
        chan,
        plot_config=plot_config,
        plot_para=plot_para,
    )
    plot_driver.figure.show()
    plot_driver.save2img("./btc_chan_analysis.png")
    
    # Print some analysis results
    print("BTC Chan Analysis Complete!")
    print(f"Number of strokes (bi): {len(chan[0].bi_list)}")
    print(f"Number of segments (seg): {len(chan[0].seg_list)}")
    print(f"Number of centers (zs): {len(chan[0].zs_list)}")
    
    bsp_points = chan[0].bs_point_lst.getSortedBspList()
    print(f"Number of buy/sell points: {len(bsp_points)}")
    
    for i, point in enumerate(bsp_points[:5]):  # Show first 5 points
        print(f"Point {i+1}: {point.type} at {point.klu.time} - price {point.klu.close}")