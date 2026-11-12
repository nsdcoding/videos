# ============================================================
# DAY 25 : RAG WITH REAL FILES - PART 1, THE PDF
# ============================================================

# On Day 22 we built the whole RAG machine. Eight steps, start to finish.
# It worked, but it had one very small line hiding in it :
#
#       if not file_name.endswith(".txt"):
#           continue
#
# That line is the subject of today's class.
#
# A real company does not keep its knowledge in .txt files. It keeps it in
# PDFs, in Word files, in intranet pages, in screenshots somebody pasted into
# a chat. Our Day 22 loader walks past every single one of them in silence.
#
# Look inside plural_labs_docs right now. There are 4 text files, 3 PDFs,
# 1 HTML page and 1 screenshot. Day 22 sees 4 files and misses more than half
# the company's knowledge, and it never prints a single warning while doing it.
#
# Today we teach it to read PDFs. The next class adds HTML and images.
#
# Only STEP 1 changes today. Steps 2 to 8 are the same machine as Day 22,
# so the comments on those steps are kept short - you already know them.
# Everything new is explained in full.


# ------------------------------------------------------------
# BEFORE YOU RUN THIS FILE : INSTALL THE NEW PACKAGE
# ------------------------------------------------------------

# On Mac, in the terminal :
#     pip3 install pypdf
#
# On Windows, in the command prompt :
#     pip install pypdf
# or python3 -m pip install X
#
# One package today. pypdf is written in pure Python, so it installs on every
# machine without needing a compiler. That is exactly why we start with it.
#
# You will hear about other PDF libraries - PyMuPDF, pdfplumber. They are
# faster and they understand page layout better. We will meet PyMuPDF in the
# screenshot class, because it can turn a PDF page into an image. For reading
# plain text out of a normal PDF, pypdf is the simplest thing that works.


# ------------------------------------------------------------
# THE IMPORTS
# ------------------------------------------------------------

import os

# re -> Python's REGULAR EXPRESSION module. This is probably new to you, so
# here is the whole idea in one paragraph before we use it.
#
# You already know how to find exact text :
#
#       text.replace("cat", "dog")
#
# That works when you know exactly what you are looking for. But today we have
# to fix messes where we do NOT know the exact text. We need to say things like
# "wherever there is a run of spaces and newlines, however long it happens to
# be, squash it down to one space". You cannot write that with .replace(),
# because you would have to call it once for two spaces, again for three
# spaces, again for a newline followed by two spaces, and so on forever.
#
# A regular expression - a regex - is a tiny language for describing a SHAPE of
# text instead of exact text. "A run of whitespace" is a shape. "A digit
# followed by a colon" is a shape. The re module is Python's reader for that
# language, and it is built into Python, so there is nothing to install.
#
# We use exactly one function from it today, re.sub, explained where we use it.
import re

