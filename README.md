# Home

Home is the API that provides information to the Home system. its coverage gos from the 
library to the finance application and all of its submodules.


## Installation for development

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

```bash
pip install -r requirements.txt
```

## Database configuration

Some requirements are mandatory in database before running the first migrate.
- Create the following schemas:
    - finance
    - library
    - log
    - security

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Used APIs
For finances many APIs are used, but primarily it is used the [Portal de Dados Abertos do Banco Central do Brasil](https://dadosabertos.bcb.gov.br/).

The API uses values from [SGS - Sistema Gerenciador de Séries Temporais](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries) as references to params.

## License

[MIT](https://choosealicense.com/licenses/mit/)