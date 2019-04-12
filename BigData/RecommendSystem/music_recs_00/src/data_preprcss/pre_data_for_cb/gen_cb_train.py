import jieba.analyse

in_file = '../../../data/merged_base.data'
out_file = '../../../data/cb_train.data'

with open(out_file, 'w') as f:
    pass

idf_file = '../../../data/idf.txt'
idf_dict = {}
with open(idf_file, 'r') as f:
    for line in f:
        word, idf_score = line.strip().split(' ')
        idf_dict[word] = idf_score

# weight of fields
RADIO_FOR_NAME = 0.9
RADIO_FOR_DESC = 0.1
RADIO_FOR_TAGS = 0.05

# prepare set to memorize item_id has presented
item_id_set = set()

with open(in_file, 'r') as f_in:
    for line in f_in:
        ss = line.strip().split('\001')
        (user_id, item_id, listen_len, listen_moment,
         gender, age, salary, user_loc,
         name, desc, total_time, item_loc, tags) = ss

        # memorize item_id, if it has presented then drop it
        if item_id in item_id_set:
            continue
        else:
            item_id_set.add(item_id)

        # 对 item 的 name、desc、tag 进行分词，召回关键词
        keyword_dict = {}  # keyword:score
        # handle `name` with dict.txt
        for kw_sc in jieba.analyse.extract_tags(name, withWeight=True):
            (keyword, score) = kw_sc
            keyword_dict[keyword] = score * RADIO_FOR_NAME
        # handle `desc` with dict.txt
        for kw_sc in jieba.analyse.extract_tags(desc, withWeight=True):
            (keyword, score) = kw_sc
            if keyword in keyword_dict:
                keyword_dict[keyword] += score * RADIO_FOR_DESC
            else:
                keyword_dict[keyword] = score * RADIO_FOR_DESC
        # handle `tags` with idf.txt
        for tag in tags.strip().split(','):
            if tag not in idf_dict:
                continue
            else:
                (keyword, score) = (tag, float(idf_dict[tag]))
                keyword_dict[keyword] = score * RADIO_FOR_TAGS

        # print(item_id)
        # print(keyword_dict)
        with open(out_file, 'a') as f:
            for keyword, score in keyword_dict.items():
                line = '{},{},{}'.format(item_id, keyword, score)
                f.write(line)
                f.write('\n')
