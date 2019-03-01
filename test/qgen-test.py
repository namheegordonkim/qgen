from qgen import *


def do_parse_test_good(raw_str: str, parse_func, expected_class, expected_str: str):
    parsed = parse_func(raw_str)
    assert expected_class == parsed.__class__
    assert expected_str == parsed.get_value()


def do_parse_test_none(raw_str: str, parse_func):
    parsed = parse_func(raw_str)
    assert parsed is None


def test_parse_answer():
    do_parse_test_good("-> answer", parse_answer, Answer, "answer")
    do_parse_test_good("->  answer", parse_answer, Answer, "answer")
    do_parse_test_good("->answer", parse_answer, Answer, "answer")
    do_parse_test_good("->    answer", parse_answer, Answer, "answer")

    do_parse_test_none("->", parse_answer)
    do_parse_test_none("", parse_answer)
    do_parse_test_none("> answer", parse_answer)
    do_parse_test_none("=> answer", parse_answer)
    do_parse_test_none(">-answer", parse_answer)
    do_parse_test_none("*answer", parse_answer)
    do_parse_test_none("=== answer ===", parse_answer)


def test_parse_question():
    do_parse_test_good("*question?", parse_question, Question, "question?")
    do_parse_test_good("**question?", parse_question, Question, "question?")
    do_parse_test_good("*question with space?", parse_question, Question, "question with space?")
    do_parse_test_good("*question", parse_question, Question, "question")

    do_parse_test_none(" *question?", parse_question)
    do_parse_test_none("*", parse_question)
    do_parse_test_none("", parse_question)


def test_parse_topic():
    do_parse_test_good("=== topic ===", parse_topic, Topic, "topic")
    do_parse_test_good("===topic===", parse_topic, Topic, "topic")
    do_parse_test_good("===topic ===", parse_topic, Topic, "topic")
    do_parse_test_good("=== topic===", parse_topic, Topic, "topic")
    do_parse_test_good("=== topic with space ===", parse_topic, Topic, "topic with space")

    do_parse_test_none("", parse_topic)
    do_parse_test_none("======", parse_topic)
    do_parse_test_none("= topic =", parse_topic)
    do_parse_test_none("== topic ==", parse_topic)
    do_parse_test_none(" === topic ===", parse_topic)


def test_parse_qna():
    good_list = [Question("question?"), Answer("answer")]
    good_qna = parse_qna(good_list)
    assert QnA is good_qna.__class__
    assert Question is good_qna.question.__class__
    assert "question?" is good_qna.question.get_value()
    assert 1 is len(good_qna.answers)
    assert "answer" is good_qna.answers[0].get_value()

    bad_list = [Question("question?"), Question("question??")]
    bad_qna = parse_qna(bad_list)
    assert None is bad_qna


def test_split_by_token():
    lst = [Question("question1"), Answer("answer1"), Question("question2"), Answer("answer2")]
    splitted = split_by_token(lst, Question)
    assert 2 is len(splitted)
    assert "question1" is splitted[0][0].get_value()
    assert "answer1" is splitted[0][1].get_value()
    assert "question2" is splitted[1][0].get_value()
    assert "answer2" is splitted[1][1].get_value()


def test_parse_topic_qna_pair():
    lst = [Topic("topic"), Question("question1"), Answer("answer1"), Question("question2"), Answer("answer2")]
    parsed = parse_topic_qna_pair(lst)
    assert TopicQnAPair is parsed.__class__
    assert Topic is parsed.topic.__class__
    assert "topic" is parsed.topic.get_value()
    assert 2 is len(parsed.qnas)
    assert "question1" is parsed.qnas[0].question.get_value()
    assert "answer1" is parsed.qnas[0].answers[0].get_value()
    assert "question2" is parsed.qnas[1].question.get_value()
    assert "answer2" is parsed.qnas[1].answers[0].get_value()


def test_parse_something():
    do_parse_test_good("=== topic ===", parse_something, Topic, "topic")
    do_parse_test_good("*question?", parse_something, Question, "question?")
    do_parse_test_good("-> answer", parse_something, Answer, "answer")

    do_parse_test_none("= topic", parse_something)
    do_parse_test_none("asdf", parse_something)


def test_tokenize():
    s = "=== topic ===\n\n*question?\n-> answer1\n-> answer2\n"
    tokenized = tokenize(s)
    assert 4 is len(tokenized)
    assert Topic is tokenized[0].__class__
    assert "topic" == tokenized[0].get_value()
    assert Question is tokenized[1].__class__
    assert "question?" == tokenized[1].get_value()
    assert Answer is tokenized[2].__class__
    assert "answer1" == tokenized[2].get_value()
    assert Answer is tokenized[3].__class__
    assert "answer2" == tokenized[3].get_value()

    s2 = "invalid"
    tokenized2 = tokenize(s2)
    assert 0 is len(tokenized2)


def test_parse_qgen_document():
    s = "=== topic1 ===\n\n*question?\n-> answer1\n-> answer2\n*question??\n-> answer1\n-> answer2\n=== topic2 " \
        "===\n\n*question?\n-> answer1\n-> answer2\n "
    document = parse_qgen_document(s)
    assert Document is document.__class__
    assert 2 is len(document.topic_qna_pairs)
    assert "topic1" == document.topic_qna_pairs[0].topic.get_value()
    assert 2 is len(document.topic_qna_pairs[0].qnas)
    assert "topic2" == document.topic_qna_pairs[1].topic.get_value()


def test_representer_flatten_topic_qna_pair():
    representer = Representer()
    qna1 = QnA(Question("question1"), [Answer("answer1"), Answer("answer2")])
    qna2 = QnA(Question("question2"), [Answer("answer3"), Answer("answer4")])

    topic_qna_pair = TopicQnAPair(Topic("topic"), [qna1, qna2])
    topic_qna_triple = representer.flatten_topic_qna_pair(topic_qna_pair)

    assert 2 is len(topic_qna_triple)
    assert "topic" == topic_qna_triple[0].topic.get_value()
    assert "topic" == topic_qna_triple[1].topic.get_value()


def test_represent_topic_qna_triple_without_answers():
    representer = Representer()
    topic_qna_triple = TopicQnATriple(Topic("topic"), Question("question"), [Answer("answer1"), Answer("answer2")])
    topic_qna_triple_s_with_answers = "question (topic)\n-> answer1\n-> answer2\n"
    topic_qna_triple_s_without_answers = "question (topic)\n"

    represented_without_answers = representer.represent_topic_qna_triple_without_answers(topic_qna_triple)
    represented_with_answers = representer.represent_topic_qna_triple_with_answers(topic_qna_triple)

    assert topic_qna_triple_s_without_answers == represented_without_answers
    assert topic_qna_triple_s_with_answers == represented_with_answers



