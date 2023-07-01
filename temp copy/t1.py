import _imports
import best4nicegui.bi as bi
import best4nicegui.reactive as rui
import pandas as pd
from nicegui import ui


from pyecharts import options as opts
from pyecharts.charts import Bar, Line

df = pd.read_excel(r"E:\working\dataset\某咖啡公司销售数据.xlsx")


ds = bi.create_source(df)

ds["产品名称"].select(multiple=True, clearable=True)


ref_chart_color = rui.color_picker()

chart_type = rui.radio(["bar", "line"])
chart_title_set = rui.switch("显示图表标题", value=True)
chart_title_input = rui.input("图表标题")


chart1 = ds.echarts()


@chart1.build_options_pyecharts
def on_df_changed(df: pd.DataFrame):
    df = df.groupby("产品类别").agg({"销售额": "mean"}).reset_index()

    c = Bar() if chart_type.value == "bar" else Line()

    c = (
        c.add_xaxis(df["产品类别"].tolist())
        .add_yaxis("系列1", df["销售额"].tolist(), color=ref_chart_color.value)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # .set_global_opts(title_opts=opts.TitleOpts(title="Bar-堆叠数据（部分）"))
    )

    print("chart_title_set")

    if chart_title_set.value:
        print("in")
        c.set_global_opts(title_opts=opts.TitleOpts(title=chart_title_input.value))

    return c


ds.table()

ui.run()
