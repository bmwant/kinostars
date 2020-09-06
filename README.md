## Guess a star

Using access to [Kinopoisk](https://www.kinopoisk.ru/) to create a simple guess-game.


### Development

```bash
$ pyenv virtualenv 3.8.1 kinostars
$ pyenv activate
$ pip install -r requirements.txt
```

Create file with credentials

```bash
$ cp creds.yml.example creds.yml
```

### Populate database

```bash
$ brew cask install phantomjs
$ python grab.py
```