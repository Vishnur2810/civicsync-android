# CivicSync for Android

Android app for [CivicSync](https://vishnur2810.github.io/civicsync/), a civic-issue platform for Chennai:
report a problem with a geotagged photo, see which department handles it and when it should be fixed,
track it, and confirm the fix.

## Download

**[Download CivicSync.apk](https://github.com/Vishnur2810/civicsync-android/releases/latest/download/CivicSync.apk)** (Android 7.0 or newer)

1. Open the link on your Android phone and download the file.
2. Open it. If Android asks, allow your browser to **install unknown apps**, then tap **Install**.
3. Open CivicSync and paste the server address.

## Connecting

The app is a client for a CivicSync server running on a laptop. On the laptop, start **CivicSync (Public link)**
and copy the `https://….trycloudflare.com` address it prints into the app. A phone on the same Wi-Fi can also use
the laptop's address, such as `192.168.1.20:8000` (the camera and GPS need the https public link).

The public address changes each time the laptop starts the public link, so paste the new one when asked.
The app remembers recent servers and reconnects to the last one automatically.

## How it is built

- [Capacitor](https://capacitorjs.com/) Android shell. `www/index.html` is the connect screen; after connecting,
  the app shows the CivicSync site with access to the phone's camera and location for geotagged reports.
- `resources/make_icons.py` draws the app icon and splash screen.
- `.github/workflows/build.yml` builds the APK on every push to `main` and publishes it under Releases.
