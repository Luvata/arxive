<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
  <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
      <title>
        RSS Feed | <xsl:value-of select="//channel/title"/>
      </title>
      <style>
        body {
          font-family: Arial, sans-serif;
        }
        h1 {
          color: #333;
        }
        a {
          color: #337ab7;
          text-decoration: none;
        }
        p {
          font-size: 14px;
          line-height: 1.42857143;
        }
        .post-author {
          font-style: italic;
        }
      </style>
    </head>
    <body>
      <h1>Recent Updates</h1>
      <xsl:for-each select="//item">
        <a>
          <xsl:attribute name="href">
            <xsl:value-of select="link"/>
          </xsl:attribute>
          <xsl:value-of select="title"/>
        </a>
        <p>
          <xsl:value-of select="description"/>
        </p>
        <p class="post-author">
          Author(s): <xsl:value-of select="dc:creator"/>
        </p>
        <hr />
      </xsl:for-each>
    </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
