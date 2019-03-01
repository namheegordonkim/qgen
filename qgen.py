from typing import *
import argparse, random, re
random.seed()

# use RegEx to parse topics, questions, answers
topic_pattern = "^===\\s*(.+?)\s*==="
question_pattern = "^\\*+(.+)"
answer_pattern = "^\\-\\>(.+)"

class ValueContainer:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Topic(ValueContainer):
    def __init__(self, value):
        super(Topic, self).__init__(value)


class Question(ValueContainer):
    def __init__(self, value):
        super(Question, self).__init__(value)


class Answer(ValueContainer):
    def __init__(self, value):
        super(Answer, self).__init__(value)


class QnA:
    answers = []
    question = None

    def __init__(self, question: Question, answers: List[Answer]):
        self.question = question
        self.answers = answers


class TopicQnAPair:
    topic = None
    qnas = []

    def __init__(self, topic: Topic, qnas: List[QnA]):
        self.topic = topic
        self.qnas = qnas


class TopicQnATriple:
    topic = None
    question = None
    answers = []

    def __init__(self, topic: Topic, question: Question, answers: List[Answer]):
        self.topic = topic
        self.question = question
        self.answers = answers


class Representer:

    def __init__(self):
        pass

    def flatten_topic_qna_pair(self, topic_qna_pair: TopicQnAPair) -> List[TopicQnATriple]:
        return [TopicQnATriple(topic_qna_pair.topic, qna.question, qna.answers)
                for qna in topic_qna_pair.qnas]

    def represent_question_of_topic(self, question: Question, topic: Topic):
        return "{:s} ({:s})".format(question.get_value(), topic.get_value())

    def represent_topic_qna_triple_without_answers(self, topic_qna_triple: TopicQnATriple) -> str:
        question_topic_line = self.represent_question_of_topic(topic_qna_triple.question, topic_qna_triple.topic)
        return "{:s}\n".format(question_topic_line)

    def represent_topic_qna_triple_with_answers(self, topic_qna_triple: TopicQnATriple):
        question_topic_line = self.represent_question_of_topic(topic_qna_triple.question, topic_qna_triple.topic)
        answer_lines = "\n".join(["-> {:s}".format(ans.get_value()) for ans in topic_qna_triple.answers])
        return "{:s}\n{:s}\n".format(question_topic_line, answer_lines)


class Document:
    topic_qna_pairs = []

    def __init__(self, topic_qna_pairs: List[TopicQnAPair]):
        self.topic_qna_pairs = topic_qna_pairs


def parse_generic(s: str, pattern: str, constructor):
    m = re.match(pattern, s)
    if not m:
        return None
    matched = m.group(1).strip().strip("\n")
    return constructor(matched)


def parse_answer(s: str) -> Answer or None:
    return parse_generic(s, answer_pattern, Answer)


def parse_question(s: str) -> Question or None:
    return parse_generic(s, question_pattern, Question)


def parse_topic(s: str) -> Topic or None:
    return parse_generic(s, topic_pattern, Topic)


def parse_qna(token_list: List[ValueContainer]) -> QnA or None:
    if len(token_list) == 0:
        return None
    if token_list[0].__class__ is not Question:
        return None
    if len(list(filter(lambda x: x.__class__ != Answer, token_list[1:]))) > 0:
        return None

    question = token_list[0]
    answers = token_list[1:]
    return QnA(question, answers)


def parse_topic_qna_pair(token_list: List[ValueContainer]) -> TopicQnAPair or None:
    if len(token_list) == 0:
        return None
    if token_list[0].__class__ is not Topic:
        return None

    topic = token_list[0]
    qna_all_token_list = token_list[1:]
    qna_all_token_splitted = split_by_token(qna_all_token_list, Question)
    qnas = [parse_qna(x) for x in qna_all_token_splitted]
    filtered = [q for q in qnas if q is not None]
    return TopicQnAPair(topic, filtered)


def split_by_token(token_list: List[ValueContainer], clazz) -> List[List[ValueContainer]]:
    if len(token_list) == 0:
        return []
    splitted = []
    buffer = []
    for i, token in enumerate(token_list):
        if token.__class__ is clazz:
            if len(buffer) > 0:
                splitted.append(buffer)
                buffer = []
        buffer.append(token)

    if len(buffer) > 0:
        splitted.append(buffer)
    return splitted


def parse_something(s: str) -> ValueContainer:
    topic = parse_topic(s)
    question = parse_question(s)
    answer = parse_answer(s)
    if topic is not None:
        return topic
    if question is not None:
        return question
    if answer is not None:
        return answer


def tokenize(s: str) -> List[ValueContainer]:
    splitted = s.split("\n")
    tokenized = [parse_something(st) for st in splitted]
    filtered = [token for token in tokenized if token is not None]
    return filtered


def parse_qgen_document(s: str) -> Document:
    tokenized = tokenize(s)
    splitted_by_topic = split_by_token(tokenized, Topic)
    topic_qna_pairs = [parse_topic_qna_pair(lst) for lst in splitted_by_topic]
    filtered = [t for t in topic_qna_pairs if t is not None]
    return Document(filtered)


def main():
    # initialize and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True, action='store', type=str,
                        help="File name to take into quiz")
    parser.add_argument("-n", "--num-questions", required=True, action='store', type=int,
                        help="Total number of questions in quiz")
    parser.add_argument('-q', '--output-quiz-file', required=True, action='store', type=str,
                        help='Output quiz filename')
    parser.add_argument('-a', '--output-answer-file', required=True, action='store', type=str,
                        help='Output answer filename')
    parser.add_argument('-A', '--output-allq-file', required=True, action='store', type=str,
                        help='Output all-questions filename')

    args = parser.parse_args()

    v = vars(args)
    filename = v['filename']
    n = v['num_questions']
    wf = v['output_quiz_file']
    af = v['output_answer_file']
    aq = v['output_allq_file']

    with open(filename, 'r') as f:
        raw_text = f.read()
    document = parse_qgen_document(raw_text)

    representer = Representer()

    all_topic_qna_triples = [representer.flatten_topic_qna_pair(topic_qna_pair)
                             for topic_qna_pair in document.topic_qna_pairs]
    all_topic_qna_triples_flattened = [item for sublist in all_topic_qna_triples
                                       for item in sublist]

    chosen_topic_qna_triples = random.sample(all_topic_qna_triples_flattened, n)

    all_questions_without_answers = \
        "\n".join(["{:d}. {:s}".format(i+1, representer.represent_topic_qna_triple_without_answers(t))
                                               for i, t in enumerate(all_topic_qna_triples_flattened)])
    chosen_questions_without_answers = \
        "\n".join(["{:d}. {:s}".format(i+1, representer.represent_topic_qna_triple_without_answers(t))
                                                  for i, t in enumerate(chosen_topic_qna_triples)])
    chosen_questions_with_answers = \
        "\n".join(["{:d}. {:s}".format(i+1, representer.represent_topic_qna_triple_with_answers(t))
                                               for i, t in enumerate(chosen_topic_qna_triples)])

    with open(wf, 'w') as f:
        f.write(chosen_questions_without_answers)
    with open(af, 'w') as f:
        f.write(chosen_questions_with_answers)
    with open(aq, 'w') as f:
        f.write(all_questions_without_answers)


if __name__ == '__main__':
    main()
