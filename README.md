# St James Senior Girls AI Bot St Jamie!

This Streamlit app serves as an AI-powered assistant for as a companion for St James Senior Girls AI Club members

## Features

- Interactive chat interface with an AI assistant
- Ability to add new knowledge sources on the fly

## Prerequisites

- Python 3.12+
- Streamlit
- embedchain library
- GitHub Personal Access Token
- OpenAI API Key

## Installation

IMPORTANT: Locate app.py lines below and comment it out if uncommented to run locally. On streamlit.io make sure they are uncommented out:
# WARNING: The following two lines are ONLY for Streamlit.
# Remove them from local install!!
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

1. Clone this repository:
   ```
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. Install the required dependencies:
   ```
   pip install streamlit embedchain
   ```

3. Set up your GitHub Personal Access Token and OpenAI API Key:
   - Create a `.streamlit/secrets.toml` file in your project directory
   - Add your tokens:
     ```
     OPENAI_API_KEY = "your_openai_api_key"
     ```

4. Ensure you have a `config.yaml` file in your project directory for embedchain configuration.

## Running the App

To run the Streamlit app, use the following command in your terminal:

```
streamlit run app.py
```

Replace `app.py` with the name of your Python file if it's different.

Note: The first time you run the app, it may take some time to start up as it loads the GitHub repositories. Subsequent runs will be faster.

## Usage

1. Once the app is running, you'll see a chat interface.
2. You can ask questions about building and Using AI apps, and the AI assistant will provide guidance
3. Use the `/add <source>` command to add new knowledge sources to the assistant's database.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## MIT License

Copyright (c) 2024 GoldZulu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
