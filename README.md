# Chat LangChain - Till's version

This is Till's version of the [Chat Langchain](https://github.com/langchain-ai/chat-langchain).

The original Chat Langchain is a chatbot specifically focused on question answering over the [LangChain documentation](https://python.langchain.com/).
Built with [LangChain](https://github.com/langchain-ai/langchain/), [FastAPI](https://fastapi.tiangolo.com/), and [Next.js](https://nextjs.org).

From there I modified it (and plan to modify it) in the following ways:

* Running locally with Ollama ✅
* Offering multiple local models 
* Offering different sources: Another website (maybe a manual of another software), a Wiki space...
* Providing functionality to evaluate performance, i.e. if the answers are close to what we expect.

## Todo / backlog

* Move from poetry to `requirements file` - as poetry is too complex for a hobby programmer like me. Maybe that's already done, but I have to test it... ❓
* Find out ifthe `_scripts` directory is needed.
* Server component should list the available models so client offers option to choose
* Server component offers different _brainz_, i.e. sites that have been scraped and ingested

## Running locally
1. Create a local Python environment: `python3.12 -m venv .venv`
2. Activate it with `source .venv/bin/activate`
3. Install backend dependencies: `pip install -r requirements.txt`.
4. Makle sure Ollama is running and has the provided models pulled. You can check it with `ollama list`.
5. Run `python backend/ingest.py` to ingest LangChain docs data into the Chroma vectorstore (only needs to be done once).
6. Start the Python backend with `python backend/main.py`.
7. Install frontend dependencies by running `cd ./frontend`, then `yarn`.
8. Run the frontend with `yarn dev` for frontend.
9. Open [localhost:3000](http://localhost:3000) in your browser.

