from multiprocessing import Process, Manager

def timeout(seconds=1, return_if_timeout=None):
    seconds = max(int(seconds), 1)
    def decorator(func):
        def worker(func, ret_dic, *args, **kwargs):
            ret_dic["return"] = func(*args, **kwargs)

        def wrapper(*args, **kwargs):
            with Manager() as manager:
                return_dictionary = manager.dict()
                worker_args = [func, return_dictionary] + list(args)
                proc = Process(target=worker, args=worker_args, kwargs=kwargs)
                proc.start()
                proc.join(seconds)
                if proc.is_alive():
                    proc.kill()
                    proc.join()
                    return return_if_timeout
                else:
                    return return_dictionary["return"]
        return wrapper
    return decorator
