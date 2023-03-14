lh-platform-integration-service
======================

Example LHRPC service.


Provided API
------------

- `reverse({ text })`


Consumed services
-----------------

None

TODO: connect to account service just as an example?


Persistence
-----------

Database collections:

- `greetings`
- `queues.welcome`


Monitoring
----------

TODO


TODO
----

- readme :)
- add lhrpc client
- add queue processing (dedicated queue + "common" queue for infrequent things)
- add Sentry
- incorporate [loading local conf](https://bitbucket.org/lhprivate/lh-account-service/commits/b267df137bd551c21067ce871c2812eb8b888b0f)
- add [smart sleep check](https://bitbucket.org/lhprivate/lh-account-service/pull-requests/309)
