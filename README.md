# 🤘 Lemmy

Lemmy is a lemmatizer for Danish 🇩🇰 and Swedish 🇸🇪. It comes ready for use. The
Danish model is trained on Dansk Sprognævn's (DSN) word list (‘fuldformliste’) and the
[Danish Universal Dependencies](https://github.com/UniversalDependencies/UD_Danish-DDT).
The Swedish model is trained on the [SALDO's
morphology](https://spraakbanken.gu.se/eng/resource/saldom) dataset and the Swedish
[Universal Dependencies
(Talbanken)](https://github.com/UniversalDependencies/UD_Swedish-Talbanken). Lemmy also
supports training on your own dataset.

The models included in Lemmy were evaluated on the respective Universal Dependencies dev
datasets. The Danish model scored > 99% accuracy, while the Swedish model scored > 97%.
All reported scores were obtained when supplying Lemmy with POS tags.

You can use Lemmy as a spaCy extension, more specifcally a spaCy pipeline component.
This is highly recommended and makes the lemmas easily accessible from the spaCy tokens.
Lemmy makes use of POS tags to predict the lemmas. When wired up to the spaCy pipeline,
Lemmy has the benefit of using spaCy’s builtin POS tagger.

Lemmy can also by used without spaCy, as a standalone lemmatizer. In that case, you will
have to provide the POS tags. Alternatively, you can use Lemmy without POS tags, though
most likely the accuracy will suffer. Currrently, only the Danish Lemmy model comes with
a model trained for use without POS tags. That is, if you want to use Lemmy on Swedish
text without POS tags, you must train your own Lemmy model.

Lemmy is heavily inspired by the [CST Lemmatizer for
Danish](https://cst.dk/online/lemmatiser/).

## Install

```bash
pip install lemmy
```

## Basic Usage Without POS tags

```python
import lemmy

# Create an instance of the standalone lemmatizer.
lemmatizer = lemmy.load("da")

# Find lemma for the word 'akvariernes'. First argument is an empty POS tag.
lemmatizer.lemmatize("", "akvariernes")
```

## Basic Usage With POS tags

```python
import lemmy

# Create an instance of the standalone lemmatizer.
# Replace 'da' with 'sv' for the Swedish lemmatizer.
lemmatizer = lemmy.load("da")

# Find lemma for the word 'akvariernes'. First argument is the user-provided POS tag.
lemmatizer.lemmatize("NOUN", "akvariernes")
```

## Usage with spaCy Model

```python
import da_custom_model as da # replace da_custom_model with name of your spaCy model
import lemmy.pipe
nlp = da.load()

# Create an instance of Lemmy's pipeline component for spaCy.
# Replace 'da' with 'sv' for the Swedish lemmatizer.
pipe = lemmy.pipe.load('da')

# Add the component to the spaCy pipeline.
nlp.add_pipe(pipe, after='tagger')

# Lemmas can now be accessed using the `._.lemmas` attribute on the tokens.
nlp("akvariernes")[0]._.lemmas
```

## Training

The ``notebooks`` folder contains examples showing how to train your own model using
Lemmy.
