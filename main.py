import asyncio
import functools
import signal
from aiosmtpd.smtp import SMTP


# 1. Define a minimal handler to log incoming emails
class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"Message from: {envelope.mail_from}")
        print(f"Message to  : {envelope.rcpt_tos}")
        print(f"Message data:\n{envelope.content.decode('utf-8', errors='ignore')}")
        return '250 OK'

# 2. Shutdown function for clean signal handling
def ask_exit(loop, server):
    print("\nStopping SMTP server...")
    server.close()
    # Schedule the loop to stop after tasks clear out
    loop.create_task(server.wait_closed()).add_done_callback(lambda _: loop.stop())

async def main():
    # Get the currently running event loop
    loop = asyncio.get_running_loop()
    
    # 3. Use functools.partial to pass custom parameters to the SMTP constructor
    # Here we enforce a 10MB data limit and disable reverse DNS checks (ident)
    smtp_factory = functools.partial(
        SMTP, 
        handler=CustomHandler(), 
        data_size_limit=10_485_760, 
        ident="MyCustomSMTPServer"
    )

    # 4. Create the TCP server using our partial class as the protocol factory
    # This listens on localhost, port 8025
    server = await loop.create_server(smtp_factory, host='127.0.0.1', port=8025)
    print("SMTP Server running on 127.0.0.1:8025")

    # 5. Add POSIX signal handlers for graceful exit (Control-C / SIGTERM)
    # Note: signal handlers are supported on Unix-like environments.
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, ask_exit, loop, server)
        except NotImplementedError:
            # Fallback for systems without add_signal_handler (like Windows)
            pass

    # Keep the server running indefinitely
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass

if __name__ == '__main__':
    try:
        # Standard way to run the asyncio loop forever in Python 3.7+
        asyncio.run(main())
    except KeyboardInterrupt:
        # Catch block for systems (like Windows) where add_signal_handler fails
        print("\nSMTP Server stopped via KeyboardInterrupt.")