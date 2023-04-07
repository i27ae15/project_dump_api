# Backend codes

class Code:
    code = '000'
    message = 'No message'


class BKFirstPhrasesGenerated(Code):
    code = 'BGP-200'
    message = 'First phrases generated'


class BKNotEnoughPhrasesToReturn(Code):
    code = 'BGP-205'
    message = 'Not enough phrases to return'


class BKTopicNotSelected(Code):
    code = 'BGT-404'
    message = 'Topic not selected'


class BKTopicSelected(Code):
    code = 'BGT-200'
    message = 'Topic selected'


# Frontend codes

class FNReturnPentagonPhrases(Code):
    code = 'FGP-101'
    message = 'Returns 5 phrases'


class FNReturnMonoPhrase(Code):
    code = 'FGP-102'
    message = 'Returns 1 phrases'


class FNSelectTopic(Code):
    code = 'FGT-101'
    message = 'Select topic'


class PhrasesP5(Code):
    code = 'P-5'
    message = 'Returns 5 phrases'


class PhrasesP1(Code):
    code = 'P-1'
    message = 'Returns 1 phrases'