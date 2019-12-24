import daemon

from server import main

with daemon.DaemonContext():
    main()
