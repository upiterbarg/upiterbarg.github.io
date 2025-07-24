import json
from django.http import HttpResponse

from .models import (
    Result,
    Browser,
    Test,
    ObjectProperties,
    GlobalProperties,
    Events,
    Observation,
    WindowProperties,
    LeakResult,
    CookieSecFetch,
)
import logging

logger = logging.getLogger(__name__)


def save_data_v2(request):
    try:
        message = "Success"
        body_json = json.loads(request.body)
        # Site is not set, we are in the Browser Mode
        if body_json["site"] == "":
            observation = {}
            observation["browser"], _ = Browser.objects.get_or_create(
                **body_json["browser"]
            )
            observation["test"], _ = Test.objects.get_or_create(**body_json["test"])
            if "events" in body_json:
                observation["events"], _ = Events.objects.get_or_create(
                    **body_json["events"]
                )
            if "op" in body_json:
                (
                    observation["object_properties"],
                    _,
                ) = ObjectProperties.objects.get_or_create(**body_json["op"])
            if "gp" in body_json:
                (
                    observation["global_properties"],
                    _,
                ) = GlobalProperties.objects.get_or_create(**body_json["gp"])
            if "win" in body_json:
                (
                    observation["window_properties"],
                    _,
                ) = WindowProperties.objects.get_or_create(**body_json["win"])
            if "loading_time" in body_json:
                observation["loading_time"] = body_json["loading_time"]
            if "complete_time" in body_json:
                observation["complete_time"] = body_json["complete_time"]
            if "timed_out" in body_json:
                observation["timed_out"] = body_json["timed_out"]
            if "apg_url" in body_json:
                observation["apg_url"] = body_json["apg_url"]
            if "retest" in body_json:
                observation["retest"] = body_json["retest"]
            obsv = Observation(**observation)
            obsv.save()
        # Site is set, we are in the dynamic confirmation mode
        else:
            leak_result = {}
            leak_result["browser"], _ = Browser.objects.get_or_create(
                **body_json["browser"]
            )
            test_json = body_json["test"]
            test_json["url_dict_version"] = "notapplicable"
            leak_result["test"], _ = Test.objects.get_or_create(**test_json)
            if "events" in body_json:
                leak_result["events"], _ = Events.objects.get_or_create(
                    **body_json["events"]
                )
            if "op" in body_json:
                (
                    leak_result["object_properties"],
                    _,
                ) = ObjectProperties.objects.get_or_create(**body_json["op"])
            if "gp" in body_json:
                (
                    leak_result["global_properties"],
                    _,
                ) = GlobalProperties.objects.get_or_create(**body_json["gp"])
            if "win" in body_json:
                (
                    leak_result["window_properties"],
                    _,
                ) = WindowProperties.objects.get_or_create(**body_json["win"])
            if "loading_time" in body_json:
                leak_result["loading_time"] = body_json["loading_time"]
            if "complete_time" in body_json:
                leak_result["complete_time"] = body_json["complete_time"]
            if "timed_out" in body_json:
                leak_result["timed_out"] = body_json["timed_out"]
            if "apg_url" in body_json:
                leak_result["apg_url"] = body_json["apg_url"]
            if "retest" in body_json:
                leak_result["retest_num"] = body_json["retest"]
            if "cookies" in body_json:
                leak_result["cookies"] = body_json["cookies"]
            if "site" in body_json:
                leak_result["site"] = body_json["site"]
            lkr = LeakResult(**leak_result)
            lkr.save()
    except Exception as e:
        logger.warning(e)
        message = "Failed"
    finally:
        return HttpResponse(message)


def save_data(request):
    """Save the data in a database.

    Request needs to be post and the body needs to be json
    and adhere to the schema of the result model.
    """
    body_json = json.loads(request.body)
    res = Result(**body_json)
    res.save()
    return HttpResponse()


def save_test(request):
    """Save the cookie/sec-fetch data in a database."""
    message = "Success"
    try:
        body_json = json.loads(request.body)
        _, _ = CookieSecFetch.objects.get_or_create(**body_json)
    except Exception as e:
        logger.warning(e)
        message = "Failed"
    finally:
        return HttpResponse(message)
