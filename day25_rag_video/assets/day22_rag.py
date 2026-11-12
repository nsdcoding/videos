# ============================================================
# DAY 22 : BUILDING A RAG SYSTEM (Retrieval Augmented Generation)
# ============================================================

# What problem are we solving?
# An LLM is very smart, but it has never seen OUR company documents.
# Ask Gemini "how many leaves do I get at Plural Labs" and it will guess,
# because our handbook was never part of its training.

# RAG is the fix. RAG = Retrieval + Augmented + Generation
# Retrieval  -> we go and FIND the right paragraph from our own files
# Augmented  -> we PASTE that paragraph into the prompt
# Generation -> the LLM ANSWERS using only that paragraph

# So the LLM is not remembering our data. We are handing it the data every time.

# Remember the diagram. There are TWO pipelines.
# Pipeline 1 - INDEXING  -> steps 1,2,3,4. Runs once, in advance. Nobody is waiting.
# Pipeline 2 - ANSWERING -> steps 5,6,7,8. Runs every single time somebody asks a question.


# ------------------------------------------------------------
# BEFORE YOU RUN THIS FILE : INSTALL THE NEW PACKAGE
# ------------------------------------------------------------

# Today we need one new thing that we have never installed before, the vector database.
# Everything else, langchain-google-genai and python-dotenv, we already have from before.

# On Mac, in the terminal :
#     pip3 install qdrant-client langchain-qdrant

# On Windows, in the command prompt :
#     pip install qdrant-client langchain-qdrant

# Two packages, because they do two different jobs :
# qdrant-client   -> the vector database itself
# langchain-qdrant -> the small wrapper that lets langchain talk to it in one line

# If you get "ModuleNotFoundError: No module named qdrant_client" after installing,
# it means pip installed into a different Python than the one running this file.
# Check with :  pip3 --version   and   python3 --version
# Both must show the same Python version.


# ------------------------------------------------------------
# THE IMPORTS
# ------------------------------------------------------------

# os -> lets us look inside a folder and see what files are sitting there
import os

# ChatGoogleGenerativeAI -> the chatting model. This is the one that writes the answer.
from langchain_google_genai import ChatGoogleGenerativeAI

# GoogleGenerativeAIEmbeddings -> the EMBEDDING model. This one does not chat.
# It only turns a piece of text into a long list of numbers.
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# QdrantVectorStore -> this is our REAL vector database.
# This is the new package we installed above.
# Qdrant is a proper production vector database, the same one companies run on a server.
# Its only job is to hold millions of vectors and answer one question very fast:
# "which stored vectors are nearest to this one?"
# We are not writing that search ourselves. The database does it for us.
from langchain_qdrant import QdrantVectorStore

# load_dotenv -> reads our .env file and picks up GOOGLE_API_KEY
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# PIPELINE 1 - INDEXING
# This whole block runs ONCE, before any question is asked.
# ============================================================


# ------------------------------------------------------------
# STEP 1 : LOAD
# "Read PDFs, docs and tickets as text"
# ------------------------------------------------------------

# Our company is Plural Labs. Their documents are sitting in this folder.
folder = "plural_labs_docs"

# documents -> an empty list. We will fill it with one dictionary per file.
# Each dictionary will hold the file name and the full text of that file.
documents = []

# os.listdir -> gives us the names of all the files inside that folder
for file_name in os.listdir(folder):

    # We only want text files. Skip anything else.
    if not file_name.endswith(".txt"):
        continue

    # os.path.join -> safely joins folder name and file name
    # On Mac it makes plural_labs_docs/leave_policy.txt
    # On Windows it makes plural_labs_docs\leave_policy.txt
    # That is why we never write the slash by hand.
    file_path = os.path.join(folder, file_name)

    # open the file in read mode and read the whole thing as one big string
    # encoding="utf-8" -> important on Windows, otherwise special characters break
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # store the file name along with the text.
    # We need the file name later, because the answer must say WHERE it came from.
    documents.append({"source": file_name, "text": text})

print("STEP 1 - LOAD : loaded", len(documents), "files")


