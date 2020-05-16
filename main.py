from flask import Flask, request, jsonify
from flask_cors import CORS

from youtube import get_comments_byt_id
from analyze import get_top_most_common

from rq import Queue, exceptions
from rq.job import Job
from worker import conn

app = Flask(__name__)
CORS(app)

q = Queue(connection=conn)

@app.route("/comments/<video_id>", methods=['GET'])
def get_results(video_id):
    job = None

    try:
        job = Job.fetch(video_id, connection=conn)
    except (exceptions.NoSuchJobError):
        job = q.enqueue(get_comments_byt_id, args=(video_id,), result_ttl=86400, job_timeout=600, job_id=video_id)

    if job.is_finished:
        number = int(request.args.get('number'))
        comments = job.result
        most_common = get_top_most_common(comments, number)

        return jsonify({ 'count': len(comments), 'comments': comments, 'mostCommon': most_common }), 200
    else:
        return jsonify({ 'progress': job.meta['progress'] if 'progress' in job.meta else 0 }), 202
