#!/usr/bin/env python3
# coding: utf-8
# File: causality_pattern.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-12

import re, jieba
import jieba.posseg as pseg
from pyltp import SentenceSplitter


import nltk
import nltk.data
from nltk import pos_tag
from nltk import RegexpParser

 


class CausalityExractor():
    def __init__(self):
        pass

    # '''1由果溯因配套式en'''
    # def ruler1_en(self, sentence):
    #     '''
    #     conm2:〈is,because〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
    #     conm2_model:<Conj>{Effect},<Conj>{Cause}
    #     '''
    #     datas = list()
    #     word_pairs =[['is', 'because']]
    #     for word in word_pairs:
    #         pattern = re.compile(r'\s?(is?)/[IN|VBZ]+\s(.*)(because|cause)/[IN|VBZ]+\s(.*)')
    #         result = pattern.findall(sentence)
    #         data = dict()
    #         if result:
    #             data['tag'] = result[0][0] + '-' + result[0][2]
    #             data['cause'] = result[0][3]
    #             data['effect'] = result[0][1]
    #             datas.append(data)
    #     if datas:
    #         return datas[0]
    #     else:
    #         return {}

    '''0由果溯因居端式精确'''
    def ruler0(self, sentence):
        '''
        cons3:因为、由于
        cons3_model:{Effect}<Conj...>{Cause}
        '''
        pattern = re.compile(r'(.*)(is|was|are|were)?\s(caused by|arise from|arise out of|trigered by|induced by)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][1]
            data['cause'] = result[0][2]
            data['effect'] = result[0][0]

        return data

    '''1由果溯因配套式'''
    def ruler1(self, sentence):
        '''
        conm2: <cause of,is>, <>                     〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        '''
        datas = list()
        word_pairs =[['cause of', 'is'], ['cause of', 'was'], ['cause of', 'are'], ['cause of', 'were'],
                     ['effect of', 'is'],['reason of','is'],['reason of','was'],['reason of','were'],['reason of','are'],
                     ['by reason that','is'],['by reason that','was'],['by reason that','were'],['by reason that','are'],
                     ['by reason why','is'],['by reason why','was'],['by reason why','are'],['by reason why','were'],
                     ['reason for','is'],['reason for','are'],['reason for','was'],['reason for','were']]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)' % (word[0], word[1]))
            result = pattern.findall(sentence)
            data = dict()
            if result:
                data['tag'] = result[0][0] + '-' + result[0][2]
                data['cause'] = result[0][3]
                data['effect'] = result[0][1]
                datas.append(data)
        if datas:
            return datas[0]
        else:
            return {}
    '''2由因到果配套式'''
    def ruler2(self, sentence):
        '''
        conm1:
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        '''
        datas = list()
        word_pairs =[['is', 'cause for'], ['was', 'cause for'], ['are', 'cause for'],["were","cause for"],
                    ['is', 'in the cause of'], ['was', 'in the cause of'], ['are', 'in the cause of'],["were","in the cause of"],
                    ['is', 'trigger of'], ['was', 'trigger of'], ['are', 'trigger of'],['were','trigger of'],
                    ['is', 'affected by'], ['was', 'affected by'], ['are', 'affected by'],['were','affected by'],
                    ['is', 'effect on'], ['was', 'effect on'], ['are', 'effect on'],['were','effect on'],
                    ['if', 'then']]

        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c]+\s(.*)' % (word[0], word[1]))
            result = pattern.findall(sentence)
            data = dict()
            if result:
                data['tag'] = result[0][0] + '-' + result[0][2]
                data['cause'] = result[0][1]
                data['effect'] = result[0][3]
                datas.append(data)
        if datas:
            return datas[0]
        else:
            return {}
    '''3由因到果居中式明确'''
    def ruler3(self, sentence):
        '''
        cons2:于是、所以、故、致使、以致[于]、因此、以至[于]、从而、因而
        cons2_model:{Cause},<Conj...>{Effect}
        '''

        pattern = re.compile(r'(.*)[,，]+.*(hence|therefore|thus|thereby|accordingly|consequently|so|in this way|that\'s why|以至于?|从而|因而)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][1]
            data['cause'] = result[0][0]
            data['effect'] = result[0][2]
        return data
    '''4由因到果居中式精确'''
    def ruler4(self, sentence):
        '''
        verb1: cause,            牵动、导向、使动、导致、勾起、引入、指引、使、予以、产生、促成、造成、引导、造就、促使、酿成、
        verb1_model:{Cause}(,)<Verb|Adverb...>{Effect}
        '''
        pattern = re.compile(r'(.*)\s+(cause|causing|caused|trigger|triggering|triggered|affect|affecting|affected|induce|inducing|induced|reveal|revealed|revealing|lead to|leading to|leaded to|bring about|bringing about|brought about|bring on|bringing on|brought on|give rise to|given rise to|giving rise to|increase|result in|induce|so that.*\sto)/[d|v]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][1]
            data['cause'] = result[0][0]
            data['effect'] = result[0][2]
        return data
    '''5由因到果前端式模糊'''
    def ruler5(self, sentence):
        '''
        prep:为了、依据、为、按照、因[为]、按、依赖、照、比、凭借、由于
        prep_model:<Prep...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(in order to|for the purpose of|after|因为|因|按|依赖|凭借|由于)/[p|c]+\s(.*)[,，]+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][0]
            data['cause'] = result[0][1]
            data['effect'] = result[0][2]

        return data

    '''6由因到果居中式模糊'''
    def ruler6(self, sentence):
        '''
        adverb:以免、以便、为此、才
        adverb_model:{Cause},<Verb|Adverb...>{Effect}
        '''
        pattern = re.compile(r'(.*)(以免|以便|为此|才)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][1]
            data['cause'] = result[0][0]
            data['effect'] = result[0][2]
        return data

    '''7由因到果前端式精确'''
    def ruler7(self, sentence):
        '''
        cons1:既[然]、因[为]、如果、由于、只要
        cons1_model:<Conj...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(because|as a result of|due to|owning to|in view of|as a consequence of|on account of)/[p|c]+\s(.*)[,，]+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][0]
            data['cause'] = result[0][1]
            data['effect'] = result[0][2]
        return data
    '''8由果溯因居中式模糊'''
    def ruler8(self, sentence):
        '''
        3
        verb2:根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、源于、根源于、立足[于]
        verb2_model:{Effect}<Prep...>{Cause}
        '''

        pattern = re.compile(r'(.*)(derive.*\sfrom|because of|since|for|through|after|stem from|result from|thanks to|as a result of|due to|owning to|in consequence of|in view of|as a consequence of|on account of|in that|on the grounds that|as|as long as|for this reason that|for the reason that)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['tag'] = result[0][1]
            data['cause'] = result[0][2]
            data['effect'] = result[0][0]
        return data


    '''抽取主函数'''
    def extract_triples(self, sentence):
        infos = list()
      #  print(sentence)
        if self.ruler0(sentence):
            infos.append(self.ruler0(sentence))
        elif self.ruler1(sentence):
            infos.append(self.ruler1(sentence))
        elif self.ruler2(sentence):
            infos.append(self.ruler2(sentence))
        elif self.ruler3(sentence):
            infos.append(self.ruler3(sentence))
        elif self.ruler4(sentence):
            infos.append(self.ruler4(sentence))
        elif self.ruler5(sentence):
            infos.append(self.ruler5(sentence))
        elif self.ruler6(sentence):
            infos.append(self.ruler6(sentence))
        elif self.ruler7(sentence):
            infos.append(self.ruler7(sentence))
        elif self.ruler8(sentence):
            infos.append(self.ruler8(sentence))
        # elif self.ruler9(sentence):
        #     infos.append(self.ruler9(sentence))

        return infos

    '''抽取主控函数'''
    def extract_main(self, content):
        sentences = self.splitSentence(content)
        datas = list()
        for sentence in sentences:
            subsents = self.fined_sentence(sentence)
            subsents.append(sentence)
            for sent in subsents:
                # sent=sent.strip()
                # text =sent.split()
                # tokens_tag = pos_tag(text)
                # sent = ' '.join([word[0] + '/' + word[1] for word in tokens_tag])
                sent = ' '.join([word.word + '/' + word.flag for word in pseg.cut(sent)])
                result = self.extract_triples(sent)
                if result:
                    for data in result:
                        if data['tag'] and data['cause'] and data['effect']:
                            datas.append(data)
        return datas

    '''文章分句处理'''
    def process_content(self, content):
        return [sentence for sentence in SentenceSplitter.split(content) if sentence]

    '''SplitSentences'''
    def splitSentence(self,paragraph):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(paragraph)
        return sentences

    '''切分最小句'''
    def fined_sentence(self, sentence):
        return re.split(r'[?!,;]', sentence)


'''测试'''
def test():
    content0 = """他之所以这么嚣张，是因为我们太软弱了"""
    content0_en = """He is so arrogant, because we are too weak. shit!"""

    content1 = """
    截至2008年9月18日12时，5·12汶川地震共造成69227人死亡，374643人受伤，17923人失踪，是中华人民共和国成立以来破坏力最大的地震，也是唐山大地震后伤亡最严重的一次地震。
    """
    content2 = '''
    2015年1月4日下午3时39分左右，贵州省遵义市习水县二郎乡遵赤高速二郎乡往仁怀市方向路段发生山体滑坡，发生规模约10万立方米,导致多辆车被埋，造成交通双向中断。此事故引起贵州省委、省政府的高度重视，省长陈敏尔作出指示，要求迅速组织开展救援工作，千方百计实施救援，减少人员伤亡和财物损失。遵义市立即启动应急救援预案，市应急办、公安、交通、卫生等救援力量赶赴现场救援。目前，灾害已造成3人遇难1人受伤，一辆轿车被埋。
    当地时间2010年1月12日16时53分，加勒比岛国海地发生里氏7.3级大地震。震中距首都太子港仅16公里，这个国家的心脏几成一片废墟，25万人在这场骇人的灾难中丧生。此次地震中的遇难者有联合国驻海地维和部队人员，其中包括8名中国维和人员。虽然国际社会在灾后纷纷向海地提供援助，但由于尸体处理不当导致饮用水源受到污染，灾民喝了受污染的水后引发霍乱，已致至少2500多人死亡。
    '''
    content3 = '''
    American Eagle 四季度符合预期 华尔街对其毛利率不满导致股价大跌
    我之所以考试没及格，是因为我没有好好学习。
    因为天晴了，所以我今天晒被子。
    因为下雪了，所以路上的行人很少。
    我没有去上课是因为我病了。
    因为早上没吃的缘故，所以今天还没到放学我就饿了.
    因为小华身体不舒服，所以她没上课间操。
    因为我昨晚没睡好，所以今天感觉很疲倦。
    因为李明学习刻苦，所以其成绩一直很优秀。
    雨水之所以不能把石块滴穿，是因为它没有专一的目标，也不能持之以恒。
    他之所以成绩不好，是因为他平时不努力学习。
    你之所以提这个问题，是因为你没有学好关联词的用法。
    减了税,因此怨声也少些了。
    他的话引得大家都笑了，室内的空气因此轻松了很多。
    他努力学习，因此通过了考试。
    既然明天要下雨，就不要再出去玩。
    既然他还是那么固执，就不要过多的与他辩论。
    既然别人的事与你无关，你就不要再去过多的干涉。
    既然梦想实现不了，就换一个你自己喜欢的梦想吧。
    既然别人需要你，你就去尽力的帮助别人。
    既然生命突显不出价值，就去追求自己想要的生活吧。
    既然别人不尊重你，就不要尊重别人。 因果复句造句
    既然题目难做，就不要用太多的时间去想，问一问他人也许会更好。
    既然我们是学生，就要遵守学生的基本规范。
    '''
    extractor = CausalityExractor()
    datas = extractor.extract_main(content0)
    for data in datas:
        print('******'*4)
        print('cause', ''.join([word.split('/')[0] for word in data['cause'].split(' ') if word.split('/')[0]]))
        print('tag', data['tag'])
        print('effect', ''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]]))

test()
