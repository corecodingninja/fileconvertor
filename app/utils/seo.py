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
            'title': 'Premium Online File Converter — Word to PDF, Image Tools & More',
            'description': 'Convert Word to PDF, PDF to Word, PNG to JPG, and optimize images online for free. Secure, fast, and private — files deleted after 10 minutes. No registration required.',
            'keywords': 'free online converter, word to pdf, pdf to word, image converter, compress image, png to jpg, jpg to png, webp converter, file converter online',
        },
        'word_to_pdf': {
            'title': 'Convert Word to PDF Online — Free & High Fidelity | ConverterHub',
            'description': 'Convert Word documents (.docx, .doc) to PDF online for free. High-fidelity conversion with preserved fonts and layouts. Instant download, no registration needed.',
            'keywords': 'word to pdf converter free, docx to pdf online, convert word to pdf, doc to pdf, word document to pdf',
        },
        'pdf_to_word': {
            'title': 'Convert PDF to Word Online — Edit PDFs as DOCX Free | ConverterHub',
            'description': 'Convert PDF to editable Word document (.docx) online for free. Smart text extraction with no account required. Your files are automatically deleted after 10 minutes.',
            'keywords': 'pdf to word converter online, pdf to docx free, convert pdf to word, pdf to editable word, extract text from pdf',
        },
        'png_to_jpg': {
            'title': 'Convert PNG to JPG Online — Free & Instant Image Converter',
            'description': 'Convert PNG images to high-quality JPG format online for free. Reduce file size while maintaining visual quality. Perfect for web optimization and faster loading times.',
            'keywords': 'png to jpg, convert png to jpg online, free image converter, png to jpeg, image format conversion',
        },
        'jpg_to_png': {
            'title': 'Convert JPG to PNG Online — Preserve Quality & Transparency',
            'description': 'Convert JPG images to PNG format online for free. Maintain high quality with transparency support. Ideal for graphics, logos, and web designs.',
            'keywords': 'jpg to png, convert jpg to png free, jpeg to png, image converter, png conversion',
        },
        'image_to_webp': {
            'title': 'Convert Images to WebP Online — Optimize for Modern Web',
            'description': 'Convert PNG or JPG images to modern WebP format online. Reduce file size by up to 35% while improving web performance and LCP scores.',
            'keywords': 'convert to webp, png to webp, jpg to webp, webp converter, image optimization, modern image format',
        },
        'compress_image': {
            'title': 'Compress Image Online — Reduce File Size Without Quality Loss',
            'description': 'Compress and optimize images online for free. Reduce file size by up to 90% while maintaining visual quality. Perfect for websites, social media, and email.',
            'keywords': 'compress image online, reduce image size, image optimizer, image compression, file size reduction, optimize images',
        },
        'image_to_bmp': {
            'title': 'Convert Images to BMP Online — Free Format Converter',
            'description': 'Convert PNG, JPG, or other images to BMP format online for free. Lossless conversion with excellent color preservation.',
            'keywords': 'convert to bmp, image to bmp, bmp converter, bitmap image format',
        },
        'image_to_tiff': {
            'title': 'Convert Images to TIFF Online — Professional Format',
            'description': 'Convert images to TIFF format online for free. Perfect for professional photography, scanning, and archival purposes.',
            'keywords': 'convert to tiff, image to tiff, tiff converter, tiff format, professional image format',
        },
        'image_to_gif': {
            'title': 'Convert Images to GIF Online — Create Animated GIFs',
            'description': 'Convert static images to GIF format online for free. Support for animation and lossless compression.',
            'keywords': 'convert to gif, image to gif, gif converter, animated gif, gif format',
        },
        'blog': {
            'title': 'File Conversion & Image Optimization Guides — ConverterHub Blog',
            'description': 'Learn how to convert, edit, and manage files. Expert tips on image optimization, PDF management, web performance, and digital literacy.',
            'keywords': 'pdf tips, word document tips, image optimization guide, web performance, file conversion tutorial, compress images',
        },
        'about': {
            'title': 'About ConverterHub — Privacy-First File Conversion Tools',
            'description': 'Discover ConverterHub\'s mission to provide secure, private, and fast file conversion services. Learn about our technology and commitment to user privacy.',
            'keywords': 'about converterhub, mission, secure file conversion, privacy-first, online tools',
        },
        'privacy': {
            'title': 'Privacy Policy — ConverterHub Data Protection Commitment',
            'description': 'Our complete privacy policy. Learn how we protect your files, ensure zero tracking, and automatically delete all data after processing.',
            'keywords': 'privacy policy, data protection, secure file conversion, gdpr compliance, data privacy',
        },
        'terms': {
            'title': 'Terms of Service — ConverterHub Usage Guidelines',
            'description': 'Read our terms of service, usage limits, and policies for using ConverterHub\'s file conversion services.',
            'keywords': 'terms of service, usage guidelines, acceptable use policy, service terms',
        },
        'contact': {
            'title': 'Contact ConverterHub — Support & Feedback',
            'description': 'Have questions or feedback? Get in touch with the ConverterHub support team. We\'d love to hear from you!',
            'keywords': 'contact us, support, feedback, customer service, get in touch',
        },
    }
    return metas.get(page, metas['home'])


