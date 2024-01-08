import datetime
import sys
from collections import Counter
import os
import pandas as pd
import re
import csv

RED = "\033[31m"
RESET = "\033[0m"
PINK = "\033[38;2;255;192;203m"

def get_frequecy_vector(sentences,filter,delimiter,dataset):
    '''
    Counting each word's frequency in the dataset and convert each log into frequency vector
    Output:
        wordlist: log groups based on length
        tuple_vector: the word in the log will be converted into a tuple (word_frequency, word_character, word_position)
        frequency_vector: the word in the log will be converted into its frequency

    '''
    """
    - For Future task by hiro87
     Save extracted param by using regex.
    """
    isDebug = False
    group_len = {}
    set = {}
    line_id=0
    if(isDebug): print("sentences: ", sentences)
    for s in sentences:  # using delimiters to get split words
        if(isDebug): print("s1: ",s)
        if(isDebug): print("filter: ",filter)
        for rgex in filter:
            s = re.sub(rgex, '<*>', s)
        if(isDebug): print("delimiter: ", delimiter)
        for de in delimiter:
            s = re.sub(de, '', s)
        if dataset=='HealthApp':
            s = re.sub(':', ': ', s)
            s = re.sub('=', '= ', s)
            s = re.sub('\|', '| ', s)
        if dataset=='Android':
            s = re.sub('\(', '( ', s)
            s = re.sub('\)', ') ', s)
        if dataset=='Android':
            s = re.sub(':', ': ', s)
            s = re.sub('=', '= ', s)
        if dataset=='HPC':
            s = re.sub('=', '= ', s)
            s = re.sub('-', '- ', s)
            s = re.sub(':', ': ', s)
        if dataset == 'BGL':
                s = re.sub('=', '= ', s)
                s = re.sub('\.\.', '.. ', s)
                s = re.sub('\(', '( ', s)
                s = re.sub('\)', ') ', s)
        if dataset == 'Hadoop':
                s = re.sub('_', '_ ', s)
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
                s = re.sub('\(', '( ', s)
                s = re.sub('\)', ') ', s)
        if dataset == 'HDFS':
                s = re.sub(':', ': ', s)
        if dataset == 'Linux':
            s = re.sub('=', '= ', s)
            s = re.sub(':', ': ', s)
        if dataset == 'Spark':
            s = re.sub(':', ': ', s)
        if dataset == 'Thunderbird':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
        if dataset == 'Windows':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
                s = re.sub('\[', '[ ', s)
                s = re.sub(']', '] ', s)
        if dataset == 'Zookeeper':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
        if(isDebug): print("s2: ", s)
        s = re.sub(',', ', ', s)
        if(isDebug): print("s3: ", s)
        s = re.sub(' +',' ',s).split(' ')
        if(isDebug): print("s4: ", s)
        s.insert(0,str(line_id))
        if(isDebug): print("s5: ", s)
        lenth = 0
        for token in s:
            # print(token)
            set.setdefault(str(lenth), []).append(token)
            lenth += 1
        if(isDebug): print("set: ",set)
        # print(s)
        # sys.exit()
        lena=len(s)
        group_len.setdefault(lena,[]).append(s)  # first grouping: logs with the same length
        if(isDebug): print("group_len: ", group_len)
        if(isDebug): print("lena: ",lena)
        # print(s)
        # sys.exit()
        line_id+=1
    # print(group_len[6])
    # sys.exit()
    tuple_vector = {}
    frequency_vector={}
    a = max(group_len.keys())  # a: the biggest length of the log in this dataset
    i=0
    fre_set={}   # saving each word's frequency
    if(isDebug): print("="*20)
    if(isDebug): print("the biggest length of the log in this dataset: ", a)
    if(isDebug): print("=" * 20)
    while i < a:
        if(isDebug): print("set[str(i)]: ", set[str(i)])
        for word in set[str(i)]:   # counting each word's frequency
            word=str(i)+' '+word
            if(isDebug): print("word: ", word)
            if word in fre_set.keys():  # check if the "word" in fre_set
                fre_set[word] = fre_set[word] + 1  # frequency of "word" + 1
            else:
                fre_set[word] = 1
            if(isDebug): print("fre_set: ", fre_set)
        i += 1
    if(isDebug): print("=" * 20)
    if(isDebug): print("using fre_set to generate frequency vector for the log")
    if(isDebug): print("=" * 20)
    for key in group_len.keys():  # using fre_set to generate frequency vector for the log
        for s in group_len[key]:  # in each log group with the same length
            position = 0
            fre = []
            fre_common = []
            skip_lineid=1
            if(isDebug): print("s: ", s)
            for word_character in s:
                if(isDebug): print("word_character: ", word_character)
                if skip_lineid==1:
                    skip_lineid=0
                    continue
                frequency_word=fre_set[str(position+1)+' '+word_character]
                if(isDebug): print("frequency_word: ", frequency_word, ", ({})".format(str(position+1)+' '+word_character))
                tuple = ((frequency_word), word_character, position)  # tuple=(frequency,word_character, position)
                fre.append(tuple)
                fre_common.append((frequency_word))
                position += 1
            if(isDebug): print("fre_common: ", fre_common)
            tuple_vector.setdefault(key,[]).append(fre)
            frequency_vector.setdefault(key,[]).append(fre_common)
    if(isDebug): print("group_len: ", group_len)
    if(isDebug): print("tuple_vector: ", tuple_vector)
    if(isDebug): print("frequency_vector: ", frequency_vector)
    if(isDebug): sys.exit()
    return group_len,tuple_vector,frequency_vector


