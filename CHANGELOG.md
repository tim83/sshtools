# Changelog

<!--next-version-placeholder-->

## v4.5.1 (2022-02-25)
### Fix
* **device.py:** Allow creating a device based on the hostname instead of the name ([`8681ed0`](https://github.com/tim83/sshtools/commit/8681ed00ce5d9d13243900bfe62367f91e7233bc))

## v4.5.0 (2022-02-24)
### Feature
* **device.py:** Allow creating a device based on the hostname instead of the name ([`260fc84`](https://github.com/tim83/sshtools/commit/260fc84efc32596c7d035d3d57cb3da2c04910a3))

## v4.4.0 (2022-02-24)
### Feature
* **device.py:** Add a method fo checking if a device can be a relay ([`ef6e76c`](https://github.com/tim83/sshtools/commit/ef6e76ce77ff292c078b3140f882ab5b3da88578))

### Fix
* **pathfinder.py:** Don't use the hostname for connecting to a relay to prevent Device-Not-Found errors ([`91bb62c`](https://github.com/tim83/sshtools/commit/91bb62c17a5490c5d242889f16fdafc73ba25ec8))

## v4.3.2 (2022-02-24)
### Performance
* **device.py:** Improve logging by providing a __str__ method for device ([`8220070`](https://github.com/tim83/sshtools/commit/8220070790d78a73bca84b6dd71280e4b8cc76da))

## v4.3.1 (2022-02-21)
### Fix
* **pathfinder.py:** Fix selecting target as relay ([`dec6b3e`](https://github.com/tim83/sshtools/commit/dec6b3ec4e87a57380afb7e73691def1f404dc9a))

## v4.3.0 (2022-02-20)
### Feature
* **device.py:** Change property-like functions to properties ([`f93e449`](https://github.com/tim83/sshtools/commit/f93e44922fe82ff1b4061b3d26bbf604f0a0446f))

### Fix
* **device.py:** Disable caching ([`2cc6ef2`](https://github.com/tim83/sshtools/commit/2cc6ef257df09544fcf42096be2b0a65ec94b355))
* **config:** Non-main limited sync for laptop-oma ([`6234f0b`](https://github.com/tim83/sshtools/commit/6234f0b7ebe1c34dcc2db602403c56052f0c8b94))
* **config:** Oma -> greta ([`93ff57f`](https://github.com/tim83/sshtools/commit/93ff57f0984fbc4d0ef9e7ef0ff935a8f9dab5ce))
* **sshin.py:** Clean up user messages and variable names & improve docstrings ([`2651b27`](https://github.com/tim83/sshtools/commit/2651b271e3064bce634cd5ea10d1a0a33032c106))
* **ssync.py:** Clean up user messages and variable names & improve docstrings ([`ede3ea7`](https://github.com/tim83/sshtools/commit/ede3ea793add46317deb6c37e480756aa8e50937))
* **smount.py:** Improve docstrings ([`6e42dde`](https://github.com/tim83/sshtools/commit/6e42dde805001fcf5e56421ffb985d5c0263a399))
* **ssync.py:** Improve docstrings ([`761d196`](https://github.com/tim83/sshtools/commit/761d19686f200222e5ae6c688587f645f7ec8257))
* **wake.py:** Improve docstrings ([`34f4ddd`](https://github.com/tim83/sshtools/commit/34f4ddd9470e0babc89b9b57d840016b6edca9aa))
* **wake.py:** Clean up user messages and variable names ([`945c28f`](https://github.com/tim83/sshtools/commit/945c28f92b603d26dcb5a9eeef17a5f56393f07f))
* **smount.py:** Clean up user messages and variable names ([`fd42275`](https://github.com/tim83/sshtools/commit/fd422758ff7e0606b3a10b2e21b501ac8a6753d0))

## v4.2.1 (2022-02-19)
### Performance
* **ssync.py:** Reuse cache finder from timtools ([`09fda45`](https://github.com/tim83/sshtools/commit/09fda454f7fb4d7610ccf66de8e0df56e738b52b))

## v4.2.0 (2022-02-19)
### Feature
* **device.py:** Use the sshable check ([`4e6af59`](https://github.com/tim83/sshtools/commit/4e6af597a84e25988813e930ee325f4c6ccd6bdf))
* **device.py:** Add a check to make sure SSH is configured correctly ([`3df00e3`](https://github.com/tim83/sshtools/commit/3df00e39c5a9d0976f799568055f1c4a6d45001a))

### Fix
* **ssync.py:** Use better error message ([`759e7ca`](https://github.com/tim83/sshtools/commit/759e7ca191ed47e5a7501f4e15ab9da5a3a29b1e))
* **ssync.py:** Prevent disappeared device from terminating sync for all devices ([`c351c3e`](https://github.com/tim83/sshtools/commit/c351c3e31d4a61ce10ea87ce8e9e640bab5dddeb))

### Performance
* **ci.yml:** Remove unneeded steps ([`4def86b`](https://github.com/tim83/sshtools/commit/4def86b19039fa4c5d177ce0a8e414196404e9cb))

## v4.1.2 (2022-02-18)
### Fix
* **ip.py:** Fix typo ([`8f2eea7`](https://github.com/tim83/sshtools/commit/8f2eea73ee99c4833b46d4931c7f716fef20a90d))

## v4.1.1 (2022-02-18)
### Fix
* Set correct CI versions ([`117432d`](https://github.com/tim83/sshtools/commit/117432dc5baeb3a63fc27c814d616373cfd85d55))

## v4.0.3 (2022-02-18)
### Fix
* Set correct CI versions ([`117432d`](https://github.com/tim83/sshtools/commit/117432dc5baeb3a63fc27c814d616373cfd85d55))
