from app.services.highlights_service import handle_highlight
from flask import Blueprint, current_app
from werkzeug.local import LocalProxy
from flask import jsonify
from app.decorators.authentication import require_appkey
from app.services.process_mails_service import handle_read_mails
from .tasks import test_task

core = Blueprint("core", __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = "core"


@core.route("/test", methods=["GET"])
def test():
    logger.info("app test route hit")
    test_task.delay()
    return "Congratulations! Your core-app test route is running!"


@core.route("/highlights", methods=["GET"])
def highlights():
    highlights = handle_highlight()
    return jsonify(highlights)


@core.route("/read-email", methods=["GET"])
def handle_mails():
    highlights = handle_read_mails()
    return jsonify(highlights)


@core.route("/restricted", methods=["GET"])
@require_appkey
def restricted():
    return (
        "Congratulations! Your core-app restricted route is running via your API key!"
    )
