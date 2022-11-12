#!/usr/bin/env python3
# coding: utf-8
# File: causality_pattern.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-12

import re


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

    content_cause = """
    He died for a noble cause.
    The drugs tend to cause drowsiness.
    The cause of the fire is not yet known.
    The immediate cause of death is unknown.
    Unemployment is a major cause of poverty.
    Tree roots can cause damage to buildings.
    High temperatures can cause hallucination.
    Idealistic young people died for the cause.
    The photo may cause offence to some people.
    Unemployment was the chief cause of poverty.
    She was the unwitting cause of the argument.
    This would cause inflation to let rip again.
    Caffeine can cause palpitations and headaches.
    The virus can cause pregnant animals to abort.
    She was soon converted to the socialist cause.
    Cars cause pollution, both smog and acid rain.
    It had been the cause of much emotional upset.
    Eating too much salt can cause fluid retention.
    Faulty wiring is the major cause of house fires.
    Vitamin deficiency in the diet can cause illness.
    The disease can cause sterility in men and women.
    These gases cause untold damage to the environment.
    The drug may cause an aggravation of the condition.
    Heavy seas can cause cancellation of ferry services.
    Brushing wet hair can cause stretching and breakage.
    Her inability to concentrate could cause an accident.
    Reports of this kind are guaranteed to cause anxiety.
    He was the unknowing cause of all the misunderstanding.
    They worked together to advance the cause of democracy.
    Heavy drinking can cause permanent damage to the brain.
    """
    content_arise = '''
    Have a plan of action To combat any type of sibling conflict that might arise, experts suggest tons of communication among the family, as well as a plan of action.
    In the end, this will aid the company in potentially avoiding lawsuits that otherwise might arise if the AI is being produced that is not abiding by AI Ethics precepts.
    Just beware of any fees or taxes that might arise with each transaction.
    Discrepancies between the trial data and real-world experience might arise from the timing of the original research.
    But some community members have raised questions about the integrity of the canisters and the plans for addressing any problems that might arise.
    Regardless of what internal drama or setbacks might arise, the Warriors can expect their no-frills big man to arrive early, stay late and do the little things — screening, boxing out, executing dribble-handoffs — required of championship runs.
    The rats didn’t show signs of health issues like seizures or epilepsy, which the researchers had worried might arise.
    These bonds cover any liabilities that might arise if an agricultural producer fails to honor its contract with migrant workers and is a way to protect those workers from abusive employment conditions.
    '''
    content_trigger = '''
    He kept his finger on the trigger. 
    Stress may act as a trigger for these illnesses. 
    Nuts can trigger off a violent allergic reaction. 
    A man pointed a gun at them and pulled the trigger. 
    Unresolved or unacknowledged fears can trigger sleepwalking. 
    The trigger for the strike was the closure of yet another factory. 
    Sometimes even a light touch on the face is enough to trigger off this pain. 
    Wire the thermometers up to trigger off an alarm bell if the temperature drops. 
    There are other trigger points. 
    When you click the trigger, it pops up an alert. 
    Does the thawing process has some kind of trigger as well? 
    Why does social media trigger feelings of loneliness and inadequacy? 
    This could trigger a tsunami that would create havoc along the coast. 
    With these functions, we can find out everything about the trigger or its context. 
    The photograph is able to achieve this result and is able to trigger these thoughts. 
    Even when they do trigger lightning, things still do not always go according to plan. 
    The problem with novelty, however, is that it tends to trigger the brain's fear system. 
    One cognitive theory suggests that aggravating and painful events trigger unpleasant feelings. 
    This could trigger a memory about what you're talking about through that lecture, which can then trigger another memory. 
    The state already has a "trigger law" on the books, which would ban most abortions, if the Supreme Court overturn Roe v Wade. 
    Thunder, the shock wave that comes from a lightning flash, is thought to be the trigger for the torrential rain that is typical of storms. 
    If you squeeze the trigger of a gun really hard and really fast, it doesn't fire any faster or harder than if you just squeezed it gently. 
    Some of them are a little trigger-happy—they'll shoot at anything that moves. 
    A hair-trigger situation has been created which could lead to an outbreak of war at any time. 
    His boozing, arrogance, and hair-trigger temper have often led him into ugly nightclub brawls. 
    It is argued, stripping cartons of their branding will trigger no mass movement to quit. 
    For example, we can change how often we receive the distracting notifications that trigger our urge to check. 
    The findings contradict research published earlier this year showing that returning adult trigger a significant decline in their parents' quality of life and wellbeing. 
    '''
    content_increase= '''
    Prices will increase pro rata. 
    We need to increase productivity. 
    Car usage is predicted to increase. 
    The population continues to increase. 
    Reading will increase your vocabulary. 
    The report recommended a 10% pay increase. 
    Worn rugs increase the danger of tripping. 
    Our main aim is to increase sales in Europe. 
    Short-term contracts increase staff turnover. 
    There was an astounding 20% increase in sales. 
    We needed to increase the volume of production. 
    Obesity can increase the risk of heart disease. 
    Wayne plans to increase the print run to 1,000. 
    This sort of increase simply cannot be justified. 
    That would increase Olympia & York's holding to 35%. 
    A good advertising campaign will increase our sales. 
    The food had been adulterated to increase its weight. 
    Companies need to take active steps to increase exports. 
    All parties are promising to increase spending on health. 
    Smoking can increase the risk of developing heart disease. 
    The tax increase sounded the death knell for the business. 
    There has been a marked increase in crimes against property. 
    The directors have just voted themselves a huge pay increase. 
    Very vigorous exercise can increase the risk of heart attacks. 
    It would be highly undesirable to increase class sizes further. 
    We are now witnessing an unprecedented increase in violent crime. 
    Testosterone does not increase their erectile or orgasmic ability. 
    Cases of breathing difficulties increase in lockstep with air pollution. 
    Mugging is on the increase. 
    We've been given a 2% pay increase. 
    '''

    content_affect='''
    How will these changes affect us? 
    Your opinion will not affect my decision. 
    Does television affect children's behaviour? 
    The new proposals affect both clergy and laity. 
    This may affect your entitlement to compensation. 
    The drug may affect your powers of concentration. 
    Climate and weather affect every aspect of our lives. 
    Cataracts affect the transparency of the eye's lenses. 
    Many external influences can affect your state of mind. 
    The new law will affect us all, directly or indirectly. 
    Your contributions will affect your pension entitlements. 
    An unhappy home environment can affect children's behaviour. 
    You never allow personal problems to affect your performance. 
    Irritable bowel syndrome seems to affect more women than men. 
    People tend to think that the problem will never affect them. 
    You're fooling yourself if you think none of this will affect you. 
    Every ingestion of food can affect our mood or thinking processes. 
    This will negatively affect the result over the first half of the year. 
    He is interested in how our perceptions of death affect the way we live. 
    Price changes must not adversely affect the living standards of the people. 
    The warming of the Earth and the consequent climatic changes affect us all. 
    Even in the artificial environment of an office, our body rhythms continue to affect us. 
    Changes in the money supply affect the level of economic activity and the interest rate. 
    His words have great affect on me. 
    How do daydreams affect daydreamers? 
    Intuition may affect reflective tasks. 
    I don't smoke, so it doesn't affect me. 
    When it grows hot, heat can affect human health. 
    Individual sins affect the entire fabric of society. 
    '''

    content_effect='''
    We warned them, but to no effect. 
    Her words had a magical effect on us. 
    His voice had an almost hypnotic effect. 
    The effect has proved hard to reproduce. 
    His words had exactly the opposite effect. 
    The crisis had a negative effect on trade. 
    The effect is almost impossible to describe. 
    The medicine did not achieve the desired effect. 
    Affairs do have a devastating effect on marriages. 
    My father's death had a profound effect on us all. 
    The overall effect of the painting is overwhelming. 
    She is unconscious of the effect she has on people. 
    Does television have an effect on children's behaviour? 
    The announcement had a dramatic effect on house prices. 
    The stage lighting gives the effect of a moonlit scene. 
    The calming effect seemed to last for about ten minutes. 
    They had seriously miscalculated the effect of inflation. 
    Unemployment is having a corrosive effect on our economy. 
    Overseas investment has had a positive effect on exports. 
    The price increase has had no perceptible effect on sales. 
    This effect is particularly noticeable in younger patients. 
    The specific impact of the greenhouse effect is unknowable. 
    Petty crime is having a deleterious effect on community life. 
    His mother's untimely death had a catastrophic effect on him.
    The aspirins soon take effect. 
    They hope to effect a reconciliation. 
    The colour green has a restful effect. 
    The new law takes effect from tomorrow. 
    One side effect of modern life is stress. 
    New controls come into effect next month. 
    '''

    content_induce='''
    Nothing would induce me to take the job. 
    Whales being sociable animals probably need the stimulus of sizeable gatherings to induce reproductives behavior. 
    Indeed, the mere presence of a grape in the other chamber (without an actual monkey to eat it) was enough to induce resentment in a female capuchin. 
    In view of this behavior it has been suggested that chemicals present in fresh buck rubs may help physiologically induce and synchronize fertility in females that visit these rubs. 
    We'll have to induce her. 
    Music can induce a meditative state. 
    Doctors said surgery could induce a heart attack. 
    Taking a brisk walk can often induce a feeling of well-being. 
    Like fireplaces, they induce sense of comfort and warmth. 
    For humans, hearing a sudden loud noise might prove frightening, but it does not induce mass fatality. 
    It's all about making the traveling experience less stressful and blue is said to induce a feeling of calm. 
    At 15 euro ($22) a tonne the price is high enough to induce power companies to switch some generation from coal to ga. 
    When people engage in activities that help others, their brain releases endorphins, the brain's natural opiates, which induce in people a feeling of well-being. 
    The authors explore factors that induce Veblen effects. 
    We also suggest that pimobendan may induce ventricular hypertrophy. 
    Induce Giardia lamblia C2 strain to complete its life cycle in vitro. 
    Even modest doses of narcotine can induce profound nausea and vomiting. 
    Xuefen syndromes of epidemic febrile disease was made in rabbits by endotoxin to induce generalized Shwartzman reaction. 
    Only a few other drugs, such as methohexital, etomidate, or propofol have the capability to induce anesthesia so rapidly. 
    Many causes could induce rhabdomyolysis, such as exercise, thermoplegia, or autoallergic disease. 
    Herbal teas can help induce sleep. 
    But it can also induce nervousness. 
    I don't say this to induce a guilt trip. 
    Presumably, all these taxes are to induce compliance. 
    The castor bean can also induce labor in pregnant women. 
    These taxonomies induce semantic relationships among objects. 
    Meeting new people is fun. But it can also induce nervousness. 
    And corroding anxiety and bad temper actual induce physical diseases. 
    Listening to soothing music can calm the senses and help induce sleep.
    '''

    content_derive='''  
    In fact, over fifty per cent of genuine British surnames derive from place names of different kinds, and so they belong to the last of our four main categories. 
    Most patients derive enjoyment from leafing through old picture albums. 
    Mr. Ying is one of those happy people who derive pleasure from helping others. 
    They derive greater pleasure from buying things. 
    Elegance, he believed, did not derive from abundance. 
    Only rarely can we derive any "real" quantities from deposits of broken pots. 
    The acquisition acts of bidders may derive from modeling: a manager does what other managers do. 
    It should be noted that in these cases, a reader can derive the intended meaning from the context. 
    It's possible that the birds can derive so much energy from these grubs that they only need to eat a few each day. 
    In one area, it made painstaking efforts to quantify fertility preference to derive figures for planned and unplanned pregnancies. 
    When food is in short supply, a ruminant can last longer than a nonruminant because it can derive more energy out of the same food. 
    These all revealed that the DNA profile found inside the gourd is extremely rare in modern Eurasians, suggesting that it may derive from a royal bloodline. 
    Although pressure to recruit women directors, unlike that to employ women in the general work force, does not derive from legislation, it is nevertheless real.
    At the same time, we derive massive economic benefits when we buy the most affordable energy on the world market and when we engage in energy trade around the world. 
    A child's ability to become deeply absorbed in something, and derive intense pleasure from that absorption, is something adults spend the rest of their lives trying to return to. 
    Student tutors feel upset when their teachable students fail, but happy when these virtual pupils succeed as they derive pride and satisfaction from someone else's accomplishment. 
    Late endosomes might derive from early endosomes by stepwise maturation. 
    Now you can derive this. 
    Many later advice manuals derive from it. 
    Derive new knowledge. 
    But I'm never going to ask you to derive things. 
    You cannot derive a complete architecture with TDD. 
    You want people who derive joy from the work they do.
    But the local Dinka derive no benefit from this money. 
    And continue to derive the macroscopic entropy changes. 
    You need to derive a filename to store this information. 
    Organizations derive greater value from existing content. 
    '''

    content_reveal='''
    These poems reveal her gentle side. 
    Officers could not reveal how he died. 
    She has refused to reveal the whereabouts of her daughter. 
    Beware of saying anything that might reveal where you live. 
    The report was a device used to hide rather than reveal problems. 
    We reveal only as much information as we can safely risk at a given time. 
    To get you started, we have asked five successful writers to reveal some of the tricks of the trade. 
    What do our responses reveal about us? 
    Reveal your thoughts and express your ideas to yourself. 
    Most people surveyed were reluctant to reveal what they ate. 
    Its plots and events reveal a lot about Frankie's actual life. 
    That would reveal which ones we have seen and which we have not. 
    Images of the Martian surface reveal many hundreds of volcanoes. 
    In some cases, a simple Google search can reveal what you think. 
    Spectroscopy can reveal the composition of those touch-up layers too. 
    Her portraits reveal her own interpretation of her subject's state of mind. 
    Companies could be forced to reveal to consumers what information they hold. 
    Exposition is whatever background information you have to reveal to the audience. 
    After the two servants reveal all this background information, we meet the young man. 
    Longevity statistics reveal that the average person doesn't last very long after retirement. 
    In a study published in Nature Scientific Reports, we reveal just how deep this injustice runs. 
    No one has found one of their canoes or any rigging, which could reveal how the canoes were sailed. 
    Such experiments cannot, however, reveal whether the birds were reexperiencing the past when retrieving the information. 
    Subsequently developed methods of recording and analyzing nerve potentials failed to reveal any such qualitative diversity. 
    The flower opens to reveal a bee. 
    She doesn't reveal much of her inner self. 
    The door opened to reveal a cosy little room. 
    His writings reveal an unattractive preciousness of style. 
    She crouched in the dark, too frightened to reveal herself. 
    Companies should be made to reveal more about their financial position. 
    '''

    content_because='''
They are here because of us. 
She resigned because of ill health. 
I was angry because I played so badly. 
The road is closed because of the snow. 
Many diets fail because they are boring. 
He walked slowly because of his bad leg. 
She's been off work because of sickness. 
Feed the dogs because they haven't eaten. 
They abandoned the match because of rain. 
She had left him because of his drinking. 
I started to cry because I cut my finger. 
I didn't get it because it cost too much. 
They knocked off $60 because of a scratch. 
John liked him because he was a nervy guy.
Some roads are closed because of drifting. 
Filming was delayed because of bad weather. 
He won't resign because he's not a quitter. 
She had scratched because of a knee injury. 

她因膝伤退出了比赛。
《牛津词典》

19.
She was marked down because of poor grammar. 

她因语法不好被扣了分。
《牛津词典》

20.
I agreed, but only because I was frightened. 

我同意了，但只是因为我受到了恐吓。
《牛津词典》

21.
I had to refuse because of a prior engagement. 

我因为已经有预约只好拒绝了。
《牛津词典》

22.
Officially, he resigned because of bad health. 

据官方说法，他是因健康状况不佳而辞职的。
《牛津词典》

23.
He was forced to retire because of ill health. 

由于健康不佳，他只得退休。
《柯林斯英汉双解大词典》

24.
We had a humongous fight just because she left. 

正因为她离开了，我们大吵了一架。
《柯林斯英汉双解大词典》

25.
The game was called off because of bad weather. 

比赛因天气恶劣被取消。
《牛津词典》

26.
I chose boxing because it is my favourite sport. 

我选择了拳击，因为那是我最喜爱的运动。
《柯林斯英汉双解大词典》

27.
People learned self-reliance because they had to. 

人们学会了自立因为他们不得不这样做。
《柯林斯英汉双解大词典》

28.
The goal was disallowed because Wark was offside. 

那个进球被判无效，因为沃克越位了。
《柯林斯英汉双解大词典》

29.
Cassandra noticed him because he was good-looking. 

卡桑德拉注意到他是因为他长得好看。
《柯林斯英汉双解大词典》
    '''
    extractor = CausalityExractor()
    datas = extractor.extract_main(content_cause)
    for data in datas:
        print('******'*4)
        print('cause', ''.join([word.split('/')[0] for word in data['cause'].split(' ') if word.split('/')[0]]))
        print('tag', data['tag'])
        print('effect', ''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]]))

test()
