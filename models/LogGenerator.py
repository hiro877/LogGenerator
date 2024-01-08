import os
import datetime
import sys
import random, string
import numpy as np
class LogGenerator:
    def __init__(self, params):
        print(params)
        self.dataset_name = params["dataset_name"]
        self.out_dir = params["out_dir"]

        self.log_amount = params["log_amount"]

        self.string_len_max = params["string_len_max"]
        self.string_len_min = params["string_len_min"]
        self.sentence_len_max = params["sentence_len_max"]
        self.sentence_len_min = params["sentence_len_min"]

        self.init_time = datetime.datetime.now()
        # self.init_time_str =
        self.per1s = params["per1s"]
        self.log_types = params["log_types"]
        # self.gini_coeff = params["gini_coeff"]
        self.hist_max = params["hist_max"]
        self.hist_min = params["hist_min"]

        self.histgram = self.make_histgram()
        self.int_pattern_contents = [""]
        self.str_pattern_contents = [["true", "false", "null", "error"]]

        if self.log_types > self.log_amount:
            print("self.log_types > self.log_amount")
            sys.exit()
        if(self.sentence_len_min < 3):
            print("self.sentence_len_min < 3")
            sys.exit()

    def make_histgram(self):
        array = [self.hist_min] * self.log_types
        target_total = 100
        current_total = self.hist_min * self.log_types
        index_max = self.log_types - 1
        while current_total < target_total:
            index = random.randint(0, index_max)
            value = random.uniform(self.hist_min, self.hist_max)
            if array[index] + value <= self.hist_max:
                array[index] += value
                current_total += value
        array = np.sort(array)
        array = array*(self.log_amount/100)
        array = np.ceil(array)
        diff = np.sum(array) - self.log_amount
        while diff > 0:
            for i in range(array.shape[0]):
                if array[i] != 1:
                    array[i] -= 1
                    diff -= 1
                if diff == 0:
                    break
        return array.astype(int).tolist()

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)

    def generate(self):
        os.makedirs(self.out_dir, exist_ok=True)
        if self.dataset_name == "BGL":
            self.generate_bgl()
        if self.dataset_name == "Android":
            self.generate_android()
        if self.dataset_name == "Thunderbird":
            self.analyze_thunderbird()
        if self.dataset_name == "Windows":
            self.analyze_windows()
        if self.dataset_name == "Linux":
            self.analyze_linux()
        if self.dataset_name == "Mac":
            self.analyze_mac()

    def generate_bgl(self):
        print("generate_bgl")
        log_label = "-"
        log_timestamp = "1111111111"
        log_mode = "R02-M1-N0-C:J12-U11"
        log_node_repeat = "R02-M1-N0-C:J12-U11"
        log_type = "RAS"
        log_component = "KERNEL"
        log_level = "INFO"

        s_format = '%Y.%M.%d'
        log_date = datetime.datetime.strftime(self.init_time, s_format)
        s_format = '%Y-%m-%d-%H.%M.%S.%f'
        # log_time = datetime.datetime.strftime(self.init_time, s_format)
        log_time = self.init_time
        # log_pid, log_tid, log_level = ["1111", "1111", "D"]
        # log_tid = "1111"
        # log_component = "ComponentA"
        # log_contents = "Contents"
        ignore_index = []
        contents_list = []

        # histgram 0より大きい値があるIndexを抽出する
        # not_zero_index = 0
        # for i in range(len(self.histgram)):
        #     if self.histgram[i] > 1:
        #         not_zero_index = i
        #         break
        # print(not_zero_index, self.histgram)
        # print(self.histgram[not_zero_index])

        for i in range(len(self.int_pattern_contents)):
            not_zero_index = self.get_not_zero_index(self.histgram)
            contents = self.generate_contents()
            self.int_pattern_contents[i] = contents

            rnd = random.randint(not_zero_index, len(self.histgram)-1)
            hist = self.histgram.pop(rnd)
            result = self.inject_parameter("int", contents, hist)
            contents_list = contents_list + result
            # sys.exit()

        # for i in range(len(self.str_pattern_contents)):
        not_zero_index = self.get_not_zero_index(self.histgram)
        contents= self.generate_contents()
        rnd = random.randint(not_zero_index, len(self.histgram)-1)
        hist = self.histgram.pop(rnd)
        result = self.inject_parameter("string", contents, hist)
        contents_list = contents_list + result
        # sys.exit()


        # range_len = self.log_types - len(self.int_pattern_contents) - len(self.str_pattern_contents)
        for hist in self.histgram:
            contents = [self.generate_contents()]
            contents = contents * hist
            print(contents)
            contents_list = contents_list + contents

        # contents = self.generate_contents()
        # print(len(contents_list))
        # print("{} {}  {}  {} {} {}: {}".format(log_date, log_time, log_pid, log_tid, log_level,
        #                                       log_component, log_contents))
        # sys.exit()

        # print(contents_list)
        random.shuffle(contents_list)
        # print(contents_list)

        now = datetime.datetime.now()
        save_path = self.out_dir+'/log_bgl_' + now.strftime('%m%d_%H%M%S') + '.log'
        log_num = 0
        with open(save_path, mode='w') as f:
            for log_contents in contents_list:
                if log_num > self.per1s:
                    log_num=0
                    log_time = log_time + datetime.timedelta(seconds=1)

                log_time_str = datetime.datetime.strftime(log_time, s_format)
                if "error" in log_contents:
                    f.writelines(
                        "{} {} {} {} {} {} {} {} {} {}\n".format("STRERR", log_timestamp, log_date, log_mode, log_time_str,
                                                               log_node_repeat
                                                               , log_type, log_component, log_level, log_contents))
                else:
                    f.writelines("{} {} {} {} {} {} {} {} {} {}\n".format(log_label, log_timestamp, log_date, log_mode, log_time_str, log_node_repeat
                                                                       ,log_type, log_component, log_level, log_contents))
                log_num+=1
            # for log in self.log_types:
            #     df = (self.parser.df_log["Content"] == log)
            #     f.writelines(log + "博" + str(df.sum()) + "\n")

    def generate_android(self):
        print("generate_android")
        s_format = '%m-%d'
        log_date = datetime.datetime.strftime(self.init_time, s_format)
        s_format = '%H:%M:%S'
        log_time = datetime.datetime.strftime(self.init_time, s_format)
        log_pid, log_tid, log_level = ["1111", "1111", "D"]
        # log_tid = "1111"
        log_component = "ComponentA"
        log_contents = "Contents"
        ignore_index = []
        contents_list = []

        # histgram 0より大きい値があるIndexを抽出する
        # not_zero_index = 0
        # for i in range(len(self.histgram)):
        #     if self.histgram[i] > 1:
        #         not_zero_index = i
        #         break
        # print(not_zero_index, self.histgram)
        # print(self.histgram[not_zero_index])

        for i in range(len(self.int_pattern_contents)):
            not_zero_index = self.get_not_zero_index(self.histgram)
            contents = self.generate_contents()
            self.int_pattern_contents[i] = contents

            rnd = random.randint(not_zero_index, len(self.histgram)-1)
            hist = self.histgram.pop(rnd)
            result = self.inject_parameter("int", contents, hist)
            contents_list = contents_list + result
            # sys.exit()

        # for i in range(len(self.str_pattern_contents)):
        not_zero_index = self.get_not_zero_index(self.histgram)
        contents= self.generate_contents()
        rnd = random.randint(not_zero_index, len(self.histgram)-1)
        hist = self.histgram.pop(rnd)
        result = self.inject_parameter("string", contents, hist)
        contents_list = contents_list + result
        # sys.exit()


        # range_len = self.log_types - len(self.int_pattern_contents) - len(self.str_pattern_contents)
        for hist in self.histgram:
            contents = [self.generate_contents()]
            contents = contents * hist
            print(contents)
            contents_list = contents_list + contents

        # contents = self.generate_contents()
        print(len(contents_list))
        print("{} {}  {}  {} {} {}: {}".format(log_date, log_time, log_pid, log_tid, log_level,
                                              log_component, log_contents))
        # sys.exit()

        # print(contents_list)
        random.shuffle(contents_list)
        # print(contents_list)

        now = datetime.datetime.now()
        save_path = self.out_dir+'/log_android_' + now.strftime('%m%d_%H%M%S') + '.log'
        log_num = 0
        with open(save_path, mode='w') as f:
            for log_contents in contents_list:
                f.writelines("{} {}  {}  {} {} {}: {}\n".format(log_date, log_time, log_pid, log_tid, log_level,
                                              log_component, log_contents))
            # for log in self.log_types:
            #     df = (self.parser.df_log["Content"] == log)
            #     f.writelines(log + "博" + str(df.sum()) + "\n")

    def generate_contents(self):
        sentence_len = random.randint(self.sentence_len_min, self.sentence_len_max)
        contents = ""
        for i in range(sentence_len):
            string_len = random.randint(self.string_len_min, self.string_len_max)
            contents = contents + self.randomname(string_len) + " "
        contents = contents[:-1]
        print(contents)
        return contents

    def inject_parameter(self, parameter_type, contents, hist):
        result = []
        if parameter_type == "int":
            return self.inject_parameter_int(contents, hist)
        if parameter_type == "string":
            return self.inject_parameter_str(contents, hist)
        return result

    def inject_parameter_int(self, contents, hist):
        print("inject_parameter_int")
        result = []

        splited_contents = contents.split(" ")
        rnd = random.randint(0, len(splited_contents)-1)
        splited_contents[rnd] = "10000"
        result.append(" ".join(splited_contents))
        # print(" ".join(splited_contents))
        for i in range(hist - 1):
            rnd_int = random.randint(-100, 100)
            splited_contents[rnd] = str(rnd_int)
            result.append(" ".join(splited_contents))
            # print(" ".join(splited_contents))
        # print(result)
        return result

    def inject_parameter_str(self, contents, hist):
        print("inject_parameter_str")
        result = []

        splited_contents = contents.split(" ")
        rnd = random.randint(0, len(splited_contents)-1)
        # splited_contents[rnd] = "10000"
        # result.append(" ".join(splited_contents))
        # print(" ".join(splited_contents))
        for str_patterns in self.str_pattern_contents:
            rand_max = len(str_patterns) - 1
            for i in range(hist):
                rnd_str = random.randint(0, rand_max)
                splited_contents[rnd] = str_patterns[rnd_str]
                result.append(" ".join(splited_contents))
                # print(" ".join(splited_contents))
            # print(result)
            return result

    def get_not_zero_index(self, list):
        not_zero_index = 0
        for i in range(len(list)):
            if self.histgram[i] > 1:
                not_zero_index = i
                break
        return not_zero_index
