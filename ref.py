# def retry(times=3, raise_if_out_of_tries=True):
#     times = max(1, times - 1) if raise_if_out_of_tries else times

#     def decorator(func):
#         def wrapper(*arg, **kwargs):
#             log = Log('meta/', 'monitor')
#             sleep_time = 1
#             for try_number in range(times):
#                 try:
#                     return func(*arg, **kwargs)
#                 except Exception as e:
#                     log.append_msg(
#                         f"Error on function with {times - try_number} retries"
#                         f" left. Sleeping for {sleep_time}. Error: {e}")
#                     sleep(sleep_time)
#             if raise_if_out_of_tries:
#                 return func(*arg, **kwargs)
#         return wrapper
#     return decorator


# ############################################################
# ############################################################
# ############################################################
# ############################################################
# ############################################################
# ############################################################

# import multiprocessing
# import time

# # bar
# def bar():
#     for i in range(100):
#         print "Tick"
#         time.sleep(1)

# if __name__ == '__main__':
#     # Start bar as a process
#     p = multiprocessing.Process(target=bar)
#     p.start()

#     # Wait for 10 seconds or until process finishes
#     p.join(10)

#     # If thread is still active
#     if p.is_alive():
#         print "running... let's kill it..."

#         # Terminate - may not work if process is stuck for good
#         p.terminate()
#         # OR Kill - will work for sure, no chance for process to finish nicely however
#         # p.kill()

#         p.join()

# ...

import stopit
with stopit.ThreadingTimeout(10) as to_ctx_mgr:
    assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
    # Something potentially very long but which
    # ...

# OK, let's check what happened
if to_ctx_mgr.state == to_ctx_mgr.EXECUTED:
    pass
    # All's fine, everything was executed within 10 seconds
elif to_ctx_mgr.state == to_ctx_mgr.EXECUTING:
    pass
    # Hmm, that's not possible outside the block
elif to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
    pass
    # Eeek the 10 seconds timeout occurred while executing the block
elif to_ctx_mgr.state == to_ctx_mgr.INTERRUPTED:
    pass
    # Oh you raised specifically the TimeoutException in the block
elif to_ctx_mgr.state == to_ctx_mgr.CANCELED:
    pass
    # Oh you called to_ctx_mgr.cancel() method within the block but it
    # executed till the end
else:
    pass