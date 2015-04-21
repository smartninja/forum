from jinja2 import evalcontextfilter
from libs import markdown

@evalcontextfilter
def markitdown(eval_ctx, value):
    return markdown.markdown(value)