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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)