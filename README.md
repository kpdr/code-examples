# Code Examples

[![pre-commit-build](https://results.pre-commit.ci/badge/github/smullins7/code-examples/main.svg)](https://results.pre-commit.ci/latest/github/smullins7/code-examples/main)

[![backend tests](https://github.com/smullins7/code-examples/actions/workflows/blog_site_backend.yml/badge.svg)](https://github.com/smullins7/code-examples/actions/)

[![Coverage Status](https://coveralls.io/repos/github/smullins7/code-examples/badge.svg?branch=main)](https://coveralls.io/github/smullins7/code-examples?branch=main)

This repo is a hodge podge of coding examples primarily meant for teaching and mentoring. Nothing is meant to be taken as production level code, but rather examples are kept simple for easier demonstration and learning.

My skill set is definitely not UI so any frontend code in here will be very rough!

<p>
  <img width="450" height="300" src="https://media.giphy.com/media/3orieS4jfHJaKwkeli/giphy.gif" alt="simpsons example">
</p>

## Prerequisite

This repo uses [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks) for linting rules. It doesn't have great monorepo support so you'll want to just install it from this directory, then:

```shell
pre-commit install
```

With that done, any commits to any project within this repo will run the linter hooks before commiting.

## Blog Site

[blog-site](./blog-site/README.md) is a simple blogging site, with posts and comments.

### Frontend

The UI component of the blog site.

### Backend

The data as a service backend of the blog site.

![Python](https://img.shields.io/badge/python-3.8-blue.svg)
