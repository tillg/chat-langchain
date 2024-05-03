# smart chat 

This is Till's version of the [Chat Langchain](https://github.com/langchain-ai/chat-langchain).

The original Chat Langchain is a chatbot specifically focused on question answering over the [LangChain documentation](https://python.langchain.com/).
Built with [LangChain](https://github.com/langchain-ai/langchain/), [FastAPI](https://fastapi.tiangolo.com/), and [Next.js](https://nextjs.org).

From there I modified it (and plan to modify it) in the following ways:

* Running locally with Ollama ✅
* Offering multiple local models 
* Offering different sources: Another website (maybe a manual of another software), a Wiki space...
* Providing functionality to evaluate performance, i.e. if the answers are close to what we expect.

## Dev Setup & Running

I use a couple of windows with a standard command (this all assumes you are in the project folder):

```bash
# Run the langfuse stack
docker-compose up

# Follow the Ollama log
less +F ~/.ollama/logs/server.log

# Run the server: Go into the project (root) directory
source .venv/bin/activate
python main.py
```

Once this runs locally, you get the following web-urls:
* [Local langfuse](http://localhost:3001)
* [Local API documentation](http://localhost:8080/docs)

## Todo / backlog

* Find out ifthe `_scripts` directory is needed.
* Server component should list the available models so client offers option to choose
* Server component offers different _brainz_, i.e. sites that have been scraped and ingested

## Done

* 2024-05-01 Serve new `chat` API
* 2024-04-29 Decision is taken to rework the backend API. Think API first!
* 2024-04-28 Added logging
* 2024-04-25 Renamed Github Repo
* 2024-04-24 Move from poetry to `requirements file` - as poetry is too complex for a hobby programmer like me.
* 2024-04-22 Simplify the original project and get it running fully locally

## Running locally

1. Create a local Python environment: `python3.12 -m venv .venv`
2. Activate it with `source .venv/bin/activate`
3. Install backend dependencies: `pip install -r requirements.txt`.
4. Makle sure Ollama is running and has the provided models pulled. You can check it with `ollama list`.
4. Configure your constants in `backend/constants.py`
5. Run `python backend/ingest.py` to ingest LangChain docs data into the Chroma vectorstore (only needs to be done once).
6. Start the Python backend with `python backend/main.py`.
7. Install frontend dependencies by running `cd ./frontend`, then `yarn`.
8. Run the frontend with `yarn dev` for frontend.
9. Open [localhost:3000](http://localhost:3000) in your browser.


## Problems & Reading
* Interesting: [The React library for LLMs.](https://github.com/llm-ui-kit/llm-ui). It also provides everything for streaming...
* [Add Langfuse to your Langchain application](https://langfuse.com/docs/integrations/langchain/tracing)