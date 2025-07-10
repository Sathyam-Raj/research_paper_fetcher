Here's the complete `README.md` file in plain text format that you can directly copy and paste into VS Code:

```text
# PubMed Research Paper Fetcher

A Python tool to fetch research papers from PubMed with pharmaceutical/biotech company affiliations and export results to CSV.

## Features

- Search PubMed using their full query syntax
- Filter papers with at least one author from pharmaceutical/biotech companies
- Export results with detailed author affiliation information
- Flexible output options (auto-saved CSV or console output)
- Debug mode for troubleshooting

## Code Organization

The project follows a modular structure:

```
research_paper_fetcher/
│
├── paperfetcher/                  # Main package
│   ├── __init__.py                # Package initialization
│   ├── api.py                     # PubMed API interactions
│   ├── processor.py               # Paper processing and filtering logic
│   ├── cli.py                     # Command-line interface
│   └── models.py                  # Data models and type definitions
│
├── tests/                         # Unit tests
│   └── test_api.py                # Test cases for API functions
│
├── .gitignore                     # Files to ignore in Git
├── pyproject.toml                 # Poetry configuration
├── README.md                      # Project documentation
└── LICENSE                        # MIT License
```

## Installation

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/research_paper_fetcher.git
   cd research_paper_fetcher
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Verify installation:
   ```bash
   poetry run get-papers-list --help
   ```

## Usage

### Basic Command

```bash
poetry run get-papers-list "your search query"
```

This will automatically save results to a CSV file with timestamp (e.g., `papers_results_20230725_143022.csv`).

### Options

| Option | Description |
|--------|-------------|
| `-f, --file FILENAME` | Save to custom filename instead of auto-generated one |
| `-p, --print` | Print results to console instead of saving to file |
| `-d, --debug` | Enable debug mode for verbose output |
| `-h, --help` | Show help message |

### Examples

1. Basic search with auto-saved CSV:
   ```bash
   poetry run get-papers-list "cancer AND immunotherapy"
   ```

2. Save to custom filename:
   ```bash
   poetry run get-papers-list "diabetes treatment" -f diabetes_papers.csv
   ```

3. Print to console instead of saving:
   ```bash
   poetry run get-papers-list "alzheimer's disease" -p
   ```

4. Debug mode:
   ```bash
   poetry run get-papers-list "parkinson's" -d
   ```

## Dependencies

### Core Libraries

- [requests](https://docs.python-requests.org/) - HTTP requests for PubMed API
- [click](https://click.palletsprojects.com/) - Command-line interface creation
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/) - Environment variable management

### Development Tools

- [Poetry](https://python-poetry.org/) - Dependency management and packaging
- [pytest](https://docs.pytest.org/) - Testing framework
- [mypy](http://mypy-lang.org/) - Static type checking
- [black](https://black.readthedocs.io/) - Code formatting

## PubMed Query Syntax

The tool supports PubMed's full query syntax. Some examples:

- `"cancer AND immunotherapy"`
- `"diabetes[Title] AND (2020[Date - Publication] : 2023[Date - Publication])"`
- `"biomarkers[Title/Abstract] AND pharmaceutical[Affiliation]"`

For advanced query syntax, refer to [PubMed's search field guide](https://pubmed.ncbi.nlm.nih.gov/help/#search-tags).

## How Non-Academic Affiliations Are Identified

The system uses these heuristics to identify non-academic authors:

1. **Academic Keywords**: Filters out affiliations containing:
   - university, college, institute, school
   - hospital, medical center, clinic
   - labs, laboratory, foundation

2. **Pharma/Biotech Keywords**: Looks for known company names (e.g., Pfizer, Novartis) and terms like:
   - "pharmaceutical", "biotech", "biosciences"
   - "inc", "ltd", "corp" in affiliation text

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PubMed/NCBI for their [E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25500/)
- Python community for the excellent libraries used in this project
```

To use this:

1. Open VS Code
2. Create a new file named `README.md`
3. Paste this entire content
4. Save the file

The document includes:
- Proper Markdown formatting
- Code blocks for commands
- Tables for options
- Clear section headers
- All necessary links
- Complete installation and usage instructions

You can customize the GitHub repository URL and any other specific details as needed for your project.