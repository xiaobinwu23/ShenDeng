
# 根据Excel表得到条形图
# 导入绘图模块
import matplotlib
import matplotlib.pyplot as plt
from xlrd import open_workbook

# 读Excel文档数据
x_data1=[]
y_data1=[]
wb = open_workbook(r'E:\1AAA\58同城-上海-计算机软件开发-能力需求.xls')
for s in wb.sheets():
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row,col).value)
        x_data1.append(str(values[0]))
        y_data1.append(int(values[1]))

# 中文乱码的处理
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

plt.rcParams['figure.figsize'] = (12.0, 10.0)  # 调整图片的整体大小
# 绘图
plt.barh(range(len(y_data1)), y_data1, align='center', color='steelblue', alpha=0.8)
# 添加轴标签
plt.xlabel('出现频数', fontproperties=zhfont1, fontsize=10,)  # y坐标注释
plt.ylabel('能力', fontproperties=zhfont1)  # x坐标注释
# 添加标题
plt.title('58同城-上海-计算机软件开发-需求能力分析', fontproperties=zhfont1)
# 添加刻度标签
plt.yticks(range(len(x_data1)), x_data1, fontproperties=zhfont1)
# 设置Y轴的刻度范围
# plt.ylim([1, 50])
# plt.xlim([1, 200])

# 为每个条形图添加数值标签
for x, y in enumerate(y_data1):
    plt.text(x, y + 100, '%s' % round(y, 1), ha='center')

# 显示图形
plt.show()