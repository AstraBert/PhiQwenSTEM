# Chatbot UI

A lightweight and modern chat interface for LLM interactions with Markdown support!

## Overview

A minimalist chat interface built with React and TypeScript, designed to be easily integrated with any LLM backend. Features a clean and modern design.

![Demo](demo/image.png)

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/ChristophHandschuh/chatbot-ui.git
cd chatbot-ui
```

2. Install dependencies
```bash
npm i
```

3. Start the development server
```bash
npm run dev
```

## Test Mode

The project includes a test backend for development and testing purposes. To use the test mode:

1. Navigate to the testbackend directory
2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. Install the required package:
```bash
pip install websockets
```
4. Run the test backend:
```bash
python test.py
```

## Credits

This project was built by:
- [Leon Binder](https://github.com/LeonBinder)
- [Christoph Handschuh](https://github.com/ChristophHandschuh)

Some code components were inspired by and adapted from [Vercel's AI Chatbot](https://github.com/vercel/ai-chatbot).

## License

This project is licensed under the Apache License 2.0. Please note that some components were adapted from Vercel's open source AI Chatbot project.
