from datetime import datetime
import json
import os
from flask import Blueprint, current_app, render_template, request
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint("blog", __name__)


# data = [{"id": i, "title": i, "data": f"Date: 2024/01/{i}"}
#         for i in range(1, 51)]


# 首頁
@bp.route("/")
@bp.route("/home")
def index():
    pagination_data, pagination = page_filter()
    return render_template("index.html", data=pagination_data, pagination=pagination)


# 閱讀文章路由
@bp.route("/article/<id>")
def article(id):
    article_path = os.path.join(
        current_app.config['BASE_DIR'], 'articles', f'{id}.json')
    with open(article_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template("article.html", data=data)


# 設置首頁顯示文章數量
def page_filter(pages=15):
    articles_path = os.path.join(current_app.config['BASE_DIR'], "articles")
    items = os.listdir(articles_path)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = pages
    offset = (page - 1) * per_page
    total = len(items)

    total_pages = (total + per_page - 1) // per_page
    if page > total_pages and total_pages > 0:
        page = total_pages
        offset = (page - 1) * per_page

    pagination_files = items[offset: offset + per_page]
    pagination_data = []

    for filename in pagination_files:
        file_path = os.path.join(articles_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            pagination_data.append(data)

    pagination = Pagination(page=page, total=total,
                            per_page=per_page, css_framework='bootstrap5')
    return pagination_data, pagination
