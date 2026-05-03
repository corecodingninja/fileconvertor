from flask import Blueprint, render_template, redirect, url_for
from app.models.conversion import ConversionJob

converter_bp = Blueprint('converter', __name__)


@converter_bp.route('/result/<job_id>')
def result(job_id):
    job = ConversionJob.query.get_or_404(job_id)
    return render_template('result.html', job=job, active_page='result')


@converter_bp.route('/error')
def error():
    return render_template('error.html')