# ---- from pypdf import PdfReader ----
#
# Look at this line next to the two lines above it. They are both imports,
# but they are written in two different shapes, and the difference is worth
# understanding because you will write both for the rest of your life.
#
#       import os                     <- bring in the WHOLE module
#       from pypdf import PdfReader   <- bring in ONE NAME out of a package
#
# With the first shape, everything stays behind its module name, and you must
# keep saying os.path.join. With the second shape, the one name you asked for
# is dropped straight into your file, so you write PdfReader(...) on its own
# rather than pypdf.PdfReader(...).
#
# Both work. We use the second here because we need exactly one thing out of
# pypdf and we mention it twice, so the shorter name is clearer. We use the
# first for os because we use many different pieces of it.
#
# WHERE DID pypdf COME FROM?
# os and re came with Python. pypdf did not - you installed it yourself with
# pip, and pip put a folder of Python files somewhere Python knows to look.
# That is all a "package" is : somebody else's Python files on your disk.
# Nothing magic, and you can go and read them.
#
# WHAT IS PdfReader?
# It is a CLASS, not a function. That capital-letters-joined-together style is
# how Python programmers signal a class - compare PdfReader with os.listdir.
# It is a convention, not a rule the language enforces, but it is followed so
# consistently that you can read a name and know what it is.
#
# The practical difference for us : calling a function gives you an answer,
# but calling a class gives you an OBJECT - a thing that holds state and has
# its own abilities attached to it. So when we write
#
#       reader = PdfReader(path)
#
# we are not asking "give me the text". We are saying "open this PDF and give
# me something I can ask questions of". Then we ask it things :
#
#       reader.pages                 -> the pages of the document
#       len(reader.pages)            -> how many pages there are
#       reader.pages[0]              -> the first page
#       reader.pages[0].extract_text()  -> the text on that page
#       reader.metadata              -> title, author, created date, if present
#
# ONE HONEST DETAIL. reader.pages looks like a list and you can loop over it,
# count it and index it - but it is not actually a list. pypdf hands back its
# own object that only parses a page at the moment you reach for it. That is
# why opening a 500 page PDF is instant : nothing has really been read yet.
# You do not have to do anything about this. It is simply worth knowing that
# "behaves like a list" and "is a list" are different claims in Python, and
# most code only ever needs the first.
#
# AND THE LIMIT THAT MATTERS MOST.
# extract_text() pulls out the text that is already stored inside the PDF as
# text. It does not look at the page and recognise letters. If a page is a
# photograph of a document, there is no text in there to pull, and pypdf
# returns an empty string - politely, with no error. Our loader checks for
# exactly that case further down, and the class after this one is about what
# to do when it happens.
from pypdf import PdfReader

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

folder = "plural_labs_docs"


# ============================================================
# STEP 0 : WHY DAY 22 CANNOT SIMPLY READ A PDF
# ============================================================

# Before we fix anything, let us watch the problem happen.
# A beginner's first instinct is reasonable : a PDF is a file, open() reads
# files, so just open it. Let us try that on one of our new PDFs.

print("STEP 0 - what happens if we read a PDF the Day 22 way")

try:
    with open(os.path.join(folder, "remote_work_policy.pdf"), "r", encoding="utf-8") as f:
        f.read()
except UnicodeDecodeError as error:
    print("    Python refused :", error)

# Read that error message slowly. "codec can't decode byte 0xf9".
#
# A .txt file is just letters, one after another. A PDF is not. A PDF is a
# small compressed database - it holds fonts, images, page sizes, and the text
# squeezed down into binary. Those bytes are not letters in any alphabet, so
# Python cannot turn them into a string and it stops.
#
# This is actually the GOOD case, because it is loud. It crashes and tells us.
# Later in this course we will meet the quiet case : a file that opens happily
# and gives us an empty string. That one is far more dangerous, because the
# program keeps running and just quietly knows nothing.
#
# So we cannot read a PDF ourselves. We need a library that understands the
# PDF format and unpacks the text for us. That is pypdf.

print("-" * 60)


# ============================================================
# PIPELINE 1 - INDEXING
# ============================================================

# ------------------------------------------------------------
# STEP 1 : LOAD - now with more than one file format
# ------------------------------------------------------------

# This is the whole lesson. Read it in three parts :
#   part A - a function that cleans up text
#   part B - one small loader function per file format
#   part C - a dictionary that picks the right loader


# ---------- part A : cleaning the text ----------

