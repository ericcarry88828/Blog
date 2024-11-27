from datetime import datetime
import os
import json
import uuid
from flask import Blueprint, g, abort, current_app, jsonify, redirect, render_template, request, url_for, session
from .auth import admin_required
from .blog import page_filter

bp = Blueprint('admin', __name__)


# 管理員頁面
@bp.route("/admin")
@admin_required
def admin():
    pagination_data, pagination = page_filter()
    return render_template('admin.html', data=pagination_data, pagination=pagination)


# 新增文章
@bp.route("/articles", methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        id = datetime.today().strftime("%Y-%m-%d_%H%M%S")
        title = request.form['title']
        date = datetime.today().date().strftime("%b %d, %Y")
        content = request.form['content']
        article_data = {
            "id": id,
            "title": title,
            "date": date,
            "content": content
        }
        file_path = os.path.join(
            current_app.config['BASE_DIR'], 'articles', f'{id}.json')
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(article_data, json_file, ensure_ascii=False, indent=4)
        return redirect(url_for("blog.article", id=id))

    return render_template("create.html")


@bp.route("/articles/<id>", methods=['GET', 'POST'])
@admin_required
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        date = datetime.today().date().strftime("%b %d, %Y")
        content = request.form['content']
        update_data = {
            'id': id,
            'title': title,
            'date': date,
            'content': content
        }
        file_path = os.path.join(
            current_app.config['BASE_DIR'], 'articles', f'{id}.json')
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(update_data, json_file, ensure_ascii=False, indent=4)

        return redirect(url_for('blog.article', id=id))

    file_path = os.path.join(
        current_app.config['BASE_DIR'], 'articles', f'{id}.json')
    try:
        if id:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
    except FileNotFoundError as e:
        abort(404)
    return render_template("update.html", data=data)


@bp.route("/delete", methods=['POST'])
@admin_required
def delete():
    data = request.get_json()
    id = data.get('id')
    file_path = os.path.join(
        current_app.config['BASE_DIR'], 'articles', f'{id}.json')
    if id and os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'error': 'No ID provided'}), 400
