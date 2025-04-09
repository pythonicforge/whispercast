# WhisperCast

WhisperCast is a cutting-edge command-line application designed to transform text into engaging audio content. Whether you're creating podcasts, audiobooks, or simply exploring the power of AI-driven text-to-speech and language models, WhisperCast provides a seamless and intuitive experience.

<br/>

### Features

#### 1. **Podcast Generation**
   - Generate high-quality podcast scripts using advanced language models.
   - Convert scripts into audio files with natural-sounding voices.
   - Customize topics and durations for tailored podcast episodes.

#### 2. **Audiobook Creation**
   - Transform text files, PDFs, or URLs into immersive audiobooks.
   - Supports multiple file formats, including `.txt`, `.pdf`, and `.docx`.
   - Ensures a conversational and engaging tone for listeners.

#### 3. **Interactive Learning with Sensei Mode**
   - Upload a file and let the AI teach you its content.
   - Ask questions interactively, and get concise, accurate answers.
   - Perfect for learning new topics or exploring complex documents.

#### 4. **Audio File Management**
   - List all generated audio files with the `ls` command.
   - Play audio files directly from the command line using the `play` command.

#### 5. **Content Fetching**
   - Fetch topic-related data from multiple sources:
     - Wikipedia summaries
     - Google News articles
     - DuckDuckGo insights
     - Reddit discussions
     - Hacker News articles
   - Combine and summarize content for comprehensive insights.

<br/>

### Installation

#### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

#### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/WhisperCast.git
   cd WhisperCast
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     GROQ_API_KEY=your_groq_api_key
     DEBUG=true
     ENVIRONMENT=development
     ```

4. Run the application:
   ```bash
   python main.py
   ```
<br/>

### Usage

### Commands
- **`podcast <topic>`**: Generate a podcast script and audio file for the given topic.
- **`audiobook <file_path>`**: Convert a file into an audiobook.
- **`sensei <file_path>`**: Learn interactively about a file's content and ask questions.
- **`ls`**: List all available audio files in the `output` directory.
- **`play <file_number>`**: Play an audio file by selecting its number from the `ls` command.
- **`clear`**: Clear the terminal screen.
- **`bye`**: Exit the application.

<br/>

### Project Structure

```
WhisperCast/
├── cli/
│   └── shell.py          # Command-line interface implementation
├── utils/
│   ├── text_to_speech.py # Text-to-speech functionality
│   ├── llm.py            # Language model interactions
│   ├── extractor.py      # File and content extraction utilities
│   ├── fetcher.py        # Fetch content from external sources
│   ├── finder.py         # File management utilities
│   ├── log_manager.py    # Logging configuration
├── main.py               # Entry point for the application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

<br/>

### Key Technologies

- **Text-to-Speech**: Powered by [Coqui TTS](https://github.com/coqui-ai/TTS) for natural-sounding audio generation.
- **Language Models**: Utilizes Groq's LLaMA 3 for advanced text processing and script generation.
- **Web Scraping**: Fetches content from Wikipedia, Google News, Reddit, and more using `BeautifulSoup` and `feedparser`.
- **Logging**: Comprehensive logging with `loguru` for debugging and monitoring.

<br/>

### Contributing

We welcome contributions to WhisperCast! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

<br/>

### License

This project is licensed under the Apache License. See the `LICENSE` file for details.

<br/>

### Acknowledgments

- [Coqui TTS](https://github.com/coqui-ai/TTS) for their exceptional text-to-speech library.
- [Groq](https://groq.com/) for their powerful language models.
- The open-source community for providing invaluable tools and resources.

<br/>

### Contact

For questions, feedback, or support, please reach out to:
- **Email**: pseudopythonic@gmail.com
- **GitHub**: [pythonicforge](https://github.com/pythonciforge)