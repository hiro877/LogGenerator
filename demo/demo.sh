
# Linux
python analyze.py --dataset Linux --data_dir ./datasets/Linux --log_file Linux.log
python analyze.py --dataset Linux --data_dir ./datasets/Linux --log_file Linux.log > Linux_results_widowed.txt
python analyze.py --dataset Linux --data_dir ./datasets/Linux --log_file Linux.log --use_template

# Mac
python analyze.py --dataset Mac --data_dir ./datasets/Mac --log_file Mac.log
python analyze.py --dataset Mac --data_dir ./datasets/Mac --log_file Mac.log > Mac_results_widowed.txt
python analyze.py --dataset Mac --data_dir ./datasets/Mac --log_file Mac.log --use_template

# Windows
python analyze.py --dataset Windows --data_dir ./datasets/Windows --log_file Windows.log --use_data_size 5000000
python analyze.py --dataset Windows --data_dir ./datasets/Windows --log_file Windows.log --use_data_size 5000000 > Windows_results_widowed.txt

python analyze.py --dataset Windows --data_dir ./datasets/Windows --log_file Windows.log.aa
python analyze.py --dataset Windows --data_dir ./datasets/Windows --log_file Windows.log.aa --use_template

# Android
python analyze.py --dataset Android --data_dir ./datasets/Android/Android_v1 --log_file Android.log
python analyze.py --dataset Android --data_dir ./datasets/Android/Android_v1 --log_file Android.log > Android_v1_results_widowed.txt
python analyze.py --dataset Android --data_dir ./datasets/Android/Android_v1 --log_file Android.log --use_template
python analyze.py --dataset Android --data_dir ./datasets/Android/Android_v1 --log_file Android.log --use_template


# BGL
python analyze.py
python analyze.py > BGL_results_widowed.txt
python analyze.py --use_template

# Tthunderbird
# log split -> split -l 5000000 Thunderbird.log Thunderbird_5000000.log1
python analyze.py --dataset Thunderbird --data_dir ./datasets/Thunderbird --log_file Thunderbird.log --use_data_size 5000000
python analyze.py --dataset Thunderbird --data_dir ./datasets/Thunderbird --log_file Thunderbird_5000000.log1aa  > Tthunderbird_results_widowed.txt
python analyze.py --dataset Thunderbird --data_dir ./datasets/Thunderbird --log_file Thunderbird_5000000.log1aa
python analyze.py --dataset Thunderbird --data_dir ./datasets/Thunderbird --log_file Thunderbird_5000000.log1aa --use_template

### Investigate Results of Histgram
python investigate_analyzed_file.py --dataset Mac --data_dir ./results/Android/Mac
python investigate_analyzed_file.py --dataset Linux --data_dir ./results/Android/Linux
python investigate_analyzed_file.py --dataset Windows --data_dir ./results/Android/Windows
python investigate_analyzed_file.py --dataset Android --data_dir ./results/Android/Android

python investigate_analyzed_file.py --dataset BGL --data_dir ./results/Android/BGL
python investigate_analyzed_file.py --dataset Thunderbird --data_dir ./results/Android/Thunderbird_5000000
#python analyze.py
#python analyze.py