def clean_text(text):
    """Tidy up the raw text that a PDF gives us."""

    # PROBLEM 1 : ligatures.
    # Open any PDF of ours and pypdf hands back "Eﬀective" and "Oﬃce"
    # and "Conﬁdential". Those are not typos and pypdf is not broken.
    #
    # When a typesetter puts certain letters next to each other - f and f, or
    # f and i - the font draws them joined together as ONE single character.
    # Printers have done this for 500 years because "ff" looks cramped.
    # Unicode kept those joined shapes as real characters of their own.
    # So inside the PDF, the word "office" is genuinely stored as o + ﬃ + c + e.
    # Five characters, not six.
    #
    # Why we must care : our search works on meaning, but the embedding model
    # still reads characters. "Oﬃce" is not the word "office" to it. A student
    # asking about the office could easily miss this chunk. So we translate
    # those joined characters back into normal letters before anything else.
    ligatures = {
        "ﬀ": "ff",    # as in oﬀice hours, staﬀ
        "ﬁ": "fi",    # as in conﬁdential, beneﬁts
        "ﬂ": "fl",    # as in ﬂexible, reﬂect
        "ﬃ": "ffi",   # as in oﬃce, suﬃcient
        "ﬄ": "ffl",   # as in shaﬄe - rare, but costs nothing to handle
    }
    for joined_character, normal_letters in ligatures.items():
        text = text.replace(joined_character, normal_letters)

    # ----------------------------------------------------------------
    # MEET re.sub - it takes THREE arguments
    #
    #       re.sub(pattern, replacement, text)
    #          |       |          |        |
    #          |       |          |        +-- the text to work on
    #          |       |          +----------- what to put instead
    #          |       +---------------------- the SHAPE to look for
    #          +------------------------------ "substitute"
    #
    # It finds every place in the text that matches the shape, and replaces
    # all of them. Not the first one - every one. You do not write a loop.
    #
    # And note how we call it below :
    #
    #       text = re.sub(...)
    #
    # The result is ASSIGNED BACK to text. re.sub does not change the text you
    # give it, because strings in Python can never be changed once they exist.
    # It builds a brand new string and hands it back. If you forget the
    # "text =" part, the function runs perfectly, does all the work, and you
    # throw the answer away. Nothing crashes. That is a bug students lose
    # whole evenings to, so look for it first when cleaning seems to do nothing.
    # ----------------------------------------------------------------

    # PROBLEM 2 : hyphens at the end of a line.
    #
    # When a document is justified, a long word gets broken across two lines
    # with a hyphen : "reimburse-" at the end of one line and "ment" at the
    # start of the next. The PDF stores it exactly like that, so pypdf gives us
    #
    #       "reimburse-\nment"
    #
    # and our search would then be looking for a word that does not exist.
    # Glue it back together by deleting the hyphen and the newline.
    #
    # Reading the pattern r"-\n" :
    #       -       an ordinary hyphen, matching itself
    #       \n      a newline, the invisible character at the end of a line
    #
    # The replacement is "" - an empty string - which is how you say "delete
    # this" with re.sub. There is no separate delete function; replacing
    # something with nothing IS deleting it.
    #
    # HONESTY NOTE, and a habit worth copying : this rule finds nothing in our
    # three PDFs. I counted - zero matches - because the tool that made them
    # does not hyphenate. It fires constantly on PDFs exported from Word or
    # from LaTeX. Keeping a rule that does nothing today costs us nothing and
    # saves us the day a student brings in a real company document. But do go
    # and count, rather than assuming your cleaning worked :
    #
    #       print(len(re.findall(r"-\n", raw_text)))
    text = re.sub(r"-\n", "", text)

    # PROBLEM 3 : ragged whitespace. This is the rule that does the real work.
    #
    # A PDF does not store sentences. It stores instructions like "draw these
    # letters at this position on the page". So where a sentence happens to
    # reach the right margin, the PDF simply starts the next line, and pypdf
    # hands that back to us as a newline sitting in the middle of a sentence.
    # One of our own pages genuinely contains this :
    #
    #       "Do not turn it off. Your\nscreen must lock automatically"
    #
    # Our handbook has 45 of those. Column layouts and tables are worse again,
    # and give long runs of spaces in the middle of a line.
    #
    # Reading the pattern r"\s+" :
    #       \s      ONE whitespace character - a space, a tab, or a newline
    #       +       "one or more of the thing just before me"
    #   so  \s+     a run of whitespace of ANY length, from one to a thousand
    #
    # Replacing all of it with a single " " turns any mess of spacing into one
    # ordinary space. "it off. Your\nscreen" becomes "it off. Your screen".
    #
    # WHY THE LITTLE r BEFORE THE QUOTES?
    # That r makes it a RAW string, and it is not decoration. Inside a normal
    # Python string a backslash starts an escape code - "\n" means newline,
    # "\t" means tab. But "\s" is not an escape code Python knows, and Python
    # 3.14 will tell you so :
    #
    #       SyntaxWarning: "\s" is an invalid escape sequence.
    #
    # The r switches that whole system off and passes the characters through
    # untouched, so the regex engine receives \ and s and reads them as its own
    # code for whitespace. Habit to build : if a string is a regex, start it
    # with r, every time, without thinking about it.
    text = re.sub(r"\s+", " ", text)

    # ORDER MATTERS, and this is the kind of thing that makes cleaning code
    # look simple and behave strangely. Problem 2 must run BEFORE problem 3.
    # Once problem 3 has turned every newline into a space, "reimburse-\nment"
    # has already become "reimburse- ment", and the pattern r"-\n" can never
    # match it again. Swap these two lines and the hyphen fix silently stops
    # working - with no error, which is exactly why you must notice it now.

    # .strip() -> remove leading and trailing spaces
    return text.strip()


