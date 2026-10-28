import subprocess
import asyncio
import sys
from pathlib import Path
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import stop_playwright


def wrapper(process, stop):
    return SimpleNamespace(stop=stop, _impl_obj=SimpleNamespace(_connection=SimpleNamespace(
        _transport=SimpleNamespace(_proc=SimpleNamespace(_transport=SimpleNamespace(_proc=process))))))


class ShutdownTests(unittest.TestCase):
    def test_responsive_driver_is_not_terminated(self):
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=None
        self.assertFalse(stop_playwright(wrapper(process,lambda:None),grace_seconds=0.5))
        process.terminate.assert_not_called()

    def test_stuck_driver_is_ended_using_its_owned_process_handle(self):
        ended=threading.Event()
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=None
        process.terminate.side_effect=ended.set
        def stop():
            if not ended.wait(2):
                raise AssertionError('Driver shutdown was not bounded')
        self.assertTrue(stop_playwright(wrapper(process,stop),grace_seconds=0.02))
        process.terminate.assert_called_once_with()

    def test_stop_error_still_cleans_up_owned_driver(self):
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=None
        def stop():
            raise RuntimeError('connection ended')
        with self.assertRaisesRegex(RuntimeError,'connection ended'):
            stop_playwright(wrapper(process,stop),grace_seconds=0.5)
        process.terminate.assert_called_once_with()

    def test_exited_driver_with_open_pipe_is_closed_on_its_loop(self):
        ended=threading.Event()
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=0
        def stop():
            if not ended.wait(2):
                raise AssertionError('The driver pipe was not closed')
        api=wrapper(process,stop)
        connection=api._impl_obj._connection
        connection._transport._proc._transport.close=ended.set
        connection._loop=SimpleNamespace(is_closed=lambda:False,call_soon_threadsafe=lambda fn:fn())
        self.assertTrue(stop_playwright(api,grace_seconds=0.02))
        process.terminate.assert_not_called()

    def test_transport_is_closed_when_exited_process_handle_was_already_cleared(self):
        ended=threading.Event()
        def stop():
            if not ended.wait(2):
                raise AssertionError('The owned driver transport was not closed')
        api=wrapper(None,stop)
        connection=api._impl_obj._connection
        connection._transport._proc._transport.close=ended.set
        connection._loop=SimpleNamespace(is_closed=lambda:False,call_soon_threadsafe=lambda fn:fn())
        self.assertTrue(stop_playwright(api,grace_seconds=0.02))

    def test_exited_driver_reader_releases_even_when_transport_does_not_deliver_eof(self):
        loop=asyncio.new_event_loop()
        reader=asyncio.StreamReader(loop=loop)
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=0
        transport=SimpleNamespace(_proc=process,close=Mock())
        sdk_process=SimpleNamespace(_transport=transport,stdout=reader,stderr=None)
        connection=SimpleNamespace(_transport=SimpleNamespace(_proc=sdk_process),_loop=loop)
        def stop():
            self.assertEqual(loop.run_until_complete(asyncio.wait_for(reader.read(),timeout=1)),b'')
        api=SimpleNamespace(stop=stop,_impl_obj=SimpleNamespace(_connection=connection))
        try:
            with patch('runtime.threading.Timer',side_effect=AssertionError('A real SDK loop must own its cleanup deadline')):
                self.assertTrue(stop_playwright(api,grace_seconds=0.02))
            transport.close.assert_called_once()
            process.terminate.assert_not_called()
        finally:
            loop.close()

    def test_exited_driver_does_not_wait_on_stale_communicate_pipe_waiters(self):
        loop=asyncio.new_event_loop()
        process=Mock(spec=subprocess.Popen)
        process.poll.return_value=0
        transport=SimpleNamespace(_proc=process,close=Mock())
        async def communicate():
            await asyncio.sleep(10)
        sdk_process=SimpleNamespace(_transport=transport,stdout=None,stderr=None,communicate=communicate)
        connection=SimpleNamespace(_transport=SimpleNamespace(_proc=sdk_process),_loop=loop)
        def stop():
            self.assertEqual(loop.run_until_complete(asyncio.wait_for(sdk_process.communicate(),timeout=1)),(None,None))
        api=SimpleNamespace(stop=stop,_impl_obj=SimpleNamespace(_connection=connection))
        try:
            self.assertTrue(stop_playwright(api,grace_seconds=0.02))
            self.assertIs(sdk_process.communicate,communicate)
            process.terminate.assert_not_called()
        finally:
            loop.close()


if __name__=='__main__':
    unittest.main()
