.PHONY: message_queue1 message_queue2 message_queue3 message_queue4 message_queue5 voice_queue1 runall

message_queue1:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url1 .venv/bin/python ./bot/main.py

message_queue2:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url1 .venv/bin/python ./bot/main.py

message_queue3:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url1 .venv/bin/python ./bot/main.py

message_queue4:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url1 .venv/bin/python ./bot/main.py

message_queue5:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url1 .venv/bin/python ./bot/main.py

voice_queue1:
	TELEGRAM_TOKEN=token1 OPENAI_KEY=key1 MESSAGE_QUEUE_URL=url2 .venv/bin/python ./bot/main.py

runall: message_queue1 message_queue2 message_queue3 message_queue4 message_queue5 voice_queue1
