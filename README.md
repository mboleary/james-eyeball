# james-eyeball
James's Eyeball

## Usage

### Client

Usage notes for the client are at the top of the `bin/client` file. Invoke by
running `./start_client.sh`. You will need to have had the `.env` file shared with
you via another channel.

### Server

Invoke with `./start_server.sh` The `.env` file will need to be shared
between server operators and users via another channel.

## Video Scripts

For the time being this works with Firefox, but not chromium-based browsers.

In order to get the camera to behave like a webcam, we need to make use of
ffmpeg, and a kernel module to convert the rtsp stream using
[v4l2loopback](https://github.com/umlaeute/v4l2loopback) into a virtual webcam.

In order for this to work, you must have the v4l2-loopback dmks module
installed. On ubuntu, this is the package that will need to be installed:

```
v4l2loopback-dkms/focal-updates,focal-updates 0.12.3-1ubuntu0.3 all
  Source for the v4l2loopback driver (DKMS)
```

After installing this package, or if you run into an error like `Could not
write header for output file #0`, make sure that you run

```
sh
sudo modprobe v4l2loopback
```

After that, run `./start_video.sh` to start the ffmpeg video stream.

## Misc.

The `zzz_from_charles` directory contains the original TCP version of this
application. The `zzz_network_test` directory contains 2 files for an end-to-end
network test.
