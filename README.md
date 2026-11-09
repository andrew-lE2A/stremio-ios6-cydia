# Stremio iOS 6 Cydia source

Static APT repository for the Stremio 6 jailbreak app. It currently publishes version **1.0.21** for `iphoneos-arm` (iOS 6+, armv7).

## Add to Cydia

Add this source in Cydia under **Manage → Sources → Edit → Add**:

`https://andrew-lE2A.github.io/stremio-ios6-cydia/`

The package installs Stremio6.app under `/Applications`, needed for its jailbreak-enabled VideoToolbox path. It targets jailbroken armv7 devices. MKV playback depends on the stream codec/profile and device decoder; not every stream or device has been validated.

## Updating

Copy a new versioned `.deb` into `debs/`, run `python3 build-repo.py`, then commit and push the package and regenerated `Packages`, `Packages.gz`, and `Release` files. Enable GitHub Pages on the `main` branch root.
