# -*- coding: utf-8 -*-#
import pandas as pd
import matplotlib.pyplot as plt
import os
import Filename

# ==== 基本参数设置 ====
folder_path = 'E:/work+study/DigSilent/DataTreating/Italy-data-csv+png'
csvfiles = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

col_x = 'U_pos_pu_time'                # 横坐标列名（可修改）
col_y = ['U_pos_pu','U_pos_pu','Ia_pos_pu',
		   'Ir_pos_pu','P_pos_pu',
           'Q_pos_pu','U_neg_pu','Ir_neg_pu']  # 纵坐标列名（可修改）

xlabel = "time/s"                # 横坐标文字
ylabel = "/.pu"                # 纵坐标文字

line_width = 1.5                   # 曲线粗细
figsize = (10, 10)                   # 图像尺寸 (宽, 高)，单位为英寸
fontsize=15                    # the size of label 
x_left=0
x_right=0
sub_col_num=2
sub_row_num=4

Filename.FileName.write_filenames(Filename.FileName(folder_path,csvfiles))
new_names=Filename.FileName.read_filenames(folder_path)
# ==== 读取数据 ====
for idx,filename in enumerate(csvfiles,1):
    csv_file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(csv_file_path)

    # name the png file with  the corresponding csv filename
    figure_name=f"{new_names[idx-1]}.png"

# ==== 绘图 ====

    fig, axes = plt.subplots(sub_row_num,sub_col_num,figsize=figsize)  
    for idx_2, ax in enumerate(axes.flat):
        ax.plot(df[col_x], df[col_y[idx_2]], linewidth=line_width)
        ax.set_xlabel(xlabel,fontsize=fontsize)
        ax.set_ylabel(f"{col_y[idx_2]+ylabel}",fontsize=fontsize)
        #ax.set_xlim(x_left,x_right)
        ax.grid(True, color='black', linestyle='--', linewidth=0.5)  

    plt.tight_layout()

    figuer_path=os.path.join(folder_path, figure_name)
    plt.savefig(figuer_path, dpi=300, bbox_inches='tight') 
    print(f"Plot: {figure_name}")
    #plt.show()



