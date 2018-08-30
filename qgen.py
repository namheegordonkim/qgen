import argparse, random, re, os

random.seed()

# use RegEx to parse topics, questions, answers
topic_pattern = "(\n===\s*.+\s*===\n)"
question_pattern = "(\n\*+.+\n)"
answer_pattern = "(\n?\-\>.+\n?)"

class TopicNetwork:
    def __init__(self, topics, p):
        self.currentIdx = random.randrange(len(topics))
        self.topics = topics
        self.p = p

    def run(self):
        """
        Run one step of the TN.
        Spit a random question of current topic.
        By probability p move onto next
        """

        print(len(self.topics))

        if len(self.topics) == 0:
            raise "Too many questions"

        # choose a random question
        self.currentIdx = self.currentIdx % len(self.topics)
        t = self.topics[self.currentIdx]
        qs = t.topic_qs

        if len(qs) <= 0:
            self.topics.pop(self.currentIdx)
            return self.run()
        random.shuffle(qs)
        q = qs.pop(random.randrange(len(qs)))
        if random.random() + len(qs)/100.0 <= self.p:
            self.currentIdx += 1
        return t, q

class Topic:
    def __init__(self, text, topic_qs):
        self.text = text
        self.topic_qs = topic_qs

class Question:
    def __init__(self, text, answers):
        self.text = text
        self.answers = answers

def parse_answers(answer_split_list):
    if len(answer_split_list) == 0:
        return []
    print(answer_split_list)
    m = re.match(answer_pattern, answer_split_list[0])
    if m == None:
        return []
    answer = m.group(1).strip().strip("\n")
    return [answer] + parse_answers(answer_split_list[1:])

def parse_questions(question_split_list):
    if len(question_split_list) == 0:
        return []

    m = re.match(question_pattern, question_split_list[0])
    if m == None:
        return parse_questions(question_split_list[1:])

    question_title = question_split_list[0].strip()
    answers = question_split_list[1].split("\n\n")[0].split("\n")

    new_question = Question(question_title, answers)
    return [new_question] + parse_questions(question_split_list[2:])

def parse_topics(topic_split_list):
    if len(topic_split_list) <= 1:
        return []

    m = re.match(topic_pattern, topic_split_list[0])
    if m == None:
        return parse_topics(topic_split_list[1:])
    topic_title = topic_split_list[0].strip()
    topic_title = re.match("(===\s*)(.+)(\s*===)",topic_title).group(2).strip()
    question_split = re.split(question_pattern, topic_split_list[1])
    questions = parse_questions(question_split)
    new_topic = Topic(topic_title, questions)
    return [new_topic] + parse_topics(topic_split_list[2:])

def main():
    # initialize and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filenames", required=True, action='store', nargs="+", type=str, help="List of file names to take into quiz")
    parser.add_argument("-n", "--num-questions", required=True, action='store', type=int, help="Total number of questions in quiz")
    parser.add_argument('-q', '--output-quiz-file', required=True, action='store', type=str, help='Output quiz filename')
    parser.add_argument('-a', '--output-answer-file', required=True, action='store', type=str, help='Output answer filename')
    parser.add_argument('-A', '--output-allq-file', required=True, action='store', type=str, help='Output all-questions filename')

    args = parser.parse_args()

    v = vars(args)
    filenames = v['filenames']
    n = v['num_questions']
    wf = open(v['output_quiz_file'], 'w')
    af = open(v['output_answer_file'], 'w')
    aq = open(v['output_allq_file'], 'w')

    allq = []

    # hierarchy:
    # topic has zero or more questions,
    # question has zero or more answers

    topics = []
    for filename in filenames:
        f = open(filename)

        rawtext = f.read()
        topic_split = re.split(topic_pattern, rawtext)
        topics = topics + parse_topics(topic_split)
        f.close()

    # write chosen number of random questions into -qgen.txt file

    num = 1
    for topic in topics:
        # print "Topic Title: " + topic.text
        for q in topic.topic_qs:
            # print "Question Title: " + q.text
            for a in q.answers:
                print("Answer: " + a)

            aq.write(str(num)+ ". " + q.text + " (" + topic.text + ")")
            aq.write("\n")
            num += 1

    topic_network = TopicNetwork(topics, 0.8)

    num = 1
    while num <= n:
        t, q = topic_network.run()
        wf.write(str(num)+ ". " + q.text + " (" + t.text + ")")
        af.write(str(num)+ ". " + q.text + " (" + t.text + ")")
        af.write("\n")
        for a in q.answers:
            af.write(a)
            af.write("\n")
        num = num+1
        for i in range(6):
            wf.write("\n")
        for i in range(2):
            af.write("\n")
    wf.close()
    af.close()
    aq.close()

    num = 1
    while num <= n:
        t, q = topic_network.run()

        num = num+1

if __name__ == '__main__':
    main()
