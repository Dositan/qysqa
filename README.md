<div align="center">
    <h1>Qysqa - shorten your URL</h1>
    <p>~ A simple URL-shortening website.</p>
    <br/>
    <strong>how do you pronounce it tho?</strong>
    <p>- It's "qısqa", which means "short" in Kazakh</p>
</div>

![Site demo](app/static/demo.png)

### Why to use?
**Simplicity.** Qysqa is really easy to use and it's completely free!

---

### Run locally
**NOTE**: We assume that you have PostgreSQL set and running.

Clone the repository:

    $ git clone https://github.com/Dositan/qysqa.git

CD into the directory, spawn virtual environment and install dependencies:

    $ cd qysqa
    $ poetry shell
    $ poetry install

Setting configuration:
1. Open [.dist.env](/.dist.env) file.
2. Update for your own purposes (you can ignore *DATABASE_URL*)


Run app with:

    $ flask run

Qysqa also provides simple CLI features:

    $ flask --help
    Usage: flask [OPTIONS] COMMAND [ARGS]...

    ...

    Commands:
    db      Perform database migrations.
    lint    Lint and check code style with black, flake8 and isort.
    routes  Show the routes for the app.
    run     Run a development server.
    shell   Run a shell in the app context.
