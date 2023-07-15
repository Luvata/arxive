<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <title><xsl:value-of select="//channel/title"/> RSS Feed</title>
                <meta charset="UTF-8" />
                <meta http-equiv="x-ua-compatible" content="IE=edge,chrome=1" />
                <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1,shrink-to-fit=no" />
                <style type="text/css">
                    /* Your custom styles can go here! */
                </style>
            </head>
            <body>
                <header>
                    <h1>RSS Feed</h1>
                    <h2>
                        <xsl:value-of select="//channel/title"/>
                    </h2>
                    <p>
                        <xsl:value-of select="//channel/description"/>
                    </p>
                    <a hreflang="en" target="_blank">
                        <xsl:attribute name="href">
                            <xsl:value-of select="//channel/link"/>
                        </xsl:attribute>
                        Visit arXiv.org &#x2192;
                    </a>
                </header>
                <main>
                    <h2>Recent Publications</h2>
                    <xsl:for-each select="//item">
                        <article>
                            <h3>
                                <a hreflang="en" target="_blank">
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="link"/>
                                    </xsl:attribute>
                                    <xsl:value-of select="title"/>
                                </a>
                            </h3>
                            <p>
                                <xsl:value-of select="description"/>
                            </p>
                            <footer>
                                Authors:
                                <xsl:value-of select="dc:creator" />
                            </footer>
                        </article>
                    </xsl:for-each>
                </main>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

