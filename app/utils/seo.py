from datetime import datetime
from flask import current_app, url_for


def generate_sitemap_xml(routes: list) -> str:
    """Generate XML sitemap string from a list of route dicts."""
    now = datetime.utcnow().strftime('%Y-%m-%d')
    urls = ''
    for route in routes:
        urls += f"""
  <url>
    <loc>{route['loc']}</loc>
    <lastmod>{route.get('lastmod', now)}</lastmod>
    <changefreq>{route.get('changefreq', 'weekly')}</changefreq>
    <priority>{route.get('priority', '0.8')}</priority>
  </url>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}
</urlset>"""


def get_page_meta(page: str) -> dict:
    """Return SEO meta tags for each page."""
    metas = {
        'home': {
            'title': 'Premium Online File Converter — Word, PDF & Image Tools',
            'description': 'Convert Word to PDF, PDF to Word, and optimize images online for free. Secure, fast, and private — files deleted after 10 minutes.',
            'keywords': 'free online converter, word to pdf, pdf to word, image converter, compress image',
        },
        'word_to_pdf': {
            'title': 'Convert Word to PDF Online — Free & High Fidelity',
            'description': 'Convert Word documents to PDF online for free. Upload your .docx or .doc file and download a perfect PDF in seconds. No registration needed.',
            'keywords': 'word to pdf converter free, docx to pdf online, convert word to pdf',
        },
        'pdf_to_word': {
            'title': 'Convert PDF to Word Online — Edit PDF as DOCX Free',
            'description': 'Convert PDF to editable Word document online for free. No account needed. Your files are deleted automatically after 10 minutes.',
            'keywords': 'pdf to word converter online, pdf to docx free, convert pdf to word',
        },
        'png_to_jpg': {
            'title': 'Convert PNG to JPG Online — Free & Fast Image Converter',
            'description': 'Convert PNG images to high-quality JPG online for free. Fast, secure, and no registration required.',
            'keywords': 'png to jpg, convert png to jpg online, free image converter',
        },
        'jpg_to_png': {
            'title': 'Convert JPG to PNG Online — Preserve Image Quality',
            'description': 'Convert JPG images to PNG online for free. Support for transparency and high-fidelity conversion.',
            'keywords': 'jpg to png, convert jpg to png free, image converter',
        },
        'image_to_webp': {
            'title': 'Convert Image to WebP — Optimize for Web Performance',
            'description': 'Convert JPG or PNG to WebP online for free. Improve your website speed and LCP scores with next-gen image formats.',
            'keywords': 'convert to webp, png to webp, jpg to webp, webp converter',
        },
        'compress_image': {
            'title': 'Compress Image Online — Reduce File Size Without Quality Loss',
            'description': 'Reduce image file size online for free. Perfect for website optimization and faster loading times. No signup required.',
            'keywords': 'compress image online, reduce image size, image optimizer',
        },
        'blog': {
            'title': 'File Conversion & Image Optimization Guides — ConverterHub Blog',
            'description': 'Learn how to convert, edit, and manage files. Expert tips on image optimization, PDF management, and web performance.',
            'keywords': 'pdf tips, word document tips, image optimization guide, web performance',
        },
        'about': {
            'title': 'About ConverterHub — Privacy-First File Tools',
            'description': 'Learn more about ConverterHub, our privacy-first mission, and the technology behind our premium conversion tools.',
            'keywords': 'about converterhub, mission, secure file conversion',
        },
        'privacy': {
            'title': 'Privacy Policy — Secure & Private File Processing',
            'description': 'Our commitment to your privacy. Read how we handle your files and ensure automatic deletion after 10 minutes.',
            'keywords': 'privacy policy, data protection, secure file conversion',
        },
        'terms': {
            'title': 'Terms of Service — Usage Guidelines',
            'description': 'The terms and conditions for using ConverterHub services. Learn about our usage limits and policies.',
            'keywords': 'terms of service, usage guidelines',
        },
        'contact': {
            'title': 'Contact Us — Feedback & Support',
            'description': 'Have questions or feedback? Get in touch with the ConverterHub team.',
            'keywords': 'contact us, support, feedback',
        },
    }
    return metas.get(page, metas['home'])


def get_json_ld(page: str, url: str) -> dict:
    """Return JSON-LD structured data for the page."""
    base_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "ConverterHub",
        "url": url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
    }
    
    page_specific = {
        'home': {
            "description": "Premium online file converter for Word, PDF, and Images."
        },
        'word_to_pdf': {
            "name": "Word to PDF Converter",
            "description": "Convert Word documents to PDF online for free."
        },
        'pdf_to_word': {
            "name": "PDF to Word Converter",
            "description": "Convert PDF documents to editable Word files."
        },
        'png_to_jpg': {
            "name": "PNG to JPG Converter",
            "description": "Convert PNG images to JPG format."
        },
        'jpg_to_png': {
            "name": "JPG to PNG Converter",
            "description": "Convert JPG images to PNG format."
        },
        'image_to_webp': {
            "name": "Image to WebP Converter",
            "description": "Convert images to next-gen WebP format."
        },
        'compress_image': {
            "name": "Image Compressor",
            "description": "Reduce image file size online."
        }
    }
    
    schema = base_schema.copy()
    if page in page_specific:
        schema.update(page_specific[page])
    return schema
