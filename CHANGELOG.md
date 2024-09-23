# CHANGELOG

## v4.30.2 (2024-09-23)

### Fix

* fix: Account for nullable network attribute ([`2db90b6`](https://github.com/tim83/sshtools/commit/2db90b601533a707318af3700d58a44af5ee2519))

* fix(ip_address.py): Always try to connect to public IPs ([`94589d8`](https://github.com/tim83/sshtools/commit/94589d8643df4996d52745af84a3590d4c8f5605))

### Style

* style: Run formatters ([`d7741ab`](https://github.com/tim83/sshtools/commit/d7741ab1d76f1254e5faae5c63270e34280b6821))

### Unknown

* Update depedencies ([`509dc9e`](https://github.com/tim83/sshtools/commit/509dc9e60fc35c97a87176598a8369c418409635))

* update ([`ffa150b`](https://github.com/tim83/sshtools/commit/ffa150b178115149b5ecb996d136c24878c67646))

* Merge branch &#39;master&#39; of https://github.com/tim83/sshtools ([`97c0365`](https://github.com/tim83/sshtools/commit/97c0365bfbb825fa5f984a48a87dedbb7f04b90a))

## v4.30.1 (2023-06-25)

### Fix

* fix(tools.py): Increase timeouts to prevent faulty errors ([`f206e19`](https://github.com/tim83/sshtools/commit/f206e19461f7114ed6f30ce8388be72050bb5091))

### Unknown

* update ([`586e3e4`](https://github.com/tim83/sshtools/commit/586e3e44cb70df2604a9a95ebdad093042d418ba))

## v4.30.0 (2023-06-04)

### Unknown

* Update ([`0ab1ce7`](https://github.com/tim83/sshtools/commit/0ab1ce71ff2c3061ebbb357971d3c817e1b7e5ad))

* update ([`a24fead`](https://github.com/tim83/sshtools/commit/a24feadacd52277c649e7ff35f432abd658064d5))

## v4.29.0 (2023-04-13)

### Ci

* ci: Prepare for uploading to gitea ([`c48430d`](https://github.com/tim83/sshtools/commit/c48430de8df9f993dde0631192c33f098de794b4))

* ci(.pre-commit-config.yaml): Remove isort (included in ruff) ([`5bc474b`](https://github.com/tim83/sshtools/commit/5bc474b2dcccf7a02d045faf7b8329cdac7b93cf))

### Feature

* feat(wake.py): Add a check to ensure the mac is defined, before waking to prevent triggering errors ([`e66ed27`](https://github.com/tim83/sshtools/commit/e66ed27e1dd02ea64ed3d367610d4df1551d8ccb))

* feat(interface.py): Add a check to ensure the mac is defined ([`ce08492`](https://github.com/tim83/sshtools/commit/ce08492a0fee4198f834904af652973fa10adaba))

* feat(interface.py): Add checks to ensure the used executable is present ([`75bfef7`](https://github.com/tim83/sshtools/commit/75bfef7f5da4cf4311c4db49319993b6d7d95f46))

### Unknown

* Add coverage ([`c27effe`](https://github.com/tim83/sshtools/commit/c27effef36abe0b1b3460659cda5d3ff42a3b8a5))

* Update deps ([`5a9d699`](https://github.com/tim83/sshtools/commit/5a9d699b20ded51a7cab0a2ef466f1c2d76de9bc))

* refractor: Make code checks happy ([`ced0753`](https://github.com/tim83/sshtools/commit/ced0753ffffb491e5e538bc644116f2d9b632811))

* refractor(setup.py): Remove setup.py

BREAKING CHANGE: Not able to install using setup.py anymore ([`df84178`](https://github.com/tim83/sshtools/commit/df84178d86158aba762f785806c713f8e80ef179))

* Remove flake8 config ([`747cf2b`](https://github.com/tim83/sshtools/commit/747cf2b7080b342e303f346dda7c5d9c0f50b2c4))

* Use the correct ci file to hash ([`c835aca`](https://github.com/tim83/sshtools/commit/c835acacc9403c9112fa15df4d72a619b8551a25))

* Remove pre-commit cache when it is not used ([`00c51f6`](https://github.com/tim83/sshtools/commit/00c51f6823069396f57368c4e9182f5e3a65ab47))

* Fix python install

- Ensure that poetry is installed before setting up python
- Use the latest python version for single-executions
- Use the matrix version for multiple-executions ([`6bb7702`](https://github.com/tim83/sshtools/commit/6bb77027e30f6f9e2ad673a1e3fe02ad1df0de63))

* Use pre-commit for ci/cd

- Add caching for poetry &amp; pre-commit
- Use pre-commit configuration instead of duplicating it in actions ([`570ec8d`](https://github.com/tim83/sshtools/commit/570ec8dcf53370d64fb011f1bf3ea85b35d74cf4))

* Merge branch &#39;master&#39; of https://github.com/tim83/sshtools ([`6fb3f70`](https://github.com/tim83/sshtools/commit/6fb3f70da9074755afc628f5246aab55535d9461))

## v4.28.1 (2023-02-20)

### Fix

* fix(ip.py): Fix priority for ascending sort ([`01bb29e`](https://github.com/tim83/sshtools/commit/01bb29e28e73690def95335ad4b322f3aa85a0a4))

* fix(ip.py): Fix priority for ascending sort ([`586830b`](https://github.com/tim83/sshtools/commit/586830ba1839daa62a1164209bfae38f34bd800f))

* fix(ip.py): Fix priority for ascending sort ([`fae8483`](https://github.com/tim83/sshtools/commit/fae848369eaa4e9737b47410d7c4709477aa4b79))

### Refactor

* refactor(ssync.py): Print the ip of the slave ([`8d2365a`](https://github.com/tim83/sshtools/commit/8d2365aedb555efad9e5b3f046ef18599da32dfd))

### Style

* style(device.py): Rename variable for clarity ([`8e4a4c7`](https://github.com/tim83/sshtools/commit/8e4a4c7b5ef4c086d9dbc05ee677ddc1ffce935b))

### Unknown

* Add RUFF to checks

- Add ruff &amp; remove flake8,isort,safety,bandit
- Improve pre-commit and include ruff
- Fix resulting problems
- Update poetry ([`2bad9db`](https://github.com/tim83/sshtools/commit/2bad9db45dcb63c48f94cb93acccc57467310cac))

* fix release version ([`75a3ced`](https://github.com/tim83/sshtools/commit/75a3ced3a97a8103031c55b09b38a375540f60f1))

* update ([`1c3d933`](https://github.com/tim83/sshtools/commit/1c3d93391f093fa664a1c76d50e06bc57882dfb9))

* update ([`826e6aa`](https://github.com/tim83/sshtools/commit/826e6aa5624d4322bf472507bb0b268071b028da))

* Merge remote-tracking branch &#39;origin/master&#39; ([`911dbe5`](https://github.com/tim83/sshtools/commit/911dbe5a086665ed85ff7a8333e745a9478e9d41))

## v4.28.0 (2023-01-29)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`10c11f6`](https://github.com/tim83/sshtools/commit/10c11f6ac4ca138b0a1585d5fc29910c171c8df3))

## v4.27.0 (2023-01-28)

### Feature

* feat(ip.py): Use IP priority in sorting IP list ([`209848a`](https://github.com/tim83/sshtools/commit/209848aaa0a8e10885fc96564877580057289ae1))

* feat(device.py): Use network priority as IP fallback instead of device ([`085487b`](https://github.com/tim83/sshtools/commit/085487b08c04146ce43452887d692717b1b32344))

* feat(connection.py): Add a priority value for networks ([`c93bc7c`](https://github.com/tim83/sshtools/commit/c93bc7c2469637971ac698fc2a30255d6022c8ff))

### Style

* style: Run reformat on JSON files ([`78ab0d7`](https://github.com/tim83/sshtools/commit/78ab0d791df20657be4a0c7fab999787a6fafdee))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`daad650`](https://github.com/tim83/sshtools/commit/daad650f25ebbcdb0d02a8c38e0f2854c579bff6))

## v4.26.4 (2023-01-15)

### Ci

* ci(.pre-commit-config.yaml): Fix flake8 repo ([`e0a65f9`](https://github.com/tim83/sshtools/commit/e0a65f90b2d08cd0eb198d16d6fdc1b6244fda83))

* ci(ci.yml): Readd cache for matrix job ([`b48ce63`](https://github.com/tim83/sshtools/commit/b48ce630646dd12c29ce12293c49cef780eb748f))

* ci(ci.yml): Set correct python-version ([`a354ce2`](https://github.com/tim83/sshtools/commit/a354ce2df27749c9e500edde0b31657833072ede))

* ci(ci.yml): Remove caching for non-matrix jobs ([`71cddfb`](https://github.com/tim83/sshtools/commit/71cddfb0b5ba53840d818e30bd63c7b8bb54ddcd))

* ci(ci.yml): Don&#39;t include the os in the matrix ([`e9009ea`](https://github.com/tim83/sshtools/commit/e9009ea9cba1fd2c80fcf9f06f0d43e6572ded56))

* ci(ci.yml): Manually install poetry and use cache ([`adeb8e7`](https://github.com/tim83/sshtools/commit/adeb8e7e88ab852a0d0e12ed32dd636dc978c683))

### Documentation

* docs(interface.py): Improve naming of an interface ([`0179c01`](https://github.com/tim83/sshtools/commit/0179c01e44a7bbb1494d1a89c57c7a16c526f1d4))

### Feature

* feat(connection.py): Enable constructing the theoretical IP for a device ([`f5c4f8a`](https://github.com/tim83/sshtools/commit/f5c4f8a1c0916b8cc88d6ce1c09cf5c8d2df35ee))

* feat(connection.py): Enable returning an interface object from a network ([`bc2214e`](https://github.com/tim83/sshtools/commit/bc2214e568b1ab7df1186dfcc65e6cc61275c527))

### Fix

* fix(device.py): Actually include all interfaces in the list

Previously only the interfaces explicitly defined in the device config where included, and not those that where defined in the network config ([`df8486b`](https://github.com/tim83/sshtools/commit/df8486bd92a2a0fd566cbe69e2c5d53a5ea9946a))

* fix(device.py): Actually use the adapters in the config to link network and ip ([`601fb0d`](https://github.com/tim83/sshtools/commit/601fb0df8a1934c46fa47aadb2a033a6d4ce36b7))

* fix(connection.py): Fix cumulative adding of 100 to ip_id ([`9716298`](https://github.com/tim83/sshtools/commit/97162983514b20c46fbebbe246a367cc92b80ca4))

* fix(ssync.py): Fix if then logic to not raise an unnecessarily reraise an error ([`a69d40f`](https://github.com/tim83/sshtools/commit/a69d40fb3a60cc56c0ecf65a2ce2ee134ced2a4e))

### Refactor

* refactor(device.py): Move str -&gt; bool logic to a separate tools function ([`3af0668`](https://github.com/tim83/sshtools/commit/3af0668820bbeaa2c34d86f1a481c6c25ea6347b))

* refactor: Replace network names with more generic ones ([`7a8a3c2`](https://github.com/tim83/sshtools/commit/7a8a3c241cf0b5a8facf111f80dce97ed1fd10ae))

### Style

* style(device.py): Make pylint happy ([`5df4d9d`](https://github.com/tim83/sshtools/commit/5df4d9df10aab4e49d36ea9278ce5f433fbf3bee))

* style(test_connection): Fix typo ([`1396edb`](https://github.com/tim83/sshtools/commit/1396edbd49be02456ee22d8c2f30f3149f6c04a5))

### Test

* test: Add tests for the construction of IPs on the device level ([`a620982`](https://github.com/tim83/sshtools/commit/a62098254336e1111791f088ed0117074ff9733e))

* test: Add tests for constructing the ip ([`6369868`](https://github.com/tim83/sshtools/commit/63698682ec2204c9a2406eca56735ca626f93b14))

* test: Add tests for interface method ([`99e943d`](https://github.com/tim83/sshtools/commit/99e943de1b1ae4f2d220ed0efa657161ed72a98a))

### Unknown

* update ([`6aad425`](https://github.com/tim83/sshtools/commit/6aad425a39c6287670c85e6d9f59990ee36e3957))

* Merge remote-tracking branch &#39;origin/master&#39; ([`0d51710`](https://github.com/tim83/sshtools/commit/0d51710a2421a53f61ac681584652ede46a0c561))

## v4.26.3 (2023-01-12)

### Ci

* ci(ci.yml): Update action versions ([`3c49a80`](https://github.com/tim83/sshtools/commit/3c49a808abd6e66d3e80441a30486b6eee500239))

### Fix

* fix(ssync.py): Select an sshable IP ([`0358873`](https://github.com/tim83/sshtools/commit/03588731bccc859f06808acccddf0b4168a9a738))

* fix(interface.py): Remove unnecessary import ([`41ed87c`](https://github.com/tim83/sshtools/commit/41ed87c85507bec76d250b0c00c74e85ecd53e26))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`185fd78`](https://github.com/tim83/sshtools/commit/185fd786a1a836b3c9faa277a8eb194c57e0c410))

## v4.26.2 (2023-01-12)

### Fix

* fix(interface.py): Don&#39;t use unnecessary sudo for wakeonlan ([`376df76`](https://github.com/tim83/sshtools/commit/376df76ce882933d98760200dca0f1e1368c879a))

* fix(sshin.py): Only select IPs that are sshable ([`6cac28f`](https://github.com/tim83/sshtools/commit/6cac28f9265ab23e4ee28c15b219d17f8f7926a0))

## v4.26.1 (2023-01-03)

### Fix

* fix(pyproject.toml): Include cachetool depedency ([`be4d6d2`](https://github.com/tim83/sshtools/commit/be4d6d225a9d5dfee3404bbb2a1c3ce0d6e178f6))

### Refactor

* refactor(ip.py): Use global IP_CACHE_TIMEOUT for the cache ([`c471594`](https://github.com/tim83/sshtools/commit/c471594653b7ac5baf511f5aa46f5533fa5a8d41))

* refactor(ip.py): Use global IP_CACHE_TIMEOUT for the cache ([`f964d6f`](https://github.com/tim83/sshtools/commit/f964d6fab47e3cd72e733817a353adf87bc47ee0))

### Unknown

* update ([`a9ef810`](https://github.com/tim83/sshtools/commit/a9ef810b0509c863ebb44b78f0270ac28733b4fd))

* update ([`4b630cd`](https://github.com/tim83/sshtools/commit/4b630cd37d705056710f269cd031c1171104fe16))

* update ([`d53519d`](https://github.com/tim83/sshtools/commit/d53519d6f813c47bce68971c803ae09c6139c585))

## v4.26.0 (2022-12-06)

### Feature

* feat(interface.py): Only use sudo when user is not root ([`5922101`](https://github.com/tim83/sshtools/commit/5922101bcc08707a4ee7ef0fa31ea5f163d8b98c))

### Unknown

* Add comment about possible replacement in the future (jump hosts) - fix line length ([`201d90b`](https://github.com/tim83/sshtools/commit/201d90b73319102e365e7f0958c41082e19879bd))

* Merge remote-tracking branch &#39;origin/master&#39; ([`29bf15e`](https://github.com/tim83/sshtools/commit/29bf15ea551cfe4d8eeebe59590ca16a85acc4b2))

## v4.25.3 (2022-11-08)

### Fix

* fix(device.py): Try numero dos ([`76909ea`](https://github.com/tim83/sshtools/commit/76909ea07a9daa7c88bc105bf051d28028de7819))

### Unknown

* Add comment about possible replacement in the future (jump hosts) ([`b501fed`](https://github.com/tim83/sshtools/commit/b501fed5ef3072b47bf4e15017ca450ccdc474ca))

## v4.25.2 (2022-11-08)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`ba0eda7`](https://github.com/tim83/sshtools/commit/ba0eda769034ebf1af61479ad91d41261b1cbc6f))

## v4.25.1 (2022-11-08)

### Fix

* fix(device.py): Remove debug code ([`6766ff6`](https://github.com/tim83/sshtools/commit/6766ff633a8a70e055a44a293f227be1eb2c207c))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`7b473ab`](https://github.com/tim83/sshtools/commit/7b473abf792dbdd95d6e02d692bc15890b211d73))

## v4.25.0 (2022-11-08)

### Fix

* fix(device.py): Allow containers to always check for networks the host is present on, even when the IP can&#39;t be checked ([`affb07e`](https://github.com/tim83/sshtools/commit/affb07e7e4e84efdfb39cb052b5fa5da62034d97))

### Unknown

* Update dependencies ([`2ac782d`](https://github.com/tim83/sshtools/commit/2ac782d42211ee1ff2af891e3f09935fdb7d8532))

* Merge remote-tracking branch &#39;origin/master&#39; ([`c1ef9e5`](https://github.com/tim83/sshtools/commit/c1ef9e572dae072998f74b8cbbf1f6a27071ee1b))

## v4.24.1 (2022-10-31)

### Feature

* feat(device.py): Add functionality for detecting container hosts ([`2eea987`](https://github.com/tim83/sshtools/commit/2eea987b15962ab5945841459333814fd5ad0c29))

### Fix

* fix(device.py): Add better documentation &amp; fix linelength ([`3d75bbb`](https://github.com/tim83/sshtools/commit/3d75bbbb8a2128eb1b45947c756ec2a291f0b33e))

* fix(device.py): Prepare for the sunsetting of the *.beta.tailscale.net addresses ([`921f008`](https://github.com/tim83/sshtools/commit/921f00845c65514a8cb85649d4a352a8d11cf2be))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`011a8fe`](https://github.com/tim83/sshtools/commit/011a8fe5fde379a0927e4ed1322290821215f7d9))

## v4.24.0 (2022-10-26)

### Feature

* feat(tools.py): Enable global config dir ([`0e874fb`](https://github.com/tim83/sshtools/commit/0e874fb71ae2c69ab2cc7b16874415ba9dceebd3))

### Unknown

* Update python ([`c65d72b`](https://github.com/tim83/sshtools/commit/c65d72ba9516ebc481af6ee67409a6307ad31552))

* Fix formatting ([`992cd75`](https://github.com/tim83/sshtools/commit/992cd75dc9b7a98d1bc79b660ed1fd4b18949d65))

* Also exclude symlinks to config ([`a7ca024`](https://github.com/tim83/sshtools/commit/a7ca024bac6e9784a1accf39d62718abd695a99f))

* Configure tests to use a dummy config ([`50ec7e7`](https://github.com/tim83/sshtools/commit/50ec7e7e6c42549f1a10c3f65ec5608982987d82))

* Remove non-functional exec configs for pycharm ([`d5d2a61`](https://github.com/tim83/sshtools/commit/d5d2a61ba46c50f2249f8c897448d6518e90456a))

* BREAKING CHANGE: Remove config from git ([`81a69d3`](https://github.com/tim83/sshtools/commit/81a69d379b3d2dbd97e79d48a448b628ea5d1b3e))

* update ([`007705b`](https://github.com/tim83/sshtools/commit/007705b3b19589b786c092512396c28ca454ebcf))

## v4.23.0 (2022-08-26)

### Fix

* fix(ip.py): Allow ip config to be None ([`9e3d545`](https://github.com/tim83/sshtools/commit/9e3d5459055272e6618ee3d33b705bac3b1af3ec))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`858cdcf`](https://github.com/tim83/sshtools/commit/858cdcf9db6ca8eb02abfda949d2f87d45b988e9))

## v4.22.0 (2022-08-17)

### Feature

* feat(ip.py): Prioritise IPs that can be reached with mosh
feat(oracle.json): Allow zerotier IP to be moshed ([`1c70082`](https://github.com/tim83/sshtools/commit/1c7008287d22b8ce8ae21999dc26386bbce96e7f))

* feat(device.py): Return False for Device.is_local when NotReachable Tim Mees 21 minutes ago - Use correct format ([`c567b9d`](https://github.com/tim83/sshtools/commit/c567b9d6e1779012a361406274bba738e67ffac1))

### Unknown

* Make flake8 happy ([`88bf2c2`](https://github.com/tim83/sshtools/commit/88bf2c2008ce6f932d797693e103f4700918d8d4))

* Merge remote-tracking branch &#39;origin/master&#39; ([`c2d633f`](https://github.com/tim83/sshtools/commit/c2d633f53594ef4a8e4abe7446067e2d80f3d747))

## v4.21.0 (2022-06-29)

### Feature

* feat(device.py): Enable limiting possible ips to only those defined in the config ([`32e5006`](https://github.com/tim83/sshtools/commit/32e50069a8be162d2b73016caed83bd063f1afd5))

### Unknown

* feature(device.py): Return False for Device.is_local when NotReachable ([`af9d2b8`](https://github.com/tim83/sshtools/commit/af9d2b8dd72adeb4d71995cc6436f48b12497b68))

* Update ([`a2d5cf3`](https://github.com/tim83/sshtools/commit/a2d5cf3c8800f70eb42ccd2122b4e1ca63031641))

* Update ([`5e11bda`](https://github.com/tim83/sshtools/commit/5e11bdaf8151461e7cb9a8b9b201b421adcf982d))

* Update ([`6d75975`](https://github.com/tim83/sshtools/commit/6d7597522ce54f534f03022363207b55926649fc))

## v4.20.0 (2022-06-12)

### Feature

* feat: Remove moshable functions and checks
BREAKING CHANGE ([`fdfa946`](https://github.com/tim83/sshtools/commit/fdfa946f4f13f3f74436f0c937766aa674e244af))

## v4.19.1 (2022-06-12)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`ab89e84`](https://github.com/tim83/sshtools/commit/ab89e844d46906d3b6d8a0bbb3183e80d4f51e7a))

## v4.19.0 (2022-06-12)

### Fix

* fix(sshin.py): Actually call the moshable check ([`b71c36c`](https://github.com/tim83/sshtools/commit/b71c36c9b23669ce2c7070753f9e151d944d856b))

* fix(ssinfo.py): Don&#39;t check for moshability to prevent newline problems ([`2734183`](https://github.com/tim83/sshtools/commit/273418391a05c9e68da61e19b1043c6dc318c130))

* fix(getip.py): Remove useless fix ([`a7fbb8d`](https://github.com/tim83/sshtools/commit/a7fbb8da36f1f921edaeacf629f668c5bf6fe059))

* fix(ip_address.py): Use the timeout on the correct function call ([`44e3044`](https://github.com/tim83/sshtools/commit/44e3044d490bebb44263583a1a09c42c0ad6b92e))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`a805d24`](https://github.com/tim83/sshtools/commit/a805d241f31788cee182953b376539389059b95e))

## v4.18.1 (2022-06-12)

### Feature

* feat(getip.py): Reenable json output ([`9a0d63a`](https://github.com/tim83/sshtools/commit/9a0d63ab1233b602682f93160023156161e320e3))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`1b91934`](https://github.com/tim83/sshtools/commit/1b91934146e3252741f1e768c1b975ce8f060825))

## v4.18.0 (2022-06-12)

### Feature

* feat(ip_address.py): Set a timeout for ssh and mosh check ([`0a7421a`](https://github.com/tim83/sshtools/commit/0a7421a52f20dd590a33cbcb89f322aa50deb6e5))

### Fix

* fix(tools.py): Increase the SSH timeout to correspond to the value in the ssh command ([`ceff47b`](https://github.com/tim83/sshtools/commit/ceff47b78eb704b896ed057763591a5e7cff96e4))

* fix(getip.py): Use better variable names ([`f583300`](https://github.com/tim83/sshtools/commit/f58330095369bd18098e2c6e031d58a4b30ba282))

## v4.17.0 (2022-06-12)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`d481f08`](https://github.com/tim83/sshtools/commit/d481f08ac8ee966abd46f4b39d126d639229643b))

## v4.16.0 (2022-06-12)

### Feature

* feat(ssinfo.py): Implement a function to lookup data about devices ([`9b474d2`](https://github.com/tim83/sshtools/commit/9b474d29d41ac7afb25ea17cac923363e92ad125))

* feat(device.py): Check tailscale magic dns ([`ddbfcf1`](https://github.com/tim83/sshtools/commit/ddbfcf1ac583ec726b57c9f1826fa76470d8953a))

### Fix

* fix(device.py): Look for the tailscale magic dns
feat(tools.py): Implement a multithreaded map function
feat(tools.py): Implement a multithreaded function to create tabular tables uniformly ([`6504bbd`](https://github.com/tim83/sshtools/commit/6504bbde29df001a35e18ac54614d0fb6d6335f7))

### Unknown

* Update dependencies ([`e020bdf`](https://github.com/tim83/sshtools/commit/e020bdf623656dfd0c96d0806d60f985e8a4acfd))

* Merge remote-tracking branch &#39;origin/master&#39; ([`d1c9d4c`](https://github.com/tim83/sshtools/commit/d1c9d4cb6e766e773291426b3038c734c47df472))

## v4.15.1 (2022-06-11)

### Fix

* fix(ip.py): Increase priority of mDNS ([`1d23ccf`](https://github.com/tim83/sshtools/commit/1d23ccfab51e45e80fa0078b60081f7a10bc1f04))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`7439fa9`](https://github.com/tim83/sshtools/commit/7439fa9c79fa5dec8a21434be854d695e86397a8))

## v4.15.0 (2022-06-10)

### Fix

* fix(ssync.py): Only sync to sshable devices ([`d5a4347`](https://github.com/tim83/sshtools/commit/d5a43476bf44573b80b39abb617f370bd1b75028))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`0f22a4d`](https://github.com/tim83/sshtools/commit/0f22a4d125be8d94fdb387c6e3a5fc72461b5417))

## v4.14.0 (2022-06-10)

### Feature

* feat(ip.py): Give hostnames a headstart ([`3234f14`](https://github.com/tim83/sshtools/commit/3234f148079a7a8ed33bc60d045ee532ebf8eeb8))

* feat(ip.py): Use latency to sort IPs instead of hardcoding ([`c117f2e`](https://github.com/tim83/sshtools/commit/c117f2e068ab1ce6ae50fc94765bbb1bfa5a30f5))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`5610d1d`](https://github.com/tim83/sshtools/commit/5610d1de488a4c6209c6ce7d36d7a0d289cb49c6))

## v4.13.1 (2022-06-01)

### Fix

* fix(sshin.py): Fix relay command execution ([`2f0ea52`](https://github.com/tim83/sshtools/commit/2f0ea5255d288c06f273cb332e04ba7c48bd7e7b))

### Unknown

* Tailscale ([`9df96ad`](https://github.com/tim83/sshtools/commit/9df96ad5877acd2e15fe897dd2754b8dc97e2f8e))

* Update IPs for kot-tim ([`ea24ac4`](https://github.com/tim83/sshtools/commit/ea24ac41b7db5357f258ef9040e9397cf6614a96))

## v4.13.0 (2022-04-25)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`b250b71`](https://github.com/tim83/sshtools/commit/b250b71dbcd1403ee294a4f8b22aef53dfb37569))

## v4.12.0 (2022-04-25)

### Feature

* feat(sshin.py): Check if a device is moshable before moshing ([`5853d70`](https://github.com/tim83/sshtools/commit/5853d70aaa9cb04c1e80ef7b840e06ef55bbe885))

* feat(forget.py): Re-add device after deletion ([`2de1412`](https://github.com/tim83/sshtools/commit/2de1412e2dd6d71e21860759c1ddaa6707a58168))

## v4.11.1 (2022-04-23)

### Fix

* fix(ip_address.py): Fix sshable and moshable checks ([`c0ff1b4`](https://github.com/tim83/sshtools/commit/c0ff1b4effc80acf7920b22a6ae75135847b7246))

### Unknown

* Edits ([`949cd25`](https://github.com/tim83/sshtools/commit/949cd25a0592d1744eee5b573bc9fef14434307f))

## v4.11.0 (2022-04-23)

### Feature

* feat(ip.py): Allow filtering based on mosh-ability ([`bb49c58`](https://github.com/tim83/sshtools/commit/bb49c586e6a612e86cea7b6624eaaf63208bd35f))

### Fix

* fix(ip_address.py): Use batchmode for MOSH ([`90ce905`](https://github.com/tim83/sshtools/commit/90ce9053b7fc8035b61c32b159c4eb8886137b07))

* fix(ip.py): Don&#39;t filter moshable by default ([`3352c28`](https://github.com/tim83/sshtools/commit/3352c2873cd537cc1ebaa349e75ab8cdd618d056))

* fix(ip.py): Take into account whether mosh is installed ([`e3d70e6`](https://github.com/tim83/sshtools/commit/e3d70e6236e3296c65e9d1f95c22f5198776dcc9))

## v4.10.1 (2022-04-21)

### Fix

* fix(ip.py): Fix check_online config check ([`a5c8e8e`](https://github.com/tim83/sshtools/commit/a5c8e8ea123fd4a792fe8f881038e40fe88b34e4))

## v4.10.0 (2022-04-21)

### Feature

* feat(sshin.py): Limit logging
feat(pathfinder.py): Limit logging ([`cea21ce`](https://github.com/tim83/sshtools/commit/cea21ce4789603c94f7b6a3c25f6e7c0778a6b40))

* feat(ip.py): Allow filtering based on sshability instead of just pingability ([`c96f1b2`](https://github.com/tim83/sshtools/commit/c96f1b226fec3e19915f0d53e70e9bd074704324))

### Fix

* fix(test_ip.py): Disable ip check thanks to github ([`5cf4e68`](https://github.com/tim83/sshtools/commit/5cf4e68c12cee4b86e094fc9fb0d12740034ea20))

* fix(test_ip.py): change test IP ([`4426066`](https://github.com/tim83/sshtools/commit/4426066d93c8c093aafae573f6743194905c5c0b))

* fix(test_ip.py): fix typo ([`1e2a7dc`](https://github.com/tim83/sshtools/commit/1e2a7dc6d8c609bb0efd66091021743dc20af449))

## v4.9.4 (2022-04-19)

### Fix

* fix(sshin.py): Remove unnescesairy prints ([`14be7a2`](https://github.com/tim83/sshtools/commit/14be7a2bd868745012684fe6cf0d91641226e259))

## v4.9.3 (2022-04-18)

### Fix

* fix(ssync.py): Actually stop sync for non-online device ([`e85e2e6`](https://github.com/tim83/sshtools/commit/e85e2e63b2a2a006c1a8eb468da58a9b2d269f11))

## v4.9.2 (2022-04-14)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`9f36435`](https://github.com/tim83/sshtools/commit/9f364356dba7a07b089d774da68ecd117b3d93d0))

## v4.9.1 (2022-04-14)

### Fix

* fix(ssync.py): Use correct method for checking presence. ([`3b102ae`](https://github.com/tim83/sshtools/commit/3b102ae1e69cdb2abf8e039cb44ab05dcb78ade8))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`7ff98c6`](https://github.com/tim83/sshtools/commit/7ff98c64f8fc68c484d9e0eff933f7f521ca03fc))

## v4.9.0 (2022-04-06)

### Feature

* feat(interface.py): Add check for wol vs wakeonlan executable ([`734c166`](https://github.com/tim83/sshtools/commit/734c1669b792c50d8607fce969bf61b2828296ff))

### Fix

* fix(ssync.py): Improve logging
feat(device.py): Enable filtering on super devices
fix(device.py): Don&#39;t look up IPs for every device when determining whether a device is super ([`8e48258`](https://github.com/tim83/sshtools/commit/8e48258fb12b9fffcc55eb58a5fc305102e3fed0))

### Unknown

* BREAKING CHANGE(ip.py): Use .list as property instead of the method .to_list() ([`fc53bd3`](https://github.com/tim83/sshtools/commit/fc53bd3ffafecf2a21b1ea1ba8b91ee1a0efeabb))

* Ignore all media files ([`2411aac`](https://github.com/tim83/sshtools/commit/2411aacd686e56f0c52df650b7338e868c0fc91f))

* Fix wrong location ([`aef0f7e`](https://github.com/tim83/sshtools/commit/aef0f7e6a9b906024967f3fa0b12b80b11c6c83f))

* Fix oracle ip ([`ea3a68f`](https://github.com/tim83/sshtools/commit/ea3a68f022555e3387d3197360fe124d0d26746e))

* Update depedencies and use &gt;= ipv ^ ([`c7776e4`](https://github.com/tim83/sshtools/commit/c7776e4cead34bf0c6bbd83264f27d14a83a3247))

* Update depedencies ([`c069edd`](https://github.com/tim83/sshtools/commit/c069eddfd5079cb398cece6ea3e86acd940ed153))

## v4.8.1 (2022-04-06)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`bbd6ef6`](https://github.com/tim83/sshtools/commit/bbd6ef628610fb4d62e606b86419e0efd94e96c3))

## v4.8.0 (2022-04-05)

### Feature

* feat(getip.py): Allow JSON output ([`5300ae6`](https://github.com/tim83/sshtools/commit/5300ae6e2abfd9313510197954e195522be4e443))

### Fix

* fix(sshin.py): Don&#39;t use mosh when it is not wanted
fix(pathfinder.py): Don&#39;t use mosh for checking reachability ([`15801de`](https://github.com/tim83/sshtools/commit/15801de6562917284bc689282c7374e334c49c04))

### Unknown

* Add homepi ([`a592702`](https://github.com/tim83/sshtools/commit/a59270245eb6c106656aea3ed1635a7b651cd907))

* Merge remote-tracking branch &#39;origin/master&#39; ([`0abb557`](https://github.com/tim83/sshtools/commit/0abb5571efeea043c3726b22882bd79c8df4a458))

## v4.7.1 (2022-03-22)

### Fix

* fix(sshin.py): improve mosh selection ([`8b9adee`](https://github.com/tim83/sshtools/commit/8b9adee56e7627b2ce98863103db20cd310ae02c))

### Unknown

* update ([`719bcc7`](https://github.com/tim83/sshtools/commit/719bcc7d3990f5dbf3a4d36e2ef44f2e2d52ba1b))

* Configure coolermaster ([`5925efc`](https://github.com/tim83/sshtools/commit/5925efc8f522d22b4e2c00292926d5b6d1c2c8cf))

* Limit precommit check to main package ([`2e88986`](https://github.com/tim83/sshtools/commit/2e889860cf710ee308d3017b8cbd74180910c8f4))

* Limit to python 3.8 ([`31d3c5d`](https://github.com/tim83/sshtools/commit/31d3c5d0a0425e64dfec12b7471793490ef36fef))

* Exclude ISO&#39;s recursively ([`52b200b`](https://github.com/tim83/sshtools/commit/52b200ba6136028a3975a3bc2cf3feec4354879e))

* Merge remote-tracking branch &#39;origin/master&#39; ([`ae74916`](https://github.com/tim83/sshtools/commit/ae749160b41d0bfddce84fc6993285e62b22c818))

## v4.7.0 (2022-03-17)

### Unknown

* Use pylint ([`b915da0`](https://github.com/tim83/sshtools/commit/b915da04a59389b084ed24d8f6f552e5109bb97a))

* Make updated pylint happy ([`2e19f0a`](https://github.com/tim83/sshtools/commit/2e19f0a79e8f52b42910cf60b6d76581c42f7190))

* Add pylint to dev requirements ([`a160744`](https://github.com/tim83/sshtools/commit/a160744cf5a20b42a4737554e1469c23ee44d475))

* Add pylint to dev requirements ([`165f71d`](https://github.com/tim83/sshtools/commit/165f71dd9254fbe57a19a178f5b2e2776402ec57))

* Merge remote-tracking branch &#39;origin/master&#39; ([`5a3c821`](https://github.com/tim83/sshtools/commit/5a3c821f95e36dfd86a5a1b6d7870e1edbf2c46c))

## v4.6.0 (2022-03-17)

### Feature

* feat: use pylint
BREAKING CHANGE: a lot ([`b35edcf`](https://github.com/tim83/sshtools/commit/b35edcf2eaa72c7ab6c6e13f5a70e6aa393f87fc))

* feat(device.py): return the hostname instead of localhost for self device ([`7d15825`](https://github.com/tim83/sshtools/commit/7d1582529557123d3ea3e29d9ac93dd38986d6a0))

### Fix

* fix(pathfinder.py): Fix not storing the correct path ([`20ecbad`](https://github.com/tim83/sshtools/commit/20ecbad9866c94211849ceb44c3a52c66f2bb518))

### Unknown

* Improve tests for timeout ([`4f21ef0`](https://github.com/tim83/sshtools/commit/4f21ef01e5f8b02ad59ffbe2c820cf0bba3b7d9e))

* Try to fix tests - definitely ([`ea00b50`](https://github.com/tim83/sshtools/commit/ea00b504898fdca1d9f39ef252286c98e483272a))

* Try to fix tests ([`8de5d92`](https://github.com/tim83/sshtools/commit/8de5d92dd00294888e12005c82ee2c369e3439dd))

* Add a test to catch the problem fixed in @cca39ff7 ([`193d6bf`](https://github.com/tim83/sshtools/commit/193d6bf853bf90bb5871f270ad50f47e03c2a1fb))

## v4.5.4 (2022-03-16)

### Performance

* perf(pathfinder.py): use multiprocessing for checking alive paths ([`df8e093`](https://github.com/tim83/sshtools/commit/df8e0932fc7716804408ae10a68c5fa05a7219f8))

### Unknown

* Add tanteleine ([`cbc79c5`](https://github.com/tim83/sshtools/commit/cbc79c59de3c9f97a973d7a29eb1fea483f9fb99))

* Remove test that required present devices ([`411c863`](https://github.com/tim83/sshtools/commit/411c86311c2fcdac6678182b156472cfb21250b4))

* Fix tests for ssync command ([`e8345f9`](https://github.com/tim83/sshtools/commit/e8345f9d9657e8ed64179c299317ad9f7c5ac065))

* Merge remote-tracking branch &#39;origin/master&#39; ([`0ea7422`](https://github.com/tim83/sshtools/commit/0ea7422d3d99b065f9d61e4627fd42c854a39ba5))

## v4.5.3 (2022-03-01)

### Unknown

* Add tests for ssync command ([`13598c5`](https://github.com/tim83/sshtools/commit/13598c5d9062f70d315ac61e74a336eb2e76140a))

* Add tests for ssync device selection ([`81ea64a`](https://github.com/tim83/sshtools/commit/81ea64af19f2a3b0b959678dd2d3523018a3ed09))

* Merge remote-tracking branch &#39;origin/master&#39; ([`7d99b2f`](https://github.com/tim83/sshtools/commit/7d99b2ffdc72b4ceaac037220369b82b913dfe1d))

## v4.5.2 (2022-03-01)

### Fix

* fix(__init__.py): fix timtools import ([`caa573b`](https://github.com/tim83/sshtools/commit/caa573b483c57fec67973228a24a2afb3b923c0d))

* fix(device.py): Specify that .is_local does not include VPNs ([`41a5043`](https://github.com/tim83/sshtools/commit/41a5043ffe6f30998dbd9866bc251dfc0f0daa0b))

### Unknown

* Update ([`6e8e415`](https://github.com/tim83/sshtools/commit/6e8e415e814173793a730ff6f9132282d7e08efd))

## v4.5.1 (2022-02-25)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`09eb0e1`](https://github.com/tim83/sshtools/commit/09eb0e15a33b0a6a30b0016192c32a276a201a68))

## v4.5.0 (2022-02-24)

### Feature

* feat(device.py): Allow creating a device based on the hostname instead of the name ([`f85cd92`](https://github.com/tim83/sshtools/commit/f85cd92b2933fff44432d4938a865e009ad7a9b0))

### Fix

* fix(device.py): Allow creating a device based on the hostname instead of the name ([`ecd6fe9`](https://github.com/tim83/sshtools/commit/ecd6fe9fe3fe835739e18fe1bda61b8d55d86d7c))

## v4.4.0 (2022-02-24)

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`9a6dd6b`](https://github.com/tim83/sshtools/commit/9a6dd6b6d1e42fa575c8a8cb09383062a242af35))

## v4.3.2 (2022-02-24)

### Feature

* feat(device.py): Add a method fo checking if a device can be a relay ([`d6b85c5`](https://github.com/tim83/sshtools/commit/d6b85c55907d494eceed0a2075f600196e8ebeb3))

### Fix

* fix(pathfinder.py): Don&#39;t use the hostname for connecting to a relay to prevent Device-Not-Found errors ([`c6ca57c`](https://github.com/tim83/sshtools/commit/c6ca57cec77f058b89811b640887ef20162a4346))

### Performance

* perf(device.py): improve logging by providing a __str__ method for device ([`e094f6b`](https://github.com/tim83/sshtools/commit/e094f6b8ac291969ffe4738b94fbf8b09520a804))

## v4.3.1 (2022-02-21)

### Fix

* fix(pathfinder.py): fix selecting target as relay ([`8356dbe`](https://github.com/tim83/sshtools/commit/8356dbe0971c4cc50e4b28c6836126003e61ee6b))

### Unknown

* Execute quality checks and tests in parallel ([`c6e8187`](https://github.com/tim83/sshtools/commit/c6e8187d826c2335ec5f309314b755c32ec69c1f))

## v4.3.0 (2022-02-20)

### Feature

* feat(device.py): Change property-like functions to properties

BREAKING CHANGE ([`8cdeeb6`](https://github.com/tim83/sshtools/commit/8cdeeb6e219027e180de375a70701e6160d87d4a))

### Fix

* fix(device.py): Disable caching
fix(pathfinder.py): Fix source and target parameters for PathFinder
fix(sshin.py): Allow connecting to a device without public key ([`58889a8`](https://github.com/tim83/sshtools/commit/58889a89a9cfb3a985ef981b20070f99285dd3c5))

* fix(config): non-main limited sync for laptop-oma ([`42bc755`](https://github.com/tim83/sshtools/commit/42bc755505f8cd616173c7d5a091044c178c3fb9))

* fix(config): oma -&gt; greta ([`6abb3cf`](https://github.com/tim83/sshtools/commit/6abb3cf564aef355a7a08064d409d21b4086d4f1))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`d49a000`](https://github.com/tim83/sshtools/commit/d49a000b8629a8fe61f8d92c40582f5014ed6702))

## v4.2.1 (2022-02-19)

### Fix

* fix(sshin.py): clean up user messages and variable names &amp; improve docstrings ([`3a147c4`](https://github.com/tim83/sshtools/commit/3a147c4ae3f04ba6d3309dc8cca9581b88f41360))

* fix(ssync.py): clean up user messages and variable names &amp; improve docstrings ([`77d4620`](https://github.com/tim83/sshtools/commit/77d46205c82766dd804beaef8248ecfe276444e2))

* fix(smount.py): improve docstrings ([`a895dec`](https://github.com/tim83/sshtools/commit/a895decfb9be88216efb3fbee7b3812aed153b5a))

* fix(ssync.py): improve docstrings ([`2af3943`](https://github.com/tim83/sshtools/commit/2af3943387f9c1872ddbe7e2ea92eea46e5bd748))

* fix(wake.py): improve docstrings ([`cd14283`](https://github.com/tim83/sshtools/commit/cd14283a82781282c1817e77f75217f1ef6ece74))

* fix(wake.py): clean up user messages and variable names ([`0c6e32c`](https://github.com/tim83/sshtools/commit/0c6e32c5effce1840fced6d1d2abf7e3dbf2230b))

* fix(smount.py): clean up user messages and variable names ([`3728403`](https://github.com/tim83/sshtools/commit/3728403d511ddb96cfe3d36bbed8bbc00220a326))

### Unknown

* Merge remote-tracking branch &#39;origin/master&#39; ([`0f13f54`](https://github.com/tim83/sshtools/commit/0f13f549b4200deb76c0070a3bba060070767e9c))

## v4.2.0 (2022-02-19)

### Feature

* feat(device.py): Use the sshable check ([`67577a2`](https://github.com/tim83/sshtools/commit/67577a2066ebbc77f35510f0760842e2327adaa5))

* feat(device.py): Add a check to make sure SSH is configured correctly ([`dc5b5f8`](https://github.com/tim83/sshtools/commit/dc5b5f87c2a93ea8a2eb97be4e84a6b8272005d0))

### Fix

* fix(ssync.py): Use better error message ([`651c1cf`](https://github.com/tim83/sshtools/commit/651c1cfc900db803f2160a9f56dd29712f917b37))

* fix(ssync.py): prevent disappeared device from terminating sync for all devices ([`3755265`](https://github.com/tim83/sshtools/commit/37552656fd37c0bd6860d7b38db69c7c934a0374))

### Performance

* perf(ssync.py): reuse cache finder from timtools ([`84f3f49`](https://github.com/tim83/sshtools/commit/84f3f498be2db014d80cb92d6d77b9ee18f7e5c3))

### Unknown

* Update README.md ([`bd1d5fc`](https://github.com/tim83/sshtools/commit/bd1d5fc9e36dd3e49bfc386bddbb763b82fde7a1))

* Create README.md ([`46059e9`](https://github.com/tim83/sshtools/commit/46059e9e3ff4b916f8c3b7f813b1a3ccfb1f4167))

* Update ([`ebe6eb1`](https://github.com/tim83/sshtools/commit/ebe6eb148af04409b033185fcb3b87b889bee0e5))

* Merge remote-tracking branch &#39;origin/master&#39; ([`a08cdb7`](https://github.com/tim83/sshtools/commit/a08cdb787ef0d1a17aad48d0318704975a59dfc1))

## v4.1.2 (2022-02-18)

### Fix

* fix(ip.py): fix typo ([`cade188`](https://github.com/tim83/sshtools/commit/cade188ca964e6991294849a8f3bc47192148ed8))

### Performance

* perf(ci.yml): remove unneeded steps ([`034b8ed`](https://github.com/tim83/sshtools/commit/034b8ed5025f2e6461a31f6796d66317940f6394))

### Unknown

* Add docstring ([`5aa1433`](https://github.com/tim83/sshtools/commit/5aa1433e411ff468927ac64633d6bd9b19bc25e5))

* feat(setup.py) load version from pyproject.toml ([`49418fd`](https://github.com/tim83/sshtools/commit/49418fdd10075999b0628d63065d57aff1a36ebe))

* fix(ci.yml) reintroduce poetry version restriction || Remove mistakes ([`0a725a7`](https://github.com/tim83/sshtools/commit/0a725a703aa1ad7203d18e57d5383edffd682588))

* fix(ci.yml) reintroduce poetry version restriction ([`dce3d0b`](https://github.com/tim83/sshtools/commit/dce3d0bf4dc16ae198ec3f7aa6244af433e25c71))

* Fix github errors #4 ([`d0b5f2d`](https://github.com/tim83/sshtools/commit/d0b5f2d8260ab0b39c6bfe7990a2ae2795a4f892))

* Fix github errors #3 ([`d424e39`](https://github.com/tim83/sshtools/commit/d424e396a8436dcb6318fb4c181efd9f8ca43c19))

* feat(setup.py) read version from pyproject.toml ([`0c30131`](https://github.com/tim83/sshtools/commit/0c30131cc62c147f3e48a6719a7ced932d1af73e))

* fix(pyproject.toml) remove setup.py from version variables ([`993989b`](https://github.com/tim83/sshtools/commit/993989be7efe1cc6cad377f44eba23d707c89a3e))

* feat(ci.yml) Create true release on save ([`d1d681b`](https://github.com/tim83/sshtools/commit/d1d681b9643da216a39ac15afe1f2ea8a2033509))

* fix(connection) don&#39;t limit network query to connected networks ([`4e09826`](https://github.com/tim83/sshtools/commit/4e0982627856a7a110cf1882b4948731eefd196f))

* fix(test_ip) remove typo&#39;s ([`cc474fe`](https://github.com/tim83/sshtools/commit/cc474fe73c0ac23d036567794db79b1d0a775080))

* Try to fix problems ([`ec42fd0`](https://github.com/tim83/sshtools/commit/ec42fd0222b782731e065295d1cb61e1d48898ac))

* fix(ci.yml) Don&#39;t use matrix unneeded ([`27d2aad`](https://github.com/tim83/sshtools/commit/27d2aad4f6b7bd4c54c90fc4bcff6f60436fdb9a))

* fix(ci.yml) Don&#39;t use matrix unneeded ([`fc00958`](https://github.com/tim83/sshtools/commit/fc00958fb359990a714fa02bd0f5e18c495a6df0))

* fix(ci.yml) test VPN status of zt ([`e6258cf`](https://github.com/tim83/sshtools/commit/e6258cfe7c07b4de2c8c9a0eef1aeb5e94fcf071))

* fix(ci.yml) test VPN status of zt ([`034f14a`](https://github.com/tim83/sshtools/commit/034f14a253e5e77a03d25cbe70579229fed29405))

* fix(pyproject.toml) add setup.py as version source ([`7ebadea`](https://github.com/tim83/sshtools/commit/7ebadeae093d24d4774bba70554e4ab61e5b1b6a))

## v4.1.1 (2022-02-18)

### Unknown

* feat(ip_address) separate VPN test ([`c396840`](https://github.com/tim83/sshtools/commit/c396840090923ae04d7755456600c4bc4e43cb04))

* fix(ci.yml) install semver adn limit pversion releases ([`26c1a5e`](https://github.com/tim83/sshtools/commit/26c1a5ea14841ad43a2d0e85476cc2924f67f301))

* Use path object ([`9b4e364`](https://github.com/tim83/sshtools/commit/9b4e36439e1e92b809a5c1832d3d61e5ed1f8263))

* Run semantic-release ([`ad4acd0`](https://github.com/tim83/sshtools/commit/ad4acd018747ee0b4c74e57d50e29506cd06d50d))

## v4.0.3 (2022-02-18)

### Fix

* fix: set correct CI versions ([`c958e39`](https://github.com/tim83/sshtools/commit/c958e39f08f55eace2a2c15c6e99cd45000a4150))

### Unknown

* Only test code when quality checks are completed ([`93387a6`](https://github.com/tim83/sshtools/commit/93387a613cdabcbd8eae7d2386f421595bcee3fa))

* fix(pathfinder) allow python 3.7 ([`407c39e`](https://github.com/tim83/sshtools/commit/407c39ee1ae1147d8918d7b6449a89907140b5e5))

* update ([`6794f90`](https://github.com/tim83/sshtools/commit/6794f90ddece4800412117897578875a8ca0b3c0))

* feat:support p3.7 ([`cd61b54`](https://github.com/tim83/sshtools/commit/cd61b54ba3e8d9cd0f8d728e591cbeb392597cea))

* fix:set semantic release ([`e306b4c`](https://github.com/tim83/sshtools/commit/e306b4c30446c2b38e4a52689fd4478c5604be8f))

* Improve CI ([`4ca4c86`](https://github.com/tim83/sshtools/commit/4ca4c86483f5a096eff37d6236388fbcd2d7165e))

* Improve CI ([`20dafa8`](https://github.com/tim83/sshtools/commit/20dafa8bccb1b5e602e4dd3dee941bfe4490ea59))

* Improve precommit ([`4cd7bb7`](https://github.com/tim83/sshtools/commit/4cd7bb7c8c6b74047a5da0f92b80526e96da6ab8))

* Exclude digikam DBs ([`4b00178`](https://github.com/tim83/sshtools/commit/4b00178eb18ffae5e65621acc305d25e7ab56bf4))

* Use pathfinder for unreachable devices #fix ([`f0cc64c`](https://github.com/tim83/sshtools/commit/f0cc64c6623e8e7bc9161c7609c2d7c02660c6cf))

* Use pathfinder for unreachable devices ([`b4bef27`](https://github.com/tim83/sshtools/commit/b4bef2791388fb12a4417cde1ccd2e3f7c6eaf6e))

* Use better log names ([`ffd17c3`](https://github.com/tim83/sshtools/commit/ffd17c371d97f8d0b7e85a350f8c87c0eff2ea1e))

* Use better imports ([`28c0c0a`](https://github.com/tim83/sshtools/commit/28c0c0a43fe41cbd24b0482da07a74632713c22e))

* Use newer timtools ([`83f3a4a`](https://github.com/tim83/sshtools/commit/83f3a4ae27664fd5d9bf61c64df4db09fdabd76c))

* Fix already mounted location ([`a969276`](https://github.com/tim83/sshtools/commit/a9692763ff6a9e130299e103b514104ab0b5a4fc))

* fix mountpoint as pathlib ([`fa3078f`](https://github.com/tim83/sshtools/commit/fa3078fb1a3d9027b860841ae45ce8dea0bb2b97))

* Fix missing files ([`9787e8d`](https://github.com/tim83/sshtools/commit/9787e8d4aa72e390670de7a86a32f341ce20fbf8))

* Fix p3.7 ([`1a3f35a`](https://github.com/tim83/sshtools/commit/1a3f35aea60aceaa6ff053dc91c1270fa1e49f20))

* Move dekstop-ben to external VLAN ([`d41e78e`](https://github.com/tim83/sshtools/commit/d41e78e0e7e511f0e245f8a9966b49b96cdc84a8))

* Update deps ([`2aeadb1`](https://github.com/tim83/sshtools/commit/2aeadb1f410dee9013fd644a972e1c78daf472a2))

* Fix dependencies ([`0e5a1ab`](https://github.com/tim83/sshtools/commit/0e5a1ab320ec9352707257f533a4fae560820517))

* Fix circular import ([`caeff11`](https://github.com/tim83/sshtools/commit/caeff119bc9d38b086286e0337f429e75f8a386c))

* Allow for public VPNs ([`4198ee3`](https://github.com/tim83/sshtools/commit/4198ee30b8162c56c4eba64588de5cc6963005ce))

* Add laptop-oma &amp; zerotier-techsupport ([`d6021cf`](https://github.com/tim83/sshtools/commit/d6021cf03ecae624477c63cac84b68555e6e4ee3))

* Use timtools package ([`f0f15cb`](https://github.com/tim83/sshtools/commit/f0f15cba898ae091d5ed2212a862739b0a171891))

* Remove public IP ([`51c02b0`](https://github.com/tim83/sshtools/commit/51c02b02b7d6e36e05531fefb03d8455120fb45d))

* Use IDs for home-tim ([`17e398f`](https://github.com/tim83/sshtools/commit/17e398fdc3693cb55421e31b59e54f2bf52afd57))

* Fix device selection ([`d9e45e5`](https://github.com/tim83/sshtools/commit/d9e45e5ac60b42fe706172059a0b2a4f4be9bb0f))

* Update ([`8813408`](https://github.com/tim83/sshtools/commit/8813408f742607addb44976bd2c2bd57340b7fa7))

* - Add VMs
- Add bridge connection for VMs
- Enable syncable device to not be presented center stage ([`f562c6b`](https://github.com/tim83/sshtools/commit/f562c6ba35b38ebebbcf6076e39010b19b8e457d))

* Update IP ([`72d9826`](https://github.com/tim83/sshtools/commit/72d982637b41f0a4018158873c36bbcf2205adaa))

* Set zerotier IPs ([`6edc709`](https://github.com/tim83/sshtools/commit/6edc709ffa1022293fcf4fc5ce63077530284c81))

* Fix ssync for different users #2 ([`2245b7f`](https://github.com/tim83/sshtools/commit/2245b7f78e70e7cb73bddfbaeebfb45ba5f60aca))

* Fix ssync for different users ([`d405ae4`](https://github.com/tim83/sshtools/commit/d405ae42e41a723a350b980647e73ae0146ac476))

* Update ([`29d0476`](https://github.com/tim83/sshtools/commit/29d0476212ae663fd81ce83969a2b2026ccd6bee))

* Add oracle VM &amp; enable non-pingable servers ([`082eca4`](https://github.com/tim83/sshtools/commit/082eca48dfc39c38971bb72fcba503c1539ae430))

* Update ([`5fccaae`](https://github.com/tim83/sshtools/commit/5fccaae748c1a933164fe2c9f45334f0f8a3be65))

* Fix ssh-forget ([`cc81d14`](https://github.com/tim83/sshtools/commit/cc81d1495f7bc4041c16825dce43f6e0962730e4))

* Enable using an ip_id to compose possible IPs ([`d626900`](https://github.com/tim83/sshtools/commit/d6269001bb8a654ed1f6d8b1fa6bd31fbbe7f787))

* Improve docstrings with parameters ([`9bb0daf`](https://github.com/tim83/sshtools/commit/9bb0daffa08d2234795ef8d84b59297f792c2033))

* Centralize the IP cache timeout ([`3cfd14f`](https://github.com/tim83/sshtools/commit/3cfd14fde025dc76700fed57f4502a27a38d64fb))

* Fix not syncing to limited devices ([`5ad5e4b`](https://github.com/tim83/sshtools/commit/5ad5e4bb9087a70e284612ac9cc840575c54cbe3))

* Clean up sync ([`2de7102`](https://github.com/tim83/sshtools/commit/2de7102a0ca99fd3f37949356525fc59e11d6186))

* Fix order ([`55475e4`](https://github.com/tim83/sshtools/commit/55475e4d129a4e6147f9f46ddffa7053c448194c))

* Use multithreaded filter ([`d58e91e`](https://github.com/tim83/sshtools/commit/d58e91e5f73b441b19d5e7627db62bf6b807da34))

* Increase timeout ([`36c3f4c`](https://github.com/tim83/sshtools/commit/36c3f4cad3b14a75eafd5a761d1a503b2b5f939e))

* Use isinstance ([`93a8596`](https://github.com/tim83/sshtools/commit/93a85963091dc1bbc656940a1a7f531018c5d384))

* Use priority for determining daily drivers ([`b8ee22a`](https://github.com/tim83/sshtools/commit/b8ee22a2192dd2925144f5e72548cded2a29fbf0))

* Supress output when writing for getip ([`7bc65c7`](https://github.com/tim83/sshtools/commit/7bc65c712734095ffdf4ba8c07903b4e029e8bfa))

* Fix python &lt;=3.9 ([`20e1c3e`](https://github.com/tim83/sshtools/commit/20e1c3ec58e082a99425f04a2ccf16ca3d9c2240))

* Fix wrong attribute typing
Update ([`6bf636b`](https://github.com/tim83/sshtools/commit/6bf636bf5ef26ef71ded6f3c7a716a7a8cf93d0b))

* Set ben user ([`e675e04`](https://github.com/tim83/sshtools/commit/e675e0454f0b5c1308ceefc6742c284086f52e0b))

* timtools has been updated to fix github actions ([`a86ac58`](https://github.com/tim83/sshtools/commit/a86ac587102d6fa319289f76a81eb5172e1fecd5))

* Update ([`69a94fe`](https://github.com/tim83/sshtools/commit/69a94fe2fae568ef7a104702e5aa59461dee0f21))

* Fix typehinting in python3.8 and lower ([`8006d0e`](https://github.com/tim83/sshtools/commit/8006d0eff34352455d0e5d85cc6d492a2ebcce70))

* Fix multithreading ([`c46c7db`](https://github.com/tim83/sshtools/commit/c46c7db8f3f47716896aae3a7c1f5fa8cdda4f8c))

* Use all possible IPs ([`1a44e15`](https://github.com/tim83/sshtools/commit/1a44e15798c211ab6c2a516fa34a52baebe6062c))

* Improve flow ([`bb65f6c`](https://github.com/tim83/sshtools/commit/bb65f6c47006d74fb53a4f2684d54335a01de37e))

* Decrease timeout ([`5978c8f`](https://github.com/tim83/sshtools/commit/5978c8fed56df39e2b5f5dbb2b2e3548478af83d))

* Increment version ([`487e0be`](https://github.com/tim83/sshtools/commit/487e0be48913017adafc791e9d1f7d31cc9c515f))

* Enable user config ([`ec19ea3`](https://github.com/tim83/sshtools/commit/ec19ea319d09c7144f785ac582fc636161b090c6))

* Fix wake-up ([`c76b910`](https://github.com/tim83/sshtools/commit/c76b9105e8c9806fc71245a9daaa56c73207ed99))

* Fix sshin &amp; smount ([`e43e2f7`](https://github.com/tim83/sshtools/commit/e43e2f75d2287ff5d647c386839b3203fc4c9f43))

* Fix getip ([`1b774aa`](https://github.com/tim83/sshtools/commit/1b774aa85144ea628779a96336045fa268c393df))

* Use network objects ([`114b815`](https://github.com/tim83/sshtools/commit/114b815bc16b0a3e4d7300b1b04a052bbd1108ff))

* Add config ([`f951cfc`](https://github.com/tim83/sshtools/commit/f951cfcc0b01e1726bdac7f76390a18a07053915))

* Implement timeout ([`c41bddc`](https://github.com/tim83/sshtools/commit/c41bddc962eedbe311a671d95442d0ce994723f9))

* Refactoring with initial data sample ([`1d8d3f4`](https://github.com/tim83/sshtools/commit/1d8d3f42fcf04be877f8218f3c8745d2252d2c30))

* Provide ordering when sorting ([`cc4d333`](https://github.com/tim83/sshtools/commit/cc4d333d1900e627e64fc3cfbf871e6fa8a2a445))

* - Make IPs with the same address a singleton
- Make IP Lists iterable ([`e1ac553`](https://github.com/tim83/sshtools/commit/e1ac553332bd9d88cdb19aa45fa937c543c73e4d))

* Fix typo ([`f923909`](https://github.com/tim83/sshtools/commit/f92390968a2af63a12e11ef5abdafe9005fb19d0))

* OO everywhere :) ([`01b059d`](https://github.com/tim83/sshtools/commit/01b059d7c84fddca3b793b767fec622466ae2e9d))

* Expand IPAddress class ([`d5c6797`](https://github.com/tim83/sshtools/commit/d5c6797fc6de5d085697ecd55ca2b36c1ab6d4dd))

* Implement OO IPAddress ([`4ae1321`](https://github.com/tim83/sshtools/commit/4ae1321de52237b7b27946a2c52e3268157a0cb6))

* Optimize wol adaptability ([`b1fffff`](https://github.com/tim83/sshtools/commit/b1fffffd54873c26a61cafaad894c668fd77d811))

* fix wol again ([`c3cb483`](https://github.com/tim83/sshtools/commit/c3cb48392e38f3762f3eaab87146a5f30db5dc97))

* fix wol ([`dd03f70`](https://github.com/tim83/sshtools/commit/dd03f70de80c57d3ca40f2e8ce3e409078a087c4))

* Enable writing access logs for logging reachability ([`0c9935c`](https://github.com/tim83/sshtools/commit/0c9935c9debb4d6afd99e1686e0f2517c82ec710))

* Enable functioning without iwgetid ([`ccc4d56`](https://github.com/tim83/sshtools/commit/ccc4d56e50a7a007d2bd6662b9dc696bd49c8d36))

* Change telenet adress ([`75378b5`](https://github.com/tim83/sshtools/commit/75378b5d009df1f52e884b6eb638452bc67dd890))

* Enable forgetting a device ([`3a47031`](https://github.com/tim83/sshtools/commit/3a4703100b7c69b8881355fe74a338ffaeeb62fd))

* Don&#39;t hardcode iwgetid path ([`5423e0f`](https://github.com/tim83/sshtools/commit/5423e0f2b63ad061c3804bfc0cabccbed26d4063))

* Fix IP order for avdel ([`fae2941`](https://github.com/tim83/sshtools/commit/fae29415fa9a016892f72694631a512e584ad4fa))

* Readd .idea ([`e015dbb`](https://github.com/tim83/sshtools/commit/e015dbb232afc7d40a297b9e89d76223b60ec90d))

* Add pycharm to gitignore ([`c6d54d2`](https://github.com/tim83/sshtools/commit/c6d54d2367547da0f22bd0f1a1cf29e9dbf6271b))

* Change AVDEL IP ([`5763ddd`](https://github.com/tim83/sshtools/commit/5763ddd0e6d5eb1643e62d6886e908bb3a54f248))

* Only warn when syncing to laptop when it is present ([`f6b9e68`](https://github.com/tim83/sshtools/commit/f6b9e68ab1a9f55e15162523b305defa45703970))

* pycharm edit ([`b15ed57`](https://github.com/tim83/sshtools/commit/b15ed57ca15eff9fce02d64e381933feacb390b4))

* Update ([`2684f5f`](https://github.com/tim83/sshtools/commit/2684f5fd082ca88b9cece57978f300c8b5da6c64))

* Use mosh and terminal mode for exe ([`54d7be1`](https://github.com/tim83/sshtools/commit/54d7be17cbd1ed88602f99a0b127171c58cb19ab))

* Fix temp dir being deleted ([`f613abe`](https://github.com/tim83/sshtools/commit/f613abe4b9f8bb6633777f7ba149aa6459d77958))

* Use pre-commit ([`564f14f`](https://github.com/tim83/sshtools/commit/564f14ffe79cca4f5e35d6c3d28c170d411be730))

* Use automated code quality ([`c5ccb6a`](https://github.com/tim83/sshtools/commit/c5ccb6a1b3413a335aa3fdd54a24ac5a08ed514b))

* Handle a lack of poetry ([`2dfdab4`](https://github.com/tim83/sshtools/commit/2dfdab43592ee8f602f4ca6c30e6b3c1d823adf8))

* Reintroduce setup.py for camerapi ([`77dd90a`](https://github.com/tim83/sshtools/commit/77dd90ae292964710de32b75b5d64c0ed278a13d))

* Implement proper timeout ([`4abf974`](https://github.com/tim83/sshtools/commit/4abf974ac5906a737553ec64d9bbf4778804f9ae))

* Update ([`cf3072c`](https://github.com/tim83/sshtools/commit/cf3072c888855419da1e1f97fe28f38e4822a8c3))

* Remove old metadata ([`504228f`](https://github.com/tim83/sshtools/commit/504228ff99c19c85b930dae5459444045a0878f2))

* Remove the last trace of prodesk ([`91721c9`](https://github.com/tim83/sshtools/commit/91721c9512e66a74251e63008a791f4256a4b1c1))

* Update depedencies ([`1489984`](https://github.com/tim83/sshtools/commit/148998408d765dd2fd24bb1ffbdb00e718064dbc))

* Remove prodesk &amp; imbit from devices ([`f61660e`](https://github.com/tim83/sshtools/commit/f61660e096031eda42c062235cdfba470b911439))

* Set imbit ip to new ([`7f19f05`](https://github.com/tim83/sshtools/commit/7f19f05f0c8dc7c81093466b67ec259a74280312))

* Limit getip to active devices (prevents double lookup after cache) ([`89a320b`](https://github.com/tim83/sshtools/commit/89a320b508ec1319716d64a663aaead6aa51d39f))

* Update ([`32643ed`](https://github.com/tim83/sshtools/commit/32643ed8cbab532ccdcd3bb2a6ecff60d4c7d8db))

* Use multithreading for caching IPS ([`55a213d`](https://github.com/tim83/sshtools/commit/55a213daaed412e39ec19aa95d4ff0c0ef1b18b6))

* Enable multiple IP tests ([`7b52b2b`](https://github.com/tim83/sshtools/commit/7b52b2b6d4dc440d612ae7488fb1837c7d25bb55))

* Update depedencies ([`c7ef730`](https://github.com/tim83/sshtools/commit/c7ef73020a19fa66c7178b2697526d442e256d7c))

* Update depedencies ([`8f96143`](https://github.com/tim83/sshtools/commit/8f96143c1b35dc63f1b1b75b9b76a23ebf6e350e))

* Remove timeout for general IPs ([`46069b8`](https://github.com/tim83/sshtools/commit/46069b845748c8680e4cf755237d74159b7e91e9))

* Increase timeout ([`d8c7603`](https://github.com/tim83/sshtools/commit/d8c7603b279d7df21b0150ec37741918219b0372))

* Increase timeout ([`25280c4`](https://github.com/tim83/sshtools/commit/25280c46297a0fa10e3a1fa7cdc9c214b57f14c6))

* Include AVDEL backups ([`dc1b22f`](https://github.com/tim83/sshtools/commit/dc1b22f8b2adac46a7ad22ba742d578c8a555b0f))

* Exclude AVDEL backups ([`736fe8f`](https://github.com/tim83/sshtools/commit/736fe8ff7f0ecf51357b9b6d6111718d072eb2b6))

* Discard DNS check fast (don&#39;t wait for the 5s timeout) ([`672d079`](https://github.com/tim83/sshtools/commit/672d079093a54ca62c0da81b1a241dafbd7f0d8b))

* Enable IP only mode ([`44aed75`](https://github.com/tim83/sshtools/commit/44aed7584be2fb03e779e4acfc699955463df582))

* Remove debug ([`411bf7b`](https://github.com/tim83/sshtools/commit/411bf7b8f68060fd57d6dda4ec724b8509e85ee8))

* Remove timeout ([`08db648`](https://github.com/tim83/sshtools/commit/08db6485bdd5a03cd00e2ee8fd1200a0e37e9661))

* Update ([`df47fdd`](https://github.com/tim83/sshtools/commit/df47fdd042928e71e6724c93b93c8b34d6c0db36))

* Fix 3.7 compatibility ([`586c219`](https://github.com/tim83/sshtools/commit/586c21992a212341dbf7d4a122ea5f1341f328f2))

* Clean up ([`7dd14ce`](https://github.com/tim83/sshtools/commit/7dd14ce648c6436a10f675655979e8e343ff8e4b))

* Use multithreading ([`31d4edb`](https://github.com/tim83/sshtools/commit/31d4edbfeec993741ee7711f059081df968eb181))

* Be flexible in fping location ([`a31cb19`](https://github.com/tim83/sshtools/commit/a31cb19336bd3f58e0b2d7da4e3fffa83f9a6ab4))

* Be flexible ([`329a1f8`](https://github.com/tim83/sshtools/commit/329a1f8483cedae95aec8b5446f7b09662bd7252))

* Clean-up ([`58f855e`](https://github.com/tim83/sshtools/commit/58f855e6d7a6ef355dadb8d810ea47c74a96b5ee))

* Allow python3.8 ([`efb7abb`](https://github.com/tim83/sshtools/commit/efb7abb577ff496c6ffc3705771904621a44f2a5))

* Fix handling None hostnames ([`bbfed59`](https://github.com/tim83/sshtools/commit/bbfed596319c6112b446ad3009a7188f2f703b54))

* Find correct fping ([`91f3bad`](https://github.com/tim83/sshtools/commit/91f3bad10abc0ddfa7e5ef30c8e72a6b11900b7a))

* Improve finding IP addresses and determing local status ([`c3a935d`](https://github.com/tim83/sshtools/commit/c3a935d6a5a6b401ba3b2f8b6fe87e3b7622f529))

* Improve remote execution ([`accf64c`](https://github.com/tim83/sshtools/commit/accf64c43adb63a164e5148a9f56bc7566be778d))

* Clean-up files ([`8eafb41`](https://github.com/tim83/sshtools/commit/8eafb4177b1849d469500904ada980cc2b674948))

* Use poetry for scripts ([`fdbb2dc`](https://github.com/tim83/sshtools/commit/fdbb2dc713561d271311396825eae51b221a3f89))

* Log python version ([`904971b`](https://github.com/tim83/sshtools/commit/904971b6822e62126e12b21860eeaba3d04a76db))

* Fix naming ([`713f25a`](https://github.com/tim83/sshtools/commit/713f25ae85b4bf76df568d57208494df06d00e5a))

* Use poetry ([`79c9479`](https://github.com/tim83/sshtools/commit/79c9479a3e5bb7765cbe6d42ff7a068a966a4697))

* Use string for port ([`f2b2085`](https://github.com/tim83/sshtools/commit/f2b2085e672d954f44c6969e06cb2a0dcf487137))

* Use singleton for device ([`a4d484d`](https://github.com/tim83/sshtools/commit/a4d484dc71e0799a3292bb9587db01bf64e630cb))

* Installed thinkcentre ([`ba18fda`](https://github.com/tim83/sshtools/commit/ba18fda7eec783820c9b00d7b243967197e8655a))

* Separate backup from cache ([`1241416`](https://github.com/tim83/sshtools/commit/12414160de9408be3076af8864b275daa64d741c))

* Use unique backup dir in user home ([`94ea578`](https://github.com/tim83/sshtools/commit/94ea578eb740d64cf363b8b58724d7956fde766f))

* Use full path for sbin tools ([`f2cf4d9`](https://github.com/tim83/sshtools/commit/f2cf4d9a3f2be58f32843dd3c03075fca2898feb))

* Add support for opensuse convention for ifaces ([`93d107c`](https://github.com/tim83/sshtools/commit/93d107c62de5b0ce72715a6e08bf0be1d53bceaa))

* Add thinkcentre p1 ([`5bc495a`](https://github.com/tim83/sshtools/commit/5bc495a4fdf38e3c68c910416bd1db53ba6a342a))

* Add desktop-ben ([`7a1b15e`](https://github.com/tim83/sshtools/commit/7a1b15e105962b0496aed342e1aab2327ac6210b))

* Use ip cache ([`6ec531f`](https://github.com/tim83/sshtools/commit/6ec531fb5a91643c654271d6901a465336fe557c))

* Prioritize local mDNS connections ([`6727156`](https://github.com/tim83/sshtools/commit/672715672bc18076a8f81b8c4925c6c36f7523bc))

* Disable MOSH when using external connection ([`26f5de5`](https://github.com/tim83/sshtools/commit/26f5de505e23c8c703ee8ba906a064032f6c74e8))

* Streamline syncing to non-reachable devices ([`4b3e77e`](https://github.com/tim83/sshtools/commit/4b3e77e29a524dd253b262acfe9ff450125bf5d6))

* Enable multithreading ([`d1a04e9`](https://github.com/tim83/sshtools/commit/d1a04e95f882acb4449b929c3a9cba19785fea7d))

* Include external IP for serverpi ([`f3f64fe`](https://github.com/tim83/sshtools/commit/f3f64fe2a49a2777b0922a49bbc70f9357d4c3dd))

* Allow smount as root ([`c5ea676`](https://github.com/tim83/sshtools/commit/c5ea6762b22b03148af234deff2938844727785a))

* Use mosh with VPN ([`80000ff`](https://github.com/tim83/sshtools/commit/80000ffa997f7fb3777a28f41520ca2b20df0876))

* Set correct sync scope ([`9c2e80a`](https://github.com/tim83/sshtools/commit/9c2e80a9c633da152d3c3ab992b73821e2e5585f))

* Always use VPN instead of public IP ([`25ce47e`](https://github.com/tim83/sshtools/commit/25ce47e5105617c243cae78fc395577c9172cf6b))

* Add kot devices ([`8e1191a`](https://github.com/tim83/sshtools/commit/8e1191a0511bc9313c9e0456e908705c58ff41ed))

* Remove mosh signifiers from vpn ([`fe9a2dc`](https://github.com/tim83/sshtools/commit/fe9a2dc4cadfbfd63596c0adba8224baa4fc64a5))

* Add envy to zerotier config ([`6720065`](https://github.com/tim83/sshtools/commit/6720065f9385c94240c1a58ccb507c3877be11c9))

* Add zerotier config ([`c2836f5`](https://github.com/tim83/sshtools/commit/c2836f5e2b9f7b83f3b6ff9ab0c57ed42fecebc7))

* Add zerotier ([`d6928d1`](https://github.com/tim83/sshtools/commit/d6928d19b8e31b59c88adcc4aa82d2819a92bedf))

* Add laptop to home ([`d5b44f2`](https://github.com/tim83/sshtools/commit/d5b44f2a6ccc781bb2cff5405dc455e58e76f596))

* Update desktop MAC ([`0f246c2`](https://github.com/tim83/sshtools/commit/0f246c20b2567b82bee44fb5c1e2ea99b70c7086))

* Set probook as relay ([`52aad41`](https://github.com/tim83/sshtools/commit/52aad41a5097b2e96514aa05678fc8697a9e0f8e))

* Clean-up ([`4b03d66`](https://github.com/tim83/sshtools/commit/4b03d661b4f2a08edba944309fdaf3af8807d31f))

* Prioritize fujitsu ([`1f456d0`](https://github.com/tim83/sshtools/commit/1f456d0dc92466630e2aed90b6e0ca72eca0fef1))

* Prioritize fujitsu ([`7c6c75b`](https://github.com/tim83/sshtools/commit/7c6c75bca80700bf2a481ea11fc43ac3934c3207))

* Disable proximus for serverpi ([`08b90cb`](https://github.com/tim83/sshtools/commit/08b90cb934044a957ae9952eab9aba6ef101dd1d))

* Include git-credentials ([`327d2dc`](https://github.com/tim83/sshtools/commit/327d2dcde980b090eff0476ba11b8a6f78ce1946))

* Add new.imbit ([`084fac5`](https://github.com/tim83/sshtools/commit/084fac56e5c17a453d1f5e3c95f433936b70ee0f))

* Change order ([`478868d`](https://github.com/tim83/sshtools/commit/478868dbc2ac7cf9c9dd5dce51979d0bc68fcd31))

* Enable sync for fujitsu ([`1f033b9`](https://github.com/tim83/sshtools/commit/1f033b9d0ffc48ba5001e45515f1cf585f6d7d34))

* Add fujitsu and update IPs ([`a435398`](https://github.com/tim83/sshtools/commit/a435398fd09de1a7a13ed15e981046cca92e1910))

* Exclude downloading iso files ([`2c45279`](https://github.com/tim83/sshtools/commit/2c4527933db1c1bd435bb803cdd0f01489f853d2))

* Increment version ([`1ee3aa9`](https://github.com/tim83/sshtools/commit/1ee3aa9622caf928d646c32eb882823e4612d570))

* Increment version ([`692aaee`](https://github.com/tim83/sshtools/commit/692aaeee7e6a4641bf51cf3e97ea83ebd484b884))

* Enable dry run ([`a3b3cdd`](https://github.com/tim83/sshtools/commit/a3b3cddf565ee70d5ad1b550ed44b18f524e1683))

* Only exclude dotfiles in the root dir ([`c6adcf3`](https://github.com/tim83/sshtools/commit/c6adcf3fe070596c187682c480c5dce2eb1f7970))

* Include .gitignore ([`2da4531`](https://github.com/tim83/sshtools/commit/2da45314f27a4b15bce524f855e20a8fec37d49c))

* Include vscode config files ([`834f767`](https://github.com/tim83/sshtools/commit/834f767c9fc1bac62f539819d43b361761b4b787))

* Exclude .raw(.xz) downloads ([`7222738`](https://github.com/tim83/sshtools/commit/7222738b7386cfa75c1777ce46e6e345ee43dfaf))

* Merge remote-tracking branch &#39;origin/master&#39;

# Conflicts:
#	setup.py ([`63613e4`](https://github.com/tim83/sshtools/commit/63613e42615177ee5890bee7ac13521bebc573fa))

* Fix exclude unnecessary files ([`b3f3d2d`](https://github.com/tim83/sshtools/commit/b3f3d2df4f3f94b19cf6d87d8e26c5c252c336ef))

* Fix exclude unnecessary files ([`9b52d60`](https://github.com/tim83/sshtools/commit/9b52d60c7fdda2970b9ed8e7154c5a4320f72870))

* Exclude unnecessary files ([`958c3b3`](https://github.com/tim83/sshtools/commit/958c3b381d0c509a51c076a24f20e3b467dbd7a0))

* Add IPs for different providers for kot ([`89e108f`](https://github.com/tim83/sshtools/commit/89e108f44369ffcbe602f72b049a8b4891838f03))

* Fix includes and excludes ([`d98b94b`](https://github.com/tim83/sshtools/commit/d98b94b4c2f164a44555a5c37aff57a75eea2cd7))

* Fix includes and excludes ([`c89ce3b`](https://github.com/tim83/sshtools/commit/c89ce3b53493719ae552db332307ca8369a07338))

* Fix problems ([`d7c8c8d`](https://github.com/tim83/sshtools/commit/d7c8c8d6eb7761ace7b799bd198ab9b0d893ea89))

* Fix WOL ([`49e0bd8`](https://github.com/tim83/sshtools/commit/49e0bd846f73486cff00faea03be9c52c7eb5aa2))

* Use mosh for IMBIT ([`12d30d3`](https://github.com/tim83/sshtools/commit/12d30d3b84d287189c7edda9035a580023fe3302))

* Fix excluding __pycache__ ([`bf40349`](https://github.com/tim83/sshtools/commit/bf40349c116aad713c48bc3a740ad031b091d716))

* Rename yoga -&gt; laptop ([`ea1a58f`](https://github.com/tim83/sshtools/commit/ea1a58fee232336e4133060055189f2d13e4db6e))

* Update IPs for yoga ([`d0ab689`](https://github.com/tim83/sshtools/commit/d0ab6892c34462fcadccb251b8297166809ae26c))

* Change hostname laptop -&gt; envy ([`d10fb28`](https://github.com/tim83/sshtools/commit/d10fb28006aa6dac76963a0b7e935f7c12d9d4aa))

* Set config dir in home dir ([`a82a79d`](https://github.com/tim83/sshtools/commit/a82a79d3d91923e6fb720da2f1e9244a9d17e18b))

* Don\&#39;t include media ([`9300294`](https://github.com/tim83/sshtools/commit/9300294f3be4e90f1aa2378e2d56ce1a6a1b9d13))

* Include all subdirs of programs ([`52ffcd3`](https://github.com/tim83/sshtools/commit/52ffcd3b7a21551abbe3de949ea8da6ddcc1692e))

* Include all subdirs of important dirs ([`85a0447`](https://github.com/tim83/sshtools/commit/85a04479fc1ee0a7f7806ddcd064e100126ddcff))

* Include all subdirs of Documents ([`280b3e0`](https://github.com/tim83/sshtools/commit/280b3e0ed5a148efc91f8ea8b02021e215fe5431))

* Exclude toshiba &amp; notebook from sync ([`2adbdfe`](https://github.com/tim83/sshtools/commit/2adbdfed8536fb865aa1aa664d794c7a09653d9e))

* Fix including Documenten/pc/config subdirs ([`cd0f0de`](https://github.com/tim83/sshtools/commit/cd0f0deacec0701ced0abcddc07e07a550d7ce82))

* Fix including Documenten/pc/config subdirs ([`6cc7607`](https://github.com/tim83/sshtools/commit/6cc76078d3285621b037ef404f88ceef14ec2221))

* Fix including Documenten/pc/config subdirs ([`35dea1b`](https://github.com/tim83/sshtools/commit/35dea1b0c59cb44d2d6d4499a0f743c795b192fd))

* Fix including Documenten/pc/config subdirs ([`24217f5`](https://github.com/tim83/sshtools/commit/24217f52d49807daeee38c2845172ce492aca537))

* Fix including Documenten/pc/config subdirs ([`6a73136`](https://github.com/tim83/sshtools/commit/6a731360b8797bbd8c998767531890e1c9042ea8))

* Enable using multiple configs &amp; using VPN connections ([`c70406e`](https://github.com/tim83/sshtools/commit/c70406e8d9e48343c6d1af660b57b1834364a131))

* Don&#39;t sync VMs ([`1118f62`](https://github.com/tim83/sshtools/commit/1118f62f6c64853f9d98c55ddcdfe30f1b8d50b9))

* Fix from port ([`3376038`](https://github.com/tim83/sshtools/commit/337603896a538b3c79027fbe0103e073e55a4071))

* Fix from port ([`f7211ab`](https://github.com/tim83/sshtools/commit/f7211aba31713cc346d75260b6a6a72e196374b8))

* Only check mDNS adress when defined IPs are unreachable ([`dc636d9`](https://github.com/tim83/sshtools/commit/dc636d958ad07b2786ebda126d04c3b3497fcb8d))

* Allow for no-ips found ([`d6fd829`](https://github.com/tim83/sshtools/commit/d6fd8292f03674ee3869b4868c72bb54293a8690))

* Fix multiple keys for &#34;127.0.0.1&#34; ([`46c4200`](https://github.com/tim83/sshtools/commit/46c4200d64ac047e6b4eecf6003826d73ea21985))

* Remove camerapi universal port ([`a8aae02`](https://github.com/tim83/sshtools/commit/a8aae025fb38d192d9825838773e0801765b6c1e))

* Increment version ([`f3889c7`](https://github.com/tim83/sshtools/commit/f3889c771632713d93b6da3a9ad280b5b1a4f2dd))

* Enable connecting to mDNS and localhost ([`5d5002b`](https://github.com/tim83/sshtools/commit/5d5002b0a9a885414c2e9f907c2bc4e17717d095))

* Increment version ([`a136db2`](https://github.com/tim83/sshtools/commit/a136db2497b0cf4bfa146e52a67cc7fd7ad4dc2a))

* Rename module ([`bcf059c`](https://github.com/tim83/sshtools/commit/bcf059cd0201c245606b75cdd2f060f22a7f8bcd))

* Configure passable exitcodes ([`a8f2444`](https://github.com/tim83/sshtools/commit/a8f2444f3b804ad629f5dd97e825976d15a9c674))

* Configure passable exitcodes ([`f58f74b`](https://github.com/tim83/sshtools/commit/f58f74bea84a0a960366ef2cb701d6a55d0b7b3d))

* Rename files ([`4b6e99a`](https://github.com/tim83/sshtools/commit/4b6e99a57fb67565f9a2ca3021a5a2c839b94721))

* Exclude VMs from limited ([`18e9e7c`](https://github.com/tim83/sshtools/commit/18e9e7c53aacac61fb285c5fbc776b8d732879f8))

* Exclude VMs from limited sync ([`ee7a9ef`](https://github.com/tim83/sshtools/commit/ee7a9ef708977306ca49578c0e32970cc6794d60))

* Rename files ([`0f3665a`](https://github.com/tim83/sshtools/commit/0f3665a9d48fc71aed09939be62fe09e9e49405b))

* Enable forcing limited sync ([`f143742`](https://github.com/tim83/sshtools/commit/f1437425f6015be5804a19802eab41327104ed4b))

* Add compression and separate dir for partial files ([`7042550`](https://github.com/tim83/sshtools/commit/70425508802bad77744cf900f346774788aa797a))

* Update includes ([`ab90d53`](https://github.com/tim83/sshtools/commit/ab90d53b8eea4ca05a7df0dedd19cb7adfb7c693))

* Update interpreter ([`d392bfb`](https://github.com/tim83/sshtools/commit/d392bfb486ce0981579884e053ed0b292c9703d2))

* Insure the port is a string ([`ce1c9a2`](https://github.com/tim83/sshtools/commit/ce1c9a208b586ea3621719eacc866993f60d29c6))

* Remove unnescesairy includes ([`6005e09`](https://github.com/tim83/sshtools/commit/6005e095f103e3fbb44f0c8f6cdf836b5ba2b2bd))

* Add iomega ([`d02aa8b`](https://github.com/tim83/sshtools/commit/d02aa8b63b2f27f6dfd26ff13075ba5961b9643a))

* Fix local no IP ([`c3ef0ca`](https://github.com/tim83/sshtools/commit/c3ef0ca64ad8c26f46463f82b7e2b268e65a2372))

* Exclude ZSH log ([`5318906`](https://github.com/tim83/sshtools/commit/5318906a780d33970bd5c6d74166929aea92b8be))

* Include config dotfiles ([`0dd3e50`](https://github.com/tim83/sshtools/commit/0dd3e5094fd20e745453ffb5c3bbe2cb2145afd9))

* Add router template ([`786c486`](https://github.com/tim83/sshtools/commit/786c486f9099d0c4441412467f2c1a4d06ac5ae5))

* Install new router ([`581957d`](https://github.com/tim83/sshtools/commit/581957d026c263643b1cfc223aaab5a1caf20896))

* Enable sync for camerapi when local ([`ec17f5d`](https://github.com/tim83/sshtools/commit/ec17f5de98bb78e1193cb48043e9b04450805743))

* Enable sync for camerapi when local ([`913d0c3`](https://github.com/tim83/sshtools/commit/913d0c355b96483c572af9e1571ac75dd5acdbda))

* Handle None ip ([`536c839`](https://github.com/tim83/sshtools/commit/536c8392b9f78eb6c2ddc5f7c6ebaf2b8408afc9))

* Fix workflows ([`7c138ce`](https://github.com/tim83/sshtools/commit/7c138ce8eff6f3b8827601a2c101f59ba36113f4))

* Don&#39;t use link ([`f86e98a`](https://github.com/tim83/sshtools/commit/f86e98afac3328e36da1697a3152771438ae7559))

* Ignore false positive ([`fdb9cb8`](https://github.com/tim83/sshtools/commit/fdb9cb85effb6c331a18fff5bd5c6cd23dec9853))

* Fix workflows ([`0392796`](https://github.com/tim83/sshtools/commit/0392796ec61c9f37cd915f1357fa4cb03c52e664))

* Fix workflows ([`de8e2d2`](https://github.com/tim83/sshtools/commit/de8e2d2a12fcc8167878e5bdfa64d38f073a3405))

* Fix workflows ([`332bb37`](https://github.com/tim83/sshtools/commit/332bb374b010352dc18a753daeec71431a08d629))

* Fix workflows ([`a6b65c9`](https://github.com/tim83/sshtools/commit/a6b65c93eed08c7047a2c3600c67121a0e8f6bc7))

* Update changed IPs ([`a12eb06`](https://github.com/tim83/sshtools/commit/a12eb06b28147c6ee576ab766e35b5df8c58ca3a))

* Fix None ips ([`cc85f39`](https://github.com/tim83/sshtools/commit/cc85f390883e652d52242ea5a5221fe8d2f7c494))

* Fix empty lines being treated as ips ([`7ae1abc`](https://github.com/tim83/sshtools/commit/7ae1abc7ac5754adedbd75c61023f2edb95f0706))

* Fix empty lines being treated as ips ([`62ebea4`](https://github.com/tim83/sshtools/commit/62ebea4487d5c0670accf895c5ea2e9a5f183753))

* Ping multiple ips simultaneously ([`4641940`](https://github.com/tim83/sshtools/commit/4641940b0f5b0372f029741fec1d27b084d194f0))

* Limit sync for pis and enable different ports then 22 for sync ([`2fa5c74`](https://github.com/tim83/sshtools/commit/2fa5c742ff6f65e95994f3e6ffd3a3f2a585e1cd))

* Remove excess excludes ([`a3365e2`](https://github.com/tim83/sshtools/commit/a3365e20957311c7726de2d0b1268225f8c5459d))

* Fix imports ([`2e80d1c`](https://github.com/tim83/sshtools/commit/2e80d1c101904d8feecb205377288330e286a845))

* use __name__ in logger ([`06ead9c`](https://github.com/tim83/sshtools/commit/06ead9c42ddf5189d10d8b1bff69c2f28da2fbdb))

* Fix imports of timtools ([`efcb23c`](https://github.com/tim83/sshtools/commit/efcb23cf1b6c72d433e74312660cf06b8862cda2))

* Merge remote-tracking branch &#39;origin/master&#39; ([`a5a2c70`](https://github.com/tim83/sshtools/commit/a5a2c707f2483c81f2f90a4c6bf5759bec7af150))

* Create pylint.yml ([`7cadf54`](https://github.com/tim83/sshtools/commit/7cadf5465ddcc346ad2d9f58f2c364a3f86899d6))

* Create python-package.yml ([`cf766d1`](https://github.com/tim83/sshtools/commit/cf766d1de390f790d6e026be3895e50c178d02cb))

* Use timtools for execution &amp; make string of port ([`4b54c12`](https://github.com/tim83/sshtools/commit/4b54c1215227ef77484dddf164882d9bb04e75ab))

* Use correct errors when device is not reachable ([`071bb05`](https://github.com/tim83/sshtools/commit/071bb050a6f3a849cd3fc0ea50bea54b20fcc267))

* Don&#39;t print the rsync command ([`d72b86e`](https://github.com/tim83/sshtools/commit/d72b86e6de9a0801d79aaa5ea099280d1cbc9957))

* Add git files ([`679951f`](https://github.com/tim83/sshtools/commit/679951fec3de023ef3916e35c364ae32c9c605b9))

* Reformat en clean up code ([`96d26e6`](https://github.com/tim83/sshtools/commit/96d26e611a48f36348464e8da46f7aaf3232e65e))

* Separate errors ([`662eca5`](https://github.com/tim83/sshtools/commit/662eca59d856e72f8a5126bdebde0e24c143e591))

* Reformat ([`2f39814`](https://github.com/tim83/sshtools/commit/2f39814a5077b58388c0a6a89e03ffc400c094d7))

* Init ([`360c348`](https://github.com/tim83/sshtools/commit/360c348b6134bcd4144e4222bc4f56ea635daf6d))