def tuple_generate(group_len,tuple_vector,frequency_vector):
    '''
    Generate word combinations
    Output:
        sorted_tuple_vector: each tuple in the tuple_vector will be sorted according their frequencies.
        word_combinations:  words in the log with the same frequency will be grouped as word combinations and will
                            be arranged in descending order according to their frequencies.
        word_combinations_reverse:  The word combinations in the log will be arranged in ascending order according
                                    to their frequencies.

    '''
    """
    単語の組み合わせを生成する
     出力：
         sorted_tuple_vector: tuple_vector 内の各タプルは頻度に従ってソートされます。
         word_combinations: ログ内の同じ頻度の単語が単語の組み合わせとしてグループ化され、頻度に従って降順に並べられます。
         word_combinations_reverse: ログ内の単語の組み合わせは、頻度に従って昇順に並べられます。
    """
    isDebug = False
    sorted_tuple_vector = {}
    word_combinations = {}
    word_combinations_reverse = {}
    for key in group_len.keys():
        root_set = {''}
        for fre in tuple_vector[key]:
            if(isDebug): print("fre: ", fre)
            sorted_fre_reverse = sorted(fre, key=lambda tup: tup[0], reverse=True)
            if(isDebug): print("sorted_fre_reverse: ", sorted_fre_reverse)
            root_set.add(sorted_fre_reverse[0])
            sorted_tuple_vector.setdefault(key,[]).append(sorted_fre_reverse)
        if(isDebug): print("sorted_tuple_vector: ", sorted_tuple_vector)
        # if(isDebug): sys.exit()
        for fc in frequency_vector[key]:
            if(isDebug): print("key: {}, fc: {}".format(key, fc))
            number = Counter(fc)
            result = number.most_common()
            if(isDebug): print("result: ", result)
            sorted_result = sorted(result, key=lambda tup: tup[1], reverse=True)
            if(isDebug): print("sorted_result: ", sorted_result)
            sorted_fre = sorted(result, key=lambda tup: tup[0], reverse=True)
            if(isDebug): print("sorted_fre: ", sorted_fre)
            word_combinations.setdefault(key,[]).append(sorted_result)
            word_combinations_reverse.setdefault(key,[]).append(sorted_fre)
    if(isDebug): print("sorted_tuple_vector: ", sorted_tuple_vector)
    if(isDebug): print("word_combinations: ", word_combinations)
    if(isDebug): print("word_combinations_reverse: ", word_combinations_reverse)
    if(isDebug): sys.exit()
    return sorted_tuple_vector, word_combinations, word_combinations_reverse

