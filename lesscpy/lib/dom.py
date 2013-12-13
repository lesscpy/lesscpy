"""
    HTML DOM names

    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""

html4 = [
    'a',
    'abbr',
    'acronym',
    'address',
    'applet',
    'area',
    'b',
    'base',
    'basefont',
    'bdo',
    'big',
    'blockquote',
    'body',
    'br',
    'button',
    'caption',
    'center',
    'cite',
    'code',
    'col',
    'colgroup',
    'dd',
    'del',
    'dfn',
    'dir',
    'div',
    'dl',
    'dt',
    'em',
    'fieldset',
    'font',
    'form',
    'frame',
    'frameset',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'hr',
    'html',
    'i',
    'iframe',
    'img',
    'input',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    #    'link',
    'map',
    'mark',
    'menu',
    'meta',
    'noframes',
    'noscript',
    'object',
    'ol',
    'optgroup',
    'option',
    'p',
    'param',
    'pre',
    'q',
    's',
    'samp',
    'script',
    'select',
    'small',
    'span',
    'strike',
    'strong',
    'style',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'template',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'title',
    'tr',
    'tt',
    'u',
    'ul',
    'var',
]

html5 = [
    'article',
    'aside',
    'audio',
    'bdi',
    'canvas',
    'command',
    'datalist',
    'details',
    'embed',
    'figcaption',
    'figure',
    'footer',
    'header',
    'hgroup',
    'keygen',
    'main',
    'mark',
    'meter',
    'nav',
    'output',
    'progress',
    ' progress-bar-stripes',
    'rp',
    'rt',
    'ruby',
    'section',
    'source',
    'summary',
    'svg',
    'time',
    'track',
    'video',
    'wbr',

    'only',  # TODO/FIXME: What is this?!?
]

svg = [
    'altGlyph',
    'altGlyphDef',
    'altGlyphItem',
    'circle',
    'desc',
    'ellipse',
    'glyphRef',
    'line',
    'path',
    'polygon',
    'polyline',
    'rect',
    'text',
    'textPath',
    'tref',
    'tspan',
]

# CSS-2(.1) media types: http://www.w3.org/TR/CSS2/media.html#media-types
# Include media types as defined in HTML4: http://www.w3.org/TR/1999/REC-html401-19991224/types.html#h-6.13
# Also explained in http://www.w3.org/TR/css3-mediaqueries/#background
html4_media_types = [
    'all',
    'aural',  # deprecated by CSS 2.1, which reserves "speech"
    'braille',
    'handheld',
    'print',
    'projection',
    'screen',
    'tty',
    'tv',
]
css2_media_types = [
    'embossed',  # CSS2, not HTML4
    'speech',  # CSS2. not HTML4
]
media_types = html4_media_types + css2_media_types

# Check http://www.w3.org/TR/css3-animations/#keyframes
# Treating them as DOM elements isn't entirely accurate (same for media types)
# but sufficent for our purposes.
css3_animation_keyframe_selectors = [
    'from',
    'to'
]

elements = html4
elements.extend(html5)
elements.extend(svg)
elements.extend(media_types)
elements.extend(css3_animation_keyframe_selectors)
