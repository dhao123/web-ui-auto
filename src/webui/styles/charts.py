"""
图表主题配置 - ECharts 配置生成器
"""
import json
from typing import List, Dict, Any, Optional


def get_echarts_theme(mode: str = "light") -> Dict[str, Any]:
    """获取ECharts主题配置"""
    is_dark = mode == "dark"
    
    return {
        "color": [
            "#7B8BE8" if is_dark else "#5B6BD1",  # 主色
            "#73D13D" if is_dark else "#52C41A",  # 成功色
            "#FFD666" if is_dark else "#FAAD14",  # 警告色
            "#FF7875" if is_dark else "#F5222D",  # 危险色
            "#69C0FF" if is_dark else "#4A90E2",  # 信息色
            "#9D7BDE" if is_dark else "#764ba2",  # 紫色
        ],
        "backgroundColor": "transparent",
        "textStyle": {
            "color": "#E8E8E8" if is_dark else "#262626",
            "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        },
        "title": {
            "textStyle": {
                "color": "#E8E8E8" if is_dark else "#262626",
                "fontWeight": 600,
            },
            "subtextStyle": {
                "color": "#8C8C8C",
            },
        },
        "tooltip": {
            "backgroundColor": "#2D2D2D" if is_dark else "rgba(255, 255, 255, 0.95)",
            "borderColor": "#404040" if is_dark else "#E8E8E8",
            "borderWidth": 1,
            "textStyle": {
                "color": "#E8E8E8" if is_dark else "#262626",
            },
        },
        "legend": {
            "textStyle": {
                "color": "#ACACAC" if is_dark else "#595959",
            },
        },
        "axisLine": {
            "lineStyle": {
                "color": "#404040" if is_dark else "#E8E8E8",
            },
        },
        "splitLine": {
            "lineStyle": {
                "color": "#333333" if is_dark else "#F0F0F0",
                "type": "dashed",
            },
        },
        "axisLabel": {
            "color": "#8C8C8C",
            "fontSize": 12,
        },
    }


def build_line_chart_option(
    dates: List[str],
    values: List[float],
    title: str = "趋势图",
    mode: str = "light",
    show_area: bool = True,
) -> Dict[str, Any]:
    """构建折线图配置"""
    theme = get_echarts_theme(mode)
    primary_color = theme["color"][0]
    is_dark = mode == "dark"
    
    area_start = "rgba(123, 139, 232, 0.3)" if is_dark else "rgba(91, 107, 209, 0.3)"
    area_end = "rgba(123, 139, 232, 0.05)" if is_dark else "rgba(91, 107, 209, 0.05)"
    
    option = {
        "tooltip": {
            "trigger": "axis",
            **theme["tooltip"],
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "top": "10%",
            "containLabel": True,
        },
        "xAxis": {
            "type": "category",
            "data": dates,
            "boundaryGap": False,
            "axisLine": theme["axisLine"],
            "axisLabel": theme["axisLabel"],
        },
        "yAxis": {
            "type": "value",
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "splitLine": theme["splitLine"],
            "axisLabel": theme["axisLabel"],
        },
        "series": [{
            "name": title,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "data": values,
            "itemStyle": {"color": primary_color},
            "lineStyle": {"width": 3, "color": primary_color},
        }],
    }
    
    if show_area:
        option["series"][0]["areaStyle"] = {
            "color": {
                "type": "linear",
                "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [
                    {"offset": 0, "color": area_start},
                    {"offset": 1, "color": area_end},
                ],
            },
        }
    
    return option


def build_pie_chart_option(
    data: List[Dict[str, Any]],
    title: str = "占比分布",
    mode: str = "light",
    show_legend: bool = True,
    inner_radius: str = "40%",
    outer_radius: str = "70%",
) -> Dict[str, Any]:
    """构建饼图配置
    
    Args:
        data: 数据列表，格式为 [{"name": "名称", "value": 数值}, ...]
        title: 图表标题
        mode: 主题模式 "light" 或 "dark"
        show_legend: 是否显示图例
        inner_radius: 内半径（设置后变为环形图）
        outer_radius: 外半径
    """
    theme = get_echarts_theme(mode)
    
    return {
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)",
            **theme["tooltip"],
        },
        "legend": {
            "show": show_legend,
            "orient": "vertical",
            "left": "left",
            **theme["legend"],
        },
        "series": [{
            "name": title,
            "type": "pie",
            "radius": [inner_radius, outer_radius],
            "center": ["60%", "50%"],
            "avoidLabelOverlap": True,
            "itemStyle": {
                "borderRadius": 4,
                "borderColor": "#fff" if mode == "light" else "#1a1a1a",
                "borderWidth": 2,
            },
            "label": {
                "show": True,
                "formatter": "{b}: {d}%",
                "color": theme["textStyle"]["color"],
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": 14,
                    "fontWeight": "bold",
                },
            },
            "data": data,
        }],
        "color": theme["color"],
    }