class tupletree:
    '''
    tupletree(sorted_tuple_vector[key], word_combinations[key], word_combinations_reverse[key], tuple_vector[key], group_len[key])

    '''
    def __init__(self,sorted_tuple_vector,word_combinations,word_combinations_reverse,tuple_vector,group_len):
        self.sorted_tuple_vector=sorted_tuple_vector
        self.word_combinations=word_combinations
        self.word_combinations_reverse = word_combinations_reverse
        self.tuple_vector = tuple_vector
        self.group_len = group_len
        # print(self.word_combinations)
        # sys.exit()

    def find_root(self, threshold_per):
        root_set_detail_ID={}
        root_set_detail={}
        root_set = {}
        i=0
        for fc in self.word_combinations:
            count=self.group_len[i]
            threshold=(max(fc, key=lambda tup: tup[0])[0])*threshold_per
            m=0
            for fc_w in fc:
                # print("fc_w: ", fc_w)
                if fc_w[0]>=threshold:
                    a = self.sorted_tuple_vector[i].append((int(count[0]), -1, -1))
                    root_set_detail_ID.setdefault(fc_w,[]).append(self.sorted_tuple_vector[i])
                    root_set.setdefault(fc_w,[]).append(self.word_combinations_reverse[i])
                    root_set_detail.setdefault(fc_w, []).append(self.tuple_vector[i])
                    break
                if fc_w[0]>=m:
                    candidate=fc_w
                    m=fc_w[0]
                if fc_w == fc[len(fc)-1]:
                    a = self.sorted_tuple_vector[i].append((int(count[0]), -1, -1))
                    root_set_detail_ID.setdefault(candidate, []).append(self.sorted_tuple_vector[i])
                    root_set.setdefault(candidate, []).append(self.word_combinations_reverse[i])
                    root_set_detail.setdefault(fc_w, []).append(self.tuple_vector[i])
            i+=1
        return root_set_detail_ID,root_set,root_set_detail

    def up_split(self,root_set_detail,root_set):
        isDebug = False
        if(isDebug): print("root_set: ", root_set)
        for key in root_set.keys():
            if(isDebug): print("key: ", key)
            tree_node=root_set[key]
            father_count = []
            if(isDebug): print("tree_node: ", tree_node)
            for node in tree_node:
                if(isDebug): print("node: ", node)
                pos = node.index(key)
                if(isDebug): print("pos: ", pos)
                for i in range(pos):
                    father_count.append(node[i])
            # sys.exit()
            father_set=set(father_count)
            if(isDebug): print("father_set: ", father_set)
            for father in father_set:
                if(isDebug): print("father: ", father, key[0])
                if father_count.count(father)==key[0]:
                    if(isDebug): print("continue")
                    continue
                else:
                    for i in range(len(root_set_detail[key])):
                        if(isDebug): print("i: ", i, len(root_set_detail[key][i]))
                        for k in range(len(root_set_detail[key][i])):
                            if(isDebug): print("k: ", k, root_set_detail[key][i][k], father[0])
                            # print(type(father[0]), type(root_set_detail[key][i][k]))
                            # print(father, root_set_detail[key][i][k])
                            # sys.exit()
                            if father[0] == root_set_detail[key][i][k]:
                                if(isDebug): print("root_set_detail[key][i][k]: ", root_set_detail[key][i][k])
                                root_set_detail[key][i][k]=(root_set_detail[key][i][k][0],'<*>',root_set_detail[key][i][k][2])
                                if(isDebug): print("root_set_detail[key][i][k]: ", root_set_detail[key][i][k])
                                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                                print("Please Check Code Here!!")
                                sys.exit()
                    break
        # if (isDebug): sys.exit()
        return root_set_detail

    def down_split(self,root_set_detail_ID,threshold, root_set_detail):
        isDebug = False
        if(isDebug): print("root_set_detail_ID: ", root_set_detail_ID)
        down_split_variables = {}   #hiro877

        for key in root_set_detail_ID.keys():
            thre = threshold
            detail_order=root_set_detail[key]
            m=[]
            child={}
            variable={''}
            variable.remove('')
            variable_set={''}
            variable_set.remove('')
            m_count=0
            fist_sentence=detail_order[0]
            for det in fist_sentence:
                if det[0] != key[0]:
                    m.append(m_count)
                m_count+=1
            for i in m:
                for node in detail_order:
                    if i <len(node):
                        child.setdefault(i, []).append(node[i][1])
            v_flag = 0
            for i in m:
                next={''}
                next.remove('')
                result = set(child[i])
                freq = len(result)
                if freq>=thre:
                        variable=variable.union(result)
                v_flag+=1
            i=0
            while i < len(root_set_detail_ID[key]):
                j=0
                while j < len(root_set_detail_ID[key][i]):
                    if isinstance(root_set_detail_ID[key][i][j],tuple):
                        if root_set_detail_ID[key][i][j][1] in variable:
                            """ extructing param by hiro877 """
                            if not key in down_split_variables:
                                down_split_variables[key] = {}
                            key_index = str(root_set_detail_ID[key][i][j][2])
                            if not key_index in down_split_variables[key]:
                                # hiro877
                                # down_split_variables[key][key_index] = []
                                down_split_variables[key][key_index] = set()
                            # down_split_variables[key][key_index].append(root_set_detail_ID[key][i][j][1])
                            param_data = remove_specific_characters_from_back(root_set_detail_ID[key][i][j][1])
                            down_split_variables[key][key_index].add(param_data)
                            """ extructing param by hiro877 End"""

                            # print(key, root_set_detail_ID[key][i][j])
                            root_set_detail_ID[key][i][j] = (
                            root_set_detail_ID[key][i][j][0], '<*>', root_set_detail_ID[key][i][j][2])
                            # print(root_set_detail_ID)
                            # # sys.exit()
                            # print(root_set_detail_ID[key][i][j])
                            # print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                            # sys.exit()
                    j += 1
                i+=1
        if(isDebug): print("root_set_detail_ID: ", root_set_detail_ID)
        # if(isDebug): sys.exit()
        # print(variable)
        # print("="*20)
        # print(down_split_variables)
        # sys.exit()
        return root_set_detail_ID, down_split_variables

