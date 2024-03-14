# PII De-Identification with Presidio

This script provides inference capabilities for anonymizing sensitive information in text reports, most of the code borrowed from the [Presidio demo](https://huggingface.co/spaces/presidio/presidio_demo).

Requires `StanfordAIMI/stanford-deidentifier-base` model weights:

```shell
user@machine:~$ git lfs clone https://huggingface.co/StanfordAIMI/stanford-deidentifier-base
```

### Run Anonymization
```
usage: anonymize_reports.py [-h] [--st_model ST_MODEL] [--st_model_package ST_MODEL_PACKAGE] 
                            [--st_ta_key ST_TA_KEY] [--st_ta_endpoint ST_TA_ENDPOINT] 
                            [--report_file REPORT_FILE] [--save_file SAVE_FILE]
                            [--data_column DATA_COLUMN] [--append APPEND]

Data Anonymization Script

optional arguments:
  -h, --help            show this help message and exit
  --st_model ST_MODEL   Model path for NER
  --st_model_package ST_MODEL_PACKAGE
                        Model package for NER
  --st_ta_key ST_TA_KEY
                        Text Analytics key (if using Azure)
  --st_ta_endpoint ST_TA_ENDPOINT
                        Text Analytics endpoint (if using Azure)
  --report_file REPORT_FILE
                        Path to the input report file
  --save_file SAVE_FILE
                        Path to save the anonymized report
  --data_column DATA_COLUMN
                        Column name of the reports in csv
  --append APPEND       Append anonymized report to input csv
```

### Requirements
```
Python 3.9.x
```

### Packages
```
azure==4.0.0
flair
pandas
presidio_analyzer
presidio_analyzer[stanza]
presidio_analyzer[transformers]
presidio_anonymizer
python-dotenv
spacy>=3.0.0,<4.0.0
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
tqdm
```

### Sources
```
- https://huggingface.co/StanfordAIMI/stanford-deidentifier-base
- https://huggingface.co/spaces/presidio/presidio_demo
- https://microsoft.github.io/presidio/
```