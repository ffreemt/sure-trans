"""Define sure_trans."""
from random import choices

import translators as ts
from about_time import about_time
from logzero import logger

# from translatepy.translators.deepl import DeeplTranslate
from tenacity import retry
from tenacity.stop import stop_after_attempt, stop_after_delay

_ = '''
dtr = DeeplTranslate()

def deepl(
    text: str,
    from_language: str ="auto",
    to_language: str ="en",
) -> str:
    """Wrap translatepy's deepl."""
    try:
        res = dtr.translate(
            text,
            destination_language=to_language,
            source_language=from_language,
        )
    except Exception as exc:
        logger.error("translarepy DeeplTranslate dtr.translate error: %s", exc)
        raise
    try:
        out = res.result
    except Exception as exc:
        logger.error("translarepy DeeplTranslate deepl res.result: %s", exc)
        raise

    return out
# '''  # does not quite work after a few requests


@retry(stop=(stop_after_delay(10) | stop_after_attempt(5)))
def sure_trans(
    text: str,
    from_language: str = "auto",
    to_language: str = "en",
) -> str:
    """Wrap [ts.deepl, ts.baidu, ts.google] etc. with tenacity.

    s = "书中自有黄金屋"
    not working: sogou; translate_html papago iflytek bing alibaba yandex niutrans mglip
    OK: caiyun, iciba argos  reverso
        tencent, baidu itranslate

    # getattr(ts, "google")
    deepl = [ts.deepl]
    _ = ["youdao", "google", "caiyun", "iciba", "argos", "reverso"]
    cand = [getattr(ts, elm) for elm in _]
    _ = ["tencent", "baidu", "itranslate"]
    cand1 = [getattr(ts, elm) for elm in _]

    cand = choices(cand, k=len(cand))
    cand1 = choices(cand1, k=len(cand1))
    """
    try:
        text = str(text)
    except Exception:
        text = ""
    if not text:
        return text

    # buffer various candidates as function's attr
    try:
        deepl = sure_trans.deepl
        cand = sure_trans.cand
        cand1 = sure_trans.cand1
    except AttributeError:  # first time only
        _ = ["deepl", "caiyun", "iciba"]
        sure_trans.deepl = [getattr(ts, elm) for elm in _]
        _ = ["youdao", "google", "caiyun", "iciba", "argos", "reverso"]
        sure_trans.cand = [getattr(ts, elm) for elm in _]
        _ = ["tencent", "baidu", "itranslate"]
        sure_trans.cand1 = [getattr(ts, elm) for elm in _]
        deepl = sure_trans.deepl
        cand = sure_trans.cand
        cand1 = sure_trans.cand1

    # randomize
    deepl = choices(deepl, k=len(deepl))
    cand = choices(cand, k=len(cand))
    cand1 = choices(cand1, k=len(cand1))

    _ = """
    for tr in deepl + cand + cand1:
        try:
            _ = tr(s, "zh", "en")
        except Exception:
            _ = 'failure'
        print(tr.__name__, _)
    # """
    for tr in deepl + cand + cand1:
        try:
            with about_time() as dur:
                res = tr(
                    text,
                    from_language=from_language,
                    to_language=to_language,
                )
            logger.info(" api used: %s, took %s", tr.__name__, dur.duration_human)
            sure_trans.api_used = tr.__name__
            break
        except Exception as exc:
            # remove invalid
            if tr in sure_trans.deepl:
                sure_trans.deepl.remove(tr)
                logger.info(" %s removed, reason: %s", tr.__name__, exc)
            if tr in sure_trans.cand:
                sure_trans.cand.remove(tr)
                logger.info(" %s removed, reason: %s", tr.__name__, exc)
            if tr in sure_trans.cand1:
                sure_trans.cand1.remove(tr)
                logger.info(" %s removed, reason: %s", tr.__name__, exc)

            continue
    else:
        raise Exception("Something is probably wrong, ping dev to fix it if you like.")

    return res
