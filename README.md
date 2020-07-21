# Wiki

In this Django-based wiki app, users are able to view, create, and edit pages in markdown rather than in html.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

## Usage

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: manage.py runserver
```

## Screenshots

![Wiki Home Page](https://i.imgur.com/htnmWue.png)

![Wiki HTML Page](https://i.imgur.com/Du9lpnm.png)

![Wiki HTML Edit Page](https://i.imgur.com/JystzRI.png)

## Credit

[HarvardX: CS50's Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)

## License

Wiki is licensed under the [MIT license](https://github.com/danrneal/wiki/blob/master/LICENSE).
