# Backend codes

class Code:
    code = '000'
    message = 'No message'


class FirstPhrasesGenerated(Code):
    code = 'BGP-200'
    message = 'First phrases generated'


class NotEnoughPhrasesToReturn(Code):
    code = 'BGP-205'
    message = 'Not enough phrases to return'


class TopicNotFound(Code):
    code = 'BGT-404'
    message = 'Topic not found'


class TopicSelected(Code):
    code = 'BGT-200'
    message = 'Topic selected'


# Frontend codes

class ReturnPentagonPhrases(Code):
    code = 'FGP-101'
    message = 'Returns 5 phrases'


class ReturnMonoPhrase(Code):
    code = 'FGP-102'
    message = 'Returns 1 phrases'


class SelectTopic(Code):
    code = 'FGT-101'
    message = 'Select topic'


# phrases

class PhrasesP5(Code):
    code = 'P-5'
    message = 'Returns 5 phrases'


class PhrasesP1(Code):
    code = 'P-1'
    message = 'Returns 1 phrases'