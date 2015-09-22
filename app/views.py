from flask import render_template, request, Response
import datetime
from app import app, db
from .models import ms_mi_log, total_log
import time
import os
import re

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hosts')
def hosts():
    return render_template("hosts.html")


@app.route('/weblog')
def weblog():
    return render_template("weblog.html")


@app.route('/index')
def main():
    interval_date = datetime.datetime.now() - datetime.timedelta(days=7)
    interval_date_str = interval_date.strftime('%Y-%m-%d')

    ms_data = total_log.query.filter(total_log.date > interval_date_str).filter_by(app_name='ms').order_by('date')
    mi_data = total_log.query.filter(total_log.date > interval_date_str).filter_by(app_name='mi').order_by('date')
    echarts_date = ','.join(["'%s'" % i.date for i in ms_data])

    ms_data_str = ','.join([str(i.total) for i in ms_data])
    mi_data_str = ','.join([str(i.total) for i in mi_data])
    return render_template("ms_mi.html", echarts_date=echarts_date, ms_data_str=ms_data_str, mi_data_str=mi_data_str)


@app.route('/query', methods=['POST'])
def query():
    query_date = request.form.get('date', '')
    if query_date != '':
        ms_mi_log_data = ms_mi_log.query.filter(ms_mi_log.date.like(query_date+'%')).order_by('ip').all()
        # for s in ms_mi_log_data:
        #     print s
    else:
        ms_mi_log_data = []

    return render_template("hosts.html", ms_mi_log_data=ms_mi_log_data)


@app.route('/api', methods=['POST'])
def api():
    ip = request.remote_addr
    rc = request.form.get('rc', None)
    uin = request.form.get('uin', None)
    mbox = request.form.get('mbox', None)
    des = request.form.get('des', None)
    print ip, rc, uin, mbox, des
    log_err = ms_mi_log(ip=ip, rc=rc, uin=uin, mbox=mbox, des=des)
    db.session.add(log_err)
    db.session.commit()
    return 'OK'


def event_stream(ip, logfile, filter=None):
    logfile = os.path.join('/logs/log_',logfile)
    with open(logfile) as f:
            f.seek(0,2)
            while True:
                for line in f.readlines():
                    if filter is not None:
                        re_filter=re.compile(r'(%s)'%filter,re.I)
                        if re.findall(re_filter,line):
                            res=re.sub(re_filter,r'<font color="red">\1</font>',line)
                            yield 'data: %s\n\n' % res.rstrip()
                    else:
                        yield 'data: %s\n\n' % line.rstrip()
                time.sleep(1)


@app.route('/stream/<ip>/<logfile>/')
@app.route('/stream/<ip>/<logfile>/<filter>')
def stream(ip, logfile, filter=None):
    return Response(event_stream(ip, logfile, filter),
                    mimetype="text/event-stream")
