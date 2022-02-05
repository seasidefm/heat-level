## Heat Level
This is the "like counter" framework for the SeasideFM live streams.

This is a small part of a greater whole, so here's how this fits in:
- User calls `?fave` in Twitch chat
- Botsuro process intercepts, logs fave to DB
- Botsuro publishes to MQTT topic
- Heat Level process receives message, gets new like count from DB
- Heat Level process publishes to MQTT topic with like count
- Python process running on stream computer receives message, sets file content
- Streamlabs OBS sees file update, displays "🔥HEAT LEVEL: 7" or similar on screen.

### Why this approach?
Surely it would be easier to just have a single python script poll a DB for changes right?

Well yes. BUT I'm trying to minimize the CPU footprint on SeasideFM's stream, so we're offloading as much as we can to a
separate process. MQTT is perfect for this, as the whole point is to have low overhead communication for IoT. I'm just
interpreting things a little differently.

MQTT also opens the door to some interesting, very interactive live stream opportunities in the future. What those might
be, I'm not yet sure. But it's low enough overhead I don't mind if it doesn't go anywhere.

The ultimate reason is: I get another excuse to run stuff on my Pi cluster :)

### How to run
To be clear, this is pretty environment-specific, but if you want to do something like this,
or you are me from the future trying to redeploy (hello!), here's the steps:

**Note that I will _not_ be covering production docker-compose hosting.**
1. Get a kubernetes cluster. I use a Pi 4 cluster personally.
2. Copy `kubernetes/example-secret.yml` to `kubernetes/heat-level/secret.yml` and populate the DB connection
3. Run `kubectl apply -f kubernetes/mqtt`
4. Once those are all up and healthy, run `kubectl apply -f kubernetes/heat-level` (you can probably do both at once, but
there should be less of a chance for failure with separation)

That's it!

Assuming you have a publisher actually creating events, you can now run the included `filt-writer.py` on your target machine, and as long as your IP addresses are set
properly, you'll receive HEAT LEVELS!

### Like what you see?
Hire me! Here's my [Angel List profile](https://angel.co/u/douglass-hooker)