def build_bar_chart_option(
    categories: List[str],
    values: List[float],
    title: str = "柱状图",
    mode: str = "light",
    horizontal: bool = False,
) -> Dict[str, Any]:
    """构建柱状图配置"""
    theme = get_echarts_theme(mode)
    primary_color = theme["color"][0]
    
    x_axis = {
        "type": "value" if horizontal else "category",
        "data": None if horizontal else categories,
        "axisLine": theme["axisLine"],
        "axisLabel": theme["axisLabel"],
    }
    
    y_axis = {
        "type": "category" if horizontal else "value",
        "data": categories if horizontal else None,
        "axisLine": {"show": False} if not horizontal else theme["axisLine"],
        "axisTick": {"show": False},
        "splitLine": theme["splitLine"] if not horizontal else {"show": False},
        "axisLabel": theme["axisLabel"],
    }
    
    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            **theme["tooltip"],
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "top": "10%",
            "containLabel": True,
        },
        "xAxis": x_axis,
        "yAxis": y_axis,
        "series": [{
            "name": title,
            "type": "bar",
            "barWidth": "60%",
            "data": values,
            "itemStyle": {
                "color": primary_color,
                "borderRadius": [4, 4, 0, 0] if not horizontal else [0, 4, 4, 0],
            },
        }],
    }


def build_gauge_chart_option(
    value: float,
    title: str = "完成率",
    mode: str = "light",
    max_value: float = 100,
    unit: str = "%",
) -> Dict[str, Any]:
    """构建仪表盘配置"""
    theme = get_echarts_theme(mode)
    is_dark = mode == "dark"
    
    return {
        "series": [{
            "type": "gauge",
            "startAngle": 180,
            "endAngle": 0,
            "min": 0,
            "max": max_value,
            "splitNumber": 5,
            "axisLine": {
                "lineStyle": {
                    "width": 15,
                    "color": [
                        [0.3, "#FF6E76"],
                        [0.7, "#FDDD60"],
                        [1, "#7CFFB2"],
                    ],
                },
            },
            "pointer": {
                "itemStyle": {
                    "color": theme["color"][0],
                },
            },
            "axisTick": {
                "distance": -15,
                "length": 8,
                "lineStyle": {
                    "color": "#404040" if is_dark else "#E8E8E8",
                    "width": 2,
                },
            },
            "splitLine": {
                "distance": -20,
                "length": 15,
                "lineStyle": {
                    "color": "#404040" if is_dark else "#E8E8E8",
                    "width": 3,
                },
            },
            "axisLabel": {
                "color": theme["textStyle"]["color"],
                "distance": 25,
                "fontSize": 12,
            },
            "detail": {
                "valueAnimation": True,
                "formatter": f"{{value}}{unit}",
                "color": theme["textStyle"]["color"],
                "fontSize": 24,
                "offsetCenter": [0, "70%"],
            },
            "title": {
                "offsetCenter": [0, "90%"],
                "fontSize": 14,
                "color": theme["textStyle"]["color"],
            },
            "data": [{"value": value, "name": title}],
        }],
    }


def generate_chart_html(
    chart_id: str,
    option: Dict[str, Any],
    width: str = "100%",
    height: str = "320px",
) -> str:
    """生成图表HTML代码
    
    Args:
        chart_id: 图表DOM元素ID
        option: ECharts配置对象
        width: 图表宽度
        height: 图表高度
    """
    option_json = json.dumps(option)
    
    return f"""
    <div id="{chart_id}" style="width: {width}; height: {height};"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        (function() {{
            var chartDom = document.getElementById('{chart_id}');
            if (!chartDom) return;
            
            var myChart = echarts.init(chartDom);
            var option = {option_json};
            myChart.setOption(option);
            
            // 响应式调整
            window.addEventListener('resize', function() {{
                myChart.resize();
            }});
        }})();
    </script>
    """


def generate_line_chart_html(
    chart_id: str,
    dates: List[str],
    values: List[float],
    title: str = "趋势图",
    mode: str = "light",
    height: str = "320px",
) -> str:
    """生成折线图HTML代码"""
    option = build_line_chart_option(dates, values, title, mode)
    return generate_chart_html(chart_id, option, height=height)


def generate_pie_chart_html(
    chart_id: str,
    data: List[Dict[str, Any]],
    title: str = "占比分布",
    mode: str = "light",
    height: str = "280px",
) -> str:
    """生成饼图HTML代码"""
    option = build_pie_chart_option(data, title, mode)
    return generate_chart_html(chart_id, option, height=height)


def generate_bar_chart_html(
    chart_id: str,
    categories: List[str],
    values: List[float],
    title: str = "柱状图",
    mode: str = "light",
    height: str = "280px",
    horizontal: bool = False,
) -> str:
    """生成柱状图HTML代码"""
    option = build_bar_chart_option(categories, values, title, mode, horizontal)
    return generate_chart_html(chart_id, option, height=height)