# ------------------------------------------------------------
# STEP 2 : CHUNK
# "Cut the text into 400 word pieces"
# ------------------------------------------------------------

# Why do we cut? Two reasons.
# 1. A whole file is too big to paste into a prompt.
# 2. If a file talks about leaves AND salary, we only want the leave part.
# Small pieces give sharp answers. Big pieces give blurry answers.

# In real projects the piece is around 400 words.
# Our demo files are small, so we will use 60 words per piece.
chunk_size = 60

# The vector database wants two matching lists, so we build exactly those two.
# chunk_texts  -> the pieces of text themselves
# chunk_labels -> a small note attached to each piece, saying which file it came from
# A note like this is called METADATA. The database carries it along with the vector
# and hands it back to us at search time.
chunk_texts = []
chunk_labels = []

# go through every file we loaded in step 1
for document in documents:

    # split() with no argument -> breaks the text on every space and newline
    # It gives us a list of individual words
    words = document["text"].split()

    # range(start, stop, step) -> 0, 60, 120, 180 ...
    # Each loop takes the next 60 words
    for start in range(0, len(words), chunk_size):

        # slice out 60 words, from start upto start + 60
        # " ".join -> glue those 60 words back into one sentence block
        piece_text = " ".join(words[start:start + chunk_size])

        # the two lists grow together, position by position.
        # piece number 7 in chunk_texts belongs to label number 7 in chunk_labels.
        chunk_texts.append(piece_text)
        chunk_labels.append({"source": document["source"]})

print("STEP 2 - CHUNK : cut into", len(chunk_texts), "chunks")


# ------------------------------------------------------------
# STEP 3 : EMBED
# "Turns each piece into numbers"
# ------------------------------------------------------------

# An embedding model reads a piece of text and returns a long list of numbers.
# That list is called a VECTOR. Here it is 3072 numbers long.
# The magic is this : two texts that MEAN the same thing get similar numbers,
# even when they use completely different words.
# "how many holidays do I get" and "leave policy 24 paid leaves" land close together.

# This is a different model from the chat model. It cannot talk. It only measures meaning.
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Let us actually SEE one vector once, so the word embedding stops being mysterious.
# embed_query -> one piece of text in, one list of numbers out.
sample_vector = embedding_model.embed_query(chunk_texts[0])

print("STEP 3 - EMBED : one chunk becomes", len(sample_vector), "numbers")
print("              first 5 of them :", sample_vector[:5])


# ------------------------------------------------------------
# STEP 4 : STORE
# "Save vectors in a vector database"
# ------------------------------------------------------------

# Now the real vector database enters.
# Read this one call carefully, because it is doing step 3 and step 4 together.
# Qdrant takes our list of texts, calls the embedding model for ALL of them itself,
# and stores every vector along with its label.
# We never loop, we never collect the vectors by hand. The database handles it.

vector_db = QdrantVectorStore.from_texts(
    # the pieces of text to store
    texts=chunk_texts,
    # which embedding model to use for turning them into numbers
    embedding=embedding_model,
    # the file name note to keep attached to each piece
    metadatas=chunk_labels,
    # a collection is like a table in SQL. All our Plural Labs vectors live in this one.
    collection_name="plural_labs",
    # ":memory:" -> run the database inside this program, nothing to install or start.
    # Change this one line to location="http://localhost:6333" and the exact same code
    # talks to a real Qdrant server instead. Nothing else in the file changes.
    location=":memory:",
)

print("STEP 4 - STORE : Qdrant vector database ready")

# A note for real projects.
# Because we said ":memory:", this database disappears when the program ends,
# so our indexing pipeline is running again on every run. That is fine for a demo.
# In a real system you would point it at a server or a folder on disk, index once,
# and then every question would skip steps 1 to 4 completely.
# That is what the diagram means by "pipeline 1 runs once in advance".

print("-" * 60)


# ============================================================
# PIPELINE 2 - ANSWERING
# Everything below runs again for EVERY single question.
# ============================================================


# ------------------------------------------------------------
# THE QUESTION
# ------------------------------------------------------------

