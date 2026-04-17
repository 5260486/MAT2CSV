import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os

class DataSegment:
    def __init__(self,voltage_number=1, sensitivity=1.5, extend_before=10, extend_after=10, 
                 min_segment_length=20, smooth_window=51, polyorder=3):
        """
        初始化连续电压突变检测器
        
        参数:
            sensitivity: 检测敏感度(值越大越敏感)
            extend_before: 第一个突变点前扩展的点数
            extend_after: 最后一个突变点后扩展的点数
            min_segment_length: 最小段长度
            smooth_window: 平滑窗口大小
            polyorder: 平滑多项式阶数
        """
        self.voltage_number=voltage_number

        self.sensitivity = sensitivity
        self.extend_before = extend_before
        self.extend_after = extend_after
        self.min_segment_length = min_segment_length
        self.smooth_window = smooth_window
        self.polyorder = polyorder
        
    def detect_continuous_changes(self, input_file, output_dir=None, plot_results=True):
        """
        检测CSV文件中的连续电压突变并提取整个变化段
        
        参数:
            input_file: 输入CSV文件路径
            output_dir: 输出目录
            plot_results: 是否绘制结果图表
        
        返回:
            continuous_segment: 连续突变段数据
            change_points: 所有突变点位置列表
        """
        # 读取CSV文件
        try:
            self.df = pd.read_csv(input_file)
            self.input_file = input_file
            print(f"成功读取文件: {input_file}")
            print(f"数据形状: {self.df.shape}")
            print(f"列名: {list(self.df.columns)}")
        except Exception as e:
            print(f"读取CSV文件失败: {e}")
            return None, []
        
        # 检查数据列
        if len(self.df.columns) < 2:
            print("错误: CSV文件需要至少包含两列")
            return None, []
        
        # 提取第一列时间数据，和其他列的数值数据
        self.time_col = self.df.columns[0]
        self.time_data = self.df[self.time_col].values

        self.value_col = self.df.columns[self.voltage_number]
        self.value_data = self.df[self.value_col].values
        self.n = len(self.value_data)

        # 设置输出目录
        if output_dir is None:
            output_dir = os.path.dirname(input_file)
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 数据预处理
        self._preprocess_data()
        
        # 检测所有突变点
        self._detect_all_change_points()
        
        # 如果没有检测到突变点，返回空结果
        if not self.change_points:
            print("未检测到任何突变点")
            return None, []
        
        # 提取连续突变段
        continuous_segment = self._extract_continuous_segment()
        
        # 绘制结果
        if plot_results:
            # 创建单独的连续段图表
            self._plot_continuous_segment(continuous_segment)
        

        self._save_statistical_data(continuous_segment)

        return continuous_segment
    
    def _preprocess_data(self):
        """数据预处理"""
        print("进行数据预处理...")
        
        # 计算数据的基本统计信息
        self.value_mean = np.mean(self.value_data)
        self.value_std = np.std(self.value_data)
        print(f"均值: {self.value_mean:.4f}, 标准差: {self.value_std:.4f}")
        
        # 使用Savitzky-Golay滤波器平滑数据
        try:
            # 调整窗口大小以适应数据长度
            window_length = min(self.smooth_window, self.n // 10)
            if window_length % 2 == 0:  # 确保窗口长度为奇数
                window_length += 1
            window_length = max(5, window_length)  # 最小窗口为5
            
            self.smoothed_value = signal.savgol_filter(
                self.value_data, 
                window_length=window_length, 
                polyorder=self.polyorder
            )
            print(f"使用窗口大小 {window_length} 进行数据平滑")
        except Exception as e:
            print(f"数据平滑失败: {e}，使用原始数据")
            self.smoothed_value = self.value_data
        
        # 计算电压的一阶导数(变化率)
        self.derivative = np.gradient(self.smoothed_value)
        
        # 计算导数的绝对值和统计量
        self.abs_derivative = np.abs(self.derivative)
        self.mean_abs = np.mean(self.abs_derivative)
        self.std_abs = np.std(self.abs_derivative, ddof=1)
        
        # 设置自适应阈值
        self.threshold = self.mean_abs + self.sensitivity * self.std_abs
        print(f"检测阈值: {self.threshold:.4f} (均值: {self.mean_abs:.4f}, 标准差: {self.std_abs:.4f})")
    
    def _detect_all_change_points(self):
        """检测所有突变点"""
        #print("检测所有突变点...")
        
        # 找到超过阈值的点
        above_threshold = self.abs_derivative > self.threshold
        
        # 使用形态学操作连接相邻的突变点
        structure = np.ones(5)  # 连接最多间隔4个点的突变
        labeled = signal.convolve(above_threshold.astype(int), structure, mode='same') > 0
        
        # 找到突变段的起始和结束位置
        diff_labeled = np.diff(np.concatenate(([0], labeled, [0])))
        starts = np.where(diff_labeled > 0)[0]
        ends = np.where(diff_labeled < 0)[0]
        
        # 收集所有候选突变点
        candidate_points = []
        for start, end in zip(starts, ends):
            if end - start >= 3:  # 至少3个点才被认为是有效段
                # 找到该段内导数绝对值最大的点作为主要突变点
                segment_derivative = self.abs_derivative[start:end]
                max_index = np.argmax(segment_derivative) + start
                candidate_points.append(max_index)
        
        # 过滤掉过于接近的突变点
        self.change_points = []
        if candidate_points:
            self.change_points.append(candidate_points[0])
            for i in range(1, len(candidate_points)):
                if candidate_points[i] - candidate_points[i-1] > self.min_segment_length // 2:
                    self.change_points.append(candidate_points[i])
        
        print(f"找到 {len(self.change_points)} 个突变点.")
    
    def _extract_continuous_segment(self):
        """提取从第一个突变点到最后一个突变点的连续段"""
        #print("提取连续突变段...")
        
        # 找到第一个和最后一个突变点
        first_change = min(self.change_points)
        last_change = max(self.change_points)

        if self.time_data[last_change]-self.time_data[first_change]>20 & len(self.change_points)>2:
            first_change=self.change_points[2]
        
        #print(f"第一个突变点: {first_change}, 最后一个突变点: {last_change}")
        
        # 扩展段范围
        start_index = max(0, first_change - self.extend_before)
        end_index = min(self.n-1, last_change + self.extend_after)
        
        # 检查段长度是否足够
        if end_index - start_index < self.min_segment_length:
            print(f"警告: 段长度不足 ({end_index - start_index} < {self.min_segment_length})")
        
        # 提取数据段
        continuous_segment = self.df.iloc[start_index:end_index+1].copy()
        
        self.start_index=start_index
        self.end_index=end_index        
        
        # 保存截取数据到CSV文件
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        output_file = os.path.join(
            self.output_dir, 
            f"{base_name}_segment.csv"
        )
        continuous_segment.to_csv(output_file, index=False)
        
        return continuous_segment
 
    def _save_statistical_data(self,continuous_segment):

        start_value = self.value_data[self.start_index]
        end_value = self.value_data[self.end_index]
        
        value_change = end_value - start_value
        change_type = "increase" if value_change > 0 else "decrease"
        
        start_time=self.time_data[self.start_index]
        end_time=self.time_data[self.end_index]

        columnslist=self.df.columns
        max_value_list=[]
        min_value_list=[]
        max_value_time_list=[]
        min_value_time_list=[]

        for i in range(1,len(columnslist)):
            value=continuous_segment[columnslist[i]].values
            max_value = np.max(value)
            min_value = np.min(value)
            max_value_time=self.time_data[np.argmax(value)+self.start_index]
            min_value_time=self.time_data[np.argmin(value)+self.start_index]

            max_value_list.append(max_value)
            min_value_list.append(min_value)
            max_value_time_list.append(max_value_time)
            min_value_time_list.append(min_value_time)

        # 保存统计信息到txt文件
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        txt_path=os.path.join(self.output_dir, f'{base_name}_statistics.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.writelines(change_type+'\n')
            f.writelines(f"plot_start_time={start_time}"+'\n')
            f.writelines(f"plot_end_time={end_time}"+'\n')
            f.writelines('\n')
            for i in range(1,len(columnslist)):
                f.writelines(f'max value and event time of {columnslist[i]}: {max_value_list[i-1]}, {max_value_time_list[i-1]}' + '\n')
                f.writelines(f'min value and event time of {columnslist[i]}: {min_value_list[i-1]}, {min_value_time_list[i-1]}' + '\n')
                f.writelines('\n')

        print("The max and min values are saved in txt.")       
    
    def _plot_continuous_segment(self, continuous_segment):
        """绘制连续段的详细图表"""
        print("生成连续段详细图表...")
        
        # 创建段图表
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        # 提取段数据
        seg_time = continuous_segment[self.time_col].values
        seg_value = continuous_segment[self.value_col].values
        
        # 绘制段数据
        ax.plot(seg_time, seg_value, 'b-', linewidth=2, label='V')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 保存段图表
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        segment_plot_file = os.path.join(
            self.output_dir, 
            f"{base_name}_segment.png"
        )
        plt.savefig(segment_plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print("连续段详细图表生成完成")

# def main():
#     # 创建检测器实例
#     detector = DataSegment(
#         voltage_number=7,
#         sensitivity=1.5,
#         extend_before=1000,
#         extend_after=1000,
#         min_segment_length=20,
#         smooth_window=50,
#         polyorder=3
#     )
    
#     folder_path = 'E:\DigSilent\模型修改\V15_奥地利\FRTData/new'
#     csvfiles = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

#     for file in csvfiles:

#         # 执行检测
#         continuous_segment = detector.detect_continuous_changes(
#         input_file=os.path.join(folder_path, file),
#         output_dir=folder_path,
#         plot_results=True)

            

# if __name__ == "__main__":
#     main()