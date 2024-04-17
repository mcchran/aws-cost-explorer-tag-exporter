import time
import random
import re

from decorator import decorator
from functools import partial

from utils import DefaultLogger


logger = DefaultLogger()

class AttemptsExceededError(Exception):
    pass


class MaxDelayExceededError(Exception):
    pass


class BlankException(Exception):
    pass


def __retry_interval(
    f,
    exception=None,
    no_catch=None,
    attempts=None,
    max_delay=None,
    backoff_base=None,
    capped_back_off_delay=None,
):
    """Retries the specific operation until it succeeds.
    Raises en error if it runs out of attempts or exceed
    maximum_delay time limit.
    Retry take place on 'exception' while 'no_catch' one breaks will break
    the retry loop raising an AttemptsExceededError.

    Default: retries on any exception while ignoring none of them.

    :param functools.partial f: the actual function call
    :param exception exception: the exception that will trigger the retring
    :param no_catch exception: the exception that is going break the retring
    :param int attempts: the attempts until to give up
    :param float max_delay: the max_delay for caller to wait
    :param float back_off_base: the base of the back off algorithm
    :param float capped_back_off_delay: the cap on delay in increase

    :raises: AttemptsExceededError, MaxDelayExceededError

    :returns: the initial function  call

    :rtype: function call
    """
    exception = exception or Exception
    attempts = attempts or 1
    no_catch = no_catch or BlankException
    max_delay = max_delay or 10
    backoff_base = backoff_base or 1
    capped_back_off_delay = capped_back_off_delay or 4

    logger.debug(
        "Retry setup: "
        "attempts: {attempts}, "
        "max_delay: {max_delay}, "
        "back_off_base: {back_off_base}, "
        "capped_back_off_delay: {capped_back_off_delay} ".format(
            attempts=attempts,
            logger=logger,
            max_delay=max_delay,
            back_off_base=backoff_base,
            capped_back_off_delay=capped_back_off_delay,
        )
    )

    attempt_count = 0
    while attempts:
        try:
            return f()
        except no_catch:
            # in case of requiring no_retry
            raise AttemptsExceededError
        except exception as e:
            logger.warning(
                "Backoff retrying, attempt: {attempt_count} "
                "for {module}.{function}\n with exception: {e}".format(
                    attempt_count=attempt_count,
                    module=f.func.__module__,
                    function=f.func.__name__,
                    e=e,
                )
            )

            attempts -= 1
            attempt_count += 1
            if not attempts:
                raise AttemptsExceededError

            # implementing the capped back off strategy
            suggested_delay = min(
                capped_back_off_delay, backoff_base * 2 ** attempt_count
            )

            # check if we have already attempted with max delay interval
            if suggested_delay >= max_delay:
                raise MaxDelayExceededError

            jitter = random.uniform(0, suggested_delay)
            suggested_delay = (jitter + suggested_delay) / 2
            time.sleep(suggested_delay)


def retry(
    exception=Exception,
    no_catch=None,
    attempts=1,
    max_delay=None,
    backoff_base=None,
    capped_back_off_delay=None,
):
    """Defines the retry decorator

    :param functools.partial f: the actual function call
    :param exception exception: the exception that will trigger the retring
    :param no_catch exception: the exception that is going break the retring
    :param int attempts: the attempts until to give up
    :param float max_delay: the max_delay for caller to wait
    :param float back_off_base: the base of the back off algorithm
    :param float capped_back_off_delay: the cap on delay in increase

    :retruns: a properly configured retry decorator
    :rtype: func
    """

    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        args = fargs or []
        kwargs = fkwargs or {}
        return __retry_interval(
            partial(f, *args, *kwargs),
            exception=exception,
            no_catch=no_catch,
            attempts=attempts,
            max_delay=max_delay,
            backoff_base=backoff_base,
            capped_back_off_delay=capped_back_off_delay,
        )

    return retry_decorator


def url_is_valid(url):
    """ Validates a url being properly formatted or not

    :param str url: the url to validate

    :return: True in case of properly formated
    :rtype: boolean
    """
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        # domain...
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # noqa
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, url)