from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

model = Doc2Vec.load("d2v.model")
# to find the vector of a document which is not in training data
test_data = word_tokenize("I love chatbots".lower())
# print('test_data')
# print(test_data)
# v1 = model.infer_vector(test_data)
# print("V1_infer")
# print(v1)

# to find most similar doc using tags
# similar_doc = model.docvecs.most_similar('1')
# print(similar_doc)

new_sentence = "I love coding in python"
tokens = word_tokenize(new_sentence.lower())
new_vector = model.infer_vector(tokens)
# gives you top 10 document tags and their cosine similarity
sims = model.docvecs.most_similar([new_vector])

# to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
print(model.docvecs['1'])
