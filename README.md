A Java applet which integrates with [HoneyBadger](https://github.com/lanmaster53/honeybadger/) to geolocate... things. Note that you must be running a HoneyBadger server, this applet doesn't do anything on its own.


### Getting Started

Before you do anything, configure the applet and HoneyBadger itself in the two sections below. If you're, say, in a class and that's done for you, read on.

To get started, run `serve.sh` to serve the `www` directory, which contains the applet (the build script puts it there if you built it yourself) and also holds `test.html`. If you visit `test.html` in your browser (check the output of `serve.sh` for the full URL), and convince the Java applet to run (which it won't in many modern browsers), then you should get a geolocation sent to your local HoneyBadger instance!


### Configuring the Applet

To configure the applet, look inside `www/test.html` to change the parameters. Specifically, you'll have to set the GUID of an active target in HoneyBadger and the URL of your HoneyBadger instance.


### Configuring HoneyBadger

You'll need a Google Maps API key, which you can get by visiting Google Cloud Platform and enabling the Places API. They have a pretty generous free trial.

Then, visit `/server/honeybadger/__init__.py` in the HoneyBadger repo and set your API key there in the `GOOGLE_API_KEY` variable.


### Building the Applet (Advanced Mode)

A signed applet is included in this repo, so don't follow the instructions in this section unless you've changed the applet code or something.

If you're building the applet yourself, note that the applet must be signed in order for basically any browser to run it. `build.sh` contains a hard-coded path to a keystore that we aren't sharing with you, so it likely won't work off the bat without you having your own keystore and configuring a path to it in `build.sh`.

Once you've got that set up, just run `build.sh` and follow the prompts.


#### Acknowledgements

This project is heavily based on Ethan Robish's [java-web-attack](https://bitbucket.org/ethanr/java-web-attack).
