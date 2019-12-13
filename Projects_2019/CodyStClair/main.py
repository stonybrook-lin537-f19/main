import nltk, parse, bigrams, verse, examples

iris = verse.analyze_poem(parse.parse_poem(examples.iris_lyrics))

gen = bigrams.PoemGenerator(parse.parse_prose(nltk.corpus.inaugural.raw()))

parody = gen.gen_poem(iris)

print("\n".join([" ".join(i) for i in parody]))