# Notice, the words here do not exactly match any sentence in our files.
# Keyword search would struggle. Meaning search will not.
question = "I am travelling to Delhi for work. How much can I spend on food and hotel per day?"

# In class, comment the line above and uncomment these one at a time.
# This one pulls from a completely different file :
# question = "My child was just born. How many weeks of paternity leave do I get?"

# This one needs the solved tickets file :
# question = "A customer says the login page keeps loading forever. What do we tell them?"

# And this one is the important test. The answer is NOT in any Plural Labs file.
# A normal chatbot would happily invent something. Watch ours refuse.
# question = "What is the work from home policy at Plural Labs?"

print("QUESTION :", question)
print("-" * 60)


# ------------------------------------------------------------
# STEP 5 and STEP 6 : RETRIEVE and RANK
# "Embed the question, find the nearest chunk" and "keep the best three"
# ------------------------------------------------------------

# In the diagram these are two boxes, but in code the database does both in one call.
# similarity_search_with_score does all of this for us :
#   - it sends our question to the SAME embedding model, turning it into a vector
#   - it compares that vector against every vector it is holding
#   - it sorts them from nearest to farthest
#   - k=3 means it keeps only the best 3 and throws the rest away

# Why the SAME embedding model? Because two different rulers cannot be compared.
# Qdrant remembers which model we gave it in step 4, so it cannot make that mistake.

# Why only 3? Every extra chunk is extra noise and extra cost.
# We want the best evidence, not all the evidence.

top_chunks = vector_db.similarity_search_with_score(question, k=3)

print("STEP 5 and 6 - RETRIEVE and RANK : the 3 winning chunks are")

# Each item in top_chunks is a pair : the matching piece, and a number.
# document -> the piece itself. It carries two things with it :
#             document.page_content -> the actual text
#             document.metadata     -> the file name note we attached in step 2
# score    -> how close the two vectors are, between 0 and 1.
#             BIGGER is better. 1 would mean exactly the same meaning.
#             Qdrant measures the angle between the two vectors to get this.

for document, score in top_chunks:
    # round -> just to keep the number readable on screen
    # [:70] -> print only the first 70 characters so the screen stays clean
    print("   ", round(score, 3), "|", document.metadata["source"], "|", document.page_content[:70], "...")


# ------------------------------------------------------------
# STEP 7 : AUGMENT
# "Paste them into the prompt"
# ------------------------------------------------------------

# This is the heart of RAG and it is honestly just string building.
# We take the 3 winning chunks and glue them into one block of text.

context = ""

for document, score in top_chunks:
    # We keep the file name on top of every piece.
    # That is what lets the model tell us the source at the end.
    # "\n\n" -> a blank line after each piece, so the model can see where one ends
    context = context + "From file " + document.metadata["source"] + ":\n" + document.page_content + "\n\n"

# Now the full prompt. Read the rules carefully, they are doing real work.
# Rule 1 stops the model from using its own training data.
# Rule 2 is our guardrail against making things up.
# Rule 3 forces it to show the source, so the user can verify.
prompt = f"""You are the internal helpdesk assistant for a company called Plural Labs.

Answer the question using ONLY the context given below.
If the answer is not in the context, say "I could not find this in the Plural Labs documents."
Do not use any outside knowledge.
At the end, mention which file your answer came from.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

print("-" * 60)
print("STEP 7 - AUGMENT : prompt built,", len(prompt), "characters")


# ------------------------------------------------------------
# STEP 8 : GENERATE
# "LLM answers using only those pieces"
# ------------------------------------------------------------

# Now finally the chat model enters. Notice it enters LAST, not first.
# temperature = 0 -> be boring and factual. For a policy bot we do not want creativity.
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

# invoke -> send the prompt, wait, get the reply
response = llm.invoke(prompt)

print("-" * 60)
print("STEP 8 - GENERATE : grounded answer")
print()
print(response.text)


# ============================================================
# THE ONE LINE TO REMEMBER
# ============================================================
# We never trained the model on Plural Labs.
# We simply searched our own files, found the right paragraph,
# and handed it to the model along with the question.
# That is the whole of RAG.
