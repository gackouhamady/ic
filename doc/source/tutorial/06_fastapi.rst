FastAPI HTTP API (Hamady GACKOU)
================================

:Author: Hamady GACKOU
:Goal: HTTP API + OpenAPI docs

Goal
----

Expose the main functionalities as an HTTP API:

- export NG20 documents
- train LDA model
- describe a document
- count lines

OpenAPI documentation
---------------------

The course recommends providing OpenAPI (Swagger) documentation for webservices
and mentions that frameworks like FastAPI generate it automatically. :contentReference[oaicite:17]{index=17}

Proposed endpoints (example)
----------------------------

- ``POST /ng20/export``  (category, n, out_dir)
- ``POST /lda/train``    (texts_dir, model_out, n_topics)
- ``POST /lda/describe`` (model_path, doc_path)
- ``POST /lines/count``  (file_path)

Running the API (future step)
-----------------------------

.. code-block:: bash

   uvicorn ic.api:app --reload

Docs available by default:

- ``/docs`` (Swagger UI)
- ``/redoc`` (ReDoc)
