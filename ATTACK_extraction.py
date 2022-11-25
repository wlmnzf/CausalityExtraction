import causality_extract

from stat_parser import Parser, display_tree


parser = Parser()

# http://www.thrivenotes.com/the-last-question/
tree = parser.parse("How can the net amount of entropy of the universe be massively decreased?")

display_tree(tree)



extractor = causality_extract.CausalityExractor()
datas = extractor.extract_main("HyperStack can use default credentials to connect to IPC$ shares on remote machines.[5]")
for data in datas:
        print('******'*4)
        print('cause', ''.join([word.split('/')[0] for word in data['cause'].split(' ') if word.split('/')[0]]))
        print('tag', data['tag'])
        print('effect', ''.join([word.split('/')[0] for word in data['effect'].split(' ') if word.split('/')[0]]))