def output_result(parse_result):
    # print(parse_result[6])
    isDebug = False
    template_set={}
    # print("=========")
    # print(parse_result)
    # sys.exit()

    for key in parse_result.keys():
        if(isDebug): print("key: ", key)
        for pr in parse_result[key]:
            if(isDebug): print("pr: ", pr)
            sort = sorted(pr, key=lambda tup: tup[2])
            print(sort)
            sys.exit()
            if(isDebug): print("sort: ", sort)
            i=1
            template=[]
            while i < len(sort):
                this=sort[i][1]
                if(isDebug): print("this: ", this)
                if bool('<*>' in this):
                    if(isDebug): print("bool('<*>' in this)")
                    template.append('<*>')
                    i+=1
                    continue
                if exclude_digits(this):
                    if(isDebug): print("exclude_digits(this)")
                    template.append('<*>')
                    i += 1
                    continue
                template.append(sort[i][1])
                i+=1
            template=tuple(template)
            template_set.setdefault(template,[]).append(pr[len(pr)-1][0])
    if(isDebug): print(template_set)
    # if(isDebug): sys.exit()
    return template_set

def output_result_extract_param(parse_result, down_split_variables, variables_templates):
    isDebug = False
    template_set={}
    exclude_digits_variables = {}
    exclude_digits_variables_output = {}
    for key in parse_result.keys():
        if(isDebug): print("key: ", key)
        for pr in parse_result[key]:
            if(isDebug): print("pr: ", pr)
            sort = sorted(pr, key=lambda tup: tup[2])
            if(isDebug): print("sort: ", sort)
            i=1
            template=[]
            while i < len(sort):
                this=sort[i][1]
                if(isDebug): print("this: ", this)
                if bool('<*>' in this):
                    if(isDebug): print("bool('<*>' in this)")
                    template.append('<*>')
                    i+=1
                    continue
                if exclude_digits(this):
                    if(isDebug): print("exclude_digits(this)")
                    """ extructing param by hiro877 """
                    if(isDebug): print("exclude_digits() is True. this={}".format(this))
                    if not key in exclude_digits_variables:
                        exclude_digits_variables[key] = {}
                    key_index = str(i-1)
                    if not key_index in exclude_digits_variables[key]:
                        # hiro877
                        # exclude_digits_variables[key][key_index] = []
                        exclude_digits_variables[key][key_index] = set()
                    # exclude_digits_variables[key][key_index].append(this)
                    exclude_digits_variables[key][key_index].add(this)
                    """ extructing param by hiro877 End"""
                    template.append('<*>')
                    i += 1
                    continue
                template.append(sort[i][1])
                i+=1
            template=tuple(template)
            template_set.setdefault(template,[]).append(pr[len(pr)-1][0])

        if key in down_split_variables:
            # print("template: {}, down_split_variables: {}".format(template, down_split_variables[key]))
            variables_templates[template] = down_split_variables[key]
        if key in exclude_digits_variables:
            # print("template: {}, exclude_digits_variables: {}".format(template, exclude_digits_variables[key]))
            exclude_digits_variables_output[template] = exclude_digits_variables[key]

    # print("=== output_result_extract_param() ===")
    # print("down_split_variables; ", down_split_variables)
    # print("exclude_digits_variables: ", exclude_digits_variables)
    # print("exclude_digits_variables_output: ", exclude_digits_variables_output)
    # print("="*20)
    # print(variables_templates)
    # print("=" * 20)
    # sys.exit()
    return template_set, variables_templates, exclude_digits_variables_output

