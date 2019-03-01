# QGen: QEC-Format Quiz Generator

Author: Nam Hee Gordon Kim (nkim412@gmail.com)

Inspired by Cal Newport's blog article: http://calnewport.com/blog/2007/07/20/monday-master-class-accelerate-qec-note-taking/

# Requirements

* python >= 3.6.0

# Note Format

The default RegEx patterns look ilke this:

```buildoutcfg
topic_pattern = "^===\\s*(.+?)\s*==="
question_pattern = "^\\*+(.+)"
answer_pattern = "^\\-\\>(.+)"
```

If the above patterns are used, the notes should follow this format.

```buildoutcfg
=== topic 1 ===

*question 1
-> evidence A
-> evidence B
-> conclusion 1

*question 2
-> evidence C
-> evidence D
-> conclusion 2

=== topic 2 ===

*question 3
-> evidence E
-> evidence F
-> conclusion 3

```

My course notes from Mark Schmidt's CPSC 540 (Machine Learning) course is included for reference. See cpsc540.txt

# How to Use

Clone the repository.

```buildoutcfg
git clone https://github.com/namheegordonkim/qgen.git
```

Run Python command

```buildoutcfg
python qgen.py \
--filename ${NOTE_FILENAME} \
--num-questions ${NUM_QUESTIONS} \
--output-quiz-file ${OUTPUT_QUIZ_FILE} \
--output-answer-file ${OUTPUT_ANSWER_FILE} \
--output-allq-file ${OUTPUT_ALLQ_FILE}
```

For example,

```buildoutcfg
python qgen.py \
--filename cpsc540.txt \
--num-questions 20 \
--output-quiz-file cpsc540-qgen.txt \
--output-answer-file cpsc540-qgen-ans.txt \
--output-allq-file cpsc540-qgen-allq.txt
```

The above command will generate three files:
1. cpsc540-qgen.txt: contains 20 questions without answers
2. cpsc540-qgen-ans.txt: contains the same 20 questions as above with answers annotated
3. cpsc540-qgen-allq.txt: contains all questions present in the note without answers

# Tips

* Treat note-taking as a data mining task. Ask: "if I was teaching this course, what would I ask on the exam?" and write it down. Provide the answer key in a logical order.
* In my own experience, this technique works best for technical courses with quantitative exams.
* In expression-heavy classes like math and physics, it is best to use QGen to test conceptual understanding and use practice exams to practice problem solving.
