# tts-relay
An app that relays text-to-speech from the internet to a local speaker via bluetooth.

## What does it do?
You go on the internet and type a message. Within seconds, you hear a semi-human voice speak the same message on your speakers.

## Why did I build this?
Imagine you're texting a roommate who's home, but isn't responding. You really need to get their attention because you need them to clean the apartment since you're bringing a hot date home. You send a message through tts relay, and immediately they get your message loud and clear. Now they're cleaning so that you can bring your hot date home with ease.

Or you can give access to this tool to any of your friends and have them surprise you with any message they want at any time of day! (yay)

## Requirements
Here's the hardware you need to get this to work:

- An always on bluetooth wireless speaker (Like a sonos, alexa, or google home. I tested this on a google home mini)
- A bluetooth-enabled device with linux running on it (I'm using a pi 5)

Before getting started, ensure that your device has `bluez` and `pulseaudio` running. In most cases you can run:

```
sudo apt update
sudo apt install bluez pulseaudio pulseaudio-module-bluetooth
```

Then confirm that the bluetooth service is running with:

```
sudo systemctl enable bluetooth.service
sudo systemctl start bluetooth.service
```

You will also need Python on the device (at least 3.12).

## How it works
A user will access a very lightweight frontend (with a password-like authentication). After they authenticate they can send a message through the website.

These authentication and speech requests are handled by the running [fastapi](https://fastapi.tiangolo.com/) process on the local linux device. When it receives the TTS request, it will queue up the speech on the running app.

The app then attempts to connect to the bluetooth speaker. On success, it generates a temporary wav file with [piper-tts](https://github.com/OHF-Voice/piper1-gpl). Pulseaudio plays this wav file and then it is deleted upon completion.

## Setup

### Bluetooth
You'll have to pair your bluetooth speakers with your device before running the app. You can do this on the cli with `bluetoothctl`. Usually something along the lines of this:

```
bluetoothctl power on
bluetoothctl scan on
# Find the mac address of your bluetooth speaker
bluetoothctl scan off
bluetoothctl pair [mac address]
bluetoothctl trust [mac address]
bluetoothctl connect [mac address]
```

Once you confirm you are connected you should be able to play audio from your device to your speaker with `paplay [sound file]`.

### API
First, run `deploy/deploy.sh` to install the proper virtual environment for this app. You might need to install an additional `venv` package on your device to get this to work.

Then setup an `.env` with `SPEAKER_MAC` and `API_KEY` defined. `SPEAKER_MAC` should be the mac address of the speaker that you connected in the last step. `API_KEY` will be the secret password you'll use to authenticate.

With these defined, now you can test the app. Run the following:

```
source .venv/bin/activate
fastapi dev --host 0.0.0.0 --port 8000
```

Fastapi should automatically detect `main.py`, but if not you can explicitly pass the filepath into the command above. With the test server running, you can send a request to it with:

```
curl http://[device's local ip address]:8000 -X POST -H "Content-type: application/json" -H "x-voice-key: [API_KEY]" -d "{\"speech\": \"Hello there, user\"}"
```

In the command above, insert your device's local ip address and the api key defined in `.env`. `x-voice-key` is the header used to authenticate the requests on the api. If everything is working well, then you should have heard a message come through on your speakers!

### Deployment
The full deployment of this can be a bit involved if you want the full experience. Here's how I've deployed this app. I have a public subdomain that I point to my home's router ip address with DDNS. I've forwarded the proper ports through my router to get to my pi 5. I'm serving the webpage in `content/` in the subdomain through nginx while the api is running on a systemd service.

This is just one flavor of how you can deploy this app. You can also keep it entirely local within your network (with its own domain too if you run your own DNS). The webpage in `content/` is very bare bones, but it does the job. Feel free to use that or don't.

You'll also notice that `deploy.sh` is very bare bones. That's there to get you started in case you want to automate the deployment of this app onto your device.

Here are a few important considerations when deploying this app:

- When creating a service file for systemd, ensure that the `USER` and `GROUP` are defined as your user. You also have to set the `Environment=XDG_RUNTIME_DIR=/run/user/1000` for pulseaudio to work correctly.
- You'll need to run `sudo loginctl enable-linger [username]` so that the process can continue running in the background properly while you are not logged into the machine.
- In `content/config.js`, you'll need to change `apiUrl` based on how you're going to deploy the app. If it's local, you'll need to point it to the local ip address, if it's public, then point it to the domain or ip address directly.
- If you're deploying this publicly through your home router, you might want to create a proxy to your api with nginx so you don't expose a bunch of ports to the internet. You'll likely want to append `/api/` to your domain and then prefix the api route names with that on the fastapi app.

### Other Considerations
The voices in `voices/` are just a few samples of what is available. You can add or remove any that you want. The easiest way to do it is by downloading more from [here](https://huggingface.co/rhasspy/piper-voices/tree/main).

---

That's it! This is my first public repo/app. It's kind of silly, but fun overall. Hope you have the same experience. [You can find more about me here!](https://polkel.dev)