def parse(sentences,filter,dataset,threshold,delimiter,starttime,efficiency,df_input):
    """
    - Variables Construction
    {"Key": {"Index Id": [v1, v2, ...], "IId2": [v1, v2, ...]}, "key2": {"": []}, ...}
    For example:
    {(6, 3): {'1': ['apple', 'orange', 'greap', 'banana', 'cherry', 'peach'], '3': ['error', 'null', 'false', 'true', 'zero', 'one']}}
    """
    group_len, tuple_vector, frequency_vector = get_frequecy_vector(sentences, filter,delimiter,dataset)
    sorted_tuple_vector, word_combinations, word_combinations_reverse= tuple_generate(group_len, tuple_vector, frequency_vector)
    df_example = df_input
    template_set = {}

    for key in group_len.keys():
        # print("key, value: ", key, group_len[key])
        Tree = tupletree(sorted_tuple_vector[key], word_combinations[key], word_combinations_reverse[key], tuple_vector[key], group_len[key])
        root_set_detail_ID, root_set, root_set_detail = Tree.find_root(0)
        '''
        ### code for root node selection evaluation.
        for k in root_set_detail:
            choose_flag=1
            for log in root_set_detail[k]:
                c=0
                loglines+=1
                while c <len(log)-1:
                    if log[c][0]==k[0]:
                        if "<*>" in log[c][1] and log[c][1] not in template[log[len(log)-1][0]]:
                            choose_flag=0
                    if choose_flag==0:
                        break
                    c+=1
                if choose_flag == 0:
                    break
                correct_choose+=1
        '''
        root_set_detail_ID = Tree.up_split(root_set_detail_ID, root_set)
        parse_result, down_split_variables = Tree.down_split(root_set_detail_ID, threshold, root_set_detail)
        template_set.update(output_result(parse_result))
        # template_set.update(output_result_extract_param(parse_result, down_split_variables))

    '''
    ### code for root node selection evaluation.
    print(
        "correct choose root noed ratio ==" + str(correct_choose / loglines) + "===detail===correct_choose:" + str(
            correct_choose) + " logline:" + str(loglines))
    '''
    endtime=datetime.datetime.now()
    print("Parsing done...")
    print("Time taken   =   " +PINK+ str(endtime-starttime)+RESET)
    if efficiency==True:
        return endtime
    '''
    output parsing result
    '''
    template_=len(sentences)*[0]
    EventID=len(sentences)*[0]
    IDnumber=0

    for k1 in template_set.keys():
        group_accuracy = {''}
        group_accuracy.remove('')
        for i in template_set[k1]:
            template_[i]=' '.join(k1)
            EventID[i] ="E"+str(IDnumber)
        IDnumber+=1
    df_example['EventTemplate']=template_
    df_example['EventId'] =EventID
    return df_example,template_set


