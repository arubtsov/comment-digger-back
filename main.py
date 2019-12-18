from flask import Flask, request, jsonify
from youtube import get_comments_byt_id
from analyze import get_top_most_common

from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)

q = Queue(connection=conn)

@app.route('/')
def hello_world():
    videoId = request.args.get('videoId')

    job = q.enqueue_call(func=get_comments_byt_id, args=(videoId,), result_ttl=5000)
    print(job.get_id())

    return str(job.get_id()), 200

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    number = int(request.args.get('number'))

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        comments = job.result
        most_common = get_top_most_common(comments, number)
        
        return jsonify({ 'count': len(comments), 'comments': comments, 'mostCommon': most_common })
    else:
        return "Nay!", 202
