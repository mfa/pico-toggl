## Use Raspberry PI Pico for Timetracking

Blogpost: https://madflex.de/use-pico-track-time

### Setup

Copy .secrets.template to .secrets and fill in your configuration from <https://toggl.com>.

Set the ip-address of the Flask instance before uploading the pico/main.py to the Pico.

Install the requirements:
```
pip install -r requirements.txt
```

### Running the Flask server
```
flask --app app.main run
```
