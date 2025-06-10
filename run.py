from domashkola import create_app


application = create_app()


if __name__ == '__main__':
    with application.app_context():
        application.run(debug=True)
