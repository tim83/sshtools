# Changelog

<!--next-version-placeholder-->

## v4.26.0 (2022-12-06)
### Feature
* **interface.py:** Only use sudo when user is not root ([`5922101`](https://github.com/tim83/sshtools/commit/5922101bcc08707a4ee7ef0fa31ea5f163d8b98c))

## v4.25.3 (2022-11-08)
### Fix
* **device.py:** Try numero dos ([`76909ea`](https://github.com/tim83/sshtools/commit/76909ea07a9daa7c88bc105bf051d28028de7819))

## v4.25.2 (2022-11-08)
### Fix
* **device.py:** Remove debug code ([`6766ff6`](https://github.com/tim83/sshtools/commit/6766ff633a8a70e055a44a293f227be1eb2c207c))

## v4.25.1 (2022-11-08)
### Fix
* **device.py:** Allow containers to always check for networks the host is present on, even when the IP can't be checked ([`affb07e`](https://github.com/tim83/sshtools/commit/affb07e7e4e84efdfb39cb052b5fa5da62034d97))

## v4.25.0 (2022-11-08)
### Feature
* **device.py:** Add functionality for detecting container hosts ([`2eea987`](https://github.com/tim83/sshtools/commit/2eea987b15962ab5945841459333814fd5ad0c29))

## v4.24.1 (2022-10-31)
### Fix
* **device.py:** Add better documentation & fix linelength ([`3d75bbb`](https://github.com/tim83/sshtools/commit/3d75bbbb8a2128eb1b45947c756ec2a291f0b33e))
* **device.py:** Prepare for the sunsetting of the *.beta.tailscale.net addresses ([`921f008`](https://github.com/tim83/sshtools/commit/921f00845c65514a8cb85649d4a352a8d11cf2be))

## v4.24.0 (2022-10-26)
### Feature
* **tools.py:** Enable global config dir ([`0e874fb`](https://github.com/tim83/sshtools/commit/0e874fb71ae2c69ab2cc7b16874415ba9dceebd3))

## v4.23.0 (2022-08-26)
### Feature
* **ip.py:** Prioritise IPs that can be reached with mosh ([`b35885f`](https://github.com/tim83/sshtools/commit/b35885faa1426dfedf0d4142a062d4b317d4eb4b))

### Fix
* **ip.py:** Allow ip config to be None ([`196f7d7`](https://github.com/tim83/sshtools/commit/196f7d7c5b4d5f2d6d78c91183d82efea01fb00c))

## v4.22.0 (2022-08-17)
### Feature
* **device.py:** Return False for Device.is_local when NotReachable Tim Mees 21 minutes ago - Use correct format ([`103f1df`](https://github.com/tim83/sshtools/commit/103f1df4377fa9410cd3a0c5767aee30d6355ee9))

## v4.21.0 (2022-06-29)
### Feature
* **device.py:** Enable limiting possible ips to only those defined in the config ([`f9462db`](https://github.com/tim83/sshtools/commit/f9462dbde7241014ad68e82e9150aece7887e5e4))

## v4.20.0 (2022-06-12)
### Feature
* Remove moshable functions and checks ([`dab1766`](https://github.com/tim83/sshtools/commit/dab1766185a66eb2c96c6d852319fd30bbbaa889))

## v4.19.1 (2022-06-12)
### Fix
* **sshin.py:** Actually call the moshable check ([`b8de6f5`](https://github.com/tim83/sshtools/commit/b8de6f5687ee9c3e2a35f479125be210739dba27))
* **ssinfo.py:** Don't check for moshability to prevent newline problems ([`8f94787`](https://github.com/tim83/sshtools/commit/8f9478777ab050a2dcec11f362fa65be3b8ef82b))
* **getip.py:** Remove useless fix ([`7097563`](https://github.com/tim83/sshtools/commit/7097563dd76fe834f880305032491c1c04724d7c))
* **ip_address.py:** Use the timeout on the correct function call ([`7d5f8af`](https://github.com/tim83/sshtools/commit/7d5f8af26d90ac4ed5cf3c4cfbd954ce817c5fbc))

## v4.19.0 (2022-06-12)
### Feature
* **getip.py:** Reenable json output ([`0902155`](https://github.com/tim83/sshtools/commit/0902155ab2b8c1fa8a8b13d92f2dedff069bee76))

## v4.18.1 (2022-06-12)
### Fix
* **tools.py:** Increase the SSH timeout to correspond to the value in the ssh command ([`d34876d`](https://github.com/tim83/sshtools/commit/d34876df83574918e856344a0e7328e1ce5e9f2c))

## v4.18.0 (2022-06-12)
### Feature
* **ip_address.py:** Set a timeout for ssh and mosh check ([`137d554`](https://github.com/tim83/sshtools/commit/137d55481448f8639d4c4e547d67c802f84867a9))

### Fix
* **getip.py:** Use better variable names ([`609d70e`](https://github.com/tim83/sshtools/commit/609d70e50ecb55f23ca13de3dbfb3312100369b8))

## v4.17.0 (2022-06-12)
### Feature
* **ssinfo.py:** Implement a function to lookup data about devices ([`2d3a259`](https://github.com/tim83/sshtools/commit/2d3a2598ca35a891e96e408f434eb58eeb4731a5))

### Fix
* **device.py:** Look for the tailscale magic dns ([`430cd3b`](https://github.com/tim83/sshtools/commit/430cd3b1c9e5c70e21afcfd59f536fae3033972f))

## v4.16.0 (2022-06-12)
### Feature
* **device.py:** Check tailscale magic dns ([`b895a31`](https://github.com/tim83/sshtools/commit/b895a31d23c75e5a506146c78b5504d6a8de82be))

### Fix
* **ip.py:** Increase priority of mDNS ([`6838364`](https://github.com/tim83/sshtools/commit/683836409316de0084ac4b3cd72c650c991cf8b1))

## v4.15.1 (2022-06-11)
### Fix
* **ssync.py:** Only sync to sshable devices ([`f2c2740`](https://github.com/tim83/sshtools/commit/f2c2740afa0cafeea2caf570fd1776b1b5bc674e))

## v4.15.0 (2022-06-10)
### Feature
* **ip.py:** Give hostnames a headstart ([`3f37550`](https://github.com/tim83/sshtools/commit/3f37550f3da7e25c3ca442d518b3d34b2a6ff15d))

## v4.14.0 (2022-06-10)
### Feature
* **ip.py:** Use latency to sort IPs instead of hardcoding ([`1c5bba9`](https://github.com/tim83/sshtools/commit/1c5bba93bf7aadbedd825fe6466d04d37c3db2e3))

## v4.13.1 (2022-06-01)
### Fix
* **sshin.py:** Fix relay command execution ([`10aaf1f`](https://github.com/tim83/sshtools/commit/10aaf1fe166f1384b14188ba0a7b8777343868d5))

## v4.13.0 (2022-04-25)
### Feature
* **sshin.py:** Check if a device is moshable before moshing ([`19d72e5`](https://github.com/tim83/sshtools/commit/19d72e521100b86c7440e26e1cc1e16632d3ffae))

## v4.12.0 (2022-04-25)
### Feature
* **forget.py:** Re-add device after deletion ([`3e95af0`](https://github.com/tim83/sshtools/commit/3e95af02085c9cdb37f4289d47bcd0a5db0185c5))

## v4.11.1 (2022-04-23)
### Fix
* **ip_address.py:** Fix sshable and moshable checks ([`98f11d8`](https://github.com/tim83/sshtools/commit/98f11d82071e169b124a5d7addb52c45de4c5d5b))

## v4.11.0 (2022-04-23)
### Feature
* **ip.py:** Allow filtering based on mosh-ability ([`4aab7d9`](https://github.com/tim83/sshtools/commit/4aab7d901ffba2ea34707c795a44d8949d0d75aa))

### Fix
* **ip_address.py:** Use batchmode for MOSH ([`3790379`](https://github.com/tim83/sshtools/commit/37903796e2aa9778e4ba469d64233f5d0924ffbc))
* **ip.py:** Don't filter moshable by default ([`81f5956`](https://github.com/tim83/sshtools/commit/81f59561787234868d4d36a7353070ae964ac3d2))
* **ip.py:** Take into account whether mosh is installed ([`a37729b`](https://github.com/tim83/sshtools/commit/a37729b76c627b13054ed37a20ad6672b6552577))

## v4.10.1 (2022-04-21)
### Fix
* **ip.py:** Fix check_online config check ([`523c064`](https://github.com/tim83/sshtools/commit/523c0644ce6d4cbcf9cc3ea06e5ba60ae9f6238b))

## v4.10.0 (2022-04-21)
### Feature
* **sshin.py:** Limit logging ([`61094bd`](https://github.com/tim83/sshtools/commit/61094bd0c4f280e5d9b6d5cf12903d064670e0f2))
* **ip.py:** Allow filtering based on sshability instead of just pingability ([`a5423e0`](https://github.com/tim83/sshtools/commit/a5423e0e3ca162986ec36b1db13036290a034662))

### Fix
* **test_ip.py:** Disable ip check thanks to github ([`03ae4e3`](https://github.com/tim83/sshtools/commit/03ae4e3cbaa072a7d3064e9df430977202ed1287))
* **test_ip.py:** Change test IP ([`78a238f`](https://github.com/tim83/sshtools/commit/78a238f8177e805994dcf42bd03ce6ef8084eca3))
* **test_ip.py:** Fix typo ([`1832c31`](https://github.com/tim83/sshtools/commit/1832c319b17e9438269fd5a3126adb0634c4f6e5))

## v4.9.4 (2022-04-19)
### Fix
* **sshin.py:** Remove unnescesairy prints ([`443a3a4`](https://github.com/tim83/sshtools/commit/443a3a4501fa5b9f3893cf338f76925a7ec9afaf))

## v4.9.3 (2022-04-18)
### Fix
* **ssync.py:** Actually stop sync for non-online device ([`17b9561`](https://github.com/tim83/sshtools/commit/17b9561a61979b1d7015aea06d4c93a2651a5fa7))

## v4.9.2 (2022-04-14)
### Fix
* **ssync.py:** Use correct method for checking presence. ([`0e49215`](https://github.com/tim83/sshtools/commit/0e49215a283668b229920006b79186decce6883e))

## v4.9.1 (2022-04-14)
### Fix
* **ssync.py:** Improve logging ([`6b957a0`](https://github.com/tim83/sshtools/commit/6b957a0524681bf39efe9ea6fcc9286b08acee28))

## v4.9.0 (2022-04-06)
### Feature
* **interface.py:** Add check for wol vs wakeonlan executable ([`49285a7`](https://github.com/tim83/sshtools/commit/49285a756f76cbc4385e67caceeca51b5c66ca23))

## v4.8.1 (2022-04-06)
### Fix
* **sshin.py:** Don't use mosh when it is not wanted ([`82ee471`](https://github.com/tim83/sshtools/commit/82ee471118569d2229745ef705d34cccd87a4252))

## v4.8.0 (2022-04-05)
### Feature
* **getip.py:** Allow JSON output ([`d3e398a`](https://github.com/tim83/sshtools/commit/d3e398a6b6d2103a40cdc8603c4a45d2f39d9b68))

## v4.7.1 (2022-03-22)
### Fix
* **sshin.py:** Improve mosh selection ([`8231f8a`](https://github.com/tim83/sshtools/commit/8231f8ad9ad70d161025f9b299a3bb88fb4e557f))

## v4.7.0 (2022-03-17)
### Feature
* Use pylint ([`a779769`](https://github.com/tim83/sshtools/commit/a77976961936b5e76a4372e6bae084dd0a0b73bd))

## v4.6.0 (2022-03-17)
### Feature
* **device.py:** Return the hostname instead of localhost for self device ([`a426faa`](https://github.com/tim83/sshtools/commit/a426faa57234ef8f5c7d6d261a9b00a998d6ec5a))

### Fix
* **pathfinder.py:** Fix not storing the correct path ([`cca39ff`](https://github.com/tim83/sshtools/commit/cca39ff7787086995082f5094c8641356cd42b12))

## v4.5.4 (2022-03-16)
### Performance
* **pathfinder.py:** Use multiprocessing for checking alive paths ([`befa103`](https://github.com/tim83/sshtools/commit/befa1037188e2db5dbf8a780dd72cbcf84137e19))

## v4.5.3 (2022-03-01)
### Fix
* **__init__.py:** Fix timtools import ([`e591038`](https://github.com/tim83/sshtools/commit/e591038d986aa12036438bac4e0cd03c9f09bfd5))

## v4.5.2 (2022-03-01)
### Fix
* **device.py:** Specify that .is_local does not include VPNs ([`7dad382`](https://github.com/tim83/sshtools/commit/7dad382f01b463ad71f18875f3155c763c876356))

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
