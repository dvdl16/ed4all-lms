## Ed4All LMS

<!-- badges here -->

Country Specific Functionality for South Africa

This is a Frappe app, intended to be used with ERPNext (version 15).

#### License

Dirk van der Laarse

### Features


### Project documentation

User documentation is hosted using Github Pages: [Ed4All LMS Project Documentation](https://ed4all-lms.laarse.co.za/)

### Development

TBD

#### Tests

TBD

#### Contributing

We use [pre-commit](https://pre-commit.com/) for linting. First time setup may be required:
```shell
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

#(optional) Run against all the files
pre-commit run --all-files
```


The Project documentation has been generated using [mdBook](https://rust-lang.github.io/mdBook/guide/creating.html)

Make sure you have [mdbook](https://rust-lang.github.io/mdBook/guide/installation.html) installed/downloaded. To modify and test locally:
```shell
cd docs
mdbook serve --open
```