# ---------- part B : one loader per file format ----------

# Every loader below follows the SAME contract, and the contract is the point.
# Each one takes a file path and returns a LIST of dictionaries, where each
# dictionary is {"page": <number or None>, "text": <the text>}.
#
# Why a list, when a text file has only one piece of text in it?
# Because a PDF has many. If we return a list from every loader, then the code
# that calls them never has to care which format it is dealing with. One file
# gives us one list, whether that list has 1 item or 400.
#
# That idea - every loader looks identical from the outside - is what will let
# us add HTML and images next class by writing one function and changing
# nothing else in this file.


def load_txt(path):
    """Read a plain text file. This is Day 22's loader, unchanged."""
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    # page is None because a text file has no pages. Nothing to number.
    # We will handle that None when we print the source at the end.
    return [{"page": None, "text": clean_text(text)}]


def load_pdf(path):
    """Read a PDF, one entry per page."""

    # PdfReader opens the file and understands its structure for us.
    reader = PdfReader(path)

    pages = []

    # reader.pages behaves like a list of page objects.
    # enumerate(..., start=1) gives us the position as we go, counting from 1
    # instead of 0 - because a human reading page one calls it page 1.
    for page_number, page in enumerate(reader.pages, start=1):

        # extract_text() -> pulls the text out of that one page.
        # It can return None for a page that has no text layer at all,
        # so "or empty string" protects us from a crash on the next line.
        raw_text = page.extract_text() or ""

        text = clean_text(raw_text)

        # THE EMPTY PAGE CHECK.
        # If a page gives us almost nothing, something is wrong with it.
        # Usually it means the page is a SCANNED IMAGE - somebody photocopied
        # a document and saved the photo inside a PDF. There are no letters in
        # that file at all, only a picture of letters. pypdf is not failing;
        # there is genuinely nothing there for it to find.
        #
        # We cannot fix that today, but we must never let it pass in silence.
        # An empty chunk in our database is worse than no chunk, because it
        # still takes up one of the 3 slots our search returns.
        # Next class we send pages like this to a vision model to be read.
        if len(text) < 100:
            print("    WARNING :", os.path.basename(path), "page", page_number,
                  "gave only", len(text), "characters - is it a scan?")
            continue

        pages.append({"page": page_number, "text": text})

    return pages


# ---------- part C : the dictionary that chooses ----------

# Here is the idea that replaces Day 22's if-statement.
#
# We already know a dictionary can hold numbers or strings as its values.
# A dictionary can also hold FUNCTIONS as its values. Look carefully at what
# is written below : load_txt, with no brackets after it.
#
#     load_txt()  -> brackets mean CALL the function right now, give me the result
#     load_txt    -> no brackets means the function ITSELF, as a value
#
# So LOADERS is a dictionary from a file extension to the function that knows
# how to read it. People call this a dispatch table, or a registry.
#
# Why this is better than a chain of if-elif-elif :
#   - adding a format is adding ONE line, not editing a growing if-block
#   - the list of what we support is visible in one place, at a glance
#   - the loop below never mentions pdf or txt at all, so it never changes

