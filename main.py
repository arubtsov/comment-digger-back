from flask import Flask, request, jsonify
from youtube import get_comments_byt_id
from analyze import get_top_most_common

app = Flask(__name__)

@app.route('/')
def hello_world():
    videoId = request.args.get('videoId')
    comments = get_comments_byt_id(videoId)
    most_common = get_top_most_common(comments, 30)

    return jsonify({ 'count': len(comments), 'comments': comments, 'mostCommon': most_common })
