# Stremio iOS 6 Cydia source

Static APT repository for the Stremio 6 jailbreak app. The repository currently publishes version **1.0.30** for `iphoneos-arm` (iOS 6+, armv7).

## Add to Cydia

Once this repository is published with GitHub Pages enabled, add its Pages URL in Cydia under **Manage → Sources → Edit → Add**. The URL will be:

`https://andrew-lE2A.github.io/stremio-ios6-cydia/`

The package installs Stremio6.app under `/Applications`, which is required for the jailbreak-enabled VideoToolbox playback path. It is intended for jailbroken armv7 devices. The app's MKV playback still depends on the video codec/profile and the device's hardware decoder; iPad 2 playback has not been validated for every stream.

## Updating the repository

1. Copy a new `Stremio6-vX.Y.Z.deb` into `debs/`.
2. Run `python3 build-repo.py` from this directory. It selects the highest semantic version, generates `Packages`, `Packages.gz`, and `Release`, and includes package checksums.
3. Commit and push the changed files. GitHub Pages should serve the repository from the `main` branch root.

Only the current highest package is listed in `Packages`; older package files can remain in `debs/` as archived downloads.
