# encoding: UTF-8
import re
import csv

in_f = '../data/dict_revised_2015_20190329_1.csv'
out_f = '../data/out.csv'
ranking_f = ac_corpus_csv = '../data/ACCorpusCharacterlist.csv'


def split_meaning_text(meaning_text):
    """根據詞性對詞條釋義文本進行分割
    :param meaning_text: 詞條釋義文本
    :return pos_meaning_list: 由各個釋義所組成的列表"""
    pos_meaning_list = re.findall(r'\[.][^\[]*', meaning_text)
    return pos_meaning_list


def extract_pos(pos_meaning):
    pos = re.match(r'\[\w]', pos_meaning).group()
    return pos


def split_pos_meaning(pos_meaning):
    meanings = re.findall(r'\d[^\d]*', pos_meaning)
    if meanings:
        return meanings
    else:
        meaning = re.sub(r'\[.]', '', pos_meaning)
        return [meaning]


def extract_index(meaning):
    index = '0'
    m = re.match(r'\d', meaning)
    if m:
        index = m.group()
    return index


def extract_gloss(meaning):
    gloss = ''
    m = re.match(r'(?:\d\.)?([^《》〈〉]*。)(?:(?:\w．)|(?:《.*》：))?', meaning)
    if m:
        gloss = m.group(1)
    return gloss


def extract_quote(meaning):
    quote = []
    book_quote = re.findall(r'(?:\w．)?\w{0,5}《[^》(?:說文解字)(?:廣韻)(?:玉篇)(?:爾雅)]+》：「[^《〈]*?」', meaning)
    article_quote = re.findall(r'(?:\w．)?\w{0,5}〈[^〉]+〉\w{0,3}：「[^《〈]*?」', meaning)
    if book_quote:
        quote += book_quote
    if article_quote:
        quote += article_quote
    if len(quote) == 4:
        pass
    elif len(quote) == 3:
        quote += ['']
    elif len(quote) == 2:
        quote += ['', '']
    elif len(quote) == 1:
        quote += ['', '', '']
    else:
        quote = ['', '', '', '']
    return quote


if __name__ == '__main__':
    rank_dict = {}
    with open(ranking_f, 'r') as rank_f:
        rank_f_csv = csv.reader(rank_f)
        header = next(rank_f_csv)
        for row in rank_f_csv:
            (ranking, char, show_times, _, _) = row
            rank_dict[char] = [ranking, show_times]

    with open(out_f, 'w') as out_f:
        note_id = 0
        out_f_csv = csv.writer(out_f)
        with open(in_f, 'r') as f:
            f_csv = csv.reader(f)
            header = next(f_csv)
            for row in f_csv:
                char = row[2]
                if char not in rank_dict:
                    continue
                (ranking, show_times) = rank_dict[char]
                meaning_text = row[10].replace('\n', '')
                pron = row[7]
                pos_meaning_list = split_meaning_text(meaning_text)
                for pos_meaning in pos_meaning_list:
                    note_id += 1
                    pos = extract_pos(pos_meaning)
                    meanings = split_pos_meaning(pos_meaning)
                    for meaning in meanings:
                        index = extract_index(meaning)
                        gloss = extract_gloss(meaning)
                        quote = extract_quote(meaning)
                        if quote == ['', '', '', '']:
                            continue
                        (quote_1, quote_2, quote_3, quote_4) = quote
                        # if quote_4 != '':  # 最多的時候會有 4 句經典的引用
                        #     print(quote)
                        row = str(
                            note_id), show_times, ranking, \
                            char, pron, pos, index, gloss, \
                            quote_1, quote_2, quote_3, quote_4
                        out_f_csv.writerow(row)