def get_json_ld(page: str, url: str) -> dict:
    """Return comprehensive JSON-LD structured data for better SEO."""
    base_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "ConverterHub",
        "url": "https://converterhub.io",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "creator": {
            "@type": "Organization",
            "name": "ConverterHub",
            "url": "https://converterhub.io",
            "logo": "https://converterhub.io/static/img/favicon.svg",
            "sameAs": ["https://twitter.com/converterhub", "https://facebook.com/converterhub"]
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "ratingCount": "5000",
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    
    page_specific_schemas = {
        'home': {
            "@type": "WebApplication",
            "name": "ConverterHub - Premium File Converter",
            "description": "Convert Word to PDF, PDF to Word, and optimize images online for free.",
            "potentialAction": [
                {
                    "@type": "Action",
                    "name": "Convert Word to PDF"
                },
                {
                    "@type": "Action",
                    "name": "Convert PDF to Word"
                },
                {
                    "@type": "Action",
                    "name": "Compress Image"
                }
            ]
        },
        'word_to_pdf': {
            "@type": "SoftwareApplication",
            "name": "Word to PDF Converter",
            "description": "Convert Word documents to PDF online for free with high fidelity.",
            "applicationCategory": "UtilitiesApplication"
        },
        'pdf_to_word': {
            "@type": "SoftwareApplication",
            "name": "PDF to Word Converter",
            "description": "Convert PDF documents to editable Word files online for free.",
            "applicationCategory": "UtilitiesApplication"
        },
        'png_to_jpg': {
            "@type": "SoftwareApplication",
            "name": "PNG to JPG Converter",
            "description": "Convert PNG images to high-quality JPG format online for free.",
            "applicationCategory": "UtilitiesApplication"
        },
        'jpg_to_png': {
            "@type": "SoftwareApplication",
            "name": "JPG to PNG Converter",
            "description": "Convert JPG images to PNG format with transparency support online for free.",
            "applicationCategory": "UtilitiesApplication"
        },
        'image_to_webp': {
            "@type": "SoftwareApplication",
            "name": "Image to WebP Converter",
            "description": "Convert images to modern WebP format for web optimization.",
            "applicationCategory": "UtilitiesApplication"
        },
        'compress_image': {
            "@type": "SoftwareApplication",
            "name": "Image Compressor",
            "description": "Compress and optimize images online without quality loss.",
            "applicationCategory": "UtilitiesApplication"
        },
        'image_to_bmp': {
            "@type": "SoftwareApplication",
            "name": "Image to BMP Converter",
            "description": "Convert images to BMP format with lossless compression.",
            "applicationCategory": "UtilitiesApplication"
        },
        'image_to_tiff': {
            "@type": "SoftwareApplication",
            "name": "Image to TIFF Converter",
            "description": "Convert images to professional TIFF format for archival.",
            "applicationCategory": "UtilitiesApplication"
        },
        'image_to_gif': {
            "@type": "SoftwareApplication",
            "name": "Image to GIF Converter",
            "description": "Convert images to GIF format with optional animation.",
            "applicationCategory": "UtilitiesApplication"
        }
    }
    
    schema = base_schema.copy()
    if page in page_specific_schemas:
        schema.update(page_specific_schemas[page])
    
    return schema


def get_faq_schema() -> dict:
    """Return FAQ structured data for home page."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Is ConverterHub free to use?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, ConverterHub is completely free to use. All conversions are performed online with no hidden fees or subscription requirements."
                }
            },
            {
                "@type": "Question",
                "name": "Is my data safe with ConverterHub?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Your files are processed in an isolated environment and automatically deleted after 10 minutes. We never view, store, or share your data. Complete privacy is guaranteed."
                }
            },
            {
                "@type": "Question",
                "name": "How fast are conversions?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Most conversions take less than 3 seconds using our high-performance clusters. Speed depends on file size and type."
                }
            },
            {
                "@type": "Question",
                "name": "What file formats do you support?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We support Word (.docx, .doc), PDF, PNG, JPG, WebP, BMP, and GIF formats with lossless quality conversion."
                }
            },
            {
                "@type": "Question",
                "name": "Do I need to create an account?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No account or registration is required. Simply upload your file and download the converted result immediately."
                }
            },
            {
                "@type": "Question",
                "name": "What is the maximum file size?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The maximum file size is 20 MB per upload. Most common files are well within this limit."
                }
            }
        ]
    }


def get_organization_schema() -> dict:
    """Return Organization structured data for better brand recognition."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "ConverterHub",
        "url": "https://converterhub.io",
        "logo": "https://converterhub.io/static/img/favicon.svg",
        "description": "Premium online file conversion and image optimization tools",
        "sameAs": [
            "https://twitter.com/converterhub",
            "https://facebook.com/converterhub",
            "https://linkedin.com/company/converterhub"
        ],
        "contact": {
            "@type": "ContactPoint",
            "contactType": "Customer Support",
            "email": "support@converterhub.io",
            "url": "https://converterhub.io/contact"
        },
        "foundingDate": "2024",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "US"
        }
    }
