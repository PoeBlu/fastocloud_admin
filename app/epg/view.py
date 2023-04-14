import os
import gzip
import shutil

from flask_classy import FlaskView, route
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.common.epg.forms import EpgForm, UploadEpgForm
from pyfastocloud_models.epg.entry import Epg
from pyfastocloud_models.utils.utils import download_file
from app import app, get_epg_tmp_folder


def gunzip(file_path, output_path):
    with gzip.open(file_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


# routes
class EpgView(FlaskView):
    route_base = '/epg/'

    @route('/update_urls', methods=['GET'])
    @login_required
    def update_urls(self):
        epgs = Epg.objects()
        epg_service_in_directory = app.config.get('EPG_IN_DIRECTORY')

        result = []
        for epg in epgs:
            try:
                path, name = download_file(epg.uri, get_epg_tmp_folder(), 10)
            except Exception:
                result.append({'url': epg.uri, 'status': False})
                continue

            out_path = os.path.expanduser(os.path.join(epg_service_in_directory, name))
            status = True
            if name.endswith('.gz'):
                try:
                    gunzip(path, out_path)
                except Exception:
                    status = False
            else:
                shutil.copy(path, out_path)

            os.unlink(path)
            result.append({'path': path, 'status': status})

        return jsonify(status='ok', result=result), 200

    @login_required
    @route('/add', methods=['GET', 'POST'])
    def add(self):
        form = EpgForm(obj=Epg())
        if request.method == 'POST' and form.validate_on_submit():
            new_entry = form.make_entry()
            new_entry.save()
            return jsonify(status='ok'), 200

        return render_template('epg/add.html', form=form)

    @login_required
    @route('/remove', methods=['POST'])
    def remove(self):
        sid = request.form['sid']
        if epg := Epg.objects(id=sid).first():
            epg.delete()
            return jsonify(status='ok'), 200

        return jsonify(status='failed'), 404

    @login_required
    @route('/edit/<sid>', methods=['GET', 'POST'])
    def edit(self, sid):
        epg = Epg.objects(id=sid).first()
        form = EpgForm(obj=epg)

        if request.method == 'POST' and form.validate_on_submit():
            epg = form.update_entry(epg)
            epg.save()
            return jsonify(status='ok'), 200

        return render_template('epg/edit.html', form=form)

    @login_required
    @route('/upload_urls', methods=['POST', 'GET'])
    def upload_urls(self):
        form = UploadEpgForm()
        return render_template('epg/upload_urls.html', form=form)

    @login_required
    @route('/upload_file', methods=['POST'])
    def upload_file(self):
        form = UploadEpgForm()
        if form.validate_on_submit():
            file_handle = form.file.data
            content = file_handle.read().decode('utf-8')
            url_set = {line.strip() for line in content.split()}
            for uniq in url_set:
                epg = Epg()
                epg.uri = uniq
                epg.save()

        return redirect(url_for('ProviderView:epg'))
