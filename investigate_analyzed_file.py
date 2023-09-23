import argparse
import sys
import os
from statistics import mean, pstdev, median_low, median_high


parser = argparse.ArgumentParser()
##### Dataset params
parser.add_argument("--dataset", default="BGL", type=str)
parser.add_argument("--data_dir", default="./results/Android/BGL", type=str)
# parser.add_argument("--save_dir", default="./results/Android/", type=str)
# parser.add_argument("--preprocessed_dir", default=None, type=str)
parser.add_argument("--log_file", default="BGL.log", type=str)
# parser.add_argument("--use_data_size", default=None, type=int)
# parser.add_argument("--use_template", action='store_true')


"""" Analyze """
# parser.add_argument("--analyze_adfuller", action='store_true')

# parser.add_argument("--window_size", default=10, type=int)
# parser.add_argument("--stride", default=1, type=int)
# parser.add_argument("--data_pct", default=1.0, type=float)

# def load_analyzed_file(data_type):
#     if data_type == "BGL":
#         return load_bgl_data()
#     return None
#
def load_analyzed_file(params, log_file):
    input_dir = './datasets/BGL/'  # The input directory of log file
    # log_file = 'BGL.log'  # The input log file name
    with open(os.path.join(params["data_dir"], log_file)) as f:
        load_data = f.readlines()

    return load_data

def investigate_hist(load_data, file_name):
    results = []
    all_num=0
    # print(load_data)
    for data in load_data[1:]:
        splited = data.split(" ")[-2]
        results.append(int(splited))
        all_num += int(splited)
    print("=" * 20)
    print("Result of Investigation {}".format(file_name))
    print("=" * 20)
    print("-Log Frequency")
    print(" : mean={}, pstdev={}".format(mean(results), pstdev(results)))
    print(" : median_low={}, median_high={}".format(median_low(results),
                                                                  median_high(results)))
    print(" : max={}, min={}".format(max(results), min(results)))
    # print("log_types      : {}".format(len(self.log_types)))
    # print("log_components : {}".format(len(self.log_components)))
    print("all_num    : {}".format((all_num)))
    print("For Copy   : {} {} {} {} {} {} {}".format(mean(results), pstdev(results), median_low(results),
                                                    median_high(results), max(results), min(results), all_num))

if __name__ == "__main__":
    params = vars(parser.parse_args())

    file_names = [".txt", "_structured.txt", "_windowed.txt", "_windowed_structured.txt"]
    for file_name in file_names:
        load_data = load_analyzed_file(params, params["dataset"]+file_name)
        investigate_hist(load_data, params["dataset"]+file_name)
    # path = "/work2/huchida/PSD_DC2/LogGenerator/datasets/Thunderbird/Thunderbird.log"
    # with open(path, encoding="UTF-8") as f:
    #     for line in f.readlines():
    #         print(line)
    #         sys.exit()
    # sys.exit()

    # log_analyzer = LogAnalyzer(params["dataset"], params["data_dir"], params["save_dir"], params["preprocessed_dir"], params["log_file"], params["use_data_size"], params["use_template"], params["analyze_adfuller"])
    # # print(log_analyzer.f())
    # #
    # # df_log = load_data(params["dataset"])
    # # # print(df_log)
    # # print(df_log[:3])
    # # print(df_log["Timestamp"])
    # log_analyzer.analyze()
    # log_analyzer.analyze_log_hist()
    # log_analyzer.analyze_windowed_hist()
