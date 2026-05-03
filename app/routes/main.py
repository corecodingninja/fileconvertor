from flask import Blueprint, render_template, make_response, current_app
from app.utils.seo import generate_sitemap_xml, get_page_meta

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    meta = get_page_meta('home')
    return render_template('index.html', meta=meta, active_page='home')


@main_bp.route('/word-to-pdf')
def word_to_pdf():
    meta = get_page_meta('word_to_pdf')
    return render_template('word-to-pdf.html', meta=meta, active_page='word_to_pdf')


@main_bp.route('/pdf-to-word')
def pdf_to_word():
    meta = get_page_meta('pdf_to_word')
    return render_template('pdf-to-word.html', meta=meta, active_page='pdf_to_word')


@main_bp.route('/png-to-jpg')
def png_to_jpg():
    meta = get_page_meta('png_to_jpg')
    return render_template('image-tool.html', meta=meta, tool_type='png_to_jpg', title='PNG to JPG', active_page='png_to_jpg')


@main_bp.route('/jpg-to-png')
def jpg_to_png():
    meta = get_page_meta('jpg_to_png')
    return render_template('image-tool.html', meta=meta, tool_type='jpg_to_png', title='JPG to PNG', active_page='jpg_to_png')


@main_bp.route('/image-to-webp')
def image_to_webp():
    meta = get_page_meta('image_to_webp')
    return render_template('image-tool.html', meta=meta, tool_type='image_to_webp', title='Image to WebP', active_page='image_to_webp')


@main_bp.route('/compress-image')
def compress_image():
    meta = get_page_meta('compress_image')
    return render_template('image-tool.html', meta=meta, tool_type='compress_image', title='Compress Image', active_page='compress_image')


@main_bp.route('/about')
def about():
    meta = get_page_meta('about')
    return render_template('about.html', meta=meta)


@main_bp.route('/privacy')
def privacy():
    meta = get_page_meta('privacy')
    return render_template('privacy.html', meta=meta)


@main_bp.route('/terms')
def terms():
    meta = get_page_meta('terms')
    return render_template('terms.html', meta=meta)


@main_bp.route('/contact')
def contact():
    meta = get_page_meta('contact')
    return render_template('contact.html', meta=meta)


@main_bp.route('/sitemap.xml')
def sitemap():
    base = current_app.config.get('SITE_URL', '')
    routes = [
        {'loc': f'{base}/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': f'{base}/word-to-pdf', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': f'{base}/pdf-to-word', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': f'{base}/png-to-jpg', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{base}/jpg-to-png', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{base}/image-to-webp', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{base}/compress-image', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': f'{base}/blog/', 'priority': '0.7', 'changefreq': 'weekly'},
        {'loc': f'{base}/about', 'priority': '0.5', 'changefreq': 'monthly'},
        {'loc': f'{base}/privacy', 'priority': '0.3', 'changefreq': 'monthly'},
        {'loc': f'{base}/terms', 'priority': '0.3', 'changefreq': 'monthly'},
    ]
    xml = generate_sitemap_xml(routes)
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@main_bp.route('/robots.txt')
def robots():
    content = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /api/\n'
        'Disallow: /tmp/\n'
        f'Sitemap: {current_app.config.get("SITE_URL", "")}/sitemap.xml\n'
    )
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    return response


@main_bp.route('/health')
def health():
    return {'status': 'ok'}, 200