def save_result(dataset,df_output,template_set):
    df_output.to_csv('Parseresult/' + dataset + 'result.csv', index=False)
    with open('Parseresult/' + dataset + '_template.csv', 'w') as f:
        for k1 in template_set.keys():
            f.write(' '.join(list(k1)))
            f.write('  ' + str(len(template_set[k1])))
            f.write('\n')
        f.close()


def exclude_digits(string):
    '''
    exclude the digits-domain words from partial constant
    '''
    # print(string)
    pattern = r'\d'
    digits = re.findall(pattern, string)
    # print(digits)
    if len(digits)==0:
        return False
    return len(digits)/len(string) >= 0.3

def analyze_dataset(target_name, sentences,filter,dataset,threshold,delimiter):
    """
        - Variables Construction
        {"Key": {"Index Id": [v1, v2, ...], "IId2": [v1, v2, ...]}, "key2": {"": []}, ...}
        For example:
        {(6, 3): {'1': ['apple', 'orange', 'greap', 'banana', 'cherry', 'peach'], '3': ['error', 'null', 'false', 'true', 'zero', 'one']}}
    """
    group_len, tuple_vector, frequency_vector = get_frequecy_vector(sentences, filter, delimiter, dataset)
    sorted_tuple_vector, word_combinations, word_combinations_reverse = tuple_generate(group_len, tuple_vector,
                                                                                       frequency_vector)
    template_set = {}
    variables_templates = {}
    for key in group_len.keys():
        Tree = tupletree(sorted_tuple_vector[key], word_combinations[key], word_combinations_reverse[key],
                         tuple_vector[key], group_len[key])
        root_set_detail_ID, root_set, root_set_detail = Tree.find_root(0)

        root_set_detail_ID = Tree.up_split(root_set_detail_ID, root_set)
        parse_result, down_split_variables = Tree.down_split(root_set_detail_ID, threshold, root_set_detail)
        template_result, variables_templates, exclude_digits_variables = output_result_extract_param(parse_result, down_split_variables, variables_templates)
        template_set.update(template_result)

    """
    Save Result
    """
    os.makedirs("Results/Analized/", exist_ok=True)
    now = datetime.datetime.now()
    save_path = "Results/Analized/" + target_name+ "_" + now.strftime('%m%d_%H%M%S') + '.csv'
    log_num = 0
    header = ["Template", "Index", "Parameters"]
    with open(save_path, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        """ down_split() """
        for key , values in variables_templates.items():
            print(key, values)
            for k, v in values.items():
                l = [key, k]
                l = l + list(v)
                writer.writerow(l)

        """ exclude_digits """
        writer.writerow(header)
        for key , values in exclude_digits_variables.items():
            print(key, values)
            for k, v in values.items():
                l = [key, k]
                l = l + list(v)
                writer.writerow(l)

def remove_specific_characters_from_back(input_str):
    # 定義された文字を格納するリスト
    characters_to_remove = [",", ")", "}", "]"]

    # 文字列を逆順で探索し、指定された文字を削除
    for char in reversed(input_str):
        if char in characters_to_remove:
            input_str = input_str[:-1]  # 最後の文字を削除
        else:
            break  # 最初の指定されていない文字で終了

    return input_str

class format_log:    # this part of code is from LogPai https://github.com/LogPai

    def __init__(self, log_format, indir='./'):
        self.path = indir
        self.logName = None
        self.df_log = None
        self.log_format = log_format

    def format(self, logName):


        self.logName=logName

        self.load_data()

        return self.df_log





    def generate_logformat_regex(self, logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\\\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex
    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe
        """
        log_messages = []
        linecount = 0
        with open(log_file, 'r', encoding='UTF-8') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf


    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logName), regex, headers, self.log_format)



