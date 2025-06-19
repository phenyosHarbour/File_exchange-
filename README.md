# Smart PDF2Word

Smart PDF2Word is an advanced tool designed to efficiently convert PDF documents into editable Word files (.docx). It aims to provide high-fidelity conversion with support for complex layouts, tables, images, and multilingual text. This project is suitable for both individual users and developers who need reliable PDF-to-Word conversion functionality in their workflow.

## Features

- 🚀 **Accurate PDF to Word Conversion:** Maintains formatting, tables, images, and fonts.
- 🖼️ **Image Extraction:** Preserves embedded images and graphics.
- 🌐 **Multilingual Support:** Handles documents in various languages.
- ⚙️ **Batch Processing:** Convert multiple PDFs at once.
- 🧩 **Easy Integration:** Usable as a standalone tool or as a library in other Python projects.
- 💻 **Cross-Platform:** Works on Windows, macOS, and Linux.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/phenyosHarbour/smart-pdf2word.git
cd smart-pdf2word
pip install -r requirements.txt
```

## Usage

### As a Command-Line Tool

```bash
python pdf2word.py input.pdf output.docx
```

- `input.pdf`: Path to your PDF file.
- `output.docx`: Desired path for the converted Word file.

### As a Library

```python
from smart_pdf2word import convert_pdf_to_word

convert_pdf_to_word("input.pdf", "output.docx")
```

## Configuration

You can adjust conversion settings (such as output quality, image handling, and language options) within the `config.py` file.

## Examples

Convert a single PDF:

```bash
python pdf2word.py sample.pdf sample.docx
```

Batch convert all PDFs in a folder:

```bash
python batch_convert.py ./pdfs ./word_docs
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and new features.

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Submit a pull request


## Acknowledgements

- Built with Python and other open-source libraries.
- Thanks to all contributors and users for their feedback!

## Contact

For issues, suggestions, or questions, please open an [issue](https://github.com/phenyosHarbour/smart-pdf2word/issues) or contact the repository owner.

---
*Happy converting!*
