# CHANGELOG



## v2.0.0 (2024-02-27)

### Breaking

* feat!: trigger major version bump ([`d73bac0`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d73bac069b0cacffe4f9bb10543d3ab3c0ca5c62))

### Unknown

* break: Update router to handle bot commands

This is final transition step to bot commands, instead of @. The router
still reacts to the links, just to trigger update message. When a link
is received bot prints warning message and suggest to use commands. This
functionality must be removed later. ([`15d4e09`](https://github.com/CaptainCucumber/EpicTalesBot/commit/15d4e097d6724f5f70420431f5a182711a31ef5b))


## v1.6.0 (2024-02-27)

### Chore

* chore: Don&#39;t need static methods outside of class. ([`6c14047`](https://github.com/CaptainCucumber/EpicTalesBot/commit/6c140479fbaed06d89ab0430c227389105380a84))

* chore: Push record to cloud table.

It&#39;s getting harder to support a single file, so let&#39;s push the data
to a table. ([`75b8439`](https://github.com/CaptainCucumber/EpicTalesBot/commit/75b84390cd27190fa7ca0bfa2d0a62dd669e2dbc))

* chore: Another iteration on the way to commands

Basic logic to store settings if doesn&#39;t exist and react to auto. ([`c5a9843`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c5a98437818de2d17c8ea09e6ac32ea0ddb4a859))

### Ci

* ci: Shell script to regenerate gettext strings

Automate manual tasks, collect all strings,
merge new strings for all locales. ([`0d0f183`](https://github.com/CaptainCucumber/EpicTalesBot/commit/0d0f1837845c915550f42c2aae4d92cb68780794))

* ci: Storage for chat settings.

Update deployment script to deploy different stacks. Storage uses
different stack to avoid potential distruption of queue stack. Of course
they all must be deployed as a single CF stack. ([`caeb105`](https://github.com/CaptainCucumber/EpicTalesBot/commit/caeb105f20f5d061aae6d139ef4cf401336e77c6))

### Feature

* feat: Use commands to do operations.

Migrate completely to commands rather than mentions. ([`66d3144`](https://github.com/CaptainCucumber/EpicTalesBot/commit/66d3144cbf53b13667e05740921c2c797e34df4a))

* feat: Chat settings.

First interation. ([`76979cb`](https://github.com/CaptainCucumber/EpicTalesBot/commit/76979cb33dc5ba8675c522f6d347fc5712b530a5))

### Fix

* fix: Handle direct bot commands.

A command might be directed to the bot in a group with @botname at the
end. Handle the case. ([`9260cae`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9260caee844b9d6644494b9ea8f510b992e7791b))

* fix: Multiple fixes

- Reply to original link rather than a command.
- Records incorrect attribute address
- Remove references to touch
- Auto transcribe on/off messages ([`f4b6d37`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f4b6d3772f69b7bca55125d9c2fa4e6e87ba272b))

### Refactor

* refactor: Properties instead of functions

Use properties instead of functions in Config. ([`d6a6589`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d6a65892fa18378303f21d57f64834d0b563ce3e))

### Unknown

* Merge branch &#39;settings&#39; ([`ee75a59`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ee75a599f2640b567bc9783930922e60265bf89b))


## v1.5.11 (2024-02-20)

### Fix

* fix: Do not reply to voice messages automatically

This is a temporary fix to avoid transcribing voice messages when
someone replies to a one. Due to a bug the bot automatically transcribes
all voice messages in the group... and it looks like people like it.

This is until the bot has settings page to allows to toggle auto
transcribe ([`a27f15f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a27f15f951ad18253aae889273861070f3acf453))


## v1.5.10 (2024-02-17)

### Chore

* chore: Measure compute time for voice messages.

It should provice user experience, waiting for a message to be
processed per processing type. As well shows if bot can further scale
on CPU ([`c1c69d0`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c1c69d04d89e9243825ab356927759a25f92d8cd))

### Fix

* fix: Post results only all segments are processed

Faster-whisper process audio in segments, meaning results will be
available during aggregation of all segments. So publish metric only
when all segments are compleated. ([`63fda5d`](https://github.com/CaptainCucumber/EpicTalesBot/commit/63fda5d81eeb262d3ec96ecf987d08e557dae79f))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`e32cbd9`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e32cbd9e5f94485e69cc395e123348d1148e2fc6))


## v1.5.9 (2024-02-16)

### Fix

* fix: Clean up progress stickers if any

In case the process was interrupted by an exception, clean up all
left overs user might have in the chat. ([`1fbb394`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1fbb3949fa80c2f9583ce9b8d3f753c0c7fa578a))


## v1.5.8 (2024-02-16)

### Fix

* fix: Safe API methods.

1. Users delete original message before bot completes transcription.
2. Group admins didn&#39;t provide sufficient permissions to post stickers.

In both cases, use safe APIs to keep going and still post the results.
Case 2 must be addressed by posting a warning message with touch. ([`024eb03`](https://github.com/CaptainCucumber/EpicTalesBot/commit/024eb0324c9ad04be03e8b694d0b04924348b37d))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`5f9e862`](https://github.com/CaptainCucumber/EpicTalesBot/commit/5f9e862b320640e1d93cae93de31a73886c42c1c))


## v1.5.7 (2024-02-16)

### Performance

* perf: Run STT model on cpu

Need to scale as much as possible within the machine to reduce cost
with growing number of requests. The plan it to run two services
cpu/gpu at the same time. ([`d6e3fc8`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d6e3fc8cce7ae37bc2e3a19e298af7343f079668))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`0ef78a4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/0ef78a47b9e60e102a353d7b74b804ec38745c0e))


## v1.5.6 (2024-02-15)

### Fix

* fix: Avoid mixing two similar languages.

Looks like GSTT confuses Russian and Ukrainian. Having a lot of negative
feedbacks from users. Need to keep them strictly separate. ([`6b8e7fe`](https://github.com/CaptainCucumber/EpicTalesBot/commit/6b8e7fe2ccc2f1994fb10797ec4d325082cacec0))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`52dae50`](https://github.com/CaptainCucumber/EpicTalesBot/commit/52dae50345ef6770376174d6eff32c9488f12d1c))


## v1.5.5 (2024-02-14)

### Chore

* chore: Push leftovers from refactoring

Add recorder to log messages for future reference. Message is passed
at init time. ([`88bee4e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/88bee4ed45118ac79c454e664b9206b14b6097f0))

* chore: Commands are now processed in dispatcher ([`40e6b71`](https://github.com/CaptainCucumber/EpicTalesBot/commit/40e6b71ef126a3256593bf9ca67114a392368132))

### Performance

* perf: Increase message visibility time.

It might take longer than 60 sec to process a link or very long
voice message. Hire the message for longer to avoice other service
processing it, leading to double result. ([`2b5ee0d`](https://github.com/CaptainCucumber/EpicTalesBot/commit/2b5ee0db684534d7e2c4bbebf6c12615e2d1cfda))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`c09b021`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c09b0214b146f30e317fc3abe9fe41f0c744a906))


## v1.5.4 (2024-02-13)

### Ci

* ci: Grasefully shutting down the service

Finish message processing with `systemctl restart` is received. ([`c223c5c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c223c5ca13decc65fc57a147e3762f7f683e3a1f))

### Fix

* fix: Handle no username case.

Looks like some users might not have a username or bot doesn&#39;t have
access to it. ([`d7f3a94`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d7f3a943cad498abae5236994dda4f874e77345e))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`1fb2f10`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1fb2f10be39b3cabde80de6277dc93fb75a9637d))


## v1.5.3 (2024-02-12)

### Fix

* fix: Reply to commands

The bot didn&#39;t responde to a command. ([`160e7c4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/160e7c47f9300ea19b15b3c205d89dcb73cfa508))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`dcf8375`](https://github.com/CaptainCucumber/EpicTalesBot/commit/dcf8375ab6a3419250187570800330a344fd1ca3))


## v1.5.2 (2024-02-12)

### Chore

* chore: Change package type name to avoid collision ([`7eaaad6`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7eaaad6f2918f015a28f394b11dcece90935743f))

* chore: Don&#39;t use blacklisted groups.

Today we already have a mechanism on API level to prevent message spam. ([`772b852`](https://github.com/CaptainCucumber/EpicTalesBot/commit/772b852e04f02dfd0c756dc0ccbcc8541e596931))

* chore: Remoce dependency on metric logger.

CW metrics work fantastic, so we don&#39;t need local storage for metrics
anymore. ([`cd3ebf4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/cd3ebf40b9c4c891d38d14f8091ee998ab803642))

* chore: Simplify metrics.

Too many dimentions makes metrics aggrigation on backend complicated and
sometimes impossible. ([`2b9cc8d`](https://github.com/CaptainCucumber/EpicTalesBot/commit/2b9cc8d57bfeab22e832e87f98015e0003d391de))

* chore: Finalize move to config file.

Adapt the code to get variables from config rather than environment. ([`c132bfe`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c132bfee558dbb5b1301b5b6d95321d322d91a77))

* chore: Ignore cache directory ([`d70c5ec`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d70c5ec5cdc0b01445079c4cf4d4936ab5128a40))

### Ci

* ci: Move away from environment variables.

User config file instead. The reason to ease maintenance and handling.
It is difficult to keep environment variables in place especially when
process can&#39;t be directly controlled. ([`8a9e5cc`](https://github.com/CaptainCucumber/EpicTalesBot/commit/8a9e5ccf2cab0a65f0365a1dd0ad15d0252b5188))

* ci: Moving from Make to systemctl

The main reason for the move is auto-recovery per process. Although
its possible to implement custom recovery mechanism in Make, it&#39;s more
convinient to use systemctl. ([`bbcd88c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/bbcd88c9bdbc3e750259518feaf34591bf50a1dd))

### Documentation

* docs: Increate log side and retention period.

Too many requests, need larger logs to debug. ([`285787c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/285787c7b32a99e1b9607e9395bed883d11717f6))

### Performance

* perf: Use headless browser for webpage content

Use playwright to download HTML content. It gives much better results
comparing to bs4. Although some pages content is not available. ([`b04b256`](https://github.com/CaptainCucumber/EpicTalesBot/commit/b04b25605c4cb2b9e771696a5f7e584037e1ef32))

### Refactor

* refactor: Finalize switch to sync APIs.

From now on each instance of the bot is a sync single thread. It allows
us to scale within a single machine having multiple threads processing
same message queue.

Why?
- Easy to maintain and test
- Resilience. A faulty message doesn&#39;t shutdown the bot, only one
instance
- Integration with 3rd party libraries that don&#39;t have async. ([`fbf7318`](https://github.com/CaptainCucumber/EpicTalesBot/commit/fbf731883a86a7826ae56fa2a5d8059f3ac0bdfb))

* refactor: Message structure to handle all messages

This is uber structure acts like a dict and
namespace at the same time. Basically it emulates
full class behaviour without haveing a class. ([`b8c712e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/b8c712e15075592b9afd6d43a0c2f6ee81ce9708))

* refactor: Sync Telegram APIs

New set of sync APIs. Unfortunatelly Telegram officially doesn&#39;t provide
sync APIs. ([`d43dcba`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d43dcba360da673f831515c57f00f4ad24d71bd9))

* refactor: Remove all async/await references.

First step to migrate to sync logic. ([`d677b27`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d677b27a4120d39ea85f2fed9856cf77d36fc14d))

### Unknown

* Fix metrics name ([`aa180a4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/aa180a4db60c64452a81add71e6f194ddabc10db))

* Remove redundant tracking system.

This is profiling rather than metrics. ([`12b7475`](https://github.com/CaptainCucumber/EpicTalesBot/commit/12b74753fa0ec61d9dbb196dd3e323585f0a5d0f))

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`ba6c54a`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ba6c54af03fd639b227840bcce23490f764c1d2a))


## v1.5.1 (2024-02-04)

### Documentation

* docs: More info in channel warning message. ([`ebdb7ec`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ebdb7ec8c62cd908f643723438afa83031fc20c9))

### Fix

* fix: Don&#39;t react to commands in channels

There is no commands in channels, at least not officially. In case the
bot sees one, just ignore it in the channel ([`8e8f7bf`](https://github.com/CaptainCucumber/EpicTalesBot/commit/8e8f7bfbaa12aedf30f51e9e2baaccd1b2f1bed0))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`bb9ca75`](https://github.com/CaptainCucumber/EpicTalesBot/commit/bb9ca752bee39c1a0125b40bfb3123845c6303cd))


## v1.5.0 (2024-02-04)

### Ci

* ci: Start process metric.

It counts how many times the bot restarted. It means it encountered
unrecoverable exception.

Fix name space typo. ([`35876c9`](https://github.com/CaptainCucumber/EpicTalesBot/commit/35876c935471cc457d8fdcbeeb6111ae4bb6e4fa))

### Feature

* feat: Tell users the bot doesn&#39;t support channels.

Show the message only once and never again (reply on touch). Give two
links to support account and bot channel. ([`1424b60`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1424b60920b7687821360e24c42d1bb77be1c77a))

* feat: Touch is a cache to mark message.

When the bot need to send one and only one message. ([`a657104`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a65710483989bb6d26585aba77fb6697aac8f1ad))

### Unknown

* No comments :( ([`7582aa3`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7582aa312f1fa64f2ad8b6622213851c2885a02f))

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`9fb4b20`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9fb4b20c0b77a5e55442f1c079e4987acfa9ba5c))


## v1.4.1 (2024-02-03)

### Build

* build: Embrase and adopt black ([`d7f3d73`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d7f3d73176ee6b4b9cf1b8772271066441ee8f30))

### Ci

* ci: Metrics for commands

Version, Start and the rest goes to unknown. ([`f1dd97c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f1dd97c21a9bd061efa42f472850795d1e0ead8d))

* ci: Emit CloudWatch metrics.

Basica metrics for CW to understand the load. ([`f479353`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f479353ae8d70cf414251f77c047b92b08c21463))

### Fix

* fix: Incorrect imports

Pushing too fast! Need to slow down! ([`dac9483`](https://github.com/CaptainCucumber/EpicTalesBot/commit/dac94835ca63bd718a48fe85866f67724de90d93))

### Unknown

* Chat and use data in metrics.

Should help to understand bot usage. ([`6064f6f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/6064f6f3023efd0e53c5c24bd05b208d7c5637cb))

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`400a003`](https://github.com/CaptainCucumber/EpicTalesBot/commit/400a0037e350ed0b3bcfba4b24b55be93ec5a807))


## v1.4.0 (2024-02-01)

### Feature

* feat: Google STT integration.

The bot falls back to Google STT when the main GPU is busy. It helps to
process the request at low cost when the bot exhausts all resources. ([`e5ae7c2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e5ae7c28c4d1a77b629ec8304f617fd8448dcaf5))

### Fix

* fix: Split very long messages to multi texts

Split extra long messages to multi messages one after another. Post
separate warning message at the end if audio exceeds 5 mins. ([`08158bf`](https://github.com/CaptainCucumber/EpicTalesBot/commit/08158bfcc4ad4b2263618d69bff3a49a51078c46))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`5485949`](https://github.com/CaptainCucumber/EpicTalesBot/commit/54859494219cf97b6da68792c99439ca9d91b405))

* Minor adjustments.

Google dependency is missing and remove unused imports. ([`ab66167`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ab66167fb56538baf300c78428c0338ae005c1f3))

* Print full function name with class.

For better data analysis print full func name. ([`ce7c702`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ce7c7020ca86807940f6fc14f3a9786160cc12d1))


## v1.3.1 (2024-02-01)

### Chore

* chore: Increase summary limit to 250 words

For both acticle and video summary. ([`d9e9cd1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d9e9cd11a68a012cee2fc4a56ea8b9a0af173f4a))

### Fix

* fix: Shorter very long voice messages.

For voice messages that translates to more than 4096 characters, limit
to 4096. This is temporary fix and should be replaced with multi
message repsonse. ([`403f1cc`](https://github.com/CaptainCucumber/EpicTalesBot/commit/403f1ccff0026db481aabf6e774ea9c80945524f))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`e17ae27`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e17ae272297d721320a7fecf9a3d746d9453c177))


## v1.3.0 (2024-01-31)

### Ci

* ci: Publish tags.

Revome debug ls command and publish tags. ([`751fac1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/751fac19b5ca7cccf5424493630460c2d59b1c1c))

* ci: Pass task count to parent make process.

Since make is called recursively, send task info to parent to parallel
it. ([`fc08d1b`](https://github.com/CaptainCucumber/EpicTalesBot/commit/fc08d1b3fa26854c87ea486123c211454e89317e))

* ci: Agressively keep voice process alive

Bot use a single thread to process voice messages, so must be kept alive
at any cost. ([`755f3bb`](https://github.com/CaptainCucumber/EpicTalesBot/commit/755f3bb551df7c162a166cc00e10d8ee875a546f))

### Feature

* feat: Tune in models for video and articles.

This is a basic tune in. Less improvisation, strictly follow the rules.
Rules are passed as a system role, helps GPT better interpret it. ([`f5fd5a7`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f5fd5a79219f693c7e188ac951459d5e24e97491))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`98c4f2f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/98c4f2ffb14e8cbbc40693e2015a1b1ac9983900))


## v1.2.2 (2024-01-31)

### Fix

* fix: Handle none text messages.

Avoid throwing an exception when message is a sticker or animation. Do
not look for a bot name there. ([`28d66f7`](https://github.com/CaptainCucumber/EpicTalesBot/commit/28d66f7d4902c0deee03ac55b537f23679fc8f1f))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`f5f0a66`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f5f0a66de27c25b65f7322d8897f296808a1b467))


## v1.2.1 (2024-01-30)

### Fix

* fix: Must check if text is even exist.

This caused a lot of issues. Need integration tests. ([`790ac24`](https://github.com/CaptainCucumber/EpicTalesBot/commit/790ac24933d230da058db7a93dcc2483ae88b642))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`eb76bdf`](https://github.com/CaptainCucumber/EpicTalesBot/commit/eb76bdfcd64bc63da4a5c3ff80c65bf11e4c1964))


## v1.2.0 (2024-01-30)

### Build

* build: Run the app using run.sh only

Include make into run to keep consistent and don&#39;t forget to generate
locales. ([`720e2e4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/720e2e4daa691b29939dc473a72a438d0db9e654))

### Ci

* ci: Update version in file and GitHub

The config and command line should update the file and GitHub version
at the same time. ([`1f5a0b4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1f5a0b4d0c2232a5eb0a7f1d18abadc67592cf09))

### Documentation

* docs: Update localization text for commands ([`ec81a3f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ec81a3f71fc963ff2235c7d46589a7df562ff662))

### Feature

* feat: Two commands /start and /version

Shows usage and bot version respectfully. ([`a77bcf8`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a77bcf8f85a3f8ff6c5f7e1d731813c21021adec))

### Fix

* fix: Catch all message processing exceptions.

This is a temporary fix for exception handling, cause it excausts pool
of running instances. ([`3f8d7cd`](https://github.com/CaptainCucumber/EpicTalesBot/commit/3f8d7cd76e5b3f4d016855ac922a99358eda845b))

### Unknown

* Add process id into each log line.

Multiple instance write into a single file and it helps to separate
them. ([`23d3277`](https://github.com/CaptainCucumber/EpicTalesBot/commit/23d32779f235c3f7cc9e645f89a5fbc2f78455cf))

* doc: Documentation for new commands. ([`91ad2ca`](https://github.com/CaptainCucumber/EpicTalesBot/commit/91ad2cad0b13ee911b2c72206ab4fdc7a84daf1d))


## v1.1.0 (2024-01-30)

### Build

* build: Careful do not push keys

Adding Makefile to ignore list. It must contain sensitive keys to run.
If changes needed in the file, force push it. ([`c17fdfb`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c17fdfb512086b79b7d8571404aec45a1cd68746))

* build: Make target to run processes in parallel

There is a tool called `parallel` that suppose to handle multiple
processes run in parallel. It has a bunch of neat features, but
debugging an issue was too hard.

Good old make can run the same processe in parallel, easy to use and
set up. However, it can&#39;t run same multiple target cocurrently, so
there is a workaround to make as many targets as processe needed.

WARNING! User tabs in make file, spaces messes things up! ([`9a3f556`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9a3f5564645ea7d4ce6af543eae0dee4fd63ef9e))

### Chore

* chore: Move from API -&gt; SNS to API -&gt; Lambda

It takes too much time to debug API -&gt; SNS integration. Let&#39;s
stick to API -&gt; Lambda -&gt; SQS for now. ([`4ad38ff`](https://github.com/CaptainCucumber/EpicTalesBot/commit/4ad38ffb76fe847ac490dab3ce6a66e57e443547))

* chore: Message routing and deployment scripts

API -&gt; SNS -&gt; Filter -&gt; SQS
                    \-&gt; SQS

This is high level routing logic. Get the messasges to SNS filter them
by type and send to different SQS queues for further processing. ([`7146fb9`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7146fb92692f2d354b2455442c6506cb8ee0bf30))

* chore: Semantic release bump support

Automatically bump version based on git commit message. Must update
bot/__init__.py file as well. Ideally executed as GitHub Action. ([`a0fa3b8`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a0fa3b8fbea046724e51f378403d6a92a94066cf))

### Ci

* ci: Enable/disable stt

Allow to disable or enable STT using command line. ([`57e4990`](https://github.com/CaptainCucumber/EpicTalesBot/commit/57e4990640beb1bad01afde02473804cb80f3cd2))

* ci: DLQ for failed processed messages.

After 3 times the message goes to DLQ ([`9a8a222`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9a8a222c05e539378237dbec8d743efadc1f138a))

### Feature

* feat: Move messages to DLQ if fail 3 times

Avoid stuck messages that bot failed to process due to exception and
move them to DLQ ([`923a811`](https://github.com/CaptainCucumber/EpicTalesBot/commit/923a81198e14dbdc7dd09860fa71cc70dad877c7))

### Fix

* fix: Delete progress sticker before posting result

Progress sticker is shows when the bot prosesses the message. Delete it
when response is ready. ([`c3449b5`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c3449b514439bbfc6fe8f3911cc7fd49c15b07b9))

* fix: Accessing bot cause exception

Due to fake initialization accessing the bot throws an exception. This
is a hot fix! ([`70f36a5`](https://github.com/CaptainCucumber/EpicTalesBot/commit/70f36a5e1839413da73d6032b55f756e876eaf15))

* fix: Missing permission

Add missing permissions to voice queue. ([`f5b2961`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f5b29616234f99982b7fc1a4cc1e2cf143f57668))

* fix: Forgot to import logging.

Router failed due to a missing import. ([`09b36e4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/09b36e48110f2753da32cbc6f70f1c845d4d9eff))

### Performance

* perf: First version to support multithreading

It improve overal performance to handle multiple messages at once. ([`ef65491`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ef654915eb908c6228c5844d00a2b6b8d1fad675))

### Refactor

* refactor: Split the logic into 3 different files.

Easy to handle and logically groupped. ([`7464bdb`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7464bdbc49d8aafb27d3c3a01037271fcfe5fb1f))

* refactor: Break main int two separate files.

Keep threads and consumer logic in main.py but the rest in messages.py ([`74ed56e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/74ed56ef8db3bd6e23273a3280eae0a0e18bf7fb))

### Unknown

* Clean up and improve logging.

Avoid spamming log messages and add exta line to follow message
processing logic. ([`3d934c2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/3d934c28c53fab770e0a75fc70719987221ea041))

* Dump the message when there is an exception

Need it only when fail to proccess. ([`c24ecd5`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c24ecd5c19b4c11430243e9f165ada0cea082180))

* BREAKING CHANGE: Change message pulling logic

Instead of pulling messages from Telegram directly, rely on messages
accumulated in SQS queue. It is part of effort to highly optimize
message processing by breaking odwn functionality into separate
independent apps. ([`227bf0b`](https://github.com/CaptainCucumber/EpicTalesBot/commit/227bf0bb1c1ec5f81a46b19de4ef7d5c33635707))

* Merge branch &#39;multithreading&#39; ([`33e8386`](https://github.com/CaptainCucumber/EpicTalesBot/commit/33e8386203e7c0c39e5e02afb676d23caefc3d99))

* Update version_bump.yml

Trying to find the config file. ([`c2885df`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c2885dfaeaa5589db2bf9f39f01d51b582dd0c8d))

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`d448306`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d44830605ff86c30cd6c7f78d05c77ee0a895895))

* Create version_bump.yml

Bump the version based on semantic-release ([`9a39a5e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9a39a5e0d54303312556f1785a9796f4d37afc8f))


## v1.0.0 (2024-01-24)

### Unknown

* Merge branch &#39;main&#39; of https://github.com/CaptainCucumber/EpicTalesBot ([`ba35d5f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ba35d5fcb7d1f318d64f558485beedfdf8ae95d2))

* Add Youtube Shorts into supported videos.

Subtitles structure same as youtube videos. ([`f9586aa`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f9586aa490f78500db70ba4e0babc77f60b77103))

* Validate if receive message has text.

This happens when the bot receives animation instead of text. ([`7ebad6e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7ebad6e29eea499c4106e8538074b3ff14f6ffdc))

* Don&#39;t store intermediate results.

Pass wav data directly to faster-whisper. ([`d7459e9`](https://github.com/CaptainCucumber/EpicTalesBot/commit/d7459e99be1198b492e8a39b4f3b7508baa86472))

* First version to migrate to faster-whisper ([`e4d796e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e4d796e25b7a761693c24251d4fd64eaf52457e7))

* Handle errors with no update.

The root cause is still under investigation, but at least it helps to
throw an exception. ([`e006f25`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e006f25b93e5967aa65bea64b426b19fd30bf300))

* Show progres emoji.

Show animated emoji as a progress. When results arrive, delete the
emoji and post results. It is not ideal solution as it cause messages
to move, but at least it gives a progress view. ([`42cd7b1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/42cd7b12d420d0d46e5109baf8ea35cec39b2dc3))

* Include word limit for summary and force formating ([`67795f0`](https://github.com/CaptainCucumber/EpicTalesBot/commit/67795f024e39e0858ce89e4e0ad3437ccfd0f35c))

* Write metrics into separate file

We don&#39;t need real-time metrics so far, keep them in a file. Cache
and internal exception handling might mess us big picture. ([`8470fac`](https://github.com/CaptainCucumber/EpicTalesBot/commit/8470fac1e054f9ccf7efddbdb88795039b4b82b7))

* Change max voice message length to 5 mins. ([`4b23fcf`](https://github.com/CaptainCucumber/EpicTalesBot/commit/4b23fcf2c52ed96d53269057dfb28766b5599605))

* Safely handle errors during article summary.

There are too many cases when users send links without articles. Catch
those cases. As well grasefully catch generic errors to let users know
the bot is working but there is a but. ([`37d9443`](https://github.com/CaptainCucumber/EpicTalesBot/commit/37d9443ebc45a27dfbca813087cf49299b908b46))

* Start command sends usage.

It doesn&#39;t fit into bot desctiption so send it after /start command.
As well it&#39;s a good reminder for users. ([`60d25f1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/60d25f138792f4868c645b0e42070f6375d60a9a))

* Clickable button.

Finally figure out to add a clickable button to the page. It needs some
love and design. ([`632b7f1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/632b7f133ad5c46dc879a657ba684c2f28574ea7))

* Fix video summary.

It looks like auto-generated or not subtitles have language in
&#39;languageCode&#39;. Instead of falling back to auto-generated look for
supported language subtitles and return then. ([`75bd63f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/75bd63fbfd096c09b603ae5f4105ed6bc4983371))

* CloudFormation for hosting website.

First create a stack to serve the webpage then sync S3 bucket with
public folder content. ([`ece1774`](https://github.com/CaptainCucumber/EpicTalesBot/commit/ece1774645947c875c8aa1dff855a7b8ab9891f7))

* Add caching operation.

Return results fast when multiple users ask for the same operation. ([`4ed6ce2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/4ed6ce2df1c80787aa4f024a224c6af28a04b923))

* Remove the icon from the button.

Remove the icon because it causes to many visual issues on the page.
Instead use simple button and prepare the page for release. ([`a5a57f9`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a5a57f92be8f99570049def04e01864ab7ff19a2))

* Landing page initial commit. ([`8751d12`](https://github.com/CaptainCucumber/EpicTalesBot/commit/8751d12a4fd44f969974340dfd2cfdcdbb8ab4d7))

* Fix incorrect closing tag. ([`5c96a32`](https://github.com/CaptainCucumber/EpicTalesBot/commit/5c96a329ac10a3240cf21fd76edae0bbf2092ce3))

* Error extraction script.

Use monit on local machine to check application.log file and alarm on
ERRORS. Since monit configuration language is limited, instead keep
the extraction logic in a separate script. It sends error line and 5
previous lines into Telegram support channel. ([`0251de6`](https://github.com/CaptainCucumber/EpicTalesBot/commit/0251de6741e579c7c980a12b5bc3fa71f5edafa1))

* Use HTML instead of Markdown.

Markdown cause a lot of issues with unescapped characters with a
certain sequences. Instead of catching all of them, let&#39;s rely on HTML
to highlight key points. ([`142f9ec`](https://github.com/CaptainCucumber/EpicTalesBot/commit/142f9ec922573ed217a5bcf5736b441df4b7c28d))

* Handle Bad Gateway errors.

Receive no context messsages from Updater during Bad Gateway. ([`bf23467`](https://github.com/CaptainCucumber/EpicTalesBot/commit/bf23467268ce40501f4c501946a16471fa8cbd61))

* Add error handler.

Log when the bot can&#39;t process a message. ([`b055e48`](https://github.com/CaptainCucumber/EpicTalesBot/commit/b055e4892af18ebfeef2e989c95e3e632e6cd057))

* Change log level for httpx

Avoid displaying Telegram token in logs. ([`f16d45f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/f16d45f10076682f3b26108bb71e28b10fe304e2))

* Add support for private chats.

User can send links and voice messages directly to the bot and it will
do the action. No need for mentioning bots in private chats. ([`29018c4`](https://github.com/CaptainCucumber/EpicTalesBot/commit/29018c45abd1338960a2913c03529491c223b294))

* Filter blacklisted groups.

We are open to public. Only leave blacklisted gorups. ([`a91c51c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a91c51ced48780f80fed592f6dfae4318096ca0f))

* Keep .mo files up-to-date when run the script.

Just to avoid human error. Compile the files before the start. ([`94f683f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/94f683f816e8475e82e358f220a0b4d04a4f0025))

* Introduce localization.

Ok, it&#39;s a plain old `gettext`. Not an ideal solution, because it
doesn&#39;t localize at runtime. It might be ok if each localization is
handled by a separate bot instance. But it might be too expensive to
host it. So far gettext covers all usecases. ([`1f9f03c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1f9f03cc51ec780e6f14549c1296682a5fabf2dc))

* Support for YouTube videos.

When a user provides a link to a YouTube video, download subtitles and
summarize them the same way we do an article.

Although Google provides YouTube APIs it adds complexity to auth calls
to YouTube. It requires to build a consent screen for the app, show it
to a user and only then get a key. It can be done once and the key saved
for later, but GC is glitching and I wans&#39;t able to pass it through.

Instead the bot will crawl the page and extract a link to subtitles from
it. It doesn&#39;t require credentials for public content. We might switch
to YT API later. ([`aef0841`](https://github.com/CaptainCucumber/EpicTalesBot/commit/aef0841c2f1856765c2d2bdac19e6d25d1274591))

* Update to small model.

It gives much better results, but eats CPU at 100%. We are at very low
usage, lets stick to small so far and see how it goes. ([`9e37072`](https://github.com/CaptainCucumber/EpicTalesBot/commit/9e3707243b2390b6ca98d3544cbdcbe93c382d93))

* Transcribe only first 60 seconds of voice message.

Introduce the limitation to avoid system abuse. ([`b929ad2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/b929ad2fbd22ac9a28bafd8c8517ea5c026629d8))

* Centralized logging.

Have one place to config logs across all files. Print logs into the
console and in a rotating file. ([`61ed59d`](https://github.com/CaptainCucumber/EpicTalesBot/commit/61ed59d02168789e0c321a99ab215c7bb9af31ff))

* Contextialize text after STT.

Even Whisper doesn&#39;t give us quality text. Let&#39;s cheet a little and
polish it using ChatGPT. Ask to improve the text to make it readable.
Tune the model to have minimal changes to original text. ([`a5069ce`](https://github.com/CaptainCucumber/EpicTalesBot/commit/a5069ceee64b1051c60a1b85a682bf11c47151b4))

* Print audio transcript in italic ([`b52cf1e`](https://github.com/CaptainCucumber/EpicTalesBot/commit/b52cf1eaa037696407c1919feb5ed6fcca0c05d5))

* Buy buy Google Speech-to-text and welcome Whisper

Having so many problems with Google STT and spacy together to get
proper contextualized response. I&#39;d rather use Whisper API. Althought
it&#39;s much more heavyweight and requires separate libraries installed
on the machine, the final result is so much better.

Maybe one day we can port back to spacy and Google STT to reduce cost. ([`07fa82c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/07fa82cb1ed0687a9aedd4e03281736f3243f95f))

* Adapting the package to run on a server

Converting to a server implementation rather than serverless. We have
a free instance now to run the bot. Debugging is better, testing is
better, life is better with a server implementation. ([`e184946`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e1849468c126fab18392fb6e06031bd520eb00f1))

* Add support for Markdown messages

Improve prompt to avoid using brackets and use Markdown for highlights ([`2cac7c5`](https://github.com/CaptainCucumber/EpicTalesBot/commit/2cac7c57e9aea164b34f4739b52bc2ca18f7b0c6))

* Fix a bug when reply contains more than a link.

This is a bug when bot parses a message that contains more than a link.
Make sure we only grab the first url. ([`e72cba2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/e72cba2b3a522fed4c983de5da39c81d1008fb3c))

* Replies to the original message.

Slightly refactor the code to avoid pilling up everything into a
single function

- close #3 ([`5635576`](https://github.com/CaptainCucumber/EpicTalesBot/commit/56355764e80f0c767d5d5eb77a2e109350b37981))

* Integrate with GPT, add article summary.

If the bot is tagged in a message with URL, download the content,
parse it and process though ChatGPT to get the summary.

Design choice: Let all integration classes handle download functionality
rather than building it outside of the class. It allows classes to
represent high level functionlity. ([`22e412c`](https://github.com/CaptainCucumber/EpicTalesBot/commit/22e412c2a5c5ecc3c6d5aa56489799166be44cf7))

* Move Speech-to-text functionality into a class

Keep things organized. Move SST to a separate class. It will grow into
features later.

Config file is now independent from os.environ, but still reads from it.
It helps to inject dependencies into it later. ([`68a456f`](https://github.com/CaptainCucumber/EpicTalesBot/commit/68a456fe08141e7e5c1de8991e9d6ed92ea9151e))

* Combine validation logic. Whitelist another chat.

Combine message handling and access logic together. Otherwise Telegram
won&#39;t call second handler if filters overlap.

Add log rotation. ([`264ecda`](https://github.com/CaptainCucumber/EpicTalesBot/commit/264ecda571e066ea29b39362ac13af48f773a4fe))

* Leave unapproved channels

Validate access to chat per message basis. Since we don&#39;t know if anyone
has already added the bot to the channel. ([`7d0a8e2`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7d0a8e2c3dd4729a748e1f6f938a9814cbab4156))

* Adapting the package to run on a server

Converting to a server implementation rather than serverless. We have
a free instance now to run the bot. Debugging is better, testing is
better, life is better with a server implementation. ([`2ba093a`](https://github.com/CaptainCucumber/EpicTalesBot/commit/2ba093a9885f0413cb69412288436a23306e71a1))

* Support multiple commands

Add support for multiple commands and leave a placeholder for a future /transcribe functionality ([`c8714bc`](https://github.com/CaptainCucumber/EpicTalesBot/commit/c8714bc8d46c0115763d426efe3189e6f76efc64))

* Introduce versions for Lambda code

The template uploads each version to S3 and relink it to Lambda and
APIs. ([`5a8ed19`](https://github.com/CaptainCucumber/EpicTalesBot/commit/5a8ed193edc60e1eca6a403ec4cf2f567df693ec))

* Learn the bot to reply with phrases

Instead of boring invalid URL return a cheesy phrase. ([`7240df1`](https://github.com/CaptainCucumber/EpicTalesBot/commit/7240df191742e37526e5318007265cb6f9b80812))

* DO NOT COMMIT keys!

Keep them local. Check your .gitignore works properly. ([`1ac342a`](https://github.com/CaptainCucumber/EpicTalesBot/commit/1ac342a0dc8855d964d060796313839a7c5ca000))

* Change EOL from \r\n to \n for all files.

Keep then Unix style. ([`8f26563`](https://github.com/CaptainCucumber/EpicTalesBot/commit/8f26563e6c09f3845351604605f88a6fef09d6d5))

* Pass keys as environment variables.

Lambda reads API keys in run-time from local environment. CloudFormation
passes variables from local `config.env` file to CloudFormation stack
and Lambda environment. ([`6bba994`](https://github.com/CaptainCucumber/EpicTalesBot/commit/6bba994b2ae336ff9b2ba6412741455ac3037de8))

* config.env must be excluded from commits

ONLY commit it with blank variables. Keep a copy with real keys on the
local machine. ([`bf82613`](https://github.com/CaptainCucumber/EpicTalesBot/commit/bf82613fece13b47a012829cf04c8c900a52968f))

* Initial commit ([`eb9f3c8`](https://github.com/CaptainCucumber/EpicTalesBot/commit/eb9f3c8aa2cc25bcbc233aa63d8ab6dcaf4c6e85))
