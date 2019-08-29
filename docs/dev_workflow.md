## Virtualenv

Activate virtualenv `workon dev`.  
To run Developement server `python3 flask_app/main.py`

## Documentation

Mkdoc used to generate the wiki. Markdown files are stored in folder *doc/*.  Published to [https://chaudiere-wiki.readthedocs.io](https://chaudiere-wiki.readthedocs.io). Pushing repository to github will trigger ReadTheDocs build.


Can be updated on the web and pushed to github from [https://stackedit.io](https://stackedit.io).  
!!! warning ""
    Don't forget to `git pull` the local repository after editing online.


To test documentation on local server, run `mkdocs serve --dev-addr 0.0.0.0:8001`.  

Configuration file `mkdoc.yml`:
``` yaml
site_name: Chaudiere
theme: readthedocs
repo_url: https://github.com/cheperboy/chaudiere/
docs_dir: docs/ 
nav:
    - Home: index.md
    - Install Raspbian: install_raspbian.md
    - Install Chaudiere: install_chaudiere.md
    - Software: software.md
    - Doc workflow: doc.md
```

### Usefule extensions

- [pymdown](https://squidfunk.github.io/mkdocs-material/extensions/pymdown/)
- [mermaid plugin](https://github.com/pugong/mkdocs-mermaid-plugin)
- [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/)

