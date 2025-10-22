> [!CAUTION]
> This repository is for viewing only. Do not work on the assignment using this repository -- the actual course assignments will be provided to you via Pawtograder.

# Homework 4

## Learning Outcomes

- Reading API documentation
- Parsing JSON data
- Visualizing data
- Sorting and filtering Pandas dataframes
- Privacy implications of pushing passwords to GitHub

## Overview

### News API

This assignment will use the News API (https://newsapi.org/docs), which provides users with data about news from around the internet.

Please go to the website and generate a free key (using a fake name and your university email address, if you don't want to share your info with them) here: https://newsapi.org/register

Store that key somewhere safe. Treat it like a password.

You'll notice that there is an existing library in Python that does what we are implementing. For full credit on this assignment, do not use that library.

### Setup

Create a `class Article` to store the details of a news article that can be returned by the API.
Objects of this type will represent an article from the response object (https://newsapi.org/docs/endpoints/top-headlines).
It should appropriately store the following as attributes or properties:
- url
- source
- author
- title
- description
- publishedAt
- content

Create a `class SearchNews`:
- The constructor should read your API key from a file, and store it as an attribute
- Add a method `def get_top_headlines(self, date: Optional[str] = None, domain: Optional[str] = None, language: Optional[str] = None, *terms) -> list[Article]:` which pulls from the `/top-headlines` endpoint
- Add a method `def get_everything(self, date: Optional[str] = None, domain: Optional[str] = None, language: Optional[str] = None, *terms) -> list[Article]:` which pulls from the `/everything` endpoint

Important: hide the key. Do not push it to GitHub. (This is why we read the key from the file.)

### Dataframes

The format of the list of Articles returned by the methods in `SearchNews` is hard to read.
Write a `class NewsProcessor`:
- Add a method `to_df` that takes a `list[Article]` and returns it as a Pandas dataframe. Each attribute / property from the `Article` should be a column, and each article should be a row.
  - Add an optional argument `sort_by` to the `to_df` method, which, if passed a `function`, uses that function to sort the rows in the dataframe.
  - Add an optional argument `filter` to the `to_df` method, which, if passed a `function`, uses that function to filter the rows in the dataframe. It should only include rows for which the `function` returns `True`.
- Add a method `plot_word_popularity` which takes a `list[Article]` and a `str` search term as arguments. It should make and display a plot of the frequency of that search term in the articles' titles. The x axis should be the range of dates covered by the articles, and the y axis should be the number of articles published with the search term on that day.

## Ethics and Privacy

Please fill out this table about API keys used in code. (Some parts are already answered for you, and you may look at Lab 1 for help):

| Question | Answer |
| -------- | ------ |
| What type of information is shared? | API key |
| Who is the subject of the information? | The programmer / code that's making API calls |
| Who is the sender of the information? | The programmer |
| Who are the potential recipients of the information? | Intended recipient: the API server<br />Unintended recipient(s): YOUR ANSWER HERE |
| What principles govern the collection and transmission of the information? | YOUR ANSWER HERE |


| Question                                                                   | Answer                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What type of information is shared?                                        | API key                                                                                                                                                                                                                                                                                                          |
| Who is the subject of the information?                                     | The programmer / code that's making API calls                                                                                                                                                                                                                                                                    |
| Who is the sender of the information?                                      | The programmer                                                                                                                                                                                                                                                                                                   |
| Who are the potential recipients of the information?                       | Intended recipient: the API server<br/>Unintended recipient(s): anyone who can view the repo/history (e.g., on GitHub or forks), automated crawlers/secret-harvesting bots, CI/CD logs/services, search engines/archives, mirrors/backups, and services that ingest public code (including some model trainers). |
| What principles govern the collection and transmission of the information? | Data minimization & purpose limitation; least privilege with scope-limited keys; secure transport (TLS); secure storage (env vars/secrets manager); avoid logging secrets; access control & auditing; short lifetimes/rotation & revocation; keep secrets out of source control (.env + .gitignore).             |


You may go back and edit your answers in the table as you answer these questions:
1. As we saw in Lab 5, large language models (LLMs) are trained on large parts of the internet. Are any popular LLMs trained on open source code like GitHub?


Yes. Some popular code models have been trained on publicly available open-source code (e.g., models behind GitHub Copilot like Codex historically; code-focused models such as Code Llama use publicly available code corpora). Details vary by provider and model.

2. If a programmer accidentally pushes their API key to GitHub, who are at least two potential unintended recipients of this data?


Secret-scanning bots and malicious scrapers that monitor GitHub for exposed credentials.

Anyone who clones/forks or views the repo (including future employers, classmates, or automated datasets that ingest public repos).
(Also common leaks: CI logs, issue text, pasted stack traces, package registries.)

3. How might we design our code to minimize the number of unintended recipients of that information? How might we redesign APIs to minimize the number of unintended recipients?


Design code to minimize unintended recipients:

Never hardcode keys. Load from environment variables or a secrets manager; keep .env out of Git.

Don’t print or log keys; scrub stack traces.

Use least-privilege, scope-limited, short-lived tokens; rotate regularly and set revocation.

Put API calls behind a server/proxy so clients never see the key.

Add pre-commit hooks/CI checks (secret scanners) and protect branches.

Redesign APIs to help:

Prefer OAuth/OIDC with short-lived, scoped access tokens (PKCE for public clients).

Support keyless client auth via backend token exchange; proof-of-possession/mTLS; IP allowlists.

Easy, immediate key revocation and granular scopes/rate limits by default.