LOADERS = {
    ".txt": load_txt,
    ".md":  load_txt,   # a markdown file is plain text too, so the same loader works
    ".pdf": load_pdf,
}


# ---------- and now the loading loop ----------

documents = []

for file_name in sorted(os.listdir(folder)):

    # os.path.splitext splits a name into two parts at the last dot.
    # "remote_work_policy.pdf" becomes ("remote_work_policy", ".pdf")
    # The [1] takes the second part, the extension.
    # .lower() because a file called NOTES.PDF must work exactly the same way.
    extension = os.path.splitext(file_name)[1].lower()

    # .get() asks the dictionary for a value WITHOUT crashing if the key is
    # missing. A plain LOADERS[extension] would raise KeyError on our .html
    # file. .get() returns None instead, and we can deal with None ourselves.
    loader = LOADERS.get(extension)

    if loader is None:
        # Day 22 skipped these silently. We refuse to. A loud skip is a to-do
        # list - it is literally printing next class's homework on the screen.
        print("    skipping", file_name, "- no loader for", extension, "yet")
        continue

    file_path = os.path.join(folder, file_name)

    # THE CALL. Note that we do not write load_pdf(file_path) anywhere.
    # We write loader(file_path), and the dictionary already decided which
    # function "loader" is. This one line reads every format we support.
    pieces = loader(file_path)

    # Each loader gave us a list. We attach the file name to every piece and
    # collect them all into one flat list of documents.
    for piece in pieces:
        documents.append({
            "source": file_name,
            "page":   piece["page"],
            "text":   piece["text"],
        })

    print("    loaded", file_name, "->", len(pieces), "piece(s)")

print("STEP 1 - LOAD :", len(documents), "pieces of text from", folder)


# A small helper for printing where something came from.
# A PDF piece can say "page 2". A text file piece cannot, so it just says the
# file name. This is the one place that None has to be handled, and we keep it
# in a function so the rest of the file stays clean.
def describe_source(source, page):
    if page is None:
        return source
    return source + " page " + str(page)


print("-" * 60)


# ------------------------------------------------------------
# STEP 2 : CHUNK
# ------------------------------------------------------------

# Same 60-word cutting as Day 22. We are deliberately not improving the
# chunking today - one change per class, so you can always see what caused
# what. Chunking gets a full class of its own next.
#
# ONE thing is new here, and it is small but important. In Day 22 the label
# carried only the file name. Now it carries the page number too, and it
# carries it all the way through the database to the final answer. That is how
# our bot will be able to say "page 2" instead of just naming a 40 page PDF
# and leaving you to search it yourself.
#
# Notice also that because we loaded page by page, a chunk can never contain
# text from two different pages. The page split did half of our chunking for
# us, for free.

chunk_size = 60

chunk_texts = []
chunk_labels = []

for document in documents:
    words = document["text"].split()

    for start in range(0, len(words), chunk_size):
        piece_text = " ".join(words[start:start + chunk_size])

        chunk_texts.append(piece_text)
        chunk_labels.append({
            "source": document["source"],
            "page":   document["page"],      # <- the new part
        })

print("STEP 2 - CHUNK : cut into", len(chunk_texts), "chunks")


# ------------------------------------------------------------
# STEP 3 and 4 : EMBED and STORE
# ------------------------------------------------------------

# Unchanged from Day 22. Qdrant calls the embedding model for every chunk and
# stores each vector together with its label.

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

vector_db = QdrantVectorStore.from_texts(
    texts=chunk_texts,
    embedding=embedding_model,
    metadatas=chunk_labels,
    collection_name="plural_labs",
    location=":memory:",
)

print("STEP 3 and 4 - EMBED and STORE : Qdrant ready with", len(chunk_texts), "vectors")
print("-" * 60)


# ============================================================
# PIPELINE 2 - ANSWERING
# ============================================================

