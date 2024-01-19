import spacy

# Carregar modelo de linguagem em português
nlp = spacy.load('pt_core_news_sm')

# Processar texto e extrair entidades
text = "O presidente Lula esteve em Brasília."
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
