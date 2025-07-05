<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                exclude-result-prefixes="tei">
    
    <xsl:template match="/">
        <html>
            <body>
                <!--Title-->
                <h2><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h2>
                <!--Title-->
                
                <!--Metadata Table-->
                <table>
                    <tr>
                        <th>Metadata</th>
                        <th>Values</th>
                        <th>Authority Control</th>
                    </tr>
                    <tr>
                        <td>Author</td>
                        <td><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:persName"/></td>
                        <td><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:idno[@type='VIAF']"/></td>
                    </tr>
                    <tr>
                        <td>Date</td>
                        <td></td>
                    </tr>
                </table>
                <!--Metadata Table-->
                
                <!--Text-->
                <div>
                    <!--First Chapter-->
                    
                    <!--Title-->
                    <!-- Titolo del capitolo -->
                    <h4>
                        <xsl:value-of select="/tei:TEI/tei:text/tei:body/tei:div[@type='chapter']/tei:head"/>
                    </h4>
                    
                    <!-- Itera solo sui dialoghi dentro l’unico capitolo -->
                    <xsl:for-each select="/tei:TEI/tei:text/tei:body/tei:div[@type='chapter']/tei:div[@type='dialogue']">
                        <p>
                            <strong><xsl:value-of select="tei:speaker"/></strong>
                            <xsl:text>: </xsl:text>
                            <xsl:value-of select="tei:p"/>
                        </p>
                    </xsl:for-each>
                    
                    
                    <!--First Chapter-->
                </div>
                <!--Text-->
            </body>
        </html>
        
    </xsl:template>
    
</xsl:stylesheet>