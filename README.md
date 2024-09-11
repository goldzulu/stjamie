# Coinweb AI Dapp Builder

This Streamlit app serves as an AI-powered assistant for building Coinweb blockchain Dapps. It utilizes the Coinweb Hello World and String Processor templates as starting points for Dapp development.

## Features

- Interactive chat interface with an AI assistant
- Knowledge base built from Coinweb starter templates
- Ability to add new knowledge sources on the fly
- Sidebar displaying available templates for reference

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
     GHPAT_TOKEN = "your_github_personal_access_token"
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
2. The sidebar displays the templates the AI has learned from and can leverage for Dapp development.
3. You can ask questions about building Coinweb Dapps, and the AI assistant will provide guidance based on the loaded templates.
4. Use the `/add <source>` command to add new knowledge sources to the assistant's database.

### Example Questions

Here are some examples of questions you can ask the AI assistant:

1. "I want to create a crowdfunding Dapp. Can you give me the file structure, the files, and relevant code I need to change from the Hello World template?"

2. "How do I implement a token transfer function in my Coinweb Dapp?"

3. "What are the main differences between the Hello World and String Processor templates?"

4. "Can you explain how to deploy a Coinweb Dapp to the testnet?"

5. "How can I add user authentication to my Coinweb Dapp?"

6. "What are some best practices for handling errors in Coinweb smart contracts?"

7. "How do I integrate a front-end framework like React with my Coinweb Dapp?"

Feel free to ask these questions or formulate your own based on your specific Dapp development needs.

## Customization

To add more Coinweb templates or other GitHub repositories:

1. Open the Python file.
2. Locate the `embedchain_bot()` function.
3. Add new repositories using the `app.add()` method:
   ```python
   app.add("repo:username/repo-name type:repo", data_type="github", loader=loader)
   ```

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
