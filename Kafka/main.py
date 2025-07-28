import sys
if len(sys.argv) > 1 and sys.argv[1] == "producer":
    import producer
else:
    import consumer
