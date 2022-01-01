from qysqa import config, create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=config["debug"], port=8000)
