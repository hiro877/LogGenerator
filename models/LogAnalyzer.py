"""
- Raw Log
1. 単位時間あたりのlog数(per 1s)
2. Type総数
3. Component総数
4. logの総数
5. 各logの頻度

- Template(BGL)
1. 単位時間あたりのTemplate数
2. Template総数
3. 各Templateの頻度

- 異常Log
1. 異常ログの数
2. NormalログとAnomalyログの比率
3. 異常ログの分布

- 定常性
"""
"""
- 改行コード変換
nkf -Lu foo.txt
- 文字コード変換
nkf -w --overwrite foo.tzt 
"""

import sys
import os
from logparser import Drain
import pandas as pd
from statistics import mean, pstdev, median_low, median_high
import statsmodels.tsa.api as tsa
import datetime
class LogAnalyzer:
    def __init__(self, dataset, input_dir, log_file, use_data_size):
        self.dataset_name = dataset
        self.input_dir = input_dir
        self.log_file = log_file
        self.dataset_path = os.path.join(self.input_dir, self.log_file)
        self.use_data_size = use_data_size

        self.parser = None
        self.log2id = {}

        # self.df_log = None
        self.make_parser()
        self.load_data()

        # Raw Log
        self.lognum_per1s = []
        self.log_types = set()
        self.log_components = set()
        self.log_num_all = 0
        # Anomaly Raw Log
        self.anomaly_log_num_all = 0
        self.anomaly_indexes = []

        # Template
        self.templatenum_per1s = []

        # ていじょうせい
        self.ids = []
        self.binaries = []


    def f(self):
        return 'hello world'

    def make_parser(self):
        print("Make Parser using {}".format(self.dataset_name))
        output_dir = 'Drain_result/'  # The output directory of parsing results
        if self.dataset_name == "BGL":
            log_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>'  # HDFS log format
            regex = [r'core\.\d+']
            st = 0.5  # Similarity threshold
            depth = 4  # Depth of all leaf nodes
        if self.dataset_name == "Android":
            log_format = '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>'
            regex = [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b']
            st = 0.2  # Similarity threshold
            depth = 6  # Depth of all leaf nodes
        if self.dataset_name == "Thunderbird":
            log_format = '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>'
            regex = [r'(\d+\.){3}\d+']
            st = 0.5  # Similarity threshold
            depth = 4  # Depth of all leaf nodes
        if self.dataset_name == "Windows":
            log_format = '<Date> <Time>, <Level>                  <Component>    <Content>'
            regex = [r'0x.*?\s']
            st = 0.7  # Similarity threshold
            depth = 5  # Depth of all leaf nodes
        if self.dataset_name == "Linux":
            log_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>'
            regex = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}']
            st = 0.39  # Similarity threshold
            depth = 6  # Depth of all leaf nodes
        if self.dataset_name == "Mac":
            log_format = '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>'
            regex = [r'([\w-]+\.){2,}[\w-]+']
            st = 0.7  # Similarity threshold
            depth = 6  # Depth of all leaf nodes

        self.parser = Drain.LogParser(log_format, indir=self.input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
        self.parser.logName = self.log_file

    def load_data(self):
        print("Load Dataset {}".format(self.dataset_name))
        if self.dataset_name == "BGL":
            self.load_bgl_data()
        if self.dataset_name == "Android":
            self.load_android_data()
        if self.dataset_name == "Thunderbird":
            self.load_thunderbird_data()
        else:
            self.load_common_data()

    def load_common_data(self):
        save_path = os.path.join(self.input_dir, "preprocessed")
        print(save_path)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, "pandas_"+self.log_file.split(".")[0]+".pkl")
        print(save_path)
        if os.path.exists(save_path):
            print("save pandas file")
            self.parser.df_log = pd.read_pickle(save_path)  # 圧縮無し
            return

        if self.use_data_size:
            self.parser.load_data_limited(self.use_data_size)
        else:
            self.parser.load_data()
        # self.df_log = self.parser.df_log
        self.parser.df_log.to_pickle(save_path)  # 圧縮無し

    def load_bgl_data(self):
        save_path = os.path.join(self.input_dir, "preprocessed")
        print(save_path)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, "pandas_"+self.log_file.split(".")[0]+".pkl")
        print(save_path)
        if os.path.exists(save_path):
            print("save pandas file")
            self.parser.df_log = pd.read_pickle(save_path)  # 圧縮無し
            return

        self.parser.load_data()
        # self.df_log = self.parser.df_log
        self.parser.df_log.to_pickle(save_path)  # 圧縮無し

    def load_android_data(self):
        save_path = os.path.join(self.input_dir, "preprocessed")
        print(save_path)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, "pandas_"+self.log_file.split(".")[0]+".pkl")
        print(save_path)
        if os.path.exists(save_path):
            print("save pandas file")
            self.parser.df_log = pd.read_pickle(save_path)  # 圧縮無し
            return

        self.parser.load_data()
        # self.df_log = self.parser.df_log
        self.parser.df_log.to_pickle(save_path)  # 圧縮無し
        # print(self.parser.df_log)

    def load_thunderbird_data(self):
        save_path = os.path.join(self.input_dir, "preprocessed")
        print(save_path)
        os.makedirs(save_path, exist_ok=True)
        save_path = os.path.join(save_path, "pandas_"+self.log_file.split(".")[0]+".pkl")
        print(save_path)
        if os.path.exists(save_path):
            print("save pandas file")
            self.parser.df_log = pd.read_pickle(save_path)  # 圧縮無し
            return

        self.parser.load_data()
        # self.df_log = self.parser.df_log
        self.parser.df_log.to_pickle(save_path)  # 圧縮無し
        # print(self.parser.df_log)

    def analyze(self):
        # count = 0
        # for idx, line in self.df_log.iterrows():
        #     logID = line['LineId']
        #     logmessageL = self.preprocess(line['Content']).strip().split()
        #     timestamp = line["Timestamp"]
        if self.dataset_name == "BGL":
            self.analyze_bgl()
        if self.dataset_name == "Android":
            self.analyze_android()
        if self.dataset_name == "Thunderbird":
            self.analyze_thunderbird()
        if self.dataset_name == "Windows":
            self.analyze_windows()
        if self.dataset_name == "Linux":
            self.analyze_linux()
        if self.dataset_name == "Mac":
            self.analyze_mac()

    def analyze_bgl(self):
        current_time = self.parser.df_log["Timestamp"][0]
        per1s= 0
        log_id = 0
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            timestamp = line["Timestamp"]
            component = line['Component']
            label = line['Label']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1



            if label != "-":
                self.anomaly_log_num_all += 1
                self.anomaly_indexes.append(idx)
                self.binaries.append(1)
            else:
                self.binaries.append(0)

            per1s += 1
            if timestamp != current_time:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=timestamp
                # sys.exit()
        self.print_results()

    def analyze_android(self):
        s_format = '%H:%M:%S.%f'
        current_time = self.parser.df_log["Time"][0]
        print(current_time)
        current_time = datetime.datetime.strptime(current_time, s_format)
        print(current_time)
        print(current_time.second)
        # sys.exit()
        per1s= 0
        log_id = 0
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            time = datetime.datetime.strptime(line["Time"], s_format)
            component = line['Component']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1

            per1s += 1
            if time.second != current_time.second:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=time
                # sys.exit()
        self.print_results()

    def analyze_thunderbird(self):
        current_time = self.parser.df_log["Timestamp"][0]
        per1s= 0
        log_id = 0
        border_time = 3600 #1hour
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            timestamp = line["Timestamp"]
            component = line['Component']
            label = line['Label']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1



            if label != "-":
                self.anomaly_log_num_all += 1
                self.anomaly_indexes.append(idx)
                self.binaries.append(1)
            else:
                self.binaries.append(0)

            per1s += 1
            if timestamp - current_time > border_time:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=timestamp
                # sys.exit()
        self.print_results()

    def analyze_linux(self):
        s_format = '%H:%M:%S'
        current_time = self.parser.df_log["Time"][0]
        current_time = datetime.datetime.strptime(current_time, s_format)
        print(current_time)
        # sys.exit()
        per1s= 0
        log_id = 0
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            time = datetime.datetime.strptime(line["Time"], s_format)
            component = line['Component']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1

            per1s += 1
            if time.second != current_time.second:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=time
                # sys.exit()
        self.print_results()

    def analyze_windows(self):
        s_format = '%H:%M:%S'
        current_time = self.parser.df_log["Time"][0]
        current_time = datetime.datetime.strptime(current_time, s_format)
        print(current_time)
        # sys.exit()
        per1s= 0
        log_id = 0
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            # print(line["Time"])
            try:
                time = datetime.datetime.strptime(line["Time"], s_format)
            except ValueError:
                time = current_time
            component = line['Component']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1

            per1s += 1
            if time.second != current_time.second:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=time
                # sys.exit()
        self.print_results()

    def analyze_mac(self):
        s_format = '%H:%M:%S'
        current_time = self.parser.df_log["Time"][0]
        current_time = datetime.datetime.strptime(current_time, s_format)
        print(current_time)
        # sys.exit()
        per1s= 0
        log_id = 0
        # print("current_time:", current_time)

        self.log_num_all = self.parser.df_log.shape[0]
        for idx, line in self.parser.df_log.iterrows():
            # logID = line['LineId']
            # content = self.parser.preprocess(line['Content']).strip().split()
            content = line['Content']
            time = datetime.datetime.strptime(line["Time"], s_format)
            component = line['Component']
            # print(line['Content'])
            # print(idx, content)

            self.log_types.add(content)
            self.log_components.add(component)
            if component in self.log2id:
                self.ids.append(self.log2id[component])
            else:
                self.ids.append(log_id)
                self.log2id[component] = log_id
                log_id += 1

            per1s += 1
            if time.second != current_time.second:
                self.lognum_per1s.append(per1s)
                per1s = 0
                current_time=time
                # sys.exit()
        self.print_results()

    def print_results(self):
        print("="*20)
        print("Result of Analysing {}".format(self.dataset_name))
        print("=" * 20)
        print("- Raw Log")
        print("lognum_per1s   : mean={}, pstdev={}".format(mean(self.lognum_per1s), pstdev(self.lognum_per1s)))
        print("               : median_low={}, median_high={}".format(median_low(self.lognum_per1s), median_high(self.lognum_per1s)))
        print("               : max={}, min={}".format(max(self.lognum_per1s), min(self.lognum_per1s)))
        print("log_types      : {}".format(len(self.log_types)))
        print("log_components : {}".format(len(self.log_components)))
        print("log_num_all    : {}".format(self.log_num_all))
        print("- Anomaly Raw Log")
        print("anomaly_log_num_all : {}".format(self.anomaly_log_num_all))

        print("- ADF statistics -")
        # print("ids: ")
        # adf_rlt_pv = tsa.adfuller(self.ids)
        # print(f'ADF statistics: {adf_rlt_pv[0]}')
        # print(f'# of lags used: {adf_rlt_pv[2]}')
        # print(f'Critical values: {adf_rlt_pv[4]}')
        # print("ids: ")
        # adf_rlt_pv = tsa.adfuller(self.binaries)
        # print(f'ADF statistics: {adf_rlt_pv[0]}')
        # print(f'# of lags used: {adf_rlt_pv[2]}')
        # print(f'Critical values: {adf_rlt_pv[4]}')
        # print(len(self.ids))
        # print(len(self.binaries))
        # sys.exit()
        # print(self.ids)
        for i in range(0, len(self.ids), 100000):
            try:
                print("- ADF statistics {} -".format(i))
                print("ids: ")
                adf_rlt_pv = tsa.adfuller(self.ids[i : i+100000])
                print(f'ADF statistics: {adf_rlt_pv[0]}')
                print(f'# of lags used: {adf_rlt_pv[2]}')
                print(f'Critical values: {adf_rlt_pv[4]}')
                if self.binaries:
                    print("binaries: ")
                    adf_rlt_pv = tsa.adfuller(self.binaries[i : i+100000])
                    print(f'ADF statistics: {adf_rlt_pv[0]}')
                    print(f'# of lags used: {adf_rlt_pv[2]}')
                    print(f'Critical values: {adf_rlt_pv[4]}')
                print("-"*20)
            except ValueError as e:
                print(e)

        print(len(self.ids))
        print(len(self.binaries))

    # def split_timestamp(self):
    #     if self.dataset == "BGL":
    #         continue

