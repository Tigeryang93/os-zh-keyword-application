# # -*- coding: utf-8 -*-
# Author: yanghu
# Data: 2018-11-09
# Use: 提取文本中的关键词，使用tf-idf和textrank算法。
import os
import re
import sys
import codecs
from pyhanlp import *
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from collections import Counter
import jieba.analyse


def generate_keywords(text, number):
    """
    textrank4zh: 针对中文文本的TextRank算法实现，用于提取关键词和摘要。 https://github.com/letiantian/TextRank4ZH
    pyhanlp: HanLP自然语言处理工具包的python接口，实现TextRank关键词提取算法。 https://github.com/hankcs/pyhanlp
    jieba: jieba分词工具包，实现TF-IDF算法，TextRank算法的关键词抽取。 https://github.com/fxsjy/jieba

    :param text: 文本
    :param number: 关键词个数
    :return: 关键词字典
    """
    keywords = {}
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)
    for item in tr4w.get_keywords(number, word_min_len=1):
        keywords.setdefault('textrankzh', []).append(item.word)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')
    abstract = ""
    TextRankKeyword = JClass('com.hankcs.hanlp.summary.TextRankKeyword')

    for item in tr4s.get_key_sentences(num=2):
        abstract += item.sentence
    tr4w.analyze(text=abstract, lower=True, window=2)
    for item in tr4w.get_keywords(number, word_min_len=1):
        keywords.setdefault('textrank_abs', []).append(item.word)

    for item in HanLP.extractKeyword(text, number):
        keywords.setdefault('hanlp', []).append(item)
    for item in HanLP.extractKeyword(abstract, number):
        keywords.setdefault('hanlp_abs', []).append(item)

    for item in jieba.analyse.extract_tags(text, topK=number, withWeight=False, allowPOS=()):
        keywords.setdefault('tfidf', []).append(item)
    for item in jieba.analyse.textrank(text, topK=number, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')):
        keywords.setdefault('jiebarank', []).append(item)
    for item in jieba.analyse.extract_tags(abstract, topK=number, withWeight=False, allowPOS=()):
        keywords.setdefault('tfidf_abs', []).append(item)
    for item in jieba.analyse.textrank(abstract, topK=number, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')):
        keywords.setdefault('jiebarank_abs', []).append(item)
    return keywords


files = os.listdir('546134406')
cop = re.compile("[^\u4e00-\u9fff^\u2000-\u206f^\u3000-\u303f^\uff00-\uffef^,]")

for file in files:
    if file[0] != '.':
        txt_path = '546134406/' + file + '/content.txt'
        contents = open(txt_path, 'r', encoding='utf-8')
        text = ""
        for content in contents.readlines():
            content = content[:-1]
            content = re.sub(cop, "", content)
            text += content
        number = 10
        key = generate_keywords(text, number)
        words = []

        if key.__contains__('textrankzh'):
            for word in key['textrankzh']:
                words.append(word)
        if key.__contains__('textrankzh_abs'):
            for word in key['textrankzh_abs']:
                words.append(word)
        if key.__contains__('tfidf'):
            for word in key['tfidf']:
                words.append(word)
        if key.__contains__('tfidf_abs'):
            for word in key['tfidf_abs']:
                words.append(word)
        if key.__contains__('jiebarank'):
            for word in key['jiebarank']:
                words.append(word)
        if key.__contains__('jiebarank_abs'):
            for word in key['jiebarank_abs']:
                words.append(word)
        if key.__contains__('hanlp_abs'):
            for word in key['hanlp_abs']:
                words.append(word)
        if key.__contains__('hanlp'):
            for word in key['hanlp']:
                words.append(word)

        if len(Counter(words)) < number:
            number = len(Counter(words))
        key_pos = {}
        for j in range(number):
            k, v = Counter(words).most_common(number)[j]
            key_pos.update({k: text.index(k)})

        filename = os.path.join('E:/实验室/谭老师/关键字/546134406', file, 'key.txt')
        newfile = open(filename, 'w', encoding='utf-8')
        for k, v in sorted(key_pos.items(), key=lambda item: item[1]):
            newfile.write(k + ' ')
        newfile.close()
        contents.close()
