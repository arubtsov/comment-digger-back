from flask import Flask, request, jsonify
from youtube import get_comments_byt_id

app = Flask(__name__)

@app.route('/')
def hello_world():
    videoId = request.args.get('videoId')
    comments = get_comments_byt_id(videoId)

    return jsonify({ 'count': len(comments), 'comments': comments })
