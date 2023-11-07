import argparse
import sys

from models import LogGenerator
from logparser import Drain


parser = argparse.ArgumentParser()
##### Dataset params
parser.add_argument("--dataset_name", default="Android", type=str)
parser.add_argument("--data_dir", default="./datasets/BGL/", type=str)
parser.add_argument("--out_dir", default="./results/Generated/", type=str)
parser.add_argument("--preprocessed_dir", default=None, type=str)
parser.add_argument("--log_file", default="BGL.log", type=str)
parser.add_argument("--use_data_size", default=None, type=int)
parser.add_argument("--use_template", action='store_true')


"""" Generate """
parser.add_argument("--log_amount", default=1000, type=int)

parser.add_argument("--string_len_min", default=4, type=int)
parser.add_argument("--string_len_max", default=10, type=int)
parser.add_argument("--sentence_len_min", default=3, type=int)
parser.add_argument("--sentence_len_max", default=6, type=int)

parser.add_argument("--per1s", default=10, type=int)
parser.add_argument("--log_types", default=50, type=int)

parser.add_argument("--hist_max", default=10, type=float)
parser.add_argument("--hist_min", default=0.05, type=float)

# parser.add_argument("--gini_coeff", default=0.5975878273414603, type=float)

def diif_ex():
    import difflib
    # 2つの文章を定義
    text1 = "CE sym 9, at 0x045ba220, mask 0x02"
    text2 = "CE sym 25, at 0x155e28e0, mask 0x08"
    # 文章を行ごとに分割
    lines1 = text1.split(', ')
    lines2 = text2.split(', ')
    # 差分を見つける
    d = difflib.Differ()
    diff = list(d.compare(lines1, lines2))
    # 異なる部分を抽出
    differences = [line for line in diff if line.startswith('- ') or line.startswith('+ ')]
    # 結果を表示
    for line in differences:
        print(line)
    sys.exit()

if __name__ == "__main__":
    # import re
    # content = "CE sym 9, at 0x045ba220, mask 0x02"
    # content = "CE sym 25, at 0x155e28e0, mask 0x08"
    # pattern = "CE sym <*> at <*> mask <*>"
    #
    # result = re.match(pattern, content)
    # print(pattern["<*>"])
    # sys.exit()
    #
    # if result:  # none以外の場合
    #     # group()で全文字を
    #     print(result.group())  # hellow python, 123,end
    #     # group(1)で数字を
    #     print(result.group(1))  # 123
    #
    # result = re.search(pattern, content)
    # print(result)
    # sys.exit()

    params = vars(parser.parse_args())
    log_generator = LogGenerator(params)
    log_generator.generate()

    # log_analyzer = LogAnalyzer(params["dataset"], params["data_dir"], params["save_dir"], params["preprocessed_dir"], params["log_file"], params["use_data_size"], params["use_template"], params["analyze_adfuller"])
    # print(log_analyzer.f())
    #
    # df_log = load_data(params["dataset"])
    # # print(df_log)
    # print(df_log[:3])
    # print(df_log["Timestamp"])
    # log_analyzer.analyze()
    # log_analyzer.analyze_log_hist()
    # log_analyzer.analyze_windowed_hist()
