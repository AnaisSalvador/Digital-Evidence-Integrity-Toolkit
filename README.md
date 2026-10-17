

\# Digital Evidence Integrity Toolkit



A lightweight Python command-line tool for verifying the integrity of digital evidence using SHA-256 hashes.



\## Overview



The Digital Evidence Integrity Toolkit creates a JSON manifest containing the SHA-256 hash and file size of each evidence file. The manifest can later be used to check whether the files have changed, are missing, or still match their recorded hashes.



This project demonstrates practical skills in Python development, cryptographic hashing, file handling, input validation, command-line interfaces, and automated testing.



\## Features



\- Calculate SHA-256 hashes using Python's `hashlib`.

\- Process files in chunks to avoid loading entire files into memory.

\- Create and save JSON integrity manifests.

\- Verify evidence files against previously recorded hashes.

\- Detect modified and missing files.

\- Validate manifest structure and hash formats.

\- Reject paths that escape the designated evidence directory.

\- Return meaningful process exit codes.

\- Run automated tests with `pytest`.



\## Project Structure



```text

Digital-Evidence-Integrity-Toolkit/

├── src/

│   └── evidence\_tool/

│       ├── \_\_init\_\_.py

│       ├── cli.py

│       ├── hasher.py

│       └── manifest.py

├── tests/

│   ├── test\_cli.py

│   ├── test\_hasher.py

│   ├── test\_manifest.py

│   └── test\_verification.py

├── sample\_evidence/

│   └── evidence.txt

├── output/

├── .gitignore

├── pyproject.toml

├── requirements-dev.txt

└── README.md

```



\## Requirements



\- Python 3.10 or newer

\- pip

\- pytest for running the test suite



\## Installation



Clone the repository and navigate to the project directory.



Install the project in editable mode:



```bash

py -m pip install -e .

```



Install the development dependency:



```bash

py -m pip install -r requirements-dev.txt

```



\## Usage



\### 1. Create an integrity manifest



Run the following command from the project root:



```bash

py -m evidence\_tool.cli create --base-dir sample\_evidence --files evidence.txt --output output/manifest.json

```



The tool calculates the SHA-256 hash and records the file size for each selected file.



\### 2. Verify evidence integrity



```bash

py -m evidence\_tool.cli verify --base-dir sample\_evidence --manifest output/manifest.json

```



Possible file verification results:



\- `MATCH`: The current file hash matches the recorded hash.

\- `MISMATCH`: The current file hash differs from the recorded hash.

\- `MISSING`: The expected file does not exist.



\### 3. Run the test suite



```bash

py -m pytest -v

```



The tests cover hash calculation, manifest creation and validation, file verification, path traversal protection, and command-line behavior.



\## Exit Codes



| Exit code | Meaning |

|---|---|

| `0` | Operation completed successfully; all verified files match |

| `1` | Verification found one or more issues |

| `2` | An operational or input error occurred |



\## Security Considerations



\- SHA-256 is used to detect changes relative to a previously generated manifest.

\- Manifest entries are validated before verification.

\- Paths are checked to prevent access outside the designated evidence directory.

\- Evidence files are read for hashing and are not automatically modified by the tool.

\- The sample evidence is synthetic and intended for testing.



For meaningful verification, protect the manifest against unauthorized modification and preserve it through an appropriate evidence-handling process.



\## Limitations



This tool does not independently establish who created or modified a file, prove that evidence is authentic, or provide a complete chain-of-custody system. Its results depend on the integrity and trustworthiness of the manifest used for comparison.



\## Technologies



\- Python

\- SHA-256

\- JSON

\- argparse

\- pytest

\- Git



\## Disclaimer



This project is intended for educational and defensive digital forensics practice. Use it with files you are authorized to examine.



