import asyncio

from telethon.sessions.sqlite import SQLiteSession
from telethon.network.connection.connection import Connection
from telethon.errors.common import InvalidChecksumError, InvalidBufferError



def _update_session_table(self):
        c = self._cursor()
        # While we can save multiple rows into the sessions table
        # currently we only want to keep ONE as the tables don't
        # tell us which auth_key's are usable and will work. Needs
        # some more work before being able to save auth_key's for
        # multiple DCs. Probably done differently.
        c.execute('delete from sessions')
        c.execute('insert or replace into sessions values (?,?,?,?,?)', (
            self._dc_id,
            self._server_address,
            self._port,
            self._auth_key.key if self._auth_key else b'',
            self._takeout_id
        ))
        self.save()


async def _recv_loop(self):
    """
    This loop is constantly putting items on the queue as they're read.
    """
    try:
        recv_l = 0
        while self._connected:
            try:
                data = await self._recv()
            except asyncio.CancelledError:
                break
            except (IOError, asyncio.IncompleteReadError) as e:
                if recv_l == 5:
                    break
                recv_l += 1
                self._log.warning('Server closed the connection: %s', e)
                await self._recv_queue.put((None, e))
                await self.disconnect()
            except InvalidChecksumError as e:
                self._log.warning('Server response had invalid checksum: %s', e)
                await self._recv_queue.put((None, e))
            except InvalidBufferError as e:
                self._log.warning('Server response had invalid buffer: %s', e)
                await self._recv_queue.put((None, e))
            except Exception as e:
                self._log.exception('Unexpected exception in the receive loop')
                await self._recv_queue.put((None, e))
                await self.disconnect()
            else:
                await self._recv_queue.put((data, None))
    finally:
        await self.disconnect()



def mon_patching():
    SQLiteSession._update_session_table = _update_session_table
    Connection._recv_loop = _recv_loop