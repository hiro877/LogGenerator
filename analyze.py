import argparse
import sys

from models import LogAnalyzer
from logparser import Drain


parser = argparse.ArgumentParser()
##### Dataset params
parser.add_argument("--dataset", default="BGL", type=str)
parser.add_argument("--data_dir", default="./datasets/BGL/", type=str)
parser.add_argument("--save_dir", default="./results/Android/", type=str)
parser.add_argument("--preprocessed_dir", default=None, type=str)
parser.add_argument("--log_file", default="BGL.log", type=str)
parser.add_argument("--use_data_size", default=None, type=int)
parser.add_argument("--use_template", action='store_true')


"""" Analyze """
parser.add_argument("--analyze_adfuller", action='store_true')

# parser.add_argument("--window_size", default=10, type=int)
# parser.add_argument("--stride", default=1, type=int)
# parser.add_argument("--data_pct", default=1.0, type=float)

# def load_data(data_type):
#     if data_type == "BGL":
#         return load_bgl_data()
#     return None
#
# def load_bgl_data():
#     input_dir = './datasets/BGL/'  # The input directory of log file
#     output_dir = 'Drain_result/'  # The output directory of parsing results
#     log_file = 'BGL.log'  # The input log file name
#     log_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>'  # HDFS log format
#     # Regular expression list for optional preprocessing (default: [])
#     regex = [
#         r'core\.\d+'
#     ]
#     st = 0.5  # Similarity threshold
#     depth = 4  # Depth of all leaf nodes
#
#     parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
#     parser.logName=log_file
#     parser.load_data()
#     return parser.df_log

if __name__ == "__main__":
    params = vars(parser.parse_args())
    # path = "/work2/huchida/PSD_DC2/LogGenerator/datasets/Thunderbird/Thunderbird.log"
    # with open(path, encoding="UTF-8") as f:
    #     for line in f.readlines():
    #         print(line)
    #         sys.exit()
    # sys.exit()

    log_analyzer = LogAnalyzer(params["dataset"], params["data_dir"], params["save_dir"], params["preprocessed_dir"], params["log_file"], params["use_data_size"], params["use_template"], params["analyze_adfuller"])
    # print(log_analyzer.f())
    #
    # df_log = load_data(params["dataset"])
    # # print(df_log)
    # print(df_log[:3])
    # print(df_log["Timestamp"])
    log_analyzer.analyze()
    log_analyzer.analyze_log_hist()
    log_analyzer.analyze_windowed_hist()
