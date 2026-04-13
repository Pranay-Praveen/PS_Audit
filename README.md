# LRS-Audit

I built this because I wanted something that actually looks at code the way a security reviewer would, not just a linter that flags syntax stuff.

You upload a file, it runs two separate analyses on it and shows them side by side. The idea is if both passes catch the same issue, it's probably real. If only one does, worth a closer look manually.

Supports .py, .c, .cpp and .java files right now.

## Running it

    pip install -r requirements.txt
    streamlit run app.py

Get an API key from openrouter.ai, paste it in the sidebar and you're good.

## Deploying

Push to GitHub and connect the repo on share.streamlit.io. Add your API key under Settings > Secrets like this:

    OPENROUTER_API_KEY = "your-key-here"

That's it.
