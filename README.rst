🤘 Lemmy
========

Lemmy is a lemmatizer for Danish 🇩🇰 . It comes already trained on Dansk
Sprognævns (DSN) word list (‘fuldformliste’) and the Danish Universal
Dependencies and is ready for use. Lemmy also supports training on your
own dataset.

The model currently included in Lemmy was evaluated on the Danish
Universal Dependencies dev dataset and scored an accruacy > 99%.

You can use Lemmy as a spaCy extension, more specifcally a spaCy
pipeline component. This is highly recommended and makes the lemmas
easily accessible from the spaCy tokens. Lemmy makes use of POS tags to
predict the lemmas. When wired up to the spaCy pipeline, Lemmy has the
benefit of using spaCy’s builtin POS tagger.

Lemmy can also by used without spaCy, as a standalone lemmatizer. In
that case, you will have to provide the POS tags. Alternatively, you can
train a Lemmy model which does not depend on POS tags, though most
likely the accuracy will suffer.

Lemmy is heavily inspired by the `CST Lemmatizer for
Danish <https://cst.dk/online/lemmatiser/>`__.

Install
-------

.. code:: bash

    pip install lemmy

Usage
-----

.. code:: python

    import da_custom_model as da # name of your spaCy model
    import lemmy.pipe
    nlp = da.load()

    # create an instance of Lemmy's pipeline component for spaCy
    pipe = lemmy.pipe.load()

    # add the comonent to the spaCy pipeline.
    nlp.add_pipe(pipe, after='tagger')

    # lemmas can now be accessed using the `._.lemma` attribute on the tokens
    nlp("akvariernes")[0]._.lemma

Training
--------

The ``notebooks`` folder contains examples showing how to train your own
model using Lemmy.