# THE QUESTION.
# This exact question was the last demo of Day 22, and Day 22 could not answer
# it. Our bot correctly refused, because the work from home rules were simply
# not in any of the four text files.
#
# Nothing about our retrieval or our prompt has improved since then. The only
# thing that changed is that the loader can now open a PDF. Watch the same
# question get a real answer.

question = "Can I work from home permanently at Plural Labs?"

# In class, try these one at a time.

# Needs page 1 of the remote work PDF :
# question = "How much is the home office setup allowance and by when must I claim it?"

# Needs the IT security PDF :
# question = "How long before my laptop screen locks, and can I change it?"

# Needs the insurance PDF :
# question = "Are my parents covered by the company health insurance?"

# A text file question, to prove we did not break Day 22 while adding PDFs :
# question = "How many paid leaves do I get in a year?"

# This one crosses TWO files - the leave policy text file and the remote work
# PDF. Watch how it handles needing evidence from both :
# question = "I am a new joiner. Can I work remotely, and how many leaves do I get?"

# And the honesty test again. Notice period is in none of our 9 files,
# not even the new ones. It must still refuse.
# question = "What is the notice period if I resign from Plural Labs?"

print("QUESTION :", question)
print("-" * 60)


# ------------------------------------------------------------
# STEP 5 and 6 : RETRIEVE and RANK
# ------------------------------------------------------------

top_chunks = vector_db.similarity_search_with_score(question, k=3)

print("STEP 5 and 6 - RETRIEVE and RANK : the 3 winning chunks are")

for document, score in top_chunks:
    # metadata["page"] is the page number we carried all the way from STEP 1.
    where = describe_source(document.metadata["source"], document.metadata["page"])
    print("   ", round(score, 3), "|", where, "|", document.page_content[:65], "...")


# ------------------------------------------------------------
# STEP 7 : AUGMENT
# ------------------------------------------------------------

# Same string building as Day 22, with the page number added to the header
# line of each piece. The model can only cite a page if we show it one.

context = ""

for document, score in top_chunks:
    where = describe_source(document.metadata["source"], document.metadata["page"])
    context = context + "From " + where + ":\n" + document.page_content + "\n\n"

prompt = f"""You are the internal helpdesk assistant for a company called Plural Labs.

Answer the question using ONLY the context given below.
If the answer is not in the context, say "I could not find this in the Plural Labs documents."
Do not use any outside knowledge.
At the end, mention which file your answer came from, and the page number if there is one.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

print("-" * 60)
print("STEP 7 - AUGMENT : prompt built,", len(prompt), "characters")


# ------------------------------------------------------------
# STEP 8 : GENERATE
# ------------------------------------------------------------

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

response = llm.invoke(prompt)

print("-" * 60)
print("STEP 8 - GENERATE : grounded answer")
print()
print(response.text)


# ============================================================
# WHAT TO TAKE AWAY FROM TODAY
# ============================================================
#
# 1. The retrieval did not get smarter today. The LOADER got wider.
#    A RAG system is only as good as the documents it can actually open,
#    and that is usually the cheapest part of it to improve.
#
# 2. A loader is not one function, it is a pipeline. Open the file, pull the
#    text out, clean the text, split it into pages, check the result is not
#    empty. The cleaning and the checking are not optional extras - the
#    ligature problem would have quietly damaged every search for the word
#    "office" in our entire company handbook.
#
# 3. A dictionary of functions turns "support one more format" from a code
#    change into a one line addition.
#
# WHAT IS STILL BROKEN, for next class :
#
#   - the HTML file is skipped, and when we do load it we must throw away the
#     navigation menu, the cookie banner and the JavaScript, or our search
#     results will be full of the words "Home HR Portal IT Desk Finance"
#
#   - the screenshot is skipped, and it cannot be opened by any text library
#     at all, because there is no text in it - only a picture of text.
#     That one needs a model with eyes.
#
#   - and we still have not improved the chunking, which is the single
#     biggest quality win